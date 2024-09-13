from ortools.constraint_solver.pywrapcp import BooleanVar, IntVar


class UnoptimisedTournamentModel:
    def __init__(self, indicators: [[BooleanVar]], points: [IntVar], gs1_indicators: [[BooleanVar]] = None,
                 gs1_points: [IntVar] = None, gs2_indicators: [[BooleanVar]] = None, gs2_points: [IntVar] = None):
        self.indicators = indicators
        self.points = points
        self.gs1_indicators = gs1_indicators
        self.gs1_points = gs1_points
        self.gs2_indicators = gs2_indicators
        self.gs2_points = gs2_points


class UnoptimisedModel:
    def __init__(self, dreamleague_season_24: UnoptimisedTournamentModel,
                 total_points: [IntVar], ranks: [IntVar]):
        self.dreamleague_season_24 = dreamleague_season_24
        self.total_points = total_points
        self.ranks = ranks
