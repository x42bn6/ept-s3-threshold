from struct import Struct

from ortools.sat.python.cp_model import CpSolver

from teams import TeamDatabase, Team
from tournament import SolvedTournament
from unoptimised_model import UnoptimisedModel


class TeamRow:
    def __init__(self, team_name: str, total_points: int,
                 dreamleague_season_24_final_placement_place: int,
                 dreamleague_season_24_final_placement_points: int,
                 dreamleague_season_24_gs1_place: int,
                 dreamleague_season_24_gs1_points: int,
                 dreamleague_season_24_gs2_place: int,
                 dreamleague_season_24_gs2_points: int):
        self.team_name = team_name
        self.total_points = total_points
        self.dreamleague_season_24_final_placement_place = dreamleague_season_24_final_placement_place
        self.dreamleague_season_24_final_placement_points = dreamleague_season_24_final_placement_points
        self.dreamleague_season_24_gs1_place = dreamleague_season_24_gs1_place
        self.dreamleague_season_24_gs1_points = dreamleague_season_24_gs1_points
        self.dreamleague_season_24_gs2_place = dreamleague_season_24_gs2_place
        self.dreamleague_season_24_gs2_points = dreamleague_season_24_gs2_points


class Display:
    def print(self,
              team_to_optimise: Team,
              max_points: float,
              unoptimised_model: UnoptimisedModel,
              solver: CpSolver,
              dreamleague_season_24: SolvedTournament,
              team_database: TeamDatabase) -> str:
        team_rows = []
        i = 0
        for team in team_database.get_all_teams():
            dreamleague_season_24_final_placement_points = solver.Value(unoptimised_model.dreamleague_season_24.points[i])
            dreamleague_season_24_gs1_points = solver.Value(unoptimised_model.dreamleague_season_24.gs1_points[i])
            dreamleague_season_24_gs2_points = solver.Value(unoptimised_model.dreamleague_season_24.gs2_points[i])
            team_rows.append(TeamRow(
                team_name=team.name,
                total_points=solver.Value(unoptimised_model.total_points[i]),
                dreamleague_season_24_final_placement_place=dreamleague_season_24.points_to_place(dreamleague_season_24_final_placement_points),
                dreamleague_season_24_final_placement_points=dreamleague_season_24_final_placement_points,
                dreamleague_season_24_gs1_place=dreamleague_season_24.gs1_points_to_place(dreamleague_season_24_gs1_points),
                dreamleague_season_24_gs1_points=dreamleague_season_24_gs1_points,
                dreamleague_season_24_gs2_place=dreamleague_season_24.gs2_points_to_place(dreamleague_season_24_gs2_points),
                dreamleague_season_24_gs2_points=dreamleague_season_24_gs2_points
            ))
            i += 1

        sorted_team_rows = sorted(team_rows, key=lambda team_row: team_row.total_points, reverse=True)

        output = ""
        output += "==What does the threshold scenario look like?==\n"
        output += f"This is the following scenario where {{{{Team|{team_to_optimise.name}}}}} fail to qualify with {round(max_points)} points.\n"
        output += '{| class="wikitable" style="font-size:85%; text-align: center;"\n'
        output += "!rowspan=\"2\" style=\"min-width:40px\"| '''Place'''\n"
        output += "!rowspan=\"2\" style=\"min-width:200px\"| '''Team'''\n"
        output += "!style=\"min-width:50px\"| '''Point'''\n"
        output += f"! colspan=\"{unoptimised_model.dreamleague_season_24.points_scoring_phases}\" style=\"min-width:50px\"|{unoptimised_model.dreamleague_season_24.icon}\n"
        output += "|-\n"
        output += f"! '''{(round(max_points) + 1)}'''\n"
        if unoptimised_model.dreamleague_season_24.points_scoring_phases == 1:
            output += "! Overall\n"
        elif unoptimised_model.dreamleague_season_24.points_scoring_phases == 2:
            output += "! Overall || GS1\n"
        elif unoptimised_model.dreamleague_season_24.points_scoring_phases == 3:
            output += "! Overall || GS1 || GS2\n"
        else:
            raise Exception(f"Unknown number of points scoring phases {unoptimised_model.dreamleague_season_24.points_scoring_phases}")
        output += "|-\n"
        i = 0

        def formatted_points(place: int, points: int | None) -> str:
            if place is None:
                return f"{points}"

            if place > 3:
                return f"{points}"

            return f"{{{{PlacementBg/{place + 1}}}}} {points}"

        for sorted_team_row in sorted_team_rows:
            if i == 8:
                output += "|-\n"
                output += '| colspan="99" | Top 8 cutoff\n'
            output += "|-\n"
            output += f"| {(i + 1)}\n"
            output += f"|style=\"text-align: left;\"| {{{{Team|{sorted_team_row.team_name}}}}}\n"
            output += f"| {sorted_team_row.total_points}\n"
            output += f"| {formatted_points(sorted_team_row.dreamleague_season_24_final_placement_place, sorted_team_row.dreamleague_season_24_final_placement_points)}\n"
            output += f"| {formatted_points(sorted_team_row.dreamleague_season_24_gs1_place, sorted_team_row.dreamleague_season_24_gs1_points)}\n"
            output += f"| {formatted_points(sorted_team_row.dreamleague_season_24_gs2_place, sorted_team_row.dreamleague_season_24_gs2_points)}\n"
            output += "|-\n"
            i += 1
        output += "|}"

        return output
