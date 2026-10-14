"""Deterministic, fictional Indian retail order-line data. Python 3.10+."""
import csv
import random
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ['line_id','order_id','order_date','customer_id','region','channel','product_id','product','category','quantity','unit_price','unit_cost','discount_pct','returned']
PRODUCTS = [('P01','Wireless headphones','Electronics',2400,1650),('P02','Smartwatch','Electronics',4200,2850),('P03','Bluetooth speaker','Electronics',1800,1200),('P04','Cotton shirt','Fashion',900,360),('P05','Running shoes','Fashion',2200,1000),('P06','Backpack','Fashion',1400,620),('P07','Desk lamp','Home',1100,500),('P08','Storage box','Home',600,260),('P09','Coffee mug','Home',400,150),('P10','Notebook set','Stationery',300,100),('P11','Pen set','Stationery',200,70),('P12','Desk organiser','Stationery',650,250)]

def generate():
    rng = random.Random(42)
    rows = []
    line = 0
    for order in range(1,8001):
        day = date(2024,1,1) + timedelta(days=rng.randrange(731))
        # Deliberately designed seasonality; simulated, not evidence about India.
        if order % 4 == 0:
            day = date(rng.choice([2024,2025]),rng.choice([10,11,12]),rng.randint(1,28))
        region = rng.choices(['North','South','West','East'],[35,28,23,14])[0]
        channel = rng.choices(['Online','Store'],[65,35])[0]
        customer = f'C{rng.randint(1,1800):04d}'
        for p in rng.sample(PRODUCTS,rng.randint(1,3)):
            line += 1
            discount = rng.choices([0,.05,.10,.20,.30],[20,20,30,20,10])[0] if channel == 'Online' else rng.choice([0,.05,.10])
            return_prob = .05 + (.09 if p[2] == 'Fashion' else 0) + (.04 if discount >= .2 else 0)
            rows.append(dict(zip(FIELDS,[f'L{line:05d}',f'O{order:05d}',day.isoformat(),customer,region,channel,p[0],p[1],p[2],rng.randint(1,4),p[3],p[4],discount,int(rng.random()<return_prob)])))
    # 60 duplicate lines, 40 invalid lines, 50 casing/whitespace issues.
    rows += [dict(x) for x in rng.sample(rows,60)]
    for i in range(20):
        rows[i]['quantity'] = 0
    for i in range(20,40):
        rows[i]['order_date'] = 'not-a-date'
    for i in range(40,90):
        rows[i]['region'] = ' '+rows[i]['region'].lower()+' '
    path = ROOT/'data/raw/orders.csv'
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(rows)
    print(f'Generated {len(rows):,} raw lines; seed=42')

if __name__ == '__main__':
    generate()
