# Own the project: learning, interview and resume guide

## Your first walkthrough
1. Open README and dashboard/index.html. Note the difference between net sales and gross profit.
2. In orders.csv, find a duplicate line ID, zero quantity and invalid date. Then inspect rejected_rows.csv to see the audit trail.
3. Open src/pipeline.py. Trace one retained line: two units at ₹100, unit cost ₹60 and 10% discount → gross sales ₹200, discount ₹20, net sales ₹180, COGS ₹120, profit ₹60. A fully returned version has ₹180 refund and zero net sales/COGS/profit.
4. Run all three README commands. Read the test output and reports/data_quality.json.
5. Open retail.sqlite in a SQLite viewer or execute queries using Python's sqlite3. Explain each query's GROUP BY and why COUNT(DISTINCT order_id) matters.
6. Compare Fashion and Electronics in the dashboard. Explain why high sales do not automatically mean high margins.
7. Build the Power BI version with BUILD_GUIDE.md if you want Power BI on your resume.

## SQL exercise you can run without extra software
From the repository root:
```bash
python -c "import sqlite3; c=sqlite3.connect('data/processed/retail.sqlite'); print(c.execute('SELECT category, ROUND(SUM(gross_profit),2) FROM orders GROUP BY category ORDER BY 2 DESC').fetchall())"
```
Change the query to compare channel margin. Do not average the row-level profit percentages: compute SUM(gross_profit)/SUM(net_sales). Add your own query and explain the business decision it informs.

## Questions you should be able to answer
| Question | Core explanation |
|---|---|
| Why this project? | Retail growth needs profit and returns visibility, not only revenue reporting. |
| What is the grain? | One order-product line with a unique line_id; an order can span multiple lines. |
| How did you handle bad data? | Normalisation plus explicit validation; duplicates/invalids retained in an exception CSV. |
| Why does AOV include returns? | It measures net revenue across all valid purchase orders; another definition would need a different denominator. |
| What is the margin formula? | Total gross profit / total net sales; weighted correctly through totals. |
| What did you learn about discounts? | High discounts associate with lower margin, but confounding prevents a causal conclusion. |
| How were returns handled? | Full-line refunds; purchase-date attribution; full COGS reversal for resalable goods. |
| What is missing for a real rollout? | Inventory, return timestamps/reasons, partial returns, fulfilment costs and experiment data. |
| What did you test? | Accounting identities, exception counts, returns, monthly coverage, SQL/Python totals and dashboard data. |
| What was the business impact? | This is simulated; recommendations were proposed, not implemented or measured. |

## Make it your work
Before publishing it as a completed project, run it yourself, change a visual, and add an original question. Good extensions: within-category discount comparisons, a retained-customer cohort table, or validation of order-level region/customer consistency. Write a short note on what you changed and why. Keep seed/data version recorded for reproducibility.

## Resume wording — use after reproducing and understanding the project
**Retail Profitability & Returns Analytics | Portfolio Case Study | Python, SQL, Interactive Dashboard**
- Analysed 16,093 simulated retail order lines using Python and SQLite; audited 60 duplicate and 40 invalid source records and reconciled financial KPIs through eight automated checks.
- Built a filterable dashboard tracking ₹4.54 crore in simulated net sales, 38.68% gross margin and 8.00% line returns; identified category and discount patterns and proposed further investigation.

After building and validating the PBIX, you may add:
- Developed a Power BI report with a star schema, DAX measures, date-based growth analysis and region/channel slicers, validated against Python and SQL outputs.

Do not claim employer/client experience, a measured profit increase, or a completed Power BI report before you have built it. Numbers describe simulated data, not achieved financial impact.

## LinkedIn draft — personalise after completing your walkthrough
I completed a retail profitability portfolio case study using Python, SQL and an interactive dashboard.

The question: which categories and discounts support profitable growth, and where do returns deserve attention?

I worked with a simulated dataset of 16,193 source records, retained 16,093 valid order lines and created an exception log for duplicates and invalid records. The analysis covers net sales, gross profit, return rates and monthly performance, with automated KPI reconciliation.

One lesson: high sales alone can hide low margins, and discount comparisons do not prove causation. The project includes assumptions and recommendations for additional measurement.

GitHub: [add the repository URL after publishing]

#DataAnalytics #SQL #Python #PortfolioProject

Add Power BI and screenshots only after completing the accompanying Desktop report.
