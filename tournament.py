from ortools.constraint_solver.pywrapcp import BooleanVar
from ortools.sat.python.cp_model import CpModel, IntVar

from region import Region
from teams import Team, TeamDatabase
from unoptimised_model import UnoptimisedTournamentModel, UnoptimisedModel


class ResolvedTournament:
    def __init__(self, name: str = None, link: str = None, icon: str = None, gs1_team_count: int = -1,
                 gs2_team_count: int = -1,
                 points: [int] = None, results: dict[Team, int] = None):
        self.name = name
        self.link = link
        self.icon = icon
        self.gs1_team_count = gs1_team_count
        self.gs2_team_count = gs2_team_count
        # r variable
        self.points = points
        # d variable
        self.results = results


class SolvedTournament:
    def __init__(self, name: str = None, link: str = None, icon: str = None, gs1_team_count: int = None,
                 gs2_team_count: int = None, team_count: int = -1, invited_teams: [Team] = None,
                 qualifier: dict[Region, [Team]] = None, points: [int] = None, gs1_points: [int] = None,
                 gs2_points: [int] = None, team_database: TeamDatabase = None):
        self.qualifier = qualifier
        self.name = name
        self.link = link
        self.icon = icon

        self.team_count = team_count
        self.gs1_team_count = gs1_team_count
        self.gs2_team_count = gs2_team_count
        self.invited_teams = invited_teams
        self.qualifier = qualifier

        # r variable
        self.points = points
        self.gs1_points = gs1_points
        self.gs2_points = gs2_points

        self.team_database = team_database

    def add_constraints(self, model: CpModel) -> UnoptimisedTournamentModel:
        # x variable
        indicators: [[BooleanVar]] = [[model.new_bool_var(f'x_{self.name}_{i}_{j}') for j in range(len(self.points))]
                                      for i in range(self.team_count)]
        # d variable
        obtained_points: [IntVar] = [model.new_int_var(0, 99999, f'd_{self.name}_{i}') for i in range(self.team_count)]

        # Each qualified team finishes somewhere
        for team in self.team_database.get_all_teams():
            model.Add(sum(indicators[self.team_database.get_team_index(team)]) == 1)

        # One placement per team
        for placement in range(self.team_count):
            model.Add(sum(indicators[i][placement] for i in range(self.team_count)) == 1)

        # Points
        for team in self.team_database.get_all_teams():
            team_index = self.team_database.get_team_index(team)
            obtained_points[team_index] = sum(
                indicators[team_index][p] * self.points[p] for p in range(len(self.points)))

        return UnoptimisedTournamentModel(indicators=indicators, points=obtained_points)
