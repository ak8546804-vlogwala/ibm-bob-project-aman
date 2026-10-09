# 🛍️ Retail Sales Analysis Dashboard

An interactive, multi-page analytics dashboard built with **Python + Streamlit** and **Plotly Express**, powered by a clean **Pandas** backend.

---

## Project Structure ##
**dataset** https://www.kaggle.com/datasets/terencekatua/retail-sales-dataset?resource=download .
retail_sales_analysis/
├── app.py                          # Main entry point & home page
├── pages/
│   ├── 1_Overview.py               # KPIs + monthly/quarterly trends
│   ├── 2_Product_Analysis.py       # Category revenue, quantity & pricing
│   ├── 3_Customer_Insights.py      # Gender, age, top-customer leaderboard
│   └── 4_Transaction_Deep_Dive.py  # Filterable table + distributions
├── backend/
│   ├── __init__.py
│   └── analysis.py                 # All pandas analysis functions
├── data/
│   └── retail_sales_dataset.csv    # Source dataset (1000 transactions)
├── requirements.txt
└── README.md
```

---

## Tech Stack

| Layer    | Library        | Purpose                               |
|----------|----------------|---------------------------------------|
| Frontend | Streamlit      | Multi-page dashboard & widgets        |
| Charts   | Plotly Express | Interactive bar, line, pie, box plots |
| Backend  | Pandas         | Data loading, grouping, aggregation   |
| Stats    | NumPy          | Descriptive statistics                |

---

## Features

### 📊 Overview
- 5 KPI cards: Total Revenue, Transactions, Unique Customers, Avg Order Value, Avg Quantity
- Monthly revenue area chart
- Monthly transaction count bar chart
- Quarterly revenue grouped bar chart
- Sidebar filters: Category, Gender, Year

### 🏷️ Product Analysis
- Revenue by category (bar chart)
- Units sold donut chart
- Average price per unit per category
- Monthly revenue trend lines by category
- Category summary table

### 👥 Customer Insights
- Revenue & transactions by gender (pie + bar)
- Revenue by age group
- Age distribution histogram
- Gender × Category revenue heatmap
- Age Group × Category grouped bar chart
- Top N customers leaderboard (configurable 5–20)

### 🔍 Transaction Deep-Dive
- Full sidebar filters: category, gender, age range, amount range, date range
- 7-metric statistics row (min, max, mean, median, std, Q1, Q3)
- Total amount histogram, price per unit bar, quantity bar, box-plot by category
- Filterable raw transaction table (sortable)
- CSV download of filtered data

---

## Setup & Run

```bash
# 1. Navigate to the project folder
cd retail_sales_analysis

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the dashboard
streamlit run app.py
```

The dashboard opens at **http://localhost:8501** in your browser.

---

## Dataset

`retail_sales_dataset.csv` — 1,000 retail transactions with columns:

| Column           | Description                          |
|------------------|--------------------------------------|
| Transaction ID   | Unique transaction identifier        |
| Date             | Transaction date (2023)              |
| Customer ID      | Unique customer identifier           |
| Gender           | Male / Female                        |
| Age              | Customer age                         |
| Product Category | Beauty / Clothing / Electronics      |
| Quantity         | Units purchased                      |
| Price per Unit   | Unit price ($)                       |
| Total Amount     | Quantity × Price per Unit ($)        |
