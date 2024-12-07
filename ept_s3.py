import pyperclip
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import CpModel

from display import Display
from ept import EPT
from ept_s3_tournaments.dreamleague_season_24 import DreamLeagueSeason24
from ept_s3_tournaments.esl_one_bangkok_2024 import ESLOneBangkok2024
from teams import Team, TeamDatabase
from tournament import SolvedTournament
from transfer_window import TransferWindow


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
        Team("Natus Vincere"),

        Team("Nigma Galaxy"),

        Team("Azure Ray"),
        Team("Gaozu"),

        Team("Talon Esports"),
        Team("BOOM Esports"),

        Team("Nouns Esports"),
        Team("Atlantic City"),
        Team("Shopify Rebellion"),

        Team("HEROIC"),
        Team("Team Waska"),
        Team("M80")
    ]
    team_database: TeamDatabase = TeamDatabase()
    for team in teams:
        team_database.add_team(team)

    dreamleague_season_24: SolvedTournament = DreamLeagueSeason24().build(team_database)

    between_dreamleague_season_24_esl_one_bangkok = TransferWindow(team_database=team_database)
    between_dreamleague_season_24_esl_one_bangkok.add_change("Nouns Esports", -30)
    between_dreamleague_season_24_esl_one_bangkok.add_change("Atlantic City", 30)
    between_dreamleague_season_24_esl_one_bangkok.add_change("Azure Ray", -125)
    between_dreamleague_season_24_esl_one_bangkok.add_change("Xtreme Gaming", -675)

    esl_one_bangkok_2024: SolvedTournament = ESLOneBangkok2024().build(team_database)

    ept: EPT = EPT(
        dreamleague_season_24=dreamleague_season_24,
        between_dreamleague_season_24_esl_one_bangkok=between_dreamleague_season_24_esl_one_bangkok,
        esl_one_bangkok_2024=esl_one_bangkok_2024,
        team_database=team_database
    )

    max_objective_value = -1
    max_solver = None
    max_team = None
    top_n = 4
    for team in team_database.get_all_teams():
        print(f"Now optimising for {team.name}")
        model = CpModel()
        unoptimised_model = ept.add_constraints(model)

        # Optimise
        [solver, status] = ept.optimise_for(team=team,
                                            unoptimised_model=unoptimised_model,
                                            model=model,
                                            top_n=top_n)

        if status != cp_model.OPTIMAL:
            print(f"Team {team.name} probably cannot finish in top {top_n}")
            continue

        if solver.objective_value > max_objective_value:
            max_objective_value = solver.objective_value
            max_solver = solver
            max_team = team

    display = Display()
    output = display.print(team_to_optimise=max_team,
                           max_points=max_objective_value,
                           top_n=top_n,
                           unoptimised_model=unoptimised_model,
                           solver=max_solver,
                           dreamleague_season_24=dreamleague_season_24,
                           between_dreamleague_season_24_esl_one_bangkok=between_dreamleague_season_24_esl_one_bangkok,
                           esl_one_bangkok_2024=esl_one_bangkok_2024,
                           team_database=team_database)
    print("Printing Liquipedia table")
    print(output)
    pyperclip.copy(output)


print("Executing solver")
main()
print("Execution complete")
