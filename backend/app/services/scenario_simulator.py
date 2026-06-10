import logging

logger = logging.getLogger(__name__)

# Baseline inputs
BASE_OIL = 82.50
BASE_FED_RATE = 5.25
BASE_GEOPOLITICS = 40.0

# Baseline outputs
BASE_USD_INR = 83.50
BASE_CPI = 4.85
BASE_REPO_RATE = 6.50
BASE_GDP_GROWTH = 7.8
BASE_NIFTY = 22800.0

class ScenarioSimulatorService:
    def simulate(self, oil_price: float, fed_rate: float, geopolitical_risk: float) -> dict:
        """
        Simulates the economic transmission effects of changes in global variables on the Indian economy.
        Using empirical economic sensitivity multipliers.
        """
        # 1. USD/INR Exchange Rate Impact
        # High oil widens CAD -> weakens Rupee (+0.08 per dollar)
        # High Fed rate causes capital outflows -> weakens Rupee (+0.6 per 1%)
        # Geopolitical risk drives dollar demand -> weakens Rupee (+0.02 per point)
        oil_diff = oil_price - BASE_OIL
        fed_diff = fed_rate - BASE_FED_RATE
        geo_diff = geopolitical_risk - BASE_GEOPOLITICS
        
        sim_usd_inr = BASE_USD_INR + (0.08 * oil_diff) + (0.60 * fed_diff) + (0.02 * geo_diff)
        sim_usd_inr = round(max(75.0, min(100.0, sim_usd_inr)), 2)
        inr_depreciation_pct = round(((sim_usd_inr - BASE_USD_INR) / BASE_USD_INR) * 100, 2)

        # 2. Indian CPI Inflation Impact
        # Oil surge has a direct transport impact (+0.035% per $1 oil increase)
        # Rupee depreciation increases imported inflation (+0.15% per 1 INR weaker rupee)
        usd_inr_diff = sim_usd_inr - BASE_USD_INR
        sim_cpi = BASE_CPI + (0.035 * oil_diff) + (0.15 * usd_inr_diff)
        sim_cpi = round(max(2.0, min(12.0, sim_cpi)), 2)

        # 3. RBI Repo Rate (Policy Reaction Function)
        # Central banks hike rates to anchor inflation expectations
        # Taylor-rule-like policy response: RBI raises repo rate by 0.50% for every 1.0% inflation rise
        cpi_diff = sim_cpi - BASE_CPI
        sim_repo_rate = BASE_REPO_RATE + (0.50 * cpi_diff)
        # Round to nearest 25 basis points (0.25)
        sim_repo_rate = round(round(sim_repo_rate * 4) / 4, 2)
        sim_repo_rate = max(4.00, min(9.50, sim_repo_rate))

        # 4. GDP Growth Impact
        # High oil compresses margins (-0.015% per $1 oil)
        # Higher repo rate raises cost of capital (-0.2% per 1% repo increase)
        repo_diff = sim_repo_rate - BASE_REPO_RATE
        sim_gdp_growth = BASE_GDP_GROWTH - (0.015 * oil_diff) - (0.20 * repo_diff)
        sim_gdp_growth = round(max(2.0, min(10.0, sim_gdp_growth)), 2)

        # 5. Equity Markets (Nifty 50) Valuation Impact
        # High oil, high interest rates, and geopolitical panic compress P/E multiples
        valuation_multiplier = (
            1.0 
            - (0.0015 * oil_diff) 
            - (0.025 * repo_diff) 
            - (0.0012 * geo_diff)
        )
        sim_nifty = BASE_NIFTY * valuation_multiplier
        sim_nifty = round(max(15000.0, min(30000.0, sim_nifty)), 0)

        # 6. Sector Impact Scores (-100 = Severe Drag, +100 = Major Tailwinds)
        energy_score = max(-100, min(100, int(2.5 * oil_diff)))
        aviation_score = max(-100, min(100, int(-3.5 * oil_diff - 1.5 * geo_diff)))
        paint_score = max(-100, min(100, int(-2.5 * oil_diff)))
        it_score = max(-100, min(100, int(4.0 * usd_inr_diff)))
        banking_score = max(-100, min(100, int(-12.0 * repo_diff)))
        auto_score = max(-100, min(100, int(-1.5 * oil_diff - 8.0 * repo_diff)))

        return {
            "inputs": {
                "oil_price": oil_price,
                "fed_rate": fed_rate,
                "geopolitical_risk": geopolitical_risk
            },
            "metrics": {
                "usd_inr": {
                    "value": sim_usd_inr,
                    "baseline": BASE_USD_INR,
                    "change": round(sim_usd_inr - BASE_USD_INR, 2),
                    "change_pct": inr_depreciation_pct,
                    "status": "Weaker Rupee" if sim_usd_inr > BASE_USD_INR else "Stronger Rupee"
                },
                "cpi_inflation": {
                    "value": sim_cpi,
                    "baseline": BASE_CPI,
                    "change": round(sim_cpi - BASE_CPI, 2),
                    "status": "Rising Inflation" if sim_cpi > BASE_CPI else "Easing Inflation"
                },
                "rbi_repo_rate": {
                    "value": sim_repo_rate,
                    "baseline": BASE_REPO_RATE,
                    "change": round(sim_repo_rate - BASE_REPO_RATE, 2),
                    "status": "Monetary Tightening" if sim_repo_rate > BASE_REPO_RATE else ("Monetary Easing" if sim_repo_rate < BASE_REPO_RATE else "Unchanged")
                },
                "gdp_growth": {
                    "value": sim_gdp_growth,
                    "baseline": BASE_GDP_GROWTH,
                    "change": round(sim_gdp_growth - BASE_GDP_GROWTH, 2),
                    "status": "Slowing Growth" if sim_gdp_growth < BASE_GDP_GROWTH else "Accelerating Growth"
                },
                "nifty_50": {
                    "value": sim_nifty,
                    "baseline": BASE_NIFTY,
                    "change": int(sim_nifty - BASE_NIFTY),
                    "change_pct": round(((sim_nifty - BASE_NIFTY) / BASE_NIFTY) * 100, 2),
                    "status": "Market Contraction" if sim_nifty < BASE_NIFTY else "Market Expansion"
                }
            },
            "sectors": [
                {"name": "Oil & Gas (Upstream)", "score": energy_score, "impact": "Beneficiary" if energy_score > 0 else "Hurt", "driver": "Crude realizations"},
                {"name": "Aviation", "score": aviation_score, "impact": "Hurt" if aviation_score < 0 else "Beneficiary", "driver": "Fuel cost pressure"},
                {"name": "Paints & Chemicals", "score": paint_score, "impact": "Hurt" if paint_score < 0 else "Beneficiary", "driver": "Crude derivative costs"},
                {"name": "IT Exporters", "score": it_score, "impact": "Beneficiary" if it_score > 0 else "Hurt", "driver": "Rupee depreciation gains"},
                {"name": "Banking & Finance", "score": banking_score, "impact": "Hurt" if banking_score < 0 else "Beneficiary", "driver": "Interest rates/yield margins"},
                {"name": "Automotive", "score": auto_score, "impact": "Hurt" if auto_score < 0 else "Beneficiary", "driver": "Fuel prices & EMI costs"}
            ]
        }

# Global Singleton instance
scenario_simulator_service = ScenarioSimulatorService()
