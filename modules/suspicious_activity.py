"""
Suspicious Activity Detection - Flag unusual patterns and behaviors
"""

class SuspiciousActivityDetector:
    """Detect and classify suspicious casino behavior"""
    
    # Classification levels
    LEVELS = [
        "NORMAL",
        "REQUIRES_CLARIFICATION",
        "POTENTIALLY_UNFAIR",
        "STATISTICALLY_UNUSUAL",
        "TERMS_DISPUTE",
        "STRONG_EVIDENCE",
        "INSUFFICIENT_DATA"
    ]
    
    def __init__(self):
        """Initialize activity tracker"""
        self.incidents = []
    
    def flag_withdrawal_delay(self, requested_date, received_date, days_threshold=3):
        """
        Flag if withdrawal takes longer than expected
        
        Args:
            requested_date: Date withdrawal was requested
            received_date: Date withdrawal was received (None if pending)
            days_threshold: Days considered normal processing
        """
        if received_date is None:
            status = "PENDING"
            days_elapsed = None
        else:
            days_elapsed = (received_date - requested_date).days
            status = "DELAYED" if days_elapsed > days_threshold else "ON_TIME"
        
        incident = {
            "type": "withdrawal_delay",
            "status": status,
            "days_elapsed": days_elapsed,
            "severity": self._classify_withdrawal_delay(days_elapsed),
            "description": f"Withdrawal processing took {days_elapsed} days" if days_elapsed else "Withdrawal still pending"
        }
        self.incidents.append(incident)
        return incident
    
    def flag_repeated_verification(self, verification_count, threshold=2):
        """Flag if casino requests verification multiple times"""
        severity = "POTENTIALLY_UNFAIR" if verification_count >= threshold else "NORMAL"
        
        incident = {
            "type": "repeated_verification",
            "count": verification_count,
            "severity": severity,
            "description": f"Casino requested verification {verification_count} times"
        }
        self.incidents.append(incident)
        return incident
    
    def flag_balance_discrepancy(self, expected_balance, actual_balance):
        """Flag if balance doesn't match recorded calculations"""
        difference = abs(expected_balance - actual_balance)
        percentage_diff = (difference / expected_balance * 100) if expected_balance else 0
        
        severity = "NORMAL"
        if percentage_diff > 5:
            severity = "POTENTIALLY_UNFAIR"
        elif percentage_diff > 1:
            severity = "REQUIRES_CLARIFICATION"
        
        incident = {
            "type": "balance_discrepancy",
            "expected": expected_balance,
            "actual": actual_balance,
            "difference": round(difference, 2),
            "percentage": round(percentage_diff, 2),
            "severity": severity,
            "description": f"Balance discrepancy of {percentage_diff:.2f}% (${difference:.2f})"
        }
        self.incidents.append(incident)
        return incident
    
    def flag_rtp_anomaly(self, observed_rtp, advertised_rtp, sample_size=None):
        """
        Flag if observed RTP differs significantly from advertised
        
        Args:
            observed_rtp: Observed RTP percentage (0-100)
            advertised_rtp: Advertised RTP percentage (0-100)
            sample_size: Number of spins/bets (None = unknown)
        """
        difference = observed_rtp - advertised_rtp
        
        # Determine severity based on difference and sample size
        severity = self._classify_rtp_difference(difference, sample_size)
        
        incident = {
            "type": "rtp_anomaly",
            "observed_rtp": observed_rtp,
            "advertised_rtp": advertised_rtp,
            "difference": round(difference, 2),
            "sample_size": sample_size,
            "severity": severity,
            "description": f"Observed RTP {observed_rtp:.1f}% vs advertised {advertised_rtp:.1f}% (difference: {difference:.1f}%)"
        }
        self.incidents.append(incident)
        return incident
    
    def flag_account_restriction(self, restriction_type, reason=None):
        """Flag if account is restricted"""
        incident = {
            "type": "account_restriction",
            "restriction": restriction_type,
            "reason": reason,
            "severity": "REQUIRES_CLARIFICATION",
            "description": f"Account restricted: {restriction_type}"
        }
        self.incidents.append(incident)
        return incident
    
    def flag_bonus_terms_change(self, original_terms, new_terms):
        """Flag if bonus terms changed after acceptance"""
        incident = {
            "type": "bonus_terms_change",
            "original": original_terms,
            "new": new_terms,
            "severity": "TERMS_DISPUTE",
            "description": "Bonus terms changed after acceptance"
        }
        self.incidents.append(incident)
        return incident
    
    def get_incidents_by_severity(self, severity=None):
        """Get incidents filtered by severity level"""
        if severity is None:
            return self.incidents
        return [i for i in self.incidents if i["severity"] == severity]
    
    def get_summary(self):
        """Get summary of all flagged incidents"""
        if not self.incidents:
            return {"total": 0, "by_severity": {}}
        
        by_severity = {}
        for level in self.LEVELS:
            count = len(self.get_incidents_by_severity(level))
            if count > 0:
                by_severity[level] = count
        
        return {
            "total": len(self.incidents),
            "by_severity": by_severity,
            "incidents": self.incidents
        }
    
    # Helper methods
    
    @staticmethod
    def _classify_withdrawal_delay(days_elapsed):
        """Classify withdrawal delay severity"""
        if days_elapsed is None:
            return "REQUIRES_CLARIFICATION"
        elif days_elapsed <= 3:
            return "NORMAL"
        elif days_elapsed <= 7:
            return "REQUIRES_CLARIFICATION"
        elif days_elapsed <= 14:
            return "POTENTIALLY_UNFAIR"
        else:
            return "STRONG_EVIDENCE"
    
    @staticmethod
    def _classify_rtp_difference(difference, sample_size):
        """Classify RTP difference severity (negative = worse than advertised)"""
        # Without sample size, we can't calculate statistical significance
        if sample_size is None or sample_size < 100:
            if abs(difference) > 10:
                return "STATISTICALLY_UNUSUAL"
            elif abs(difference) > 5:
                return "REQUIRES_CLARIFICATION"
            else:
                return "NORMAL"
        
        # With larger sample size, tighter margins
        if abs(difference) > 5:
            return "POTENTIALLY_UNFAIR"
        elif abs(difference) > 2:
            return "REQUIRES_CLARIFICATION"
        else:
            return "NORMAL"
