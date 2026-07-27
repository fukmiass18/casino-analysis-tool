"""
Casino Scoring System - Rate casinos across multiple categories
"""

class CasinoScorer:
    """Score a casino across 12 key categories"""
    
    CATEGORIES = [
        "registration",
        "kyc",
        "bonuses",
        "game_selection",
        "gameplay",
        "rtp_results",
        "deposits",
        "withdrawals",
        "support",
        "transparency",
        "safety",
        "trust"
    ]
    
    CATEGORY_DESCRIPTIONS = {
        "registration": "Speed, ease, clarity of account creation",
        "kyc": "Friction, delays, document requests",
        "bonuses": "Value, transparency, wagering restrictions",
        "game_selection": "Range, providers, stability, availability",
        "gameplay": "Responsiveness, errors, crashes, stability",
        "rtp_results": "Observed RTP vs advertised RTP",
        "deposits": "Speed, fees, available methods",
        "withdrawals": "Processing time, delays, restrictions, obstruction",
        "support": "Response time, quality, helpfulness",
        "transparency": "Accuracy of terms, clarity of rules",
        "safety": "Responsible gambling controls, fraud prevention",
        "trust": "Complaints, account restrictions, evidence quality"
    }
    
    def __init__(self):
        """Initialize scorer with default scores"""
        self.scores = {cat: None for cat in self.CATEGORIES}
        self.notes = {cat: "" for cat in self.CATEGORIES}
    
    def set_score(self, category, score, note=""):
        """
        Set score for a category
        
        Args:
            category (str): One of CATEGORIES
            score (int): Score 1-10 (1=poor, 10=excellent)
            note (str): Optional detailed note
        """
        if category not in self.CATEGORIES:
            raise ValueError(f"Invalid category: {category}")
        if not 1 <= score <= 10:
            raise ValueError("Score must be between 1 and 10")
        
        self.scores[category] = score
        self.notes[category] = note
    
    def calculate_overall_score(self):
        """Calculate average score across all categories"""
        valid_scores = [s for s in self.scores.values() if s is not None]
        if not valid_scores:
            return None
        return sum(valid_scores) / len(valid_scores)
    
    def get_risk_level(self):
        """Determine risk level based on overall score"""
        overall = self.calculate_overall_score()
        
        if overall is None:
            return "INCOMPLETE"
        elif overall >= 8:
            return "GREEN"  # Low risk, good experience
        elif overall >= 6:
            return "YELLOW"  # Medium risk, proceed with caution
        else:
            return "RED"  # High risk, not recommended
    
    def get_recommendation(self):
        """Generate recommendation based on scores"""
        risk = self.get_risk_level()
        overall = self.calculate_overall_score()
        
        if risk == "INCOMPLETE":
            return "INCOMPLETE - More data needed"
        elif risk == "GREEN":
            return f"RECOMMENDED - Overall score {overall:.1f}/10. Casino meets expectations."
        elif risk == "YELLOW":
            return f"CAUTION - Overall score {overall:.1f}/10. Proceed with care and manage expectations."
        else:
            return f"NOT RECOMMENDED - Overall score {overall:.1f}/10. Significant concerns identified."
    
    def get_problem_areas(self, threshold=5):
        """Get categories scoring below threshold"""
        problems = []
        for cat, score in self.scores.items():
            if score is not None and score < threshold:
                problems.append({
                    "category": cat,
                    "score": score,
                    "note": self.notes[cat]
                })
        return sorted(problems, key=lambda x: x["score"])
    
    def get_strengths(self, threshold=8):
        """Get categories scoring above threshold"""
        strengths = []
        for cat, score in self.scores.items():
            if score is not None and score >= threshold:
                strengths.append({
                    "category": cat,
                    "score": score,
                    "note": self.notes[cat]
                })
        return sorted(strengths, key=lambda x: x["score"], reverse=True)
    
    def get_report_dict(self):
        """Get complete scoring report as dictionary"""
        return {
            "category_scores": self.scores,
            "category_notes": self.notes,
            "overall_score": round(self.calculate_overall_score(), 1) if self.calculate_overall_score() else None,
            "risk_level": self.get_risk_level(),
            "recommendation": self.get_recommendation(),
            "problem_areas": self.get_problem_areas(),
            "strengths": self.get_strengths()
        }
