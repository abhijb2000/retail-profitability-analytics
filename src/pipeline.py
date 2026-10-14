"""Validate, clean, calculate metrics, build SQLite database and publish outputs."""
import csv
import json
import sqlite3
from collections import defaultdict
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGIONS={'North','South','East','West'}
CHANNELS={'Online','Store'}

def money(x):
    return float(Decimal(str(x)).quantize(Decimal('.01'),rounding=ROUND_HALF_UP))

def clean(rows):
    seen=set(); valid=[]; rejects=[]; duplicates=0; normalised=0
    for n,raw in enumerate(rows,2):
        r=dict(raw)
        if r['line_id'] in seen:
            duplicates+=1; rejects.append({'source_row':n,'reason':'duplicate_line_id',**raw}); continue
        seen.add(r['line_id'])
        before=r['region']; r['region']=before.strip().title()
        normalised+=int(before!=r['region'])
        try:
            date.fromisoformat(r['order_date'])
            r['quantity']=int(r['quantity']); r['returned']=int(r['returned'])
            r['unit_price']=float(r['unit_price']); r['unit_cost']=float(r['unit_cost']); r['discount_pct']=float(r['discount_pct'])
            if r['quantity']<=0: raise ValueError('quantity_must_be_positive')
            if r['region'] not in REGIONS or r['channel'] not in CHANNELS: raise ValueError('unknown_dimension')
            if not 0<=r['discount_pct']<=1 or r['unit_cost']<0 or r['unit_price']<=0 or r['returned'] not in (0,1): raise ValueError('invalid_numeric_range')
            if any(not str(r[k]).strip() for k in ('line_id','order_id','customer_id','product_id')): raise ValueError('missing_key')
        except (ValueError,TypeError) as e:
            rejects.append({'source_row':n,'reason':str(e),**raw}); continue
        # Returned stock is assumed resalable: refund all revenue and reverse COGS.
        r['gross_sales']=money(r['quantity']*r['unit_price'])
        r['discount_amount']=money(r['gross_sales']*r['discount_pct'])
        r['billed_sales']=money(r['gross_sales']-r['discount_amount'])
        r['refund_amount']=r['billed_sales'] if r['returned'] else 0.0
        r['net_sales']=money(r['billed_sales']-r['refund_amount'])
        r['cogs']=money(r['quantity']*r['unit_cost']*(1-r['returned']))
        r['gross_profit']=money(r['net_sales']-r['cogs'])
        r['month']=r['order_date'][:7]
        r['discount_band']='20%+' if r['discount_pct']>=.2 else ('5–10%' if r['discount_pct']>0 else '0%')
        valid.append(r)
    return valid,rejects,{'raw_rows':len(rows),'clean_rows':len(valid),'duplicate_rows':duplicates,'invalid_rows':len(rejects)-duplicates,'normalised_regions':normalised}

def write_csv(path,rows,fieldnames=None):
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fieldnames or list(rows[0])); w.writeheader(); w.writerows(rows)

def aggregate(rows,key):
    buckets=defaultdict(list)
    for r in rows: buckets[r[key]].append(r)
    out=[]
    for name,group in sorted(buckets.items()):
        sales=money(sum(r['net_sales'] for r in group)); profit=money(sum(r['gross_profit'] for r in group))
        out.append({'name':name,'net_sales':sales,'gross_profit':profit,'margin_pct':round(100*profit/sales,2) if sales else 0,'lines':len(group),'return_rate_pct':round(100*sum(r['returned'] for r in group)/len(group),2)})
    return out

def run():
    with (ROOT/'data/raw/orders.csv').open(encoding='utf-8') as f: raw=list(csv.DictReader(f))
    rows,rejects,quality=clean(raw)
    out=ROOT/'data/processed'; out.mkdir(parents=True,exist_ok=True)
    write_csv(out/'orders_clean.csv',rows); write_csv(out/'rejected_rows.csv',rejects)
    (ROOT/'reports/data_quality.json').write_text(json.dumps(quality,indent=2))
    db=out/'retail.sqlite'; db.unlink(missing_ok=True)
    con=sqlite3.connect(db)
    int_cols={'quantity','returned'}
    numeric={'unit_price','unit_cost','discount_pct','gross_sales','discount_amount','billed_sales','refund_amount','net_sales','cogs','gross_profit'}
    columns=list(rows[0]); types=['INTEGER' if c in int_cols else 'REAL' if c in numeric else 'TEXT' for c in columns]
    schema=','.join(f'{c} {t}'+(' PRIMARY KEY' if c=='line_id' else ' NOT NULL') for c,t in zip(columns,types))
    con.execute(f'CREATE TABLE orders ({schema})')
    con.executemany('INSERT INTO orders VALUES ('+','.join('?' for _ in columns)+')',[[r[c] for c in columns] for r in rows])
    con.executescript((ROOT/'sql/views.sql').read_text()); con.commit()
    results={}
    # Every named SELECT in the query file is executed and exported.
    for block in (ROOT/'sql/analysis.sql').read_text().split('-- QUERY: ')[1:]:
        name,query=block.split('\n',1)
        cur=con.execute(query.strip()); names=[d[0] for d in cur.description]
        result=[dict(zip(names,x)) for x in cur.fetchall()]
        results[name.strip()]=result
        write_csv(out/(name.strip()+'.csv'),result,names)
    con.close()
    sales=money(sum(r['net_sales'] for r in rows)); profit=money(sum(r['gross_profit'] for r in rows)); orders=len({r['order_id'] for r in rows})
    metrics={'net_sales':sales,'gross_profit':profit,'margin_pct':round(100*profit/sales,2),'orders':orders,'customers':len({r['customer_id'] for r in rows}),'aov':money(sales/orders),'return_rate_pct':round(100*sum(r['returned'] for r in rows)/len(rows),2)}
    summary={'metrics':metrics,'quality':quality,'categories':aggregate(rows,'category'),'regions':aggregate(rows,'region'),'channels':aggregate(rows,'channel'),'discounts':aggregate(rows,'discount_band'),'monthly':aggregate(rows,'month'),'sql_results':results}
    (ROOT/'reports/summary.json').write_text(json.dumps(summary,indent=2))
    payload=json.dumps(rows,separators=(',',':')).replace('</','<\\/')
    template=(ROOT/'dashboard/template.html').read_text()
    (ROOT/'dashboard/index.html').write_text(template.replace('__DATA__',payload),encoding='utf-8')
    # Actual findings are regenerated from results, never typed as estimated outcomes.
    top=max(summary['categories'],key=lambda x:x['gross_profit'])
    low=min(summary['categories'],key=lambda x:x['margin_pct'])
    highret=max(summary['categories'],key=lambda x:x['return_rate_pct'])
    bands={x['name']:x for x in summary['discounts']}
    report=f'''# Retail profitability — decision memo

Fictional portfolio case study | 2024–2025 | INR | generated from reports/summary.json

## Executive result
Net sales: INR {sales:,.2f}; gross profit: INR {profit:,.2f}; gross margin: {metrics['margin_pct']}%; distinct orders: {orders:,}; net sales/order: INR {metrics['aov']:,.2f}.

## Findings and actions
1. **{top['name']} contributes the most gross profit:** INR {top['gross_profit']:,.2f}. Consider prioritising stock availability, subject to inventory and demand evidence not present here.
2. **{low['name']} has the lowest category margin:** {low['margin_pct']}%. Review cost and promotion mix before adding volume.
3. **{highret['name']} has the highest line return rate:** {highret['return_rate_pct']}%. Investigate product descriptions, sizing, and quality using additional return-reason data.
4. **20%+ discounted lines show {bands['20%+']['margin_pct']}% margin versus {bands['0%']['margin_pct']}% on zero-discount lines.** Pilot a controlled discount test; the observed association does not establish causality because product/channel mix differs.

## Validation and limitations
{quality['raw_rows']:,} source lines → {quality['clean_rows']:,} accepted; {quality['duplicate_rows']} duplicates and {quality['invalid_rows']} invalid lines quarantined. {quality['normalised_regions']} region values normalised. SQL and Python KPI totals reconcile in tests.

Returned lines receive full refunds with fully reversed COGS. This assumes resalable returns and excludes handling fees, delivery, tax, marketing, and overhead: gross profit is **not net profit**. Returns are attributed to original purchase dates; no return timestamp exists. Order counts include fully returned orders. Partial line returns are unsupported. Data was simulated; findings are not evidence about a real retailer and actions are recommendations, not achieved business impact.

## Next measurement
Track margin, conversion, net sales per customer, and return rate in a randomised promotion pilot. Define sample size and decision thresholds before launch. Add inventory, return reasons and fulfilment costs before implementation.
'''
    (ROOT/'reports/business_findings.md').write_text(report)
    print(json.dumps(summary['metrics'],indent=2)); print(json.dumps(quality,indent=2))

if __name__=='__main__': run()
