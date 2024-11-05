from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import CpModel, CpSolver

from display import Display
from ept import EPT
from qualifier import Qualifier
from region import Region
from teams import Team, TeamDatabase
from tournament import SolvedTournament


def main():
    teams: [Team] = [
        Team("Team Liquid"),
        Team("Gaimin Gladiators"),
        Team("Team Falcons"),
        Team("Xtreme Gaming"),
        Team("BetBoom Team"),
        Team("Tundra Esports"),

        Team("AVULUS"),
        Team("Palianytsia"),

        Team("PARIVISION"),
        Team("Team Spirit"),

        Team("Nigma Galaxy"),

        Team("Azure Ray"),

        Team("Talon Esports"),

        Team("Nouns Esports"),

        Team("HEROIC"),
        Team("Team Waska")
    ]
    team_database: TeamDatabase = TeamDatabase()
    for team in teams:
        team_database.add_team(team)

    dreamleague_season_24 = SolvedTournament(name="DreamLeague Season 24", link="DreamLeague/Season 24",
                                             icon="{{LeagueIconSmall/dreamleague|name=DreamLeague Season 24|link=DreamLeague/Season 24|date=2024-11-10}}",
                                             team_count=16,
                                             invited_teams=team_database.get_teams_by_names("Team Liquid",
                                                                                            "Gaimin Gladiators",
                                                                                            "Team Falcons",
                                                                                            "Xtreme Gaming",
                                                                                            "BetBoom Team",
                                                                                            "Tundra Esports"),
                                             qualifiers={Region.NA: Qualifier(region=Region.NA,
                                                                              teams=team_database.get_teams_by_names(
                                                                                  "Nouns Esports"),
                                                                              num_qualified=1),
                                                         Region.SA: Qualifier(region=Region.SA,
                                                                              teams=team_database.get_teams_by_names(
                                                                                  "HEROIC",
                                                                                  "Team Waska"),
                                                                              num_qualified=2),
                                                         Region.WEU: Qualifier(region=Region.WEU,
                                                                               teams=team_database.get_teams_by_names(
                                                                                   "AVULUS",
                                                                                   "Palianytsia"),
                                                                               num_qualified=2),
                                                         Region.EEU: Qualifier(region=Region.EEU,
                                                                               teams=team_database.get_teams_by_names(
                                                                                   "PARIVISION",
                                                                                   "Team Spirit"),
                                                                               num_qualified=2),
                                                         Region.MESWA: Qualifier(region=Region.MESWA,
                                                                                 teams=team_database.get_teams_by_names(
                                                                                     "Nigma Galaxy"), num_qualified=1),
                                                         Region.CHINA: Qualifier(region=Region.CHINA,
                                                                                 teams=team_database.get_teams_by_names(
                                                                                     "Azure Ray"),
                                                                                 num_qualified=1),
                                                         Region.SEA: Qualifier(region=Region.SEA,
                                                                               teams=team_database.get_teams_by_names(
                                                                                   "Talon Esports"),
                                                                               num_qualified=1)},
                                             points=[3000, 2500, 2000, 1600, 1200, 1000, 600, 400, 250, 250, 125, 125,
                                                     70, 70, 30,
                                                     30],
                                             gs1_points=[300, 150, 75],
                                             gs2_points=[300],
                                             gs1_team_count=8,
                                             gs2_team_count=8,
                                             playoff_team_count=4,

                                             gs1_a_teams=team_database.get_teams_by_names("PARIVISION",
                                                                                          "Team Liquid",
                                                                                          "BetBoom Team",
                                                                                          "Nigma Galaxy",
                                                                                          "Nouns Esports",
                                                                                          "Xtreme Gaming",
                                                                                          "AVULUS",
                                                                                          "Gaimin Gladiators"),
                                             gs1_b_teams=team_database.get_teams_by_names("Talon Esports",
                                                                                          "Azure Ray",
                                                                                          "HEROIC",
                                                                                          "Team Falcons",
                                                                                          "Team Spirit",
                                                                                          "Team Waska",
                                                                                          "Tundra Esports",
                                                                                          "Palianytsia"),

                                             team_database=team_database)

    dreamleague_season_24.team_can_finish_between_gs1("PARIVISION", 1, 2)
    dreamleague_season_24.team_can_finish_between_gs1("Team Liquid", 3, 4)
    dreamleague_season_24.team_can_finish_between_gs1("Xtreme Gaming", 5, 6)
    dreamleague_season_24.team_can_finish_between_gs1("BetBoom Team", 7, 8)
    dreamleague_season_24.team_can_finish_between_gs1("Gaimin Gladiators", 9, 10)
    dreamleague_season_24.team_can_finish_between_gs1("AVULUS", 11, 12)
    dreamleague_season_24.team_can_finish_between_gs1("Nigma Galaxy", 13, 14)
    dreamleague_season_24.team_can_finish_between_gs1("Nouns Esports", 15, 16)

    dreamleague_season_24.team_can_finish_between_gs1("Team Falcons", 1, 2)
    dreamleague_season_24.team_can_finish_between_gs1("Team Waska", 3, 4)
    dreamleague_season_24.team_can_finish_between_gs1("Tundra Esports", 5, 6)
    dreamleague_season_24.team_can_finish_between_gs1("Team Spirit", 7, 8)
    dreamleague_season_24.team_can_finish_between_gs1("Talon Esports", 9, 10)
    dreamleague_season_24.team_can_finish_between_gs1("Azure Ray", 11, 12)
    dreamleague_season_24.team_can_finish_between_gs1("HEROIC", 13, 14)
    dreamleague_season_24.team_can_finish_between_gs1("Palianytsia", 15, 16)

    dreamleague_season_24.team_can_finish_between_gs2("BetBoom Team", 1, 8)
    dreamleague_season_24.team_can_finish_between_gs2("PARIVISION", 1, 8)
    dreamleague_season_24.team_can_finish_between_gs2("Team Spirit", 1, 8)
    dreamleague_season_24.team_can_finish_between_gs2("Team Falcons", 1, 8)
    dreamleague_season_24.team_can_finish_between_gs2("Team Liquid", 1, 8)
    dreamleague_season_24.team_can_finish_between_gs2("Team Waska", 1, 8)
    dreamleague_season_24.team_can_finish_between_gs2("Tundra Esports", 4, 8)
    dreamleague_season_24.team_can_finish_between_gs2("Xtreme Gaming", 4, 8)

    ept: EPT = EPT(
        dreamleague_season_24=dreamleague_season_24,
        team_database=team_database
    )

    max_objective_value = -1
    max_solver = None
    max_team = None
    for team in team_database.get_all_teams():
        print(f"Now optimising for {team.name}")
        model = CpModel()
        unoptimised_model = ept.add_constraints(model)

        # Optimise
        [solver, status] = ept.optimise_for(team=team,
                                            unoptimised_model=unoptimised_model, model=model)

        if status != cp_model.OPTIMAL:
            print(f"Team {team.name} probably cannot finish in top 8")
            continue

        if solver.objective_value > max_objective_value:
            max_objective_value = solver.objective_value
            max_solver = solver
            max_team = team

    display = Display()
    display.print(team_to_optimise=max_team,
                  max_points=max_objective_value,
                  unoptimised_model=unoptimised_model,
                  solver=max_solver,
                  dreamleague_season_24=dreamleague_season_24,
                  team_database=team_database)


print("Executing solver")
main()
print("Execution complete")
