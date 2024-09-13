from ortools.constraint_solver.pywrapcp import BooleanVar
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import CpModel, IntVar

from region import Region
from teams import Team, TeamDatabase
from tournament import SolvedTournament
from unoptimised_model import UnoptimisedModel, UnoptimisedTournamentModel


class EPT:
    def __init__(self, dreamleague_season_24: SolvedTournament, team_database: TeamDatabase):
        self.dreamleague_season_24 = dreamleague_season_24
        self.team_database = team_database

    def add_constraints(self, model: CpModel) -> UnoptimisedModel:
        dreamleague_season_24 = self.dreamleague_season_24.add_constraints(model)

        team_count = len(self.team_database.get_all_teams())
        team_count_range = range(team_count)

        total_points = [model.NewIntVar(0, 99999, f'd_{i}') for i in team_count_range]
        for t in self.team_database.get_all_teams():
            team_index = self.team_database.get_team_index(t)
            total_points[team_index] = dreamleague_season_24.points[team_index]

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
                                total_points=total_points,
                                ranks=ranks)

    def optimise_for(self, team: Team, unoptimised_model: UnoptimisedModel, model: CpModel):
        team_index = self.team_database.get_team_index(team)
        model.Add(unoptimised_model.ranks[team_index] > 8)
        model.Maximize(unoptimised_model.total_points[team_index])

        solver = cp_model.CpSolver()
        status = solver.Solve(model)
        if status == cp_model.OPTIMAL:
            objective_value = solver.ObjectiveValue()
            print("Objective value:", objective_value)
        else:
            print("No optimal solution found, probably unable to finish outside of top 8.")


def main():
    teams: [Team] = [
        Team("Team Falcons"),
        Team("BetBoom Team"),
        Team("Gaimin Gladiators"),
        Team("Xtreme Gaming"),

        Team("Nouns Esports"),

        Team("HEROIC"),
        Team("beastcoast"),

        Team("Team Liquid"),
        Team("Tundra Esports"),
        Team("Cloud9"),

        Team("Team Spirit"),
        Team("1win"),

        Team("PSG Quest"),

        Team("Azure Ray"),

        Team("Aurora Gaming"),
        Team("Talon Esports")
    ]
    team_database: TeamDatabase = TeamDatabase()
    for team in teams:
        team_database.add_team(team)

    model = CpModel()
    ept: EPT = EPT(
        dreamleague_season_24=SolvedTournament(name="DreamLeague Season 24", link="DreamLeague/Season 24",
                                               icon="{{LeagueIconSmall/dreamleague|name=DreamLeague Season 24|link=DreamLeague/Season 24|date=2024-11-10}}",
                                               team_count=16,
                                               invited_teams=team_database.get_teams_by_names("Team Falcons",
                                                                                              "BetBoom Team",
                                                                                              "Gaimin Gladiators",
                                                                                              "Xtreme Gaming"),
                                               qualifier={
                                                   Region.NA: team_database.get_teams_by_names("Nouns Esports"),
                                                   Region.SA: team_database.get_teams_by_names("HEROIC", "beastcoast"),
                                                   Region.WEU: team_database.get_teams_by_names("Team Liquid",
                                                                                                "Tundra Esports",
                                                                                                "Cloud9"),
                                                   Region.EEU: team_database.get_teams_by_names("Team Spirit", "1win"),
                                                   Region.MESWA: team_database.get_teams_by_names("PSG Quest"),
                                                   Region.CHINA: team_database.get_teams_by_names("Azure Ray"),
                                                   Region.SEA: team_database.get_teams_by_names("Aurora Gaming",
                                                                                                "Talon Esports")
                                               },
                                               points=[3000, 2500, 2000, 1600, 1200, 1000, 600, 400, 250, 250, 125, 125,
                                                       70, 70, 30, 30],
                                               gs1_points=[300],
                                               gs2_points=[300, 150, 75],
                                               team_database=team_database),
        team_database=team_database
    )
    unoptimised_model = ept.add_constraints(model)
    ept.optimise_for(team=team_database.get_team_by_name("Gaimin Gladiators"), unoptimised_model=unoptimised_model,
                     model=model)


print("Executing solver")
main()
print("Execution complete")
