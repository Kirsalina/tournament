import math

class TournamentCalculator:
    def __init__(self):
        self.game_params = {
            'min_bet': 0.0,
            'rtp': 0.0,
            'volatility': 0.0
        }
        self.tournament_params = {
            'prize': 0.0,
            'goal_multiplier': 0.0,
            'expected_players': 0
        }

    def analyze_tournament(self, min_bet: float, rtp: float,
                         tournament_prize: float, goal_multiplier: float, 
                         expected_players: int, volatility: float) -> dict:
        self.game_params['min_bet'] = min_bet
        self.game_params['rtp'] = rtp
        self.game_params['volatility'] = volatility
        
        self.tournament_params['prize'] = tournament_prize
        self.tournament_params['goal_multiplier'] = goal_multiplier
        self.tournament_params['expected_players'] = expected_players
        
        return {
            'expected_revenue': self._calculate_expected_revenue(),
            'revenue_per_player': self._calculate_revenue_per_player(),
            'hit_chance': self._calculate_hit_chance(),
            'risk_assessment': self._assess_risk(),
            'volatility_impact': self._assess_volatility_impact()
        }

    def _calculate_expected_revenue(self) -> float:
        # Calculate attempts needed for first hit
        p_hit = self._calculate_hit_chance()
        expected_attempts = 1 / p_hit  # Expected number of spins until first success
        
        # Total bets made by all players until goal is hit
        total_bets = expected_attempts * self.tournament_params['expected_players']
        
        # Calculate revenue
        house_margin = 1 - (self.game_params['rtp']/100)
        expected_house_revenue = total_bets * self.game_params['min_bet'] * house_margin
        return expected_house_revenue - self.tournament_params['prize']

    def _calculate_revenue_per_player(self) -> float:
        if self.tournament_params['expected_players'] == 0:
            return 0.0
        return self._calculate_expected_revenue() / self.tournament_params['expected_players']

    def _calculate_hit_chance(self) -> float:
        # Base hit rate adjusted by RTP
        base_hit_rate = (1 / self.tournament_params['goal_multiplier']) * (self.game_params['rtp'] / 100)
        
        # Volatility reduces hit chance more as goal multiplier increases
        volatility_factor = 1 - (self.game_params['volatility'] / 10)
        goal_scale_factor = 1 / (1 + math.log10(self.tournament_params['goal_multiplier']))
        
        # Combine factors
        hit_chance = base_hit_rate * volatility_factor * goal_scale_factor
        
        return min(hit_chance, 1.0)  # Cap at 100%
    def _assess_risk(self) -> str:
        expected_rev = self._calculate_expected_revenue()
        if expected_rev < 0:
            return "HIGH - Expected negative revenue"
        if self.tournament_params['prize'] > expected_rev * 0.5:
            return "MEDIUM - Prize is significant portion of expected revenue"
        return "LOW - Settings appear balanced"

    def _assess_volatility_impact(self) -> str:
        vol = self.game_params['volatility']
        if vol >= 8:
            return "HIGH - Expect significant variance in results"
        elif vol >= 5:
            return "MEDIUM - Moderate result variance expected"
        return "LOW - More consistent results expected"