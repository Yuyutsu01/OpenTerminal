import logging

logger = logging.getLogger(__name__)

# Core Knowledge Graph Definition
NODES = [
    {"id": "oil", "label": "Crude Oil Price", "category": "Commodity", "description": "Global price of Brent and WTI crude oil. India imports 80%+ of its needs."},
    {"id": "usd_strength", "label": "US Dollar Index (DXY)", "category": "Global Forex", "description": "Strength of the US dollar against global currencies."},
    {"id": "us_bond_yields", "label": "US 10Y Bond Yields", "category": "Global Bond", "description": "Yield on long-term US government debt. Risk-free asset benchmark."},
    {"id": "fii_flow", "label": "FII Capital Flows", "category": "Capital Flow", "description": "Foreign Institutional Investors equity/debt inflows into India."},
    {"id": "usd_inr", "label": "USD/INR Rate", "category": "Forex", "description": "Exchange value of 1 USD in Indian Rupees. Weaker Rupee raises import cost."},
    {"id": "inflation", "label": "CPI/WPI Inflation", "category": "Macro Indicator", "description": "Rate of domestic price increase. High inflation reduces real income."},
    {"id": "rbi_rates", "label": "RBI Repo Rate", "category": "Policy Rate", "description": "Benchmark interest rate set by RBI to manage liquidity and pricing."},
    {"id": "borrowing_cost", "label": "Cost of Capital", "category": "Finance", "description": "Loan and equity borrowing rates for Indian corporations and consumers."},
    {"id": "consumer_spending", "label": "Consumer Spending", "category": "Macro Indicator", "description": "Discretionary purchase power. Higher rates and inflation suppress spending."},
    {"id": "corp_earnings", "label": "Corporate Profit Margins", "category": "Corporate", "description": "Net earnings and margins of listed companies. Oil increases raw material costs."},
    {"id": "stock_market", "label": "Indian Equity Market", "category": "Market", "description": "Valuation and pricing of Nifty 50 and Sensex listed equities."}
]

EDGES = [
    # Global to Capital Flow / Forex
    {"source": "us_bond_yields", "target": "fii_flow", "relationship": "Rises in US yields prompt FII capital flight from emerging markets.", "sign": "-"},
    {"source": "usd_strength", "target": "usd_inr", "relationship": "A stronger dollar directly pressures the Rupee.", "sign": "+"},
    {"source": "fii_flow", "target": "usd_inr", "relationship": "FII capital flight triggers rupee depreciation due to dollar outflows.", "sign": "+"},
    
    # Oil Transmission
    {"source": "oil", "target": "usd_inr", "relationship": "India's massive oil imports require purchasing more dollars, weakening the rupee.", "sign": "+"},
    {"source": "oil", "target": "inflation", "relationship": "Increases transportation, shipping, and manufacturing raw material costs.", "sign": "+"},
    {"source": "oil", "target": "corp_earnings", "relationship": "Raises input chemical/fuel costs, compressing corporate profit margins.", "sign": "-"},
    
    # Forex Transmission
    {"source": "usd_inr", "target": "inflation", "relationship": "Weaker rupee results in imported inflation (purchasing global inputs costs more).", "sign": "+"},
    
    # Inflation and RBI Response
    {"source": "inflation", "target": "rbi_rates", "relationship": "RBI hikes interest rates to cool excess demand and anchor prices.", "sign": "+"},
    {"source": "inflation", "target": "consumer_spending", "relationship": "Erodes consumer purchasing power for discretionary products.", "sign": "-"},
    
    # RBI Rates to Finance / Spending
    {"source": "rbi_rates", "target": "borrowing_cost", "relationship": "Banks transmit central bank hikes to retail and corporate loan rates.", "sign": "+"},
    {"source": "borrowing_cost", "target": "consumer_spending", "relationship": "Higher EMIs (loans) leave consumers with less cash to spend.", "sign": "-"},
    {"source": "borrowing_cost", "target": "corp_earnings", "relationship": "Increases corporate debt interest servicing cost, shrinking net profit.", "sign": "-"},
    
    # Earnings/Spending to Market
    {"source": "consumer_spending", "target": "corp_earnings", "relationship": "Declining retail volumes result in lower corporate sales revenue.", "sign": "+"},
    {"source": "corp_earnings", "target": "stock_market", "relationship": "Falling corporate earnings drive stock index valuations down.", "sign": "+"},
    {"source": "borrowing_cost", "target": "stock_market", "relationship": "Higher cost of capital increases the discount rate, lowering equity present value.", "sign": "-"}
]

class RelationshipEngineService:
    def get_graph(self) -> dict:
        """
        Returns nodes and links representing the macroeconomic knowledge graph.
        """
        return {
            "nodes": NODES,
            "links": EDGES
        }

    def trace_causality(self, source_id: str, target_id: str) -> list[dict]:
        """
        Traces a transmission path between a source node and target node,
        returning the sequential chain of effects.
        """
        # Simple DFS/BFS path finding
        graph = {}
        for edge in EDGES:
            src = edge["source"]
            targ = edge["target"]
            if src not in graph:
                graph[src] = []
            graph[src].append(edge)
            
        paths = []
        
        def find_paths(current, target, current_path):
            if current == target:
                paths.append(list(current_path))
                return
            if current not in graph:
                return
            for edge in graph[current]:
                # Avoid cycles
                if edge not in current_path:
                    current_path.append(edge)
                    find_paths(edge["target"], target, current_path)
                    current_path.pop()
                    
        find_paths(source_id, target_id, [])
        
        if not paths:
            return []
            
        # Return the shortest path found
        shortest_path = min(paths, key=len)
        
        # Format the causality list for presentation
        causality_chain = []
        for i, step in enumerate(shortest_path):
            src_node = next((n for n in NODES if n["id"] == step["source"]), None)
            targ_node = next((n for n in NODES if n["id"] == step["target"]), None)
            causality_chain.append({
                "step": i + 1,
                "source": src_node["label"] if src_node else step["source"],
                "target": targ_node["label"] if targ_node else step["target"],
                "relationship": step["relationship"],
                "sign": step["sign"]
            })
            
        return causality_chain

# Global Singleton instance
relationship_engine_service = RelationshipEngineService()
