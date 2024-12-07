from qualifier import Qualifier
from region import Region
from teams import TeamDatabase
from tournament import SolvedTournament


class DreamLeagueSeason24:
    def build(self, team_database: TeamDatabase) -> SolvedTournament:
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
                                                                                         "Nigma Galaxy"),
                                                                                     num_qualified=1),
                                                             Region.CHINA: Qualifier(region=Region.CHINA,
                                                                                     teams=team_database.get_teams_by_names(
                                                                                         "Azure Ray"),
                                                                                     num_qualified=1),
                                                             Region.SEA: Qualifier(region=Region.SEA,
                                                                                   teams=team_database.get_teams_by_names(
                                                                                       "Talon Esports"),
                                                                                   num_qualified=1)},
                                                 points=[3000, 2500, 2000, 1600, 1200, 1000, 600, 400,
                                                         250, 250, 125, 125, 70, 70, 30, 30],
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
                                                 gs2_teams=team_database.get_teams_by_names("Team Falcons",
                                                                                            "BetBoom Team",
                                                                                            "Team Spirit",
                                                                                            "PARIVISION",
                                                                                            "Team Waska",
                                                                                            "Team Liquid",
                                                                                            "Xtreme Gaming",
                                                                                            "Tundra Esports"),
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

        dreamleague_season_24.team_can_finish_between_gs2("BetBoom Team", 1, 1)
        dreamleague_season_24.team_can_finish_between_gs2("Team Spirit", 2, 2)
        dreamleague_season_24.team_can_finish_between_gs2("PARIVISION", 3, 3)
        dreamleague_season_24.team_can_finish_between_gs2("Team Falcons", 4, 4)
        dreamleague_season_24.team_can_finish_between_gs2("Tundra Esports", 5, 5)
        dreamleague_season_24.team_can_finish_between_gs2("Team Liquid", 6, 6)
        dreamleague_season_24.team_can_finish_between_gs2("Xtreme Gaming", 7, 7)
        dreamleague_season_24.team_can_finish_between_gs2("Team Waska", 8, 8)

        dreamleague_season_24.team_can_finish_between("Team Falcons", 1, 1)
        dreamleague_season_24.team_can_finish_between("BetBoom Team", 2, 2)
        dreamleague_season_24.team_can_finish_between("Team Spirit", 3, 3)
        dreamleague_season_24.team_can_finish_between("PARIVISION", 4, 4)
        dreamleague_season_24.guaranteed_playoff_lb_or_eliminated("Team Falcons", "PARIVISION", "Team Spirit")

        return dreamleague_season_24
