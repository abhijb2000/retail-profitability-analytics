import csv
import json
import sqlite3
import unittest
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from pipeline import clean

class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.con=sqlite3.connect(ROOT/'data/processed/retail.sqlite')
    def tearDown(self): self.con.close()
    def test_quality_reconciliation(self):
        q=json.loads((ROOT/'reports/data_quality.json').read_text())
        self.assertEqual(q['raw_rows'],q['clean_rows']+q['duplicate_rows']+q['invalid_rows'])
        self.assertEqual(q['duplicate_rows'],60);self.assertEqual(q['invalid_rows'],40)
        self.assertEqual(q['normalised_regions'],50)
    def test_sql_python_reconciliation(self):
        m=json.loads((ROOT/'reports/summary.json').read_text())['metrics']
        r=self.con.execute('SELECT SUM(net_sales), SUM(gross_profit),COUNT(DISTINCT order_id) FROM orders').fetchone()
        self.assertAlmostEqual(r[0],m['net_sales'],places=2); self.assertAlmostEqual(r[1],m['gross_profit'],places=2);self.assertEqual(r[2],m['orders'])
    def test_accounting_identity(self):
        n=self.con.execute('SELECT COUNT(*) FROM orders WHERE ABS(net_sales-(gross_sales-discount_amount-refund_amount))>.01 OR ABS(gross_profit-(net_sales-cogs))>.01').fetchone()[0]
        self.assertEqual(n,0)
    def test_returns_reversed(self):
        self.assertEqual(self.con.execute('SELECT COUNT(*) FROM orders WHERE returned=1 AND (net_sales<>0 OR cogs<>0 OR gross_profit<>0)').fetchone()[0],0)
    def test_cleaning_duplicate_invalid_and_return(self):
        with (ROOT/'data/raw/orders.csv').open() as f: sample=dict(next(csv.DictReader(f)))
        sample.update(order_date='2025-01-01',quantity='2',region=' north ',unit_price='100',unit_cost='60',discount_pct='.1',returned='1')
        invalid=dict(sample,line_id='bad',discount_pct='1.5')
        rows,rejects,q=clean([sample,dict(sample),invalid])
        self.assertEqual(len(rows),1);self.assertEqual(len(rejects),2)
        self.assertEqual(rows[0]['refund_amount'],180);self.assertEqual(rows[0]['net_sales'],0)
    def test_no_missing_months(self):
        self.assertEqual(self.con.execute('SELECT COUNT(DISTINCT month) FROM orders').fetchone()[0],24)
    def test_queries_exported(self):
        s=json.loads((ROOT/'reports/summary.json').read_text())
        self.assertEqual(len(s['sql_results']),10)
        self.assertEqual(len(s['sql_results']['monthly_growth']),24)
    def test_dashboard_embedded(self):
        html=(ROOT/'dashboard/index.html').read_text()
        self.assertNotIn('__DATA__',html)
        data=html.split('const DATA=',1)[1].split(';\nconst $',1)[0]
        self.assertEqual(len(json.loads(data)),self.con.execute('SELECT COUNT(*) FROM orders').fetchone()[0])

if __name__=='__main__':unittest.main()
