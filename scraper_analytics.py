"""
CodeAlpha Data Analytics Internship - Task 1: Web Scraping Analytics
Script: scraper_analytics.py
Generates visual analytics and statistical summaries from scraped data.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_scraped_data(data_path="data/scraped_products.csv", output_dir="visualizations"):
    os.makedirs(output_dir, exist_ok=True)
    if not os.path.exists(data_path):
        print(f"[Error] Dataset not found at: {data_path}. Please run scraper.py first.")
        return

    df = pd.read_csv(data_path)
    print("=" * 60)
    print("DATA QUALITY & DESCRIPTIVE STATS AUDIT")
    print("=" * 60)
    print(df.info())
    print("\nDescriptive Statistics for Numeric Features:")
    print(df[["price_gbp", "star_rating", "in_stock_count", "price_usd_approx"]].describe())

    # Setup styling
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    sns.set_palette("crest")

    # Figure 1: Price Distribution & Boxplot
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    sns.histplot(df["price_gbp"], kde=True, ax=axes[0], color="#2b5c8f", bins=15)
    axes[0].set_title("Price Distribution (£ GBP)", fontsize=14, fontweight="bold", pad=12)
    axes[0].set_xlabel("Price (£)")
    axes[0].set_ylabel("Product Count")

    sns.boxplot(y=df["price_gbp"], ax=axes[1], color="#52b788")
    axes[1].set_title("Price Dispersion & Outliers", fontsize=14, fontweight="bold", pad=12)
    axes[1].set_ylabel("Price (£)")
    plt.tight_layout()
    p1 = os.path.join(output_dir, "price_distribution.png")
    plt.savefig(p1, dpi=300)
    plt.close()
    print(f"[Exported] {p1}")

    # Figure 2: Rating Distribution
    plt.figure(figsize=(8, 5))
    rating_counts = df["star_rating"].value_counts().sort_index()
    colors = ["#e76f51", "#f4a261", "#e9c46a", "#2a9d8f", "#264653"]
    bars = plt.bar(rating_counts.index.astype(str), rating_counts.values, color=colors[:len(rating_counts)])
    plt.title("Distribution of Product Star Ratings (1-5)", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel("Star Rating")
    plt.ylabel("Number of Books")
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.3, int(yval), ha='center', va='bottom', fontweight='bold')
    plt.tight_layout()
    p2 = os.path.join(output_dir, "ratings_breakdown.png")
    plt.savefig(p2, dpi=300)
    plt.close()
    print(f"[Exported] {p2}")

    # Figure 3: Price by Category (Top 8 Categories)
    if "category" in df.columns and df["category"].nunique() > 1:
        top_cats = df["category"].value_counts().head(8).index
        df_sub = df[df["category"].isin(top_cats)]
        plt.figure(figsize=(10, 6))
        sns.barplot(data=df_sub, x="price_gbp", y="category", hue="category", estimator="mean", errorbar=None, palette="viridis", legend=False)
        plt.title("Average Book Price by Category (Top Categories)", fontsize=14, fontweight="bold", pad=12)
        plt.xlabel("Mean Price (£)")
        plt.ylabel("Category")
        plt.tight_layout()
        p3 = os.path.join(output_dir, "category_pricing.png")
        plt.savefig(p3, dpi=300)
        plt.close()
        print(f"[Exported] {p3}")

    print("\nVisual analytics successfully generated in visualizations/ folder!")

if __name__ == "__main__":
    analyze_scraped_data()
