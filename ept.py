from ortools.constraint_solver.pywrapcp import BooleanVar
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import CpModel, IntVar

from teams import TeamDatabase, Team
from tournament import SolvedTournament
from transfer_window import TransferWindow
from unoptimised_model import UnoptimisedModel


class EPT:
    def __init__(self, dreamleague_season_24: SolvedTournament,
                 between_dreamleague_season_24_esl_one_bangkok: TransferWindow,
                 team_database: TeamDatabase):
        self.dreamleague_season_24 = dreamleague_season_24
        self.between_dreamleague_season_24_esl_one_bangkok = between_dreamleague_season_24_esl_one_bangkok
        self.team_database = team_database

    def add_constraints(self, model: CpModel) -> UnoptimisedModel:
        dreamleague_season_24 = self.dreamleague_season_24.add_constraints(model)

        team_count = len(self.team_database.get_all_teams())
        team_count_range = range(team_count)
        total_points = [model.NewIntVar(0, 99999, f'd_{i}') for i in team_count_range]
        for t in self.team_database.get_all_teams():
            team_index = self.team_database.get_team_index(t)
            total_points[team_index] = dreamleague_season_24.points[team_index] + \
                                       dreamleague_season_24.gs1_points[team_index] + \
                                       dreamleague_season_24.gs2_points[team_index] + \
                                       self.between_dreamleague_season_24_esl_one_bangkok.as_table()[team_index]

        # Ranks
        aux: [[BooleanVar]] = {(i, j): model.NewBoolVar(f'aux_{i}_{j}') for i in team_count_range for j in
                               team_count_range}
        ranks: [IntVar] = {team: model.NewIntVar(1, team_count, f'ranks_{team}') for team in team_count_range}
        big_m: int = 20000
        for i in team_count_range:
            for j in team_count_range:
                if i == j:
                    model.Add(aux[(i, j)] == 1)
                else:
                    model.Add(total_points[i] - total_points[j] <= (1 - aux[(i, j)]) * big_m)
                    model.Add(total_points[j] - total_points[i] <= aux[(i, j)] * big_m)
            ranks[i] = sum(aux[(i, j)] for j in team_count_range)

        return UnoptimisedModel(dreamleague_season_24=dreamleague_season_24,
                                between_dreamleague_season_24_esl_one_bangkok=self.between_dreamleague_season_24_esl_one_bangkok,
                                total_points=total_points,
                                ranks=ranks)

    def optimise_for(self, team: Team, unoptimised_model: UnoptimisedModel, model: CpModel):
        team_index = self.team_database.get_team_index(team)
        model.Add(unoptimised_model.ranks[team_index] > 8)
        model.Maximize(unoptimised_model.total_points[team_index])

        solver = cp_model.CpSolver()
        status = solver.Solve(model)
        if status != cp_model.OPTIMAL:
            print("No optimal solution found, probably unable to finish outside of top 8.")

        return [solver, status]
