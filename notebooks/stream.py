import os
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from prophet import Prophet

# Directory configuration
BASE_DIR = "/Users/rashidkarimov/Desktop/agro/data/processed/analysis/statistics_committee"
IMG_DIR = "/Users/rashidkarimov/Desktop/agro/images/2D"
os.makedirs(IMG_DIR, exist_ok=True)

# Metric definitions with units
METRICS = {
    "Tomato Area": ("tomato_area_features.csv", "tomato_area", "Area (hectares)"),
    "Tomato Yield": ("tomato_yield_features.csv", "tomato_yield", "Yield (tons/ha)"),
    "Tomato Production": ("tomato_prod_features.csv", "tomato_prod", "Production (tons)"),
    "Cucumber Area": ("cucumber_area_features.csv", "cucumber_area", "Area (hectares)"),
    "Cucumber Yield": ("cucumber_yield_features.csv", "cucumber_yield", "Yield (tons/ha)"),
    "Cucumber Production": ("cucumber_prod_features.csv", "cucumber_prod", "Production (tons)"),
}

# Streamlit app setup
st.set_page_config(page_title="Greenhouse Forecast Dashboard", layout="wide")
st.title("Greenhouse Forecast Dashboard (2D)")

# User input
choice = st.selectbox("Select Crop & Metric", list(METRICS.keys()))
fname, metric, unit = METRICS[choice]
df_path = os.path.join(BASE_DIR, fname)

# Load data with error handling
try:
    with st.spinner("Loading data..."):
        df = pd.read_csv(df_path)
except FileNotFoundError:
    st.error(f"Data file not found: {df_path}. Please check the file path.")
    st.stop()
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.stop()

# Debug data: Display unique settings to check for duplicates
st.write("### Data Debugging")
st.write("Unique 'Setting' values in the data:", df["Setting"].unique())

# Clean the 'Setting' column
df["Setting"] = df["Setting"].str.strip().str.lower()

# Filter for national data (Republic of Azerbaijan)
az_mask = df["Setting"].str.contains("republic", case=False, na=False)
az_df = df[az_mask].copy()
if az_df.empty:
    st.warning("No data found for 'Republic of Azerbaijan'. National forecast unavailable.")
    st.stop()

# Debug: Show national data
st.write("National data (Republic of Azerbaijan):", az_df)

# National Forecast Section
st.subheader("National Forecast")
ts = az_df[["year", metric]].rename(columns={"year": "ds", metric: "y"})
ts["ds"] = pd.to_datetime(ts["ds"].astype(str) + "-12-31")

with st.spinner("Fitting Prophet model..."):
    m = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False)
    m.fit(ts)

future = m.make_future_dataframe(periods=5, freq="YE")
forecast = m.predict(future)

# Plot national forecast
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(ts["ds"], ts["y"], marker="o", linestyle="-", color="blue", label="Historical")
ax.plot(forecast["ds"], forecast["yhat"], marker="o", linestyle="--", color="green", label="Forecast")
ax.fill_between(forecast["ds"], forecast["yhat_lower"], forecast["yhat_upper"], color="green", alpha=0.2, label="Confidence Interval")
ax.set_title(f"{choice} - National Forecast (Next 5 Years)", fontsize=14, pad=10)
ax.set_xlabel("Year", fontsize=12)
ax.set_ylabel(unit, fontsize=12)
ax.legend(loc="best")
ax.grid(True, linestyle="--", alpha=0.7)
ax.tick_params(axis="x", rotation=45)
fig.tight_layout()

st.pyplot(fig)

# Save forecast plot
out_path = os.path.join(IMG_DIR, f"{choice.replace(' ', '_')}_forecast.png")
fig.savefig(out_path, dpi=150, bbox_inches="tight")
plt.close(fig)
st.success(f"Forecast plot saved to: {out_path}")

# Regional Insights Section
st.subheader("Regional Insights")
df_no_rep = df[~az_mask].copy()
if "growth" not in df_no_rep.columns:
    st.warning("Feature 'growth' not found in the data. Regional growth analysis skipped.")
else:
    # Debug: Show regional data before processing
    st.write("Regional data (excluding Republic of Azerbaijan):", df_no_rep[["Setting", "growth"]])

    # Remove duplicates in 'Setting' and sort by growth
    df_no_rep = df_no_rep.drop_duplicates(subset=["Setting"])
    top10 = df_no_rep.sort_values("growth", ascending=False).head(10)

    # Check for duplicate regions
    unique_regions = top10["Setting"].nunique()
    if unique_regions < len(top10):
        st.warning(f"Only {unique_regions} unique regions found in the top 10. Check your data for duplicates in the 'Setting' column.")

    if top10.empty:
        st.warning("No regional data available after filtering.")
    else:
        fig2, ax2 = plt.subplots(figsize=(12, 6))
        bars = ax2.bar(top10["Setting"], top10["growth"], color="teal", edgecolor="black")
        ax2.set_title(f"{choice} - Top 10 Regions by Growth", fontsize=14, pad=10)
        ax2.set_ylabel("Growth (%)", fontsize=12)
        ax2.set_xticks(range(len(top10["Setting"])))
        ax2.set_xticklabels(top10["Setting"], rotation=45, ha="right", fontsize=10)
        ax2.grid(True, axis="y", linestyle="--", alpha=0.7)
        fig2.tight_layout()

        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width() / 2, height, f"{height:.1f}%", 
                     ha="center", va="bottom", fontsize=10)

        st.pyplot(fig2)

        # Save growth plot
        growth_path = os.path.join(IMG_DIR, f"{choice.replace(' ', '_')}_top10_growth.png")
        fig2.savefig(growth_path, dpi=150, bbox_inches="tight")
        plt.close(fig2)
        st.success(f"Top-10 growth chart saved to: {growth_path}")

# Year-over-Year Change Section
st.subheader("Year-over-Year Change")
yr_list = sorted(ts["ds"].dt.year.unique())
if len(yr_list) >= 2:
    y_end = ts.loc[ts["ds"].dt.year == yr_list[-1], "y"].iloc[0]
    y_prev = ts.loc[ts["ds"].dt.year == yr_list[-2], "y"].iloc[0]
    yoy_change = y_end - y_prev
    # Use 'normal' for default coloring (green for positive, red for negative)
    st.metric(label=f"Year-over-Year Change ({yr_list[-2]}→{yr_list[-1]})", 
              value=f"{yoy_change:.1f}", 
              delta=f"{yoy_change:.1f}", 
              delta_color="normal")
else:
    st.info("Insufficient data (less than 2 years) for Year-over-Year calculation.")