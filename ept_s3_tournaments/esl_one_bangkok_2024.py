from qualifier import Qualifier
from region import Region
from teams import TeamDatabase
from tournament import SolvedTournament


class ESLOneBangkok2024:
    def build(self, team_database: TeamDatabase) -> SolvedTournament:
        esl_one_bangkok = SolvedTournament(name="ESL One Bangkok 2024", link="ESL One/Bangkok/2024",
                                                 icon="{{LeagueIconSmall/esl one|name=ESL One Bangkok 2024|link=ESL One/Bangkok/2024|date=2024-12-15}}",
                                                 team_count=12,
                                                 invited_teams=team_database.get_teams_by_names("Team Falcons",
                                                                                                "BetBoom Team",
                                                                                                "Team Spirit",
                                                                                                "PARIVISION"),
                                                 qualifiers={Region.NA: Qualifier(region=Region.NA,
                                                                                  teams=team_database.get_teams_by_names(
                                                                                      "Shopify Rebellion"),
                                                                                  num_qualified=1),
                                                             Region.SA: Qualifier(region=Region.SA,
                                                                                  teams=team_database.get_teams_by_names(
                                                                                      "M80"),
                                                                                  num_qualified=1),
                                                             Region.WEU: Qualifier(region=Region.WEU,
                                                                                   teams=team_database.get_teams_by_names(
                                                                                       "Team Liquid",
                                                                                       "AVULUS"),
                                                                                   num_qualified=2),
                                                             Region.EEU: Qualifier(region=Region.EEU,
                                                                                   teams=team_database.get_teams_by_names(
                                                                                       "Natus Vincere"),
                                                                                   num_qualified=1),
                                                             Region.MESWA: Qualifier(region=Region.MESWA,
                                                                                     teams=team_database.get_teams_by_names(
                                                                                         "Nigma Galaxy"),
                                                                                     num_qualified=1),
                                                             Region.CHINA: Qualifier(region=Region.CHINA,
                                                                                     teams=team_database.get_teams_by_names(
                                                                                         "Gaozu"),
                                                                                     num_qualified=1),
                                                             Region.SEA: Qualifier(region=Region.SEA,
                                                                                   teams=team_database.get_teams_by_names(
                                                                                       "BOOM Esports"),
                                                                                   num_qualified=1)},
                                                 points=[4800, 3600, 3000, 2400, 1680, 1680, 780, 780, 420, 420, 210, 210],
                                                 gs1_points=[480],
                                                 gs1_team_count=6,
                                                 playoff_team_count=8,

                                                 gs1_a_teams=team_database.get_teams_by_names("AVULUS",
                                                                                              "BOOM Esports",
                                                                                              "Natus Vincere",
                                                                                              "Shopify Rebellion",
                                                                                              "Team Falcons",
                                                                                              "Team Spirit"),
                                                 gs1_b_teams=team_database.get_teams_by_names("BetBoom Team",
                                                                                              "Gaozu",
                                                                                              "M80",
                                                                                              "Nigma Galaxy",
                                                                                              "PARIVISION",
                                                                                              "Team Liquid"),
                                                 team_database=team_database)

        return esl_one_bangkok
