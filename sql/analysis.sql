-- QUERY: executive_kpis
SELECT ROUND(SUM(net_sales),2) net_sales, ROUND(SUM(gross_profit),2) gross_profit,
ROUND(100.0*SUM(gross_profit)/NULLIF(SUM(net_sales),0),2) margin_pct,
COUNT(DISTINCT order_id) orders,
ROUND(SUM(net_sales)/NULLIF(COUNT(DISTINCT order_id),0),2) aov,
ROUND(100.0*SUM(returned)/COUNT(*),2) line_return_rate_pct FROM orders;

-- QUERY: monthly_growth
WITH prior AS (SELECT *,LAG(net_sales) OVER(ORDER BY month) previous_month_sales FROM monthly_performance)
SELECT *,ROUND(100.0*(net_sales-previous_month_sales)/NULLIF(previous_month_sales,0),2) mom_growth_pct FROM prior ORDER BY month;

-- QUERY: category_profitability
SELECT category,ROUND(SUM(net_sales),2) net_sales,ROUND(SUM(gross_profit),2) gross_profit,
ROUND(100.0*SUM(gross_profit)/NULLIF(SUM(net_sales),0),2) margin_pct,
ROUND(100.0*AVG(returned),2) line_return_rate_pct FROM orders GROUP BY category ORDER BY gross_profit DESC;

-- QUERY: region_channel_mix
SELECT region,channel,COUNT(DISTINCT order_id) orders,ROUND(SUM(net_sales),2) net_sales,
ROUND(SUM(gross_profit),2) gross_profit FROM orders GROUP BY region,channel ORDER BY net_sales DESC;

-- QUERY: product_ranking
WITH p AS (SELECT product_id,product,category,ROUND(SUM(gross_profit),2) gross_profit FROM orders GROUP BY product_id,product,category)
SELECT *,DENSE_RANK() OVER(PARTITION BY category ORDER BY gross_profit DESC) profit_rank_in_category FROM p ORDER BY category,profit_rank_in_category;

-- QUERY: discount_analysis
SELECT discount_band,COUNT(*) lines,ROUND(SUM(net_sales),2) net_sales,
ROUND(100.0*SUM(gross_profit)/NULLIF(SUM(net_sales),0),2) margin_pct,
ROUND(100.0*AVG(returned),2) line_return_rate_pct FROM orders GROUP BY discount_band;

-- QUERY: repeat_customers
SELECT COUNT(*) customers,SUM(CASE WHEN orders>1 THEN 1 ELSE 0 END) repeat_customers,
ROUND(100.0*SUM(CASE WHEN orders>1 THEN 1 ELSE 0 END)/COUNT(*),2) repeat_customer_pct FROM customer_metrics;

-- QUERY: customer_value_segments
SELECT CASE WHEN net_sales>=20000 THEN 'High value' WHEN net_sales>=10000 THEN 'Medium value' ELSE 'Low value' END value_segment,
COUNT(*) customers,ROUND(SUM(net_sales),2) net_sales FROM customer_metrics GROUP BY value_segment;

-- QUERY: year_over_year
WITH yearly AS (SELECT SUBSTR(month,1,4) year,SUM(net_sales) net_sales FROM monthly_performance GROUP BY year),
prior AS (SELECT *,LAG(net_sales) OVER(ORDER BY year) previous_year_sales FROM yearly)
SELECT year,ROUND(net_sales,2) net_sales,ROUND(100.0*(net_sales-previous_year_sales)/NULLIF(previous_year_sales,0),2) yoy_growth_pct FROM prior;

-- QUERY: loss_making_lines
SELECT line_id,order_id,product,discount_pct,net_sales,gross_profit FROM orders WHERE gross_profit<0 ORDER BY gross_profit;
