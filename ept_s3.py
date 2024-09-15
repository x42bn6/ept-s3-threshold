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
        Team("Team Falcons"),
        Team("BetBoom Team"),
        Team("Gaimin Gladiators"),
        Team("Xtreme Gaming"),

        Team("nouns"),

        Team("HEROIC"),
        Team("beastcoast"),

        Team("Team Liquid"),
        Team("Tundra Esports"),
        Team("Cloud9"),

        Team("Team Spirit"),
        Team("1win"),

        Team("PSG Quest"),

        Team("Azure Ray"),

        Team("Aurora"),
        Team("Talon Esports")
    ]
    team_database: TeamDatabase = TeamDatabase()
    for team in teams:
        team_database.add_team(team)

    ept: EPT = EPT(
        dreamleague_season_24=SolvedTournament(name="DreamLeague Season 24", link="DreamLeague/Season 24",
                                               icon="{{LeagueIconSmall/dreamleague|name=DreamLeague Season 24|link=DreamLeague/Season 24|date=2024-11-10}}",
                                               team_count=16,
                                               invited_teams=team_database.get_teams_by_names("Team Falcons",
                                                                                              "BetBoom Team",
                                                                                              "Gaimin Gladiators",
                                                                                              "Xtreme Gaming"),
                                               qualifiers={
                                                   Region.NA: Qualifier(
                                                       region=Region.NA,
                                                       teams=team_database.get_teams_by_names("nouns"),
                                                       num_qualified=1
                                                   ),
                                                   Region.SA: Qualifier(
                                                       region=Region.SA,
                                                       teams=team_database.get_teams_by_names("HEROIC", "beastcoast"),
                                                       num_qualified=2
                                                   ),
                                                   Region.WEU: Qualifier(
                                                       region=Region.WEU,
                                                       teams=team_database.get_teams_by_names("Team Liquid",
                                                                                              "Tundra Esports",
                                                                                              "Cloud9"),
                                                       num_qualified=3
                                                   ),
                                                   Region.EEU: Qualifier(
                                                       region=Region.EEU,
                                                       teams=team_database.get_teams_by_names("Team Spirit", "1win"),
                                                       num_qualified=2
                                                   ),
                                                   Region.MESWA: Qualifier(
                                                       region=Region.MESWA,
                                                       teams=team_database.get_teams_by_names("PSG Quest"),
                                                       num_qualified=1
                                                   ),
                                                   Region.CHINA: Qualifier(
                                                       region=Region.CHINA,
                                                       teams=team_database.get_teams_by_names("Azure Ray"),
                                                       num_qualified=1
                                                   ),
                                                   Region.SEA: Qualifier(
                                                       region=Region.SEA,
                                                       teams=team_database.get_teams_by_names("Aurora",
                                                                                              "Talon Esports"),
                                                       num_qualified=2
                                                   )
                                               },
                                               points=[3000, 2500, 2000, 1600, 1200, 1000, 600, 400, 250, 250, 125, 125,
                                                       70, 70, 30, 30],
                                               gs1_points=[300],
                                               gs2_points=[300, 150, 75],
                                               gs1_team_count=8,
                                               gs2_team_count=8,
                                               team_database=team_database),
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
    display.print(team_to_optimise=max_team, max_points=max_objective_value, unoptimised_model=unoptimised_model,
                  solver=max_solver, team_database=team_database)


print("Executing solver")
main()
print("Execution complete")
