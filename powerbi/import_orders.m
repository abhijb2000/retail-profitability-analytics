// Create a blank query, paste this in Advanced Editor, edit CsvPath, name FactOrders.
let
    CsvPath = "C:/YOUR_FOLDER/retail-profitability/data/processed/orders_clean.csv",
    Source = Csv.Document(File.Contents(CsvPath), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Headers, {
        {"line_id", type text}, {"order_id", type text}, {"order_date", type date},
        {"customer_id", type text}, {"region", type text}, {"channel", type text},
        {"product_id", type text}, {"product", type text}, {"category", type text},
        {"quantity", Int64.Type}, {"returned", Int64.Type},
        {"unit_price", Currency.Type}, {"unit_cost", Currency.Type}, {"discount_pct", type number},
        {"gross_sales", Currency.Type}, {"discount_amount", Currency.Type}, {"billed_sales", Currency.Type},
        {"refund_amount", Currency.Type}, {"net_sales", Currency.Type},
        {"cogs", Currency.Type}, {"gross_profit", Currency.Type}, {"month", type text}, {"discount_band", type text}
    }, "en-US")
in
    Typed
