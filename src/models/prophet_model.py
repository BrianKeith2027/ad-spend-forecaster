"""
Prophet Forecasting Model for Ad Spend
Author: Brian Stratton
"""
import pandas as pd
import numpy as np
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error
import logging
import warnings
warnings.filterwarnings("ignore")
logger = logging.getLogger(__name__)

class AdSpendProphetModel:
      """Facebook Prophet model for ad spend forecasting with seasonality."""
      def __init__(self, changepoint_prior_scale=0.05):
                self.changepoint_prior_scale = changepoint_prior_scale
                self.model = None
                self.forecast = None

      def prepare_data(self, df, channel=None):
                data = df.copy()
                if channel:
                              data = data[data["channel"] == channel]
                          daily = data.groupby("date")["spend"].sum().reset_index()
                daily.columns = ["ds", "y"]
                daily["ds"] = pd.to_datetime(daily["ds"])
                return daily

      def fit(self, df, channel=None):
                train_data = self.prepare_data(df, channel)
                self.model = Prophet(yearly_seasonality=True, weekly_seasonality=True,
                    changepoint_prior_scale=self.changepoint_prior_scale, interval_width=0.90)
                self.model.add_country_holidays(country_name="US")
                self.model.fit(train_data)
                return self

      def predict(self, periods=365):
                future = self.model.make_future_dataframe(periods=periods)
                self.forecast = self.model.predict(future)
                return self.forecast

      def get_monthly_forecast(self, periods=365):
                if self.forecast is None:
                              self.predict(periods)
                          fc = self.forecast.copy()
                fc["month"] = fc["ds"].dt.to_period("M")
                return fc.groupby("month").agg(
                    spend=("yhat", "sum"), lower=("yhat_lower", "sum"), upper=("yhat_upper", "sum")
                ).reset_index()

      def evaluate(self, df, channel=None, test_days=90):
                data = self.prepare_data(df, channel)
                cutoff = data["ds"].max() - pd.Timedelta(days=test_days)
                train = data[data["ds"] <= cutoff]
                test = data[data["ds"] > cutoff]
                m = Prophet(yearly_seasonality=True, weekly_seasonality=True,
                    changepoint_prior_scale=self.changepoint_prior_scale)
                m.add_country_holidays(country_name="US")
                m.fit(train)
                pred = m.predict(m.make_future_dataframe(periods=test_days))
                merged = test.merge(pred[["ds", "yhat"]], on="ds")
                mae = mean_absolute_error(merged["y"], merged["yhat"])
                mape = mean_absolute_percentage_error(merged["y"], merged["yhat"]) * 100
                rmse = np.sqrt(((merged["y"] - merged["yhat"]) ** 2).mean())
                return {"mae": round(mae, 2), "mape": round(mape, 2), "rmse": round(rmse, 2)}

  if __name__ == "__main__":
        from src.data.generate_ad_data import generate_ad_spend_data
        logging.basicConfig(level=logging.INFO)
        df = generate_ad_spend_data()
        model = AdSpendProphetModel()
        model.fit(df, channel="google_ads")
        model.predict(365)
        print("Metrics:", model.evaluate(df, channel="google_ads"))
