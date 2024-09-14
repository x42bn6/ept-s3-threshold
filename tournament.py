from math import floor

from ortools.constraint_solver.pywrapcp import BooleanVar
from ortools.sat.python.cp_model import CpModel, IntVar

from qualifier import Qualifier
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
                 qualifiers: dict[Region, Qualifier] = None, points: [int] = None, gs1_points: [int] = None,
                 gs2_points: [int] = None, gs1_a_teams: [Team] = None, gs1_b_teams: [Team] = None,
                 gs2_teams: [Team] = None, team_database: TeamDatabase = None):
        self.name = name
        self.link = link
        self.icon = icon

        self.team_count = team_count
        self.gs1_team_count = gs1_team_count
        self.gs2_team_count = gs2_team_count

        self.invited_teams = invited_teams
        self.qualifiers = qualifiers
        self.gs1_a_teams = gs1_a_teams
        self.gs1_b_teams = gs1_b_teams
        self.gs2_teams = gs2_teams

        # r variable
        self.points = points
        self.gs1_points = gs1_points
        self.gs2_points = gs2_points

        self.team_database = team_database

    def add_constraints(self, model: CpModel) -> UnoptimisedTournamentModel:
        # x variable
        indicators: [[BooleanVar]] = [[model.new_bool_var(f'x_{self.name}_{i}_{j}') for j in range(len(self.points))]
                                      for i in range(self.team_count)]

        self.basic_constraints(indicators, model)

        # GS1
        # Assume equal groups + (A1 = 1st, B1 = 2nd, A2 = 3rd, etc.)
        # x variable
        gs1_indicators: [[BooleanVar]] = [
            [model.new_bool_var(f'x_{self.name}_gs1_{i}_{j}') for j in range(len(self.points))]
            for i in range(self.team_count)]

        if self.gs1_a_teams is None or self.gs1_b_teams is None:
            print("No GS1 teams setup.  Assuming that any team can obtain points")
            self.basic_constraints(gs1_indicators, model)
        else:
            # A finishes 1st, 3rd, 5th, etc.
            for team in self.gs1_a_teams:
                team_index = self.team_database.get_team_index(team)
                row_sum = 0
                for placement in range(0, self.gs1_team_count * 2, 2):
                    row_sum += gs1_indicators[team_index]
                model.Add(row_sum == 1)

            # B finishes 2nd, 4th, 6th, etc.
            for team in self.gs1_b_teams:
                team_index = self.team_database.get_team_index(team)
                row_sum = 0
                for placement in range(1, self.gs1_team_count * 2, 2):
                    row_sum += gs1_indicators[team_index]
                model.Add(row_sum == 1)

            # One placement per team
            for placement in range(self.team_count):
                model.Add(sum(gs1_indicators[i][placement] for i in range(self.team_count)) == 1)

        # Bind stages together such that if you are in the tournament, you are in GS1
        for team in self.team_database.get_all_teams():
            team_index = self.team_database.get_team_index(team)
            model.Add(sum(indicators[team_index]) == sum(gs1_indicators[team_index]))

        # Points
        # Overall
        # d variable
        obtained_points: [IntVar] = [model.new_int_var(0, 99999, f'd_{self.name}_{i}') for i in range(self.team_count)]
        for team in self.team_database.get_all_teams():
            team_index = self.team_database.get_team_index(team)
            obtained_points[team_index] = sum(
                indicators[team_index][p] * self.points[p] for p in range(len(self.points)))

        # GS1
        # d variable
        gs1_obtained_points: [IntVar] = [model.new_int_var(0, 99999, f'd_{self.name}_gs1_{i}')
                                         for i in range(self.team_count)]
        gs1_points_extended: [int] = [0] * self.team_count
        for p in range(self.team_count):
            point_index = floor(p / 2)
            if point_index < len(self.gs1_points):
                gs1_points_extended[p] = self.gs1_points[point_index]
        for team in self.team_database.get_all_teams():
            team_index = self.team_database.get_team_index(team)
            gs1_obtained_points[team_index] = sum(
                gs1_indicators[team_index][p] * gs1_points_extended[p] for p in range(len(gs1_points_extended)))

        return UnoptimisedTournamentModel(
            indicators=indicators,
            points=obtained_points,
            gs1_indicators=gs1_indicators,
            gs1_points=gs1_obtained_points
        )

    def basic_constraints(self, indicators, model):
        # Each invited team finishes somewhere
        for team in self.invited_teams:
            model.Add(sum(indicators[self.team_database.get_team_index(team)]) == 1)

        # Each qualified team finishes somewhere
        for region, regional_qualifier in self.qualifiers.items():
            regional_sum = 0
            for team in regional_qualifier.teams:
                team_index = self.team_database.get_team_index(team)
                model.Add(sum(indicators[team_index]) <= 1)
                regional_sum += sum(indicators[team_index])
            model.Add(regional_sum == regional_qualifier.num_qualified)

        # One placement per team
        for placement in range(self.team_count):
            model.Add(sum(indicators[i][placement] for i in range(self.team_count)) == 1)
