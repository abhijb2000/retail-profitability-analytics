# Retail Profitability & Returns Analytics

**Portfolio case study prepared for Abhijit Samal · Python · SQLite · interactive dashboard · Power BI build kit**

Open `dashboard/index.html` for the completed interactive dashboard.

## Business problem
A fictional omnichannel retailer wants to grow sales without sacrificing margin. Which categories generate profit? Where do returns and heavy discounts erode revenue? This project turns order-line records into a validated dataset, SQL answers, an interactive dashboard, and a decision memo.

**Data is entirely simulated, not real customer/company data.** It covers 2024–2025 in INR. The generator uses seed 42 and deliberately introduces data-quality problems. The patterns reflect generator assumptions, not market research.

## Results
| Metric | Validated result |
|---|---:|
| Source rows | 16,193 |
| Accepted order lines | 16,093 |
| Duplicate / invalid rows | 60 / 40 |
| Distinct orders | 7,980 |
| Net sales | ₹45,361,050 |
| Gross profit | ₹17,544,050 |
| Gross margin | 38.68% |
| Line return rate | 8.00% |

Fashion contributes ₹6,322,500 gross profit but has a 14.22% line return rate. Electronics has the lowest category margin at 25.58%. Lines discounted by 20%+ show 27.07% margin versus 44.10% for zero-discount lines. These are descriptive associations; promotion effects require a controlled test. See [decision memo](reports/business_findings.md).

## Run in five minutes
1. Download and unzip this repository. Install Python 3.10+ if necessary.
2. Open a terminal **inside this folder**, containing README.md.
3. Run these commands (use `py` instead of `python` on Windows if needed):

```bash
python src/generate_data.py
python src/pipeline.py
python -m unittest discover -s tests -v
```

4. Double-click `dashboard/index.html`. It works offline and needs no web server or extra libraries. Change region, category, channel and date filters; export the filtered rows.
5. Open `data/processed/orders_clean.csv` in Excel or import it into Power BI. Follow [the Power BI guide](powerbi/BUILD_GUIDE.md).

Already-generated outputs are included, so you can inspect the project immediately. The HTML is the **completed dashboard**. Power BI files are a build kit (M query, DAX and theme), **not a completed or Desktop-validated PBIX**. Build and verify your own PBIX before listing Power BI development as completed experience.

## Analysis design
The pipeline normalises region values, deduplicates by line ID, validates dates and numeric ranges, quarantines rejected rows, calculates financial columns, creates SQLite tables/views, executes ten analytical queries and rebuilds the dashboard and memo. No source records are silently modified in the raw CSV. Duplicates use first-record-wins; conflicting duplicate versions would need investigation in production.

SQL demonstrates aggregations, CASE, CTEs, LAG, DENSE_RANK, distinct order counts, customer segmentation, monthly/annual growth and returns analysis. Python uses the standard library for reproducibility without dependency setup. Eight automated checks cover financial identities, refund handling, rejected-row reconciliation and SQL/Python agreement. GitHub Actions reruns the pipeline on push/PR.

### Metric contracts
| Metric | Definition |
|---|---|
| Gross sales | quantity × list unit price |
| Billed sales | gross sales − discount amount |
| Refund | billed sales for fully returned lines; otherwise 0 |
| Net sales | billed sales − refunds |
| COGS | quantity × unit cost for retained lines; otherwise 0 |
| Gross profit | net sales − COGS |
| Gross margin | sum(gross profit) / sum(net sales) |
| Net AOV | net sales / distinct order IDs, including returned orders |
| Return rate | returned line count / all accepted line count |

Money is rounded at line level to two decimals. Margins are calculated from totals, not averaged line percentages. Order counts across categories are non-additive because orders may contain multiple categories.

### Limitations
Full-line returns are attributed to purchase date; no return date/reason exists. Returned products are assumed resalable, reversing all COGS. Tax, shipping, marketing, handling and overhead are excluded. This is gross-profit analysis, not net-profit accounting. Dataset/customer patterns and seasonality are designed. No measured business uplift or real employer impact is claimed.

## Repository contents
```text
data/raw/orders.csv                 original simulated records
data/processed/orders_clean.csv     validated analytical dataset
data/processed/rejected_rows.csv    row-level exceptions
data/processed/retail.sqlite        runnable SQL database
data/processed/*.csv                ten SQL result exports
src/generate_data.py                seeded generator
src/pipeline.py                     cleaning, metrics, SQLite and reporting
sql/views.sql                      reusable analytical views
sql/analysis.sql                   ten named business queries
dashboard/index.html               completed offline dashboard
dashboard/template.html            editable source template
powerbi/                           build instructions, M, DAX, theme
reports/                           decision memo, QA, learning guide
tests/test_pipeline.py             eight meaningful validation checks
.github/workflows/validate.yml      reproducibility checks
```

## Publish to your GitHub
Create a repository named `retail-profitability-analytics` on your account `abhijb2000`. Upload the **contents of this folder**, not the ZIP itself. Ensure `.github/workflows/validate.yml` is included (a git push preserves it). No credentials are required in this project.

If using git locally:
```bash
git init
git add .
git commit -m "Add reproducible retail profitability analytics case study"
git branch -M main
git remote add origin https://github.com/abhijb2000/retail-profitability-analytics.git
git push -u origin main
```
The remote must exist first; authenticate through your own GitHub client. Suggested topics: `data-analysis`, `sql`, `python`, `retail-analytics`, `portfolio`. Add `power-bi` after completing that dashboard. This package does not create a GitHub repository or publish a website automatically.

## Demonstrate ownership
Read [learning and interview guide](reports/LEARNING_GUIDE.md). Reproduce at least one SQL query, verify one KPI manually, and add a new analysis before using this as an interview example. This prepared starter gives you a working foundation; your implementation and understanding are what you should present.

## License
Original project code and generated data are supplied under MIT; see LICENSE. Third-party tools remain subject to their own terms.
