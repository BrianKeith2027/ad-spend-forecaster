"""
Synthetic Ad Spend Data Generator
Author: Brian Stratton
"""
import numpy as np
import pandas as pd
import os
import logging

logger = logging.getLogger(__name__)

CHANNELS = ["google_ads", "meta_ads", "linkedin", "programmatic"]
CHANNEL_CONFIG = {
      "google_ads": {"base": 4750, "trend": 0.0005, "noise": 300, "roas": 3.2},
      "meta_ads": {"base": 3270, "trend": 0.0004, "noise": 250, "roas": 2.8},
      "linkedin": {"base": 1150, "trend": 0.0006, "noise": 100, "roas": 1.9},
      "programmatic": {"base": 2260, "trend": 0.0002, "noise": 200, "roas": 2.1},
}

def generate_ad_spend_data(start_date="2022-01-01", end_date="2025-12-31", seed=42):
      np.random.seed(seed)
      dates = pd.date_range(start=start_date, end=end_date, freq="D")
      records = []
      for channel in CHANNELS:
                cfg = CHANNEL_CONFIG[channel]
                for i, date in enumerate(dates):
                              dow = date.dayofweek
                              month = date.month
                              trend_f = 1 + cfg["trend"] * i
                              weekly_f = 1.0 if dow < 5 else (0.3 if channel == "linkedin" else 0.7)
                              yearly_f = 1.0 + 0.15 * np.sin(2 * np.pi * (month - 1) / 12)
                              if month in [11, 12]: yearly_f *= 1.35
                                            if month == 1: yearly_f *= 0.80
                                                          noise = np.random.normal(0, cfg["noise"])
                              spend = max(cfg["base"] * trend_f * weekly_f * yearly_f + noise, 50)
                              cpc = np.random.uniform(0.80, 4.50)
                              clicks = int(spend / cpc)
                              impressions = int(clicks / np.random.uniform(0.015, 0.045))
                              ctr = clicks / impressions if impressions > 0 else 0
                              conversions = int(clicks * np.random.uniform(0.02, 0.08))
                              roas = np.random.normal(cfg["roas"], 0.4)
                              revenue = spend * max(roas, 0.5)
                              camp = np.random.choice(["brand", "performance", "retargeting"], p=[0.3, 0.5, 0.2])
                              records.append({"date": date, "channel": channel, "campaign_type": camp,
                                  "spend": round(spend, 2), "impressions": impressions, "clicks": clicks,
                                  "conversions": conversions, "revenue": round(revenue, 2),
                                  "cpc": round(cpc, 2), "ctr": round(ctr, 4), "roas": round(roas, 2)})
                      df = pd.DataFrame(records).sort_values(["date", "channel"]).reset_index(drop=True)
            logger.info("Generated %d rows", len(df))
    return df

def save_data(df, output_dir="data/sample"):
      os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "ad_spend_history.csv")
    df.to_csv(path, index=False)
    return path

if __name__ == "__main__":
      logging.basicConfig(level=logging.INFO)
    df = generate_ad_spend_data()
    save_data(df)
    print("Rows:", len(df))
    print(df.groupby("channel")["spend"].agg(["mean", "sum"]).round(2))
