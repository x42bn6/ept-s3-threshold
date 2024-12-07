from math import floor

from ortools.constraint_solver.pywrapcp import BooleanVar
from ortools.sat.python.cp_model import CpModel, IntVar

from qualifier import Qualifier
from region import Region
from teams import Team, TeamDatabase
from unoptimised_model import UnoptimisedTournamentModel


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


class TeamConstraint:
    def __init__(self, team: Team, best: int, worst: int):
        self.team = team
        self.best = best
        self.worst = worst


class SolvedTournament:
    def __init__(self,
                 name: str = None,
                 link: str = None,
                 icon: str = None,
                 gs1_team_count: int = None,
                 gs2_team_count: int = None,
                 playoff_team_count: int = None,
                 team_count: int = -1,
                 invited_teams: [Team] = None,
                 qualifiers: dict[Region, Qualifier] = None,
                 points: [int] = None,
                 gs1_points: [int] = None,
                 gs2_points: [int] = None,
                 gs1_a_teams: [Team] = None,
                 gs1_b_teams: [Team] = None,
                 gs2_teams: [Team] = None,
                 team_database: TeamDatabase = None):
        self.name = name
        self.link = link
        self.icon = icon

        self.team_count = team_count
        self.gs1_team_count = gs1_team_count
        self.gs2_team_count = gs2_team_count
        self.playoff_team_count = playoff_team_count

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

        self.team_constraints: [TeamConstraint] = []
        self.team_gs1_constraints: [TeamConstraint] = []
        self.team_gs2_constraints: [TeamConstraint] = []
        self.team_guaranteed_playoff_lb_or_eliminated: [Team] = []

    def add_constraints(self, model: CpModel) -> UnoptimisedTournamentModel:
        # x variable
        all_team_count = len(self.team_database.get_all_teams())
        indicators: [[BooleanVar]] = [[model.new_bool_var(f'x_{self.name}_{i}_{j}') for j in range(len(self.points))]
                                      for i in range(all_team_count)]

        self.basic_constraints(indicators=indicators, model=model)

        # Points
        # Overall
        # d variable
        obtained_points: [IntVar] = [model.new_int_var(0, 99999, f'd_{self.name}_{i}') for i in range(all_team_count)]
        for team in self.team_database.get_all_teams():
            team_index = self.team_database.get_team_index(team)
            obtained_points[team_index] = sum(
                indicators[team_index][p] * self.points[p] for p in range(len(self.points)))

        gs1_indicators, gs1_obtained_points = self.setup_group_stage_1(model)
        gs2_indicators = None
        gs2_obtained_points = None

        # Bind stages together such that if you are in the tournament, you are in GS1
        for team in self.team_database.get_all_teams():
            team_index = self.team_database.get_team_index(team)
            model.Add(sum(indicators[team_index]) == sum(gs1_indicators[team_index]))

        # Bottom GS1 = final result
        for team in self.team_database.get_all_teams():
            team_index = self.team_database.get_team_index(team)
            for p in range(self.gs1_team_count, self.team_count):
                model.Add(indicators[team_index][p] == gs1_indicators[team_index][p])

        # DreamLeague or ESL One?
        if self.gs2_team_count is not None:
            gs2_indicators, gs2_obtained_points = self.setup_group_stage_2(model)
            self.setup_2_group_stage_tournament(gs1_indicators, gs2_indicators, indicators, model)
        else:
            pass

        # Team constraints
        for team_constraint in self.team_constraints:
            team_sum = 0
            for i in range(team_constraint.best, team_constraint.worst + 1):
                team_sum += indicators[self.team_database.get_team_index(team_constraint.team)][i]
            model.Add(team_sum == 1)

        # GS1 constraints
        for team_gs1_constraint in self.team_gs1_constraints:
            team_sum = 0
            for i in range(team_gs1_constraint.best, team_gs1_constraint.worst + 1):
                team_sum += gs1_indicators[self.team_database.get_team_index(team_gs1_constraint.team)][i]
            model.Add(team_sum == 1)

        # Guaranteed LB or eliminated - both Grand Finalists cannot come from here
        lb_or_eliminated_sum = 0
        for team in self.team_guaranteed_playoff_lb_or_eliminated:
            for i in [0, 1]:
                lb_or_eliminated_sum += indicators[self.team_database.get_team_index(team)][i]
        model.Add(lb_or_eliminated_sum <= 1)

        points_scoring_phases = 1
        if self.gs1_team_count is not None:
            points_scoring_phases += 1
        if self.gs2_team_count is not None:
            points_scoring_phases += 1

        return UnoptimisedTournamentModel(
            icon=self.icon,
            points_scoring_phases=points_scoring_phases,
            indicators=indicators,
            points=obtained_points,
            gs1_indicators=gs1_indicators,
            gs1_points=gs1_obtained_points,
            gs2_indicators=gs2_indicators,
            gs2_points=gs2_obtained_points
        )

    def setup_2_group_stage_tournament(self, gs1_indicators, gs2_indicators, indicators, model):
        # Anyone who finished bottom half in GS 1 (e.g. 8-16) cannot be in GS2
        for team in self.team_database.get_all_teams():
            team_index = self.team_database.get_team_index(team)
            qualified_for_tournament = model.new_bool_var(f"{self.name}_{team_index}_qualified_for_tournament")
            model.Add(sum(indicators[team_index]) == 1).only_enforce_if(qualified_for_tournament)
            model.Add(sum(indicators[team_index]) == 0).only_enforce_if(qualified_for_tournament.Not())

            gs1_top = model.new_bool_var(f"{self.name}_{team_index}_gs1_top")
            model.Add(sum(gs1_indicators[team_index][0:self.gs1_team_count]) == 1).only_enforce_if(gs1_top)
            model.Add(sum(gs1_indicators[team_index][0:self.gs1_team_count]) == 0).only_enforce_if(gs1_top.Not())

            gs1_bottom = model.new_bool_var(f"{self.name}_{team_index}_gs1_bottom")
            model.Add(sum(gs1_indicators[team_index][self.gs1_team_count:self.team_count]) == 1).only_enforce_if(
                gs1_bottom)
            model.Add(sum(gs1_indicators[team_index][self.gs1_team_count:self.team_count]) == 0).only_enforce_if(
                gs1_bottom.Not())

            not_qualified_or_gs1_bottom = model.new_bool_var(f"{self.name}_{team_index}_not_qualified_or_gs1_bottom")
            model.AddBoolOr([qualified_for_tournament.Not(), gs1_bottom]).only_enforce_if(not_qualified_or_gs1_bottom)
            model.AddBoolAnd([qualified_for_tournament, gs1_bottom.Not()]).only_enforce_if(
                not_qualified_or_gs1_bottom.Not())

            model.Add(sum(gs2_indicators[team_index]) == 1).only_enforce_if(gs1_top)
            model.Add(sum(gs2_indicators[team_index]) == 0).only_enforce_if(not_qualified_or_gs1_bottom)
        # If you finish in the top half of GS2, you finish top 4 overall
        for team in self.team_database.get_all_teams():
            team_index = self.team_database.get_team_index(team)
            gs2_top_4 = model.new_bool_var(f"{self.name}_{team_index}_gs2_top_4")
            model.Add(sum(gs2_indicators[team_index][0:self.playoff_team_count]) == 1).only_enforce_if(gs2_top_4)
            model.Add(sum(gs2_indicators[team_index][0:self.playoff_team_count]) == 0).only_enforce_if(gs2_top_4.Not())
            model.Add(sum(indicators[team_index][0:self.playoff_team_count]) == 1).only_enforce_if(gs2_top_4)
            model.Add(sum(indicators[team_index][0:self.playoff_team_count]) == 0).only_enforce_if(gs2_top_4.Not())

            # Bottom GS2 = final result
            for placement in range(4, 8):
                model.Add(indicators[team_index][placement] == gs2_indicators[team_index][placement])

        # GS2 constraints
        for team_gs2_constraint in self.team_gs2_constraints:
            team_sum = 0
            for i in range(team_gs2_constraint.best, team_gs2_constraint.worst + 1):
                team_sum += gs2_indicators[self.team_database.get_team_index(team_gs2_constraint.team)][i]
            model.Add(team_sum == 1)

    def setup_group_stage_1(self, model):
        # GS1
        # Assume equal groups + (A1 = 1st, B1 = 2nd, A2 = 3rd, etc.)
        all_team_count = len(self.team_database.get_all_teams())
        # x variable
        gs1_indicators: [[BooleanVar]] = [
            [model.new_bool_var(f'x_{self.name}_gs1_{i}_{j}') for j in range(self.team_count)]
            for i in range(all_team_count)]
        if self.gs1_a_teams is None or self.gs1_b_teams is None:
            print("No GS1 teams setup.  Assuming that any team can obtain points")
            self.basic_constraints(indicators=gs1_indicators, model=model)
        else:
            # A finishes 1st, 3rd, 5th, etc.
            for team in self.gs1_a_teams:
                team_index = self.team_database.get_team_index(team)
                row_sum = 0
                for placement in range(0, self.gs1_team_count * 2, 2):
                    row_sum += gs1_indicators[team_index][placement]
                model.Add(row_sum == 1)

            # B finishes 2nd, 4th, 6th, etc.
            for team in self.gs1_b_teams:
                team_index = self.team_database.get_team_index(team)
                row_sum = 0
                for placement in range(1, self.gs1_team_count * 2, 2):
                    row_sum += gs1_indicators[team_index][placement]
                model.Add(row_sum == 1)

            # One placement per team
            for placement in range(self.team_count):
                model.Add(
                    sum(gs1_indicators[i][placement] for i in range(len(self.team_database.get_all_teams()))) == 1)

        # d variable
        gs1_obtained_points: [IntVar] = [model.new_int_var(0, 99999, f'd_{self.name}_gs1_{i}')
                                         for i in range(all_team_count)]
        gs1_points_extended: [int] = [0] * self.team_count
        for p in range(self.team_count):
            point_index = floor(p / 2)
            if point_index < len(self.gs1_points):
                gs1_points_extended[p] = self.gs1_points[point_index]
        for team in self.team_database.get_all_teams():
            team_index = self.team_database.get_team_index(team)
            gs1_obtained_points[team_index] = sum(
                gs1_indicators[team_index][p] * gs1_points_extended[p] for p in range(len(gs1_points_extended)))
        return gs1_indicators, gs1_obtained_points

    def setup_group_stage_2(self, model):
        # GS2
        all_team_count = len(self.team_database.get_all_teams())
        # x variable
        gs2_indicators: [[BooleanVar]] = [
            [model.new_bool_var(f'x_{self.name}_gs2_{i}_{j}') for j in range(self.team_count)]
            for i in range(all_team_count)]
        if self.gs2_teams is None:
            print("No GS2 teams setup.  Assuming that any team can obtain points")
            # A team may qualify here (we bind GS1 and GS2 later)
            for team in self.team_database.get_all_teams():
                model.Add(sum(gs2_indicators[self.team_database.get_team_index(team)]) <= 1)

            # One placement per team
            for placement in range(self.gs2_team_count):
                model.Add(sum(gs2_indicators[i][placement] for i in range(all_team_count)) == 1)
        else:
            # Each GS2 team finishes somewhere
            for team in self.gs2_teams:
                model.Add(sum(gs2_indicators[self.team_database.get_team_index(team)]) == 1)

            # One placement per team
            for placement in range(self.gs2_team_count):
                row_sum = 0
                for team in self.gs2_teams:
                    team_index = self.team_database.get_team_index(team)
                    row_sum += gs2_indicators[team_index][placement]
                model.Add(row_sum == 1)

        # d variable
        gs2_obtained_points: [IntVar] = [model.new_int_var(0, 99999, f'd_{self.name}_gs2_{i}')
                                         for i in range(all_team_count)]
        gs2_points_extended: [int] = [0] * self.team_count
        for p in range(self.team_count):
            if p < len(self.gs2_points):
                gs2_points_extended[p] = self.gs2_points[p]
        for team in self.team_database.get_all_teams():
            team_index = self.team_database.get_team_index(team)
            gs2_obtained_points[team_index] = sum(
                gs2_indicators[team_index][p] * gs2_points_extended[p] for p in range(len(gs2_points_extended)))
        return gs2_indicators, gs2_obtained_points

    def basic_constraints(self, indicators: [[BooleanVar]], model: CpModel):
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
            model.Add(sum(indicators[i][placement] for i in range(len(self.team_database.get_all_teams()))) == 1)

    def team_can_finish_between(self, team_name: str, best: int, worst: int):
        self.team_can_finish_between_inner(team_name, best, worst, self.team_constraints)

    def team_can_finish_between_gs1(self, team_name: str, best: int, worst: int):
        self.team_can_finish_between_inner(team_name, best, worst, self.team_gs1_constraints)

    def team_can_finish_between_gs2(self, team_name: str, best: int, worst: int):
        self.team_can_finish_between_inner(team_name, best, worst, self.team_gs2_constraints)

    def team_can_finish_between_inner(self, team_name: str, best: int, worst: int, constraints: [TeamConstraint]):
        team = self.team_database.get_team_by_name(team_name)
        constraints.append(TeamConstraint(team=team, best=best - 1, worst=worst - 1))

    def guaranteed_playoff_lb_or_eliminated(self, *team_names: str):
        self.team_guaranteed_playoff_lb_or_eliminated = self.team_database.get_teams_by_names(*team_names)

    def points_to_place(self, points: int) -> int:
        return self.points_to_place_inner(points, self.points)

    def gs1_points_to_place(self, points: int) -> int | None:
        return self.points_to_place_inner(points, self.gs1_points)

    def gs2_points_to_place(self, points: int) -> int | None:
        return self.points_to_place_inner(points, self.gs2_points)

    @staticmethod
    def points_to_place_inner(points: int, point_table: [int]) -> int | None:
        try:
            return point_table.index(points)
        except ValueError:
            return None