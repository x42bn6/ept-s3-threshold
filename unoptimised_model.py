from ortools.constraint_solver.pywrapcp import BooleanVar, IntVar

from transfer_window import TransferWindow


class UnoptimisedTournamentModel:
    def __init__(self, icon: str, points_scoring_phases: int, indicators: [[BooleanVar]], points: [IntVar], gs1_indicators: [[BooleanVar]] = None,
                 gs1_points: [IntVar] = None, gs2_indicators: [[BooleanVar]] = None, gs2_points: [IntVar] = None):
        self.icon = icon
        self.points_scoring_phases = points_scoring_phases
        self.indicators = indicators
        self.points = points
        self.gs1_indicators = gs1_indicators
        self.gs1_points = gs1_points
        self.gs2_indicators = gs2_indicators
        self.gs2_points = gs2_points


class UnoptimisedModel:
    def __init__(self,
                 dreamleague_season_24: UnoptimisedTournamentModel,
                 between_dreamleague_season_24_esl_one_bangkok: TransferWindow,
                 total_points: [IntVar], ranks: [IntVar]):
        self.dreamleague_season_24 = dreamleague_season_24
        self.between_dreamleague_season_24_esl_one_bangkok = between_dreamleague_season_24_esl_one_bangkok
        self.total_points = total_points
        self.ranks = ranks
