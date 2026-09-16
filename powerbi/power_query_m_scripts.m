// =============================================================================
// Power Query (M) Transformation Scripts
// Project: Market & Business Strategy Intelligence — Indian Electric 2W Market
// Target Tool: Microsoft Power BI Desktop (Power Query Editor)
// Data Source: Verified Analytical Marts (data/processed/sql/*.csv)
// =============================================================================

// -----------------------------------------------------------------------------
// Global Configuration Parameter: DataFolderPath
// Set this parameter in Power Query to point to the project data directory.
// Example: "C:\Users\Tanya Verma\OneDrive\Desktop\Market-Business-Strategy-Intelligence\data\processed\sql\"
// -----------------------------------------------------------------------------
let
    DataFolderPath = "data/processed/sql/" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]
in
    DataFolderPath;


// =============================================================================
// 1. Table: DimManufacturer
// Purpose: Manufacturer dimension providing OEM hierarchy, portfolio counts, and verification.
// =============================================================================
let
    Source = Csv.Document(File.Contents(DataFolderPath & "sql_competitive_analysis.csv"), [Delimiter=",", Columns=18, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    SelectedColumns = Table.SelectColumns(PromotedHeaders, {"manufacturer", "mfg_product_count", "mfg_portfolio_share_pct", "verification_status"}),
    RemovedDuplicates = Table.Distinct(SelectedColumns, {"manufacturer"}),
    ChangedTypes = Table.TransformColumnTypes(RemovedDuplicates, {
        {"manufacturer", type text},
        {"mfg_product_count", Int64.Type},
        {"mfg_portfolio_share_pct", type number},
        {"verification_status", type text}
    }),
    AddedAuditDate = Table.AddColumn(ChangedTypes, "Data_Ingestion_Date", each DateTime.Date(DateTime.LocalNow()), type date)
in
    AddedAuditDate;


// =============================================================================
// 2. Table: DimProduct
// Purpose: Product catalog dimension containing model attributes, category, and provenance.
// =============================================================================
let
    Source = Csv.Document(File.Contents(DataFolderPath & "sql_competitive_analysis.csv"), [Delimiter=",", Columns=18, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    SelectedColumns = Table.SelectColumns(PromotedHeaders, {"product", "manufacturer", "category", "verification_status"}),
    RemovedDuplicates = Table.Distinct(SelectedColumns, {"product"}),
    TrimmedText = Table.TransformColumns(RemovedDuplicates, {
        {"product", Text.Trim, type text},
        {"manufacturer", Text.Trim, type text},
        {"category", Text.Trim, type text}
    }),
    ChangedTypes = Table.TransformColumnTypes(TrimmedText, {
        {"product", type text},
        {"manufacturer", type text},
        {"category", type text},
        {"verification_status", type text}
    }),
    AddedAuditFlag = Table.AddColumn(ChangedTypes, "Is_Verified_Catalog", each if [verification_status] = "verified" then true else false, type logical)
in
    AddedAuditFlag;


// =============================================================================
// 3. Table: FactProductMetrics
// Purpose: Core analytical fact table with technical specs, prices, and computed ratios.
// =============================================================================
let
    Source = Csv.Document(File.Contents(DataFolderPath & "sql_competitive_analysis.csv"), [Delimiter=",", Columns=18, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    SelectedColumns = Table.SelectColumns(PromotedHeaders, {
        "product", "manufacturer", "price", "battery_kwh", "certified_range_km",
        "top_speed_kmph", "motor_power_kw", "price_per_km", "price_per_kwh", "verification_status"
    }),
    ReplacedBlanks = Table.ReplaceValue(SelectedColumns, "", null, Replacer.ReplaceValue, {
        "price", "battery_kwh", "certified_range_km", "top_speed_kmph", "motor_power_kw", "price_per_km", "price_per_kwh"
    }),
    ChangedTypes = Table.TransformColumnTypes(ReplacedBlanks, {
        {"product", type text},
        {"manufacturer", type text},
        {"price", Currency.Type},
        {"battery_kwh", type number},
        {"certified_range_km", type number},
        {"top_speed_kmph", type number},
        {"motor_power_kw", type number},
        {"price_per_km", Currency.Type},
        {"price_per_kwh", Currency.Type},
        {"verification_status", type text}
    }),
    AddedWhPerKm = Table.AddColumn(ChangedTypes, "energy_efficiency_wh_per_km", each 
        if [battery_kwh] <> null and [certified_range_km] <> null and [certified_range_km] > 0 
        then Number.Round(([battery_kwh] * 1000.0) / [certified_range_km], 2) 
        else null, 
        type number
    )
in
    AddedWhPerKm;


// =============================================================================
// 4. Table: CompetitiveAnalysis
// Purpose: Multi-dimensional rankings (price rank, range rank, speed rank, efficiency rank).
// =============================================================================
let
    Source = Csv.Document(File.Contents(DataFolderPath & "sql_competitive_analysis.csv"), [Delimiter=",", Columns=18, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    SelectedColumns = Table.SelectColumns(PromotedHeaders, {
        "product", "manufacturer", "manufacturer_rank", "product_rank",
        "price_efficiency_rank", "range_rank", "speed_rank", "mfg_portfolio_share_pct"
    }),
    ReplacedBlanks = Table.ReplaceValue(SelectedColumns, "", null, Replacer.ReplaceValue, {
        "manufacturer_rank", "product_rank", "price_efficiency_rank", "range_rank", "speed_rank"
    }),
    ChangedTypes = Table.TransformColumnTypes(ReplacedBlanks, {
        {"product", type text},
        {"manufacturer", type text},
        {"manufacturer_rank", Int64.Type},
        {"product_rank", Int64.Type},
        {"price_efficiency_rank", Int64.Type},
        {"range_rank", Int64.Type},
        {"speed_rank", Int64.Type},
        {"mfg_portfolio_share_pct", type number}
    })
in
    ChangedTypes;


// =============================================================================
// 5. Table: PricingAnalysis
// Purpose: Pricing percentiles, quartiles, market benchmarks, and premium positioning.
// =============================================================================
let
    Source = Csv.Document(File.Contents(DataFolderPath & "sql_pricing_analysis.csv"), [Delimiter=",", Columns=17, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    SelectedColumns = Table.SelectColumns(PromotedHeaders, {
        "product", "manufacturer", "price", "battery_capacity_kwh", "range_km",
        "top_speed_kmh", "price_per_km", "price_per_kwh", "price_bucket",
        "value_rank", "price_percentile", "price_quartile", "product_price_rank",
        "avg_market_price", "mfg_avg_price", "relative_price_position",
        "price_premium_vs_market_pct"
    }),
    ReplacedBlanks = Table.ReplaceValue(SelectedColumns, "", null, Replacer.ReplaceValue, {
        "price", "battery_capacity_kwh", "range_km", "top_speed_kmh", "price_per_km",
        "price_per_kwh", "value_rank", "price_percentile", "price_quartile",
        "product_price_rank", "avg_market_price", "mfg_avg_price",
        "price_premium_vs_market_pct"
    }),
    ChangedTypes = Table.TransformColumnTypes(ReplacedBlanks, {
        {"product", type text},
        {"manufacturer", type text},
        {"price", Currency.Type},
        {"battery_capacity_kwh", type number},
        {"range_km", type number},
        {"top_speed_kmh", type number},
        {"price_per_km", Currency.Type},
        {"price_per_kwh", Currency.Type},
        {"price_bucket", type text},
        {"value_rank", Int64.Type},
        {"price_percentile", type number},
        {"price_quartile", Int64.Type},
        {"product_price_rank", Int64.Type},
        {"avg_market_price", Currency.Type},
        {"mfg_avg_price", Currency.Type},
        {"relative_price_position", type text},
        {"price_premium_vs_market_pct", type number}
    })
in
    ChangedTypes;


// =============================================================================
// 6. Table: ProductPositioning
// Purpose: Segmentation across price tiers, range brackets, battery, and performance.
// =============================================================================
let
    Source = Csv.Document(File.Contents(DataFolderPath & "sql_product_positioning.csv"), [Delimiter=",", Columns=18, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    SelectedColumns = Table.SelectColumns(PromotedHeaders, {
        "product" meta [NewName="product"], // Note: maps model_name to product for join consistency
        "manufacturer", "price_bucket", "range_bucket", "battery_bucket",
        "performance_bucket", "positioning_summary", "manufacturer_product_rank",
        "manufacturer_budget_count", "manufacturer_midmarket_count", "manufacturer_premium_count"
    }),
    RenamedColumns = Table.RenameColumns(PromotedHeaders, {{"model_name", "product"}}),
    CleanedColumns = Table.SelectColumns(RenamedColumns, {
        "product", "manufacturer", "price_bucket", "range_bucket", "battery_bucket",
        "performance_bucket", "positioning_summary", "manufacturer_product_rank",
        "manufacturer_budget_count", "manufacturer_midmarket_count", "manufacturer_premium_count"
    }),
    ChangedTypes = Table.TransformColumnTypes(CleanedColumns, {
        {"product", type text},
        {"manufacturer", type text},
        {"price_bucket", type text},
        {"range_bucket", type text},
        {"battery_bucket", type text},
        {"performance_bucket", type text},
        {"positioning_summary", type text},
        {"manufacturer_product_rank", Int64.Type},
        {"manufacturer_budget_count", Int64.Type},
        {"manufacturer_midmarket_count", Int64.Type},
        {"manufacturer_premium_count", Int64.Type}
    })
in
    ChangedTypes;


// =============================================================================
// 7. Table: KPIStatus
// Purpose: Verified benchmark KPIs, calculation dates, and analytical methodologies.
// =============================================================================
let
    Source = Csv.Document(File.Contents(DataFolderPath & "sql_kpi_results.csv"), [Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangedTypes = Table.TransformColumnTypes(PromotedHeaders, {
        {"kpi_name", type text},
        {"value", type number},
        {"unit", type text},
        {"source", type text},
        {"verification_status", type text},
        {"calculation_date", type date},
        {"methodology", type text}
    })
in
    ChangedTypes;


// =============================================================================
// 8. Table: PendingMarketRegistrations
// Purpose: Fail-closed schema table for future Vahan registration data.
// In strict accordance with the provenance safeguard, this table loads 0 rows.
// =============================================================================
let
    EmptySchema = #table(
        type table [
            Date = date,
            Month = Int64.Type,
            Year = Int64.Type,
            State = text,
            VehicleCategory = text,
            FuelType = text,
            Manufacturer = text,
            Registrations = Int64.Type,
            Source = text,
            VerificationStatus = text
        ],
        {} // 0 rows inserted - strictly pending verified Vahan data
    )
in
    EmptySchema;
