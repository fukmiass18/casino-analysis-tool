"""
RTP Calculator - Observed return-to-player analysis
"""

class RTPCalculator:
    """Calculate observed RTP from test session data"""
    
    def __init__(self, total_wagered, total_returned, advertised_rtp=None):
        """
        Initialize RTP calculator
        
        Args:
            total_wagered (float): Total amount wagered across all bets
            total_returned (float): Total amount returned (winnings + remaining balance)
            advertised_rtp (float, optional): Advertised RTP from casino (0-100)
        """
        self.total_wagered = total_wagered
        self.total_returned = total_returned
        self.advertised_rtp = advertised_rtp
    
    def calculate_observed_rtp(self):
        """Calculate observed RTP percentage"""
        if self.total_wagered == 0:
            return 0
        return (self.total_returned / self.total_wagered) * 100
    
    def calculate_rtp_difference(self):
        """Calculate difference between observed and advertised RTP"""
        if self.advertised_rtp is None:
            return None
        observed = self.calculate_observed_rtp()
        return observed - self.advertised_rtp
    
    def calculate_net_result(self):
        """Calculate net profit or loss"""
        return self.total_returned - self.total_wagered
    
    def get_summary(self):
        """Return summary of RTP analysis"""
        observed_rtp = self.calculate_observed_rtp()
        net_result = self.calculate_net_result()
        
        summary = {
            "total_wagered": self.total_wagered,
            "total_returned": self.total_returned,
            "observed_rtp": round(observed_rtp, 2),
            "net_result": round(net_result, 2),
            "advertised_rtp": self.advertised_rtp,
            "rtp_difference": round(self.calculate_rtp_difference(), 2) if self.advertised_rtp else None,
        }
        
        return summary


class BonusAnalyzer:
    """Analyze bonus value and wagering requirements"""
    
    def __init__(self, bonus_amount, wagering_requirement_multiplier, max_withdrawal=None):
        """
        Initialize bonus analyzer
        
        Args:
            bonus_amount (float): Bonus credit received
            wagering_requirement_multiplier (float): e.g., 35 for 35x requirement
            max_withdrawal (float, optional): Max amount withdrawable from bonus
        """
        self.bonus_amount = bonus_amount
        self.wagering_requirement_multiplier = wagering_requirement_multiplier
        self.max_withdrawal = max_withdrawal
    
    def calculate_wagering_requirement(self):
        """Calculate total wagering required to clear bonus"""
        return self.bonus_amount * self.wagering_requirement_multiplier
    
    def calculate_effective_bonus_value(self, actual_rtp):
        """
        Calculate the true value of the bonus after applying actual RTP
        
        Args:
            actual_rtp (float): Observed RTP as decimal (e.g., 0.95 for 95%)
        """
        wagering_required = self.calculate_wagering_requirement()
        winnings_from_wagering = wagering_required * (actual_rtp - 1)
        return max(0, winnings_from_wagering)
    
    def get_summary(self):
        """Return bonus analysis summary"""
        return {
            "bonus_amount": self.bonus_amount,
            "wagering_multiplier": self.wagering_requirement_multiplier,
            "wagering_required": round(self.calculate_wagering_requirement(), 2),
            "max_withdrawal": self.max_withdrawal,
        }
