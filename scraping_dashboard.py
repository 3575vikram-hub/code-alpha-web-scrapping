"""
E-Commerce Product Catalog Intelligence Dashboard
Multi-Page Catalog Scraping, Price Dispersion Analytics & Star Rating Audits
"""

import os
import sys
import random
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="E-Commerce Catalog Intelligence",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #0575e6 0%, #00f260 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.02rem;
        color: #555;
        margin-bottom: 1.2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 46px;
        white-space: pre-wrap;
        background-color: #f1f5f9;
        border-radius: 8px 8px 0px 0px;
        padding: 10px 16px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0575e6 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)


def generate_catalog_dataset(num_samples=100, seed=42):
    """Generate realistic e-commerce scraped book catalog with zero external dependencies."""
    random.seed(seed)
    categories = [
        "Poetry", "Historical Fiction", "Fiction", "Mystery", "History",
        "Young Adult", "Business", "Science Fiction", "Classics", "Philosophy",
        "Travel", "Romance", "Nonfiction", "Art", "Autobiography", "Thriller"
    ]
    sample_titles = [
        "A Light in the Attic", "Tipping the Velvet", "Soumission", "Sharp Objects",
        "Sapiens: A Brief History of Humankind", "The Requiem Red", "The Dirty Little Secrets of Getting Your Dream Job",
        "The Coming Woman", "The Boys in the Boat", "The Black Maria", "Starving Hearts", "Shakespeare's Sonnets",
        "Set Me Free", "Scott Pilgrim's Precious Little Life", "Rip it Up and Start Again", "Our Band Could Be Your Life",
        "Olio", "Mesa Selimovic: Dervis i smrt", "Libertarianism for Beginners", "It's Only the Himalayas",
        "How to Stop Worrying and Start Living", "Deep Work", "Atomic Habits", "Thinking, Fast and Slow",
        "Educated: A Memoir", "Zero to One", "Grit", "The Psychology of Money", "Clean Code", "Design Patterns"
    ]

    records = []
    for i in range(1, num_samples + 1):
        title = sample_titles[(i - 1) % len(sample_titles)]
        if i > len(sample_titles):
            title = f"{title} (Vol. {i // len(sample_titles) + 1})"

        price_gbp = round(random.uniform(11.50, 59.99), 2)
        star_rating = random.randint(1, 5)
        stock_count = random.randint(1, 24)
        cat = categories[(i - 1) % len(categories)]
        price_usd = round(price_gbp * 1.30, 2)

        if price_gbp < 20:
            tier = "Budget (<£20)"
        elif price_gbp <= 40:
            tier = "Mid-Range (£20-£40)"
        elif price_gbp <= 60:
            tier = "Premium (£40-£60)"
        else:
            tier = "Luxury (>£60)"

        records.append({
            "title": title,
            "price_gbp": price_gbp,
            "star_rating": star_rating,
            "is_in_stock": True,
            "product_url": f"http://books.toscrape.com/catalogue/item_{i}.html",
            "image_url": f"http://books.toscrape.com/media/cache/sample_{i}.jpg",
            "upc": f"a8f7c{i:05d}9e",
            "category": cat,
            "in_stock_count": stock_count,
            "description": f"An insightful publication in {cat} exploring key conceptual themes.",
            "price_usd_approx": price_usd,
            "price_tier": tier
        })

    return pd.DataFrame(records)


# ==========================================
# SIDEBAR: DATA INPUT SELECTION
# ==========================================
st.sidebar.image("https://img.icons8.com/fluency/96/books.png", width=64)
st.sidebar.title("Catalog Analytics System")
st.sidebar.markdown("---")
st.sidebar.markdown("### 📂 Data Source")

data_source = st.sidebar.radio(
    "Select Catalog Source:",
    [
        "📁 Upload My Own Catalog (CSV / Excel)",
        "🛒 System Default Catalog",
        "⚡ Generate Custom Catalog"
    ]
)

df_loaded = None

if data_source == "📁 Upload My Own Catalog (CSV / Excel)":
    uploaded_file = st.sidebar.file_uploader("Upload product catalog CSV / Excel:", type=["csv", "xlsx"])
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                df_loaded = pd.read_csv(uploaded_file)
            else:
                df_loaded = pd.read_excel(uploaded_file)
            st.sidebar.success(f"Loaded {len(df_loaded):,} products from file!")
        except Exception as e:
            st.sidebar.error(f"Error reading file: {e}")
    else:
        st.sidebar.info("Upload a catalog CSV to inspect, or switch to System Default.")

elif data_source == "⚡ Generate Custom Catalog":
    num_gen = st.sidebar.slider("Number of Catalog Products:", min_value=20, max_value=500, value=100, step=10)
    rand_seed = st.sidebar.number_input("Random Seed:", value=42, step=1)
    if st.sidebar.button("🎲 Generate Fresh Catalog", type="primary"):
        st.session_state["generated_catalog_df"] = generate_catalog_dataset(num_samples=num_gen, seed=int(rand_seed))
        st.sidebar.success(f"Generated {num_gen:,} catalog items!")

    if "generated_catalog_df" in st.session_state:
        df_loaded = st.session_state["generated_catalog_df"]
    else:
        df_loaded = generate_catalog_dataset(num_samples=num_gen, seed=int(rand_seed))

else:
    # Default catalog path
    possible_paths = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "scraped_products.csv"),
        os.path.join("CodeAlpha_Web_Scraping", "data", "scraped_products.csv"),
        os.path.join("sample_data", "sample_scraped_books.csv"),
        "scraped_products.csv"
    ]
    for p in possible_paths:
        if os.path.exists(p):
            df_loaded = pd.read_csv(p)
            break

    if df_loaded is None:
        df_loaded = generate_catalog_dataset(num_samples=100, seed=42)

# Fallback guarantee
if df_loaded is None or df_loaded.empty:
    df_loaded = generate_catalog_dataset(num_samples=100, seed=42)

# ==========================================
# INTELLIGENT COLUMN STANDARDIZATION
# ==========================================
col_map = {c.lower().strip(): c for c in df_loaded.columns}

def safe_col(names, fallback=None):
    for n in names:
        if n.lower() in col_map:
            return col_map[n.lower()]
    return fallback

title_col = safe_col(["title", "name", "book_title", "product_name"], fallback="title")
price_col = safe_col(["price_gbp", "price", "cost", "unit_price"], fallback="price_gbp")
rating_col = safe_col(["star_rating", "rating", "stars"], fallback="star_rating")
category_col = safe_col(["category", "genre", "department"], fallback="category")
stock_col = safe_col(["in_stock_count", "stock", "quantity", "inventory"], fallback="in_stock_count")

df = df_loaded.copy()

df["title"] = df[title_col].astype(str) if title_col in df.columns else "Untitled Product"
df["price_gbp"] = pd.to_numeric(df[price_col], errors="coerce").fillna(19.99) if price_col in df.columns else 19.99
df["star_rating"] = pd.to_numeric(df[rating_col], errors="coerce").fillna(3).astype(int) if rating_col in df.columns else 3
df["category"] = df[category_col].astype(str) if category_col in df.columns else "General"
df["in_stock_count"] = pd.to_numeric(df[stock_col], errors="coerce").fillna(10).astype(int) if stock_col in df.columns else 10
if "price_usd_approx" not in df.columns:
    df["price_usd_approx"] = (df["price_gbp"] * 1.30).round(2)

# ==========================================
# SIDEBAR FILTERS
# ==========================================
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 Filter Catalog")

search_query = st.sidebar.text_input("Search Titles / Keywords:", "")

cat_list = sorted(df["category"].unique())
chosen_cats = st.sidebar.multiselect("Filter Categories", cat_list, default=cat_list)

min_r, max_r = st.sidebar.slider("Star Rating (1-5)", min_value=1, max_value=5, value=(1, 5))

p_min = float(df["price_gbp"].min())
p_max = float(df["price_gbp"].max())
if p_min >= p_max:
    p_max = p_min + 1.0

price_range = st.sidebar.slider("Price (£)", min_value=p_min, max_value=p_max, value=(p_min, p_max))

filtered_df = df[
    (df["category"].isin(chosen_cats)) &
    (df["star_rating"] >= min_r) &
    (df["star_rating"] <= max_r) &
    (df["price_gbp"] >= price_range[0]) &
    (df["price_gbp"] <= price_range[1])
]

if search_query:
    filtered_df = filtered_df[filtered_df["title"].str.contains(search_query, case=False, na=False)]

if filtered_df.empty:
    st.warning("No catalog products matched your filters. Showing active dataset.")
    filtered_df = df.copy()

# Sidebar Download
st.sidebar.markdown("---")
st.sidebar.markdown("### 💾 Dataset Template")
csv_bytes = df.to_csv(index=False).encode("utf-8")
st.sidebar.download_button(
    "📥 Download Catalog CSV Template",
    data=csv_bytes,
    file_name="catalog_dataset.csv",
    mime="text/csv"
)

# ==========================================
# MAIN DASHBOARD INTERFACE
# ==========================================
st.markdown('<div class="main-title">🛒 E-Commerce Product Catalog Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Multi-Page Catalog Scraping, Price Dispersion Analytics & Star Rating Audits</div>', unsafe_allow_html=True)

# Top KPIs
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("📚 Books Listed", f"{len(filtered_df):,}")
c2.metric("💷 Average Price", f"£{filtered_df['price_gbp'].mean():.2f}")
c3.metric("⭐ Median Rating", f"{filtered_df['star_rating'].median():.1f} / 5")
c4.metric("📦 Units in Stock", f"{filtered_df['in_stock_count'].sum():,}")
c5.metric("🏷️ Categories", f"{filtered_df['category'].nunique()}")

st.markdown("---")

t1, t2, t3 = st.tabs(["📊 Pricing & Rating Analytics", "📖 Interactive Catalog Browser", "📥 Data Exports"])

with t1:
    col_x, col_y = st.columns(2)
    with col_x:
        st.subheader("Price Distribution (£ GBP)")
        fig_hist = px.histogram(
            filtered_df,
            x="price_gbp",
            nbins=20,
            marginal="box",
            color_discrete_sequence=["#0575e6"],
            title="Book Price Dispersion & Spread"
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    with col_y:
        st.subheader("Star Rating Proportions")
        rating_counts = filtered_df["star_rating"].value_counts().reset_index()
        rating_counts.columns = ["Rating", "Count"]
        rating_counts = rating_counts.sort_values("Rating")
        fig_pie = px.pie(
            rating_counts,
            names="Rating",
            values="Count",
            hole=0.45,
            color_discrete_sequence=px.colors.sequential.Teal,
            title="Proportion of Products by Star Rating (1-5)"
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("Average Price by Category (£)")
    cat_avg = filtered_df.groupby("category")["price_gbp"].mean().reset_index().sort_values("price_gbp", ascending=False)
    fig_cat_price = px.bar(
        cat_avg.head(15),
        x="price_gbp",
        y="category",
        orientation="h",
        color="price_gbp",
        color_continuous_scale="Blues",
        labels={"price_gbp": "Avg Price (£)", "category": "Category"},
        title="Top Categories Ranked by Average Price"
    )
    st.plotly_chart(fig_cat_price, use_container_width=True)

with t2:
    st.subheader("Interactive Catalog Browser")
    disp_cols = ["title", "price_gbp", "star_rating", "category", "in_stock_count", "price_usd_approx"]
    st.dataframe(
        filtered_df[[c for c in disp_cols if c in filtered_df.columns]],
        use_container_width=True,
        height=380
    )

with t3:
    st.subheader("Export Catalog Dataset")
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.download_button(
            "📥 Download Filtered CSV",
            data=filtered_df.to_csv(index=False).encode("utf-8"),
            file_name="catalog_filtered_data.csv",
            mime="text/csv"
        )
    with col_d2:
        st.download_button(
            "📥 Download Filtered JSON",
            data=filtered_df.to_json(orient="records", indent=2).encode("utf-8"),
            file_name="catalog_filtered_data.json",
            mime="application/json"
        )
