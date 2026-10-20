# E-Commerce Web Scraping & Pricing Intelligence

A modular, production-grade Python web scraping pipeline and interactive analytics dashboard built to extract e-commerce product catalogs, pricing tiers, star ratings, categories, and inventory metrics with automated data cleaning and visual analytics.

---

## 📌 Project Overview
- **Domain**: E-Commerce Intelligence & Web Scraping
- **Key Capabilities**:
  - Traverses paginated catalog items with custom session management and retry handling.
  - Parses individual product detail pages to retrieve UPC codes, stock numbers, and genre categories.
  - Normalizes text, cleans price symbols, handles nulls, and derives pricing tiers (Budget, Mid-Range, Premium, Luxury).
  - Exports validated datasets in both CSV and JSON formats.
  - Generates statistical audit charts (price distributions, rating proportions, category averages).
  - Features an interactive Streamlit dashboard for catalog browsing, price analysis, and custom data uploads.

---

## 📂 Repository Structure
```text
├── data/
│   ├── scraped_products.csv        # Cleaned dataset (CSV)
│   └── scraped_products.json       # Cleaned dataset (JSON)
├── visualizations/
│   ├── price_distribution.png      # Price histogram & boxplot
│   ├── ratings_breakdown.png       # Star rating breakdown
│   └── category_pricing.png        # Average price by category
├── scraper.py                      # Main scraping & extraction pipeline
├── scraper_analytics.py            # Statistical audit & visualizer
├── scraping_dashboard.py           # Interactive Streamlit dashboard
├── requirements.txt                # Project dependencies
└── README.md                       # Project documentation
```

---

## 🚀 Getting Started

### 1. Installation
```bash
pip install -r requirements.txt
```

### 2. Run the Scraper
```bash
# Scrape live catalog pages (e.g., 3 pages)
python scraper.py --pages 3
```

### 3. Generate Analytics
```bash
python scraper_analytics.py
```
Outputs visual charts to `visualizations/` folder.

### 4. Launch the Interactive Dashboard
```bash
streamlit run scraping_dashboard.py
```
Features:
- **Custom CSV Uploader**: Upload any product catalog dataset or generate fresh data.
- **Price Dispersion Analysis**: Histograms and boxplots showing price spreads.
- **Star Rating Audits**: Donut charts showing product customer reception.
- **Interactive Catalog Browser**: Filter by price, rating, or search query with CSV/JSON exports.
