import logging
import re
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# Pre-seeded news articles representing typical high-impact economic developments
SEED_NEWS = [
    {
        "id": 1,
        "title": "Fed raises interest rates by 25 basis points in bid to curb stubborn inflation",
        "source": "Bloomberg",
        "category": "Global Policy",
        "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(),
        "content": "The Federal Reserve raised its benchmark interest rate by a quarter percentage point, citing continued labor market strength and elevated inflation pressure. Chairman Powell indicated that further hikes remain on the table if economic indicators do not soften."
    },
    {
        "id": 2,
        "title": "Federal Reserve hikes interest rate by 0.25% as inflation remains persistent",
        "source": "Reuters",
        "category": "Global Policy",
        "timestamp": (datetime.now() - timedelta(hours=2.1)).isoformat(),
        "content": "US Federal Reserve officials voted to increase interest rates by 25 basis points today, pointing to persistent inflation and robust job growth. Economists suggest this hike may widen the interest rate gap with emerging markets, triggering potential currency outflows."
    },
    {
        "id": 3,
        "title": "OPEC+ oil ministers agree to extend voluntary crude oil production cuts through Q3",
        "source": "Bloomberg",
        "category": "Commodities",
        "timestamp": (datetime.now() - timedelta(hours=4)).isoformat(),
        "content": "OPEC+ ministers reached an agreement to extend their voluntary oil production cuts of 2.2 million barrels per day. The decision is aimed at stabilizing global oil prices amidst rising US production and soft Chinese demand forecast."
    },
    {
        "id": 4,
        "title": "RBI keeps repo rate unchanged at 6.50%, maintains stance on withdrawal of accommodation",
        "source": "RBI Bulletin",
        "category": "Domestic Policy",
        "timestamp": (datetime.now() - timedelta(hours=6)).isoformat(),
        "content": "The Reserve Bank of India Monetary Policy Committee decided by a 5-1 majority to keep the policy repo rate unchanged at 6.50%. RBI Governor Shaktikanta Das stated that the focus remains on bringing inflation durably down to the 4% target."
    },
    {
        "id": 5,
        "title": "Middle East tensions escalate following shipping corridor disruptions in the Red Sea",
        "source": "Reuters",
        "category": "Geopolitics",
        "timestamp": (datetime.now() - timedelta(hours=8)).isoformat(),
        "content": "Tensions intensified in the Red Sea as cargo vessels faced fresh attacks, forcing shipping conglomerates to reroute containers around Africa's Cape of Good Hope. The rerouting is expected to increase freight costs and delay shipments to Europe and India."
    },
    {
        "id": 6,
        "title": "SEBI issues new guidelines to tighten index derivative trading and curb speculative retail options",
        "source": "SEBI Circular",
        "category": "Domestic Regulation",
        "timestamp": (datetime.now() - timedelta(hours=12)).isoformat(),
        "content": "The Securities and Exchange Board of India (SEBI) announced a series of strict measures for derivatives trading, including higher margin requirements and limiting weekly expiries. The moves seek to address financial stability risks from retail options trading."
    },
    {
        "id": 7,
        "title": "IMF raises India's GDP growth forecast to 6.8% on robust domestic investment",
        "source": "IMF News",
        "category": "Global Reports",
        "timestamp": (datetime.now() - timedelta(days=1)).isoformat(),
        "content": "The International Monetary Fund upgraded India's growth projection for the current fiscal year to 6.8%, up from its previous estimate of 6.5%. The IMF credited strong public infrastructure investments and resilient private consumption."
    }
]

# Simple sentiment dictionaries
POSITIVE_WORDS = {"raise", "hike", "growth", "upgrade", "recovery", "expansion", "stabilize", "increase", "strong", "benefit", "boost"}
NEGATIVE_WORDS = {"fall", "drop", "decline", "cut", "inflation", "deficit", "disruption", "tension", "conflict", "risk", "warn", "worry"}

class NewsIntelligenceEngine:
    def __init__(self):
        self.articles = list(SEED_NEWS)

    def process_news(self) -> list[dict]:
        """
        Processes news articles: removes duplicates, ranks importance,
        detects sentiment, and generates summaries.
        """
        # 1. Deduplicate news based on Jaccard Headline similarity
        deduplicated = self._deduplicate(self.articles)
        
        processed = []
        for article in deduplicated:
            # 2. Sentiment analysis
            sentiment, score = self._analyze_sentiment(article["title"] + " " + article["content"])
            
            # 3. Importance ranking
            importance = self._rank_importance(article)
            
            # 4. Bullet summary generation
            summary = self._generate_bullet_summary(article)
            
            processed.append({
                **article,
                "sentiment": sentiment,
                "sentiment_score": score,
                "importance": importance,
                "summary": summary
            })
            
        return processed

    def _deduplicate(self, articles: list[dict]) -> list[dict]:
        """
        Jaccard-similarity based text deduplicator.
        Removes articles that talk about the exact same event.
        """
        unique_articles = []
        for art in articles:
            # Check similarity with existing unique articles
            is_dup = False
            art_words = self._tokenize(art["title"])
            
            for u_art in unique_articles:
                u_words = self._tokenize(u_art["title"])
                # Calculate Jaccard similarity
                intersection = len(art_words.intersection(u_words))
                union = len(art_words.union(u_words))
                similarity = intersection / union if union > 0 else 0
                
                # If similarity is higher than 40%, flag as duplicate
                if similarity > 0.4:
                    is_dup = True
                    # Keep the one with longer content
                    if len(art["content"]) > len(u_art["content"]):
                        unique_articles.remove(u_art)
                        unique_articles.append(art)
                    break
            if not is_dup:
                unique_articles.append(art)
                
        return unique_articles

    def _tokenize(self, text: str) -> set[str]:
        # Lowercase, keep alphanumeric words, split
        clean_text = re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())
        words = set(clean_text.split())
        # Filter out common stop words
        stop_words = {"the", "a", "an", "in", "to", "of", "by", "as", "at", "for", "on", "and"}
        return words - stop_words

    def _analyze_sentiment(self, text: str) -> tuple[str, float]:
        """
        Rule-based financial sentiment analyzer.
        """
        words = self._tokenize(text)
        pos_count = len(words.intersection(POSITIVE_WORDS))
        neg_count = len(words.intersection(NEGATIVE_WORDS))
        
        diff = pos_count - neg_count
        total = pos_count + neg_count
        
        score = diff / total if total > 0 else 0.0
        
        if score > 0.15:
            sentiment = "Positive"
        elif score < -0.15:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
            
        return sentiment, round(score, 2)

    def _rank_importance(self, article: dict) -> str:
        """
        Ranks importance based on category and keywords.
        """
        title = article["title"].lower()
        content = article["content"].lower()
        
        # High priority indicators
        high_indicators = {"fed", "federal reserve", "rbi", "repo rate", "rate hike", "nuclear", "war", "conflict", "tariff", "trade war"}
        
        # Check overlaps
        words = set((title + " " + content).split())
        if len(words.intersection(high_indicators)) >= 1 or article["category"] in ["Global Policy", "Domestic Policy"]:
            return "High"
        elif article["category"] in ["Commodities", "Geopolitics"]:
            return "Medium"
        return "Low"

    def _generate_bullet_summary(self, article: dict) -> list[str]:
        """
        Extracts key sentences and creates formatted bullet points.
        """
        content = article["content"]
        # Split into sentences
        sentences = [s.strip() for s in content.split(".") if s.strip()]
        
        bullets = []
        for s in sentences[:3]:
            # Add bullet points
            bullets.append(s)
            
        # If too few, mock some structured bullets
        if len(bullets) < 2:
            bullets.append(f"Development reported by {article['source']}.")
            
        return bullets

# Global Singleton instance
news_intelligence_engine = NewsIntelligenceEngine()
