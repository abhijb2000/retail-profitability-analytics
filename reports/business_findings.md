# Retail profitability — decision memo

Fictional portfolio case study | 2024–2025 | INR | generated from reports/summary.json

## Executive result
Net sales: INR 45,361,050.00; gross profit: INR 17,544,050.00; gross margin: 38.68%; distinct orders: 7,980; net sales/order: INR 5,684.34.

## Findings and actions
1. **Fashion contributes the most gross profit:** INR 6,322,500.00. Consider prioritising stock availability, subject to inventory and demand evidence not present here.
2. **Electronics has the lowest category margin:** 25.58%. Review cost and promotion mix before adding volume.
3. **Fashion has the highest line return rate:** 14.22%. Investigate product descriptions, sizing, and quality using additional return-reason data.
4. **20%+ discounted lines show 27.07% margin versus 44.1% on zero-discount lines.** Pilot a controlled discount test; the observed association does not establish causality because product/channel mix differs.

## Validation and limitations
16,193 source lines → 16,093 accepted; 60 duplicates and 40 invalid lines quarantined. 50 region values normalised. SQL and Python KPI totals reconcile in tests.

Returned lines receive full refunds with fully reversed COGS. This assumes resalable returns and excludes handling fees, delivery, tax, marketing, and overhead: gross profit is **not net profit**. Returns are attributed to original purchase dates; no return timestamp exists. Order counts include fully returned orders. Partial line returns are unsupported. Data was simulated; findings are not evidence about a real retailer and actions are recommendations, not achieved business impact.

## Next measurement
Track margin, conversion, net sales per customer, and return rate in a randomised promotion pilot. Define sample size and decision thresholds before launch. Add inventory, return reasons and fulfilment costs before implementation.
