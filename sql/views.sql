CREATE VIEW monthly_performance AS
SELECT month, ROUND(SUM(net_sales),2) net_sales,
ROUND(SUM(gross_profit),2) gross_profit,
COUNT(DISTINCT order_id) orders,
ROUND(100.0*SUM(gross_profit)/NULLIF(SUM(net_sales),0),2) margin_pct
FROM orders GROUP BY month;

CREATE VIEW customer_metrics AS
SELECT customer_id, COUNT(DISTINCT order_id) orders,
ROUND(SUM(net_sales),2) net_sales, MAX(order_date) last_order_date
FROM orders GROUP BY customer_id;
