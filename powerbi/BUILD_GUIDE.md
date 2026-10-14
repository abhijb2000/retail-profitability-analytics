# Build your Power BI version

The completed deliverable is `dashboard/index.html`. These instructions and code are a companion kit; no PBIX is supplied or tested in Power BI Desktop. Use Desktop on Windows and save your completed `Retail_Profitability.pbix` in this folder after validating it.

## 1. Import the cleaned data
Run the Python pipeline first, or use the included cleaned CSV. In Desktop, select Get data → Text/CSV → `data/processed/orders_clean.csv` → Transform data. Rename the query **FactOrders**. Set `order_date` to Date, IDs to Text, quantity/returned to Whole number, discount_pct to Decimal number, and financial columns to Fixed decimal number. Choose Close & apply.

Alternatively use New source → Blank query → Advanced Editor, paste `import_orders.m`, replace CsvPath with your actual Windows path (forward slashes are supported), and name it FactOrders. This imports Python-cleaned data; do not claim you performed the cleaning in Power Query unless you actually recreate it there.

## 2. Build the model
Create three reference queries from FactOrders:

| New dimension | Keep these columns | Remove duplicates on |
|---|---|---|
| DimProduct | product_id, product, category | product_id |
| DimCustomer | customer_id | customer_id |
| DimRegion | region | region |

Use Reference, then Choose columns, then Remove duplicates. Keep the original fact columns for reconciliation. Create DimDate using the first block in `measures.dax`. Mark it as a date table using Date. Sort YearMonth by YearMonthSort.

In Model view create active, single-direction one-to-many relationships:

| One side | Many side |
|---|---|
| DimDate[Date] | FactOrders[order_date] |
| DimProduct[product_id] | FactOrders[product_id] |
| DimCustomer[customer_id] | FactOrders[customer_id] |
| DimRegion[region] | FactOrders[region] |

Avoid bidirectional relationships. Use dimension columns on axes/slicers; hide corresponding fact dimension keys from Report view once the model works. Disable auto date/time for this file if using the explicit DimDate table.

## 3. Add DAX
Create each remaining block in `measures.dax` as a **separate new measure** on FactOrders; the complete file is not one pasteable expression. Format sales/profit/AOV as INR currency, percentages as Percentage with two decimals, and counts as whole numbers. Percentage measures return fractions; do not multiply them by 100 as well.

DATEADD needs the date model above. Put MoM on a chart/table by DimDate[YearMonth], rather than interpreting it as a total-period card. January 2024 and 2024 YoY are blank because prior-period observations are outside the dataset.

## 4. Design three pages
Import `theme.json` using the report theme menu. Use a 16:9 canvas, generous spacing, and clear titles.

| Page | Visual | Fields |
|---|---|---|
| Executive overview | 4 cards | Net Sales, Gross Profit, Gross Margin %, Orders |
| Executive overview | Line chart | DimDate[YearMonth] / Net Sales |
| Executive overview | Bar chart | DimProduct[category] / Gross Profit |
| Executive overview | Slicers | DimRegion[region], FactOrders[channel], DimDate[Date] |
| Profit & returns | Matrix | DimProduct[category], Net Sales, Gross Profit, Gross Margin %, Line Return Rate % |
| Profit & returns | Clustered column | FactOrders[discount_band] / Gross Margin % |
| Profit & returns | Product table | DimProduct[product] / Net Sales, Gross Profit, Line Return Rate % |
| Growth & customers | Matrix | DimDate[YearMonth] / Net Sales, MoM Growth %, YoY Growth % |
| Growth & customers | Cards | Customers, Net AOV |
| Growth & customers | Region chart | DimRegion[region] / Net Sales |

Sync region/channel/date slicers between pages if you want consistent scope. Add a text box with the simulated-data and returns assumptions. For a category drillthrough page, use DimProduct[category] as the drillthrough field and include a back button. Use View → Performance analyzer to inspect load times once visuals are finished; no benchmark is claimed by this kit.

## 5. Reconcile before claiming completion
Clear all filters. Expect 16,093 lines; 7,980 orders; net sales ₹45,361,050; gross profit ₹17,544,050; margin 38.68%; line return rate 8.00%. Region/category totals should sum to overall sales, while distinct orders across categories may overlap. Compare each month against `data/processed/monthly_growth.csv`. A mismatch usually indicates incorrect data types, relationships, filters, or summing percentages.

Test one region + one category + one month against the HTML dashboard. Check slicer interactions and drillthrough. Save the PBIX and export page screenshots to reports. Update README to state that the Power BI report is now built and validated, linking the screenshots.

## Microsoft references
- https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-date-tables
- https://learn.microsoft.com/en-us/powerquery-m/csv-document
- https://learn.microsoft.com/en-us/dax/dateadd-function-dax

These support date-table marking, CSV imports and classic date-column time intelligence. UI labels may vary by Desktop release.
