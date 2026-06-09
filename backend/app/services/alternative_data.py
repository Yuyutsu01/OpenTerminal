import logging
import random
from datetime import datetime

logger = logging.getLogger(__name__)

class AlternativeDataService:
    def get_alternative_metrics(self) -> dict:
        """
        Returns a dictionary of alternative economic data parameters.
        Includes satellite index, container shipping volumes, job posting metrics, and funding index.
        """
        now = datetime.now()
        
        # 1. Port Traffic & Container Volumes (JNPT Mumbai, Chennai, Mundra)
        port_traffic = [
            {"port": "JNPT (Mumbai)", "traffic_TEU": 540000, "growth_yoy": 4.8, "congestion_status": "Normal"},
            {"port": "Mundra Port (Gujarat)", "traffic_TEU": 610000, "growth_yoy": 9.2, "congestion_status": "Low"},
            {"port": "Chennai Port", "traffic_TEU": 142000, "growth_yoy": -1.5, "congestion_status": "Moderate"},
            {"port": "Kolkata Port", "traffic_TEU": 85000, "growth_yoy": 2.1, "congestion_status": "Normal"}
        ]
        
        # 2. Satellite Activity index (Industrial activity proxy based on night-lights and heat emission)
        satellite_indices = {
            "NCR Delhi (Industrial Belt)": {"index": 112.5, "status": "High Activity", "yoy_change": 6.8},
            "Pune-Mumbai Auto Zone": {"index": 118.2, "status": "High Activity", "yoy_change": 8.1},
            "Bengaluru-Chennai Tech & Mfg": {"index": 122.4, "status": "Peak Activity", "yoy_change": 11.2},
            "Jamnagar Refinery Hub": {"index": 98.4, "status": "Maintenance Shutdowns", "yoy_change": -3.5}
        }
        
        # 3. Google Trends (Search counts for key economic terms, reflecting citizen anxiety/sentiment)
        google_trends = {
            "Gold Prices Today": {"query_volume": 88, "weekly_trend": "Rising", "significance": "High inflation hedge sentiment"},
            "Personal Loan Interest": {"query_volume": 62, "weekly_trend": "Stable", "significance": "Consumer credit demand"},
            "Stock Market Crash": {"query_volume": 42, "weekly_trend": "Declining", "significance": "Retail investor confidence"},
            "Recession": {"query_volume": 28, "weekly_trend": "Declining", "significance": "Low public economic anxiety"}
        }

        # 4. Job Market Index (Online job posting aggregation)
        job_market = {
            "IT & Software Development": {"posting_index": 85.0, "yoy_change": -12.5, "sentiment": "Soft Hiring"},
            "Banking & Finance": {"posting_index": 114.2, "yoy_change": 8.4, "sentiment": "Strong Hiring"},
            "Manufacturing & Infra": {"posting_index": 125.6, "yoy_change": 14.8, "sentiment": "Robust Hiring"},
            "Retail & E-commerce": {"posting_index": 105.0, "yoy_change": 3.2, "sentiment": "Steady"}
        }

        # 5. Startup Funding Index (Normalized monthly venture capital influx in India)
        # Seed, Series A-D aggregate tracking
        startup_funding_history = [
            {"date": "2025-06", "volume_usd_m": 820, "deal_count": 78},
            {"date": "2025-05", "volume_usd_m": 940, "deal_count": 82},
            {"date": "2025-04", "volume_usd_m": 680, "deal_count": 65},
            {"date": "2025-03", "volume_usd_m": 1200, "deal_count": 94},
            {"date": "2025-02", "volume_usd_m": 750, "deal_count": 72},
            {"date": "2025-01", "volume_usd_m": 580, "deal_count": 58}
        ]

        return {
            "port_traffic": port_traffic,
            "satellite_activity": satellite_indices,
            "google_trends": google_trends,
            "job_market": job_market,
            "startup_funding": {
                "latest_volume_usd_m": 820,
                "latest_deal_count": 78,
                "history": startup_funding_history
            },
            "last_updated": now.isoformat()
        }

# Global Singleton instance
alternative_data_service = AlternativeDataService()
