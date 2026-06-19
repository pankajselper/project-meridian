\# Data Dictionary — Online Retail II



\*\*Source:\*\* UCI Machine Learning Repository — Online Retail II

\*\*Combined shape:\*\* 1,067,371 rows × 8 columns (both sheets combined)

\*\*Date range:\*\* 2009-12-01 to 2011-12-09

\*\*Unique customers:\*\* 5,942 | \*\*Unique countries:\*\* 43 | \*\*Unique products:\*\* 5,305 | \*\*Unique invoices:\*\* 53,628



| Column | Type | Non-null | Description | Known issues |

|---|---|---|---|---|

| Invoice | object (string) | 1,067,371 | 6-digit invoice number. Invoices starting with "C" are cancellations (19,494 rows). | None |

| StockCode | object (string) | 1,067,371 | Product code, uniquely identifies an item. | None |

| Description | object (string) | 1,062,989 | Product name. | 4,382 missing values |

| Quantity | int64 | 1,067,371 | Units sold per line item. | Contains negative values (returns/cancellations) |

| InvoiceDate | datetime64 | 1,067,371 | Date and time of transaction. | None — loaded correctly as a real datetime |

| Price | float64 | 1,067,371 | Unit price in GBP (£). | 5 rows have negative price — likely accounting adjustments, to investigate Day 3 |

| Customer ID | float64 | 824,364 | Unique customer identifier. | \*\*243,007 missing (\~23%)\*\* — these rows can't be used for customer-level analysis (RFM, churn, CLV) but may still count toward revenue totals |

| Country | object (string) | 1,067,371 | Country where the order was placed. | None |



\*\*Other findings:\*\*

\- 34,335 fully duplicate rows identified — to be removed during Day 3 cleaning.

\- Decision needed on Day 3: whether to drop or separately handle the \~243K rows missing Customer ID.

