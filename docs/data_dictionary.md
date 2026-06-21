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



\## Day 3 — Cleaning the Data



Before touching the raw file, I wrote out a plan for how I'd handle each issue found on Day 2, so the cleaning wasn't just random deletions but a documented set of decisions.



\*\*Duplicates:\*\* Found 34,335 rows that were exact copies of another row — same invoice, product, quantity, date, price, customer, everything. These aren't real repeat purchases, just an export/data entry error, so I dropped them.



\*\*Negative and zero price rows:\*\* I actually checked these manually before deciding anything. The 5 negative-price rows all had the description "Adjust bad debt" — clearly internal accounting corrections, not real sales. The zero-price rows (6,019 of them) mostly had negative quantities and descriptions like "short" or "mixed," which look like inventory/stock adjustments rather than legitimate transactions (e.g. free promo items would still usually have a description that says so). I removed both groups for the same reason — they're not real customer transactions.



\*\*Cancelled orders:\*\* 19,104 invoices start with "C," meaning they were cancelled. I didn't delete these — they're real business events and matter later when I look at revenue leakage. Instead I added a new column, `is\_cancelled`, so they can be filtered in or out depending on the analysis.



\*\*Missing product descriptions:\*\* 4,382 rows had no description. Quantity, price, and customer info were all fine, so I just filled these with "Unknown" instead of dropping the row.



\*\*Missing Customer ID:\*\* This was the biggest issue — about 23% of rows have no customer attached. Since I can't do customer-level analysis (RFM, churn, lifetime value) without knowing who the customer is, I split the data into two files:

\- `sales\_clean\_full.csv` (1,027,017 rows) — includes everything, used for revenue-level totals

\- `sales\_clean\_customer\_level.csv` (797,815 rows) — only rows with a known Customer ID, used for anything customer-specific



\*\*New columns added:\*\*

\- `is\_cancelled` — flags cancelled orders

\- `TotalPrice` — Quantity × Price, needed for basically every revenue calculation from here on



All of this logic lives in `src/etl/clean.py`, so the cleaning can be re-run end-to-end any time, rather than being a one-off manual edit.

