from collections import Counter
from enum import Enum
from ortools.sat.python import cp_model

class SolvedModel:
    def __init__(self, model, teamlist,
                 r_s21, r_kl, r_s22, r_birmingham, r_s23,
                 points_s21, points_s21_kl, points_kl, points_kl_s22, points_s22, points_s22_birmingham, d_birmingham,
                 points_birmingham_s23, d_s23, points_s23_riyadh, d,
                 currentpoints, solver, maxpoints, team_to_optimise):
        self.model = model
        self.teamlist = teamlist
        self.r_s21 = r_s21
        self.r_kl = r_kl
        self.r_s22 = r_s22
        self.r_birmingham = r_birmingham
        self.r_s23 = r_s23
        self.points_s21 = points_s21
        self.points_s21_kl = points_s21_kl
        self.points_kl = points_kl
        self.points_kl_s22 = points_kl_s22
        self.points_s22 = points_s22
        self.points_s22_birmingham = points_s22_birmingham
        self.d_birmingham = d_birmingham
        self.points_birmingham_s23 = points_birmingham_s23
        self.d_s23 = d_s23
        self.points_s23_riyadh = points_s23_riyadh
        self.d = d
        self.currentpoints = currentpoints
        self.solver = solver
        self.maxpoints = maxpoints
        self.team_to_optimise = team_to_optimise

    def printsolution(self):
        teamlist = self.teamlist
        teams = len(teamlist)
        currentpoints = self.currentpoints
        solver = self.solver

        mat = [[0] * 11] * teams

        def format_points_tournament(points):
            if points == None:
                return ""
            if points == 0:
                return ""
            return round(points)

        def format_points_in_between(points):
            if points == None:
                return ""
            if points > 0:
                return "+" + str(points)
            return points

        for t in range(teams):
            teamname = list(currentpoints.keys())[t]

            mat[t] = [0] * 12
            mat[t][0] = teamname
            mat[t][1] = format_points_tournament(self.points_s21.get(teamname))
            mat[t][2] = format_points_in_between(self.points_s21_kl.get(teamname))
            mat[t][3] = format_points_tournament(self.points_kl.get(teamname))
            mat[t][4] = format_points_in_between(self.points_kl_s22.get(teamname))
            mat[t][5] = format_points_tournament(self.points_s22.get(teamname))
            mat[t][6] = format_points_in_between(self.points_s22_birmingham.get(teamname))
            mat[t][7] = format_points_tournament(solver.Value(self.d_birmingham[t]))
            mat[t][8] = format_points_in_between(self.points_birmingham_s23.get(teamname))
            mat[t][9] = format_points_tournament(solver.Value(self.d_s23[t]))
            mat[t][10] = format_points_in_between(self.points_s23_riyadh.get(teamname))
            mat[t][11] = solver.Value(self.d[t])
        sortedmatrix = sorted(mat, key=lambda x: x[11], reverse=True)

        def get_team_name(t):
            return teamlist[t]

        def is_placeholder_team(teamname):
            return teamname in ["NA team", "SA team", "WEU team 1", "WEU team 2", "EEU team", "MENA team", "China team",
                                "SEA team"]

        def get_placementbg(tournamentpoints, points):
            if points not in tournamentpoints:
                return ""

            i = tournamentpoints.index(points)
            if i < 4:
                return f"{{{{PlacementBg/{i + 1}}}}} "
            return ""

        print("Printing Liquipedia table")
        print()
        print("==What does the threshold scenario look like?==")
        print(
            f"This is the following scenario where {{{{Team|{get_team_name(self.team_to_optimise)}}}}} fail to qualify with {round(self.maxpoints)} points.")
        print()
        print('{| class="wikitable" style="font-size:85%; text-align: center;"')
        print("!style=\"min-width:40px\"|'''Place'''")
        print("!style=\"min-width:200px\"|'''Team'''")
        print("!style=\"min-width:50px\"|'''Point'''")
        print("|rowspan=99|")
        print(
            "!style=\"min-width:50px\"|{{LeagueIconSmall/dreamleague|name=DreamLeague Season 21|link=DreamLeague/Season 21|date=2023-09-24}}")
        print(
            "!style=\"min-width:50px; font-size: larger;\"|<span title=\"Point changes between DreamLeague Season 21 and ESL One Kuala Lumpur 2023\">&hArr;</span>")
        print(
            "!style=\"min-width:50px\"|{{LeagueIconSmall/esl one|name=ESL One Kuala Lumpur 2023|link=ESL One/Kuala Lumpur/2023|date=2023-12-17}}")
        print(
            "!style=\"min-width:50px; font-size: larger;\"|<span title=\"Point changes between ESL One Kuala Lumpur 2023 and DreamLeague Season 22\">&hArr;</span>")
        print(
            "!style=\"min-width:50px\"|{{LeagueIconSmall/dreamleague|name=DreamLeague Season 22|link=DreamLeague/Season 22|date=2024-03-10}}")
        print(
            "!style=\"min-width:50px; font-size: larger;\"|<span title=\"Point changes between DreamLeague Season 22 and ESL One Birmingham 2024\">&hArr;</span>")
        print(
            "!style=\"min-width:50px\"|{{LeagueIconSmall/esl one|name=ESL One Birmingham 2024|link=ESL One/Birmingham/2024|date=2024-04-28}}")
        print(
            "!style=\"min-width:50px; font-size: larger;\"|<span title=\"Point changes between ESL One Birmingham 2024 and DreamLeague Season 23\">&hArr;</span>")
        print(
            "!style=\"min-width:50px\"|{{LeagueIconSmall/dreamleague|name=DreamLeague Season 23|link=DreamLeague/Season 23|date=2024-05-26}}")
        print(
            "!style=\"min-width:50px; font-size: larger;\"|<span title=\"Point changes DreamLeague Season 23 and Riyadh Masters 2024\">&hArr;</span>")
        print(
            "!style=\"min-width:50px\"|{{LeagueIconSmall/riyadh masters|name=Riyadh Masters 2024|link=Riyadh Masters/2024|date=2024-07-21}}")
        i = 0
        for row in sortedmatrix:
            if i == 8:
                print("|-")
                print('| colspan="99" | Top 8 cutoff')
            print("|-")

            teamcomponent = f"{{{{Team|{row[0]}}}}}" if not is_placeholder_team(
                row[0]) else f"{row[0]} with 0 EPT points"
            s21component = f"{get_placementbg(self.r_s21, row[1])}{row[1]}"
            klcomponent = f"{get_placementbg(self.r_kl, row[3])}{row[3]}"
            s22component = f"{get_placementbg(self.r_s22, row[5])}{row[5]}"
            birminghamcomponent = f"{get_placementbg(self.r_birmingham, row[7])}{row[7]}"
            s23component = f"{get_placementbg(self.r_s23, row[9])}{row[9]}"

            print(f'| {(i + 1)}')
            print(f'!style="text-align: left;"| {teamcomponent}')

            if i == 8:
                print(
                    f'| style="font-weight: bold; background-color: var(--achievement-placement-down, #cd5b5b);" | {row[11]}')
            else:
                print(f"| '''{row[11]}'''")
            print(f"| {s21component}")
            print(f"| {row[2]}")
            print(f"| {klcomponent}")
            print(f"| {row[4]}")
            print(f"| {s22component}")
            print(f"| {row[6]}")
            print(f"| {birminghamcomponent}")
            print(f"| {row[8]}")
            print(f"| {s23component}")
            print(f"| {row[10]}")
            if i < 8:
                print(f'|[[Riyadh_Masters/2024#Group_Stage_Seeds|GS]]')
            else:
                print(f"|")
            i += 1
        print("|}")


class Counter_tweaked(Counter):
    def __add__(self, other):
        if not isinstance(other, Counter):
            return NotImplemented
        result = Counter_tweaked()
        for elem, count in self.items():
            newcount = count + other[elem]
            result[elem] = newcount
        for elem, count in other.items():
            if elem not in self:
                result[elem] = count
        return result


class Tournament(Enum):
    BIRMINGHAM = 1
    S23 = 2


class Model:
    def __init__(self):
        self.points_s21 = {
            'BetBoom Team': 1600,
            'Gaimin Gladiators': 400,
            'Team Spirit': 2400,
            'Team Liquid': 200,
            'OG': 1280,
            'Shopify Rebellion': 2000,
            'Entity': 880,
            'Tundra Esports': 880,
            'PSG Quest': 100,
            'Talon Esports': 100
        }

        self.points_s21_kl = {
            'OG': -384,
            'Shopify Rebellion': -2000,
            'Aurora': 100,
            'Tundra Esports': -880,
            'Entity': -264,
            'Talon Esports': -100
        }

        self.points_kl = {
            'BetBoom Team': 2400,
            'Team Falcons': 1680,
            'Gaimin Gladiators': 3600,
            'Team Liquid': 3000,
            'G2.iG': 1680,
            'Team Secret': 780,
            'Tundra Esports': 780,
            'Blacklist International': 420,
            'LGD Gaming': 420,
            'Azure Ray': 4800,
        }

        self.points_kl_s22 = {
            'Xtreme Gaming': 3360,
            'Team Secret': -234,
            'Tundra Esports': -780,
            'Azure Ray': -4800
        }

        self.points_s22 = {
            'BetBoom Team': 3500,
            'Xtreme Gaming': 2800,
            'Team Falcons': 4200,
            'Gaimin Gladiators': 1680,
            'Team Spirit': 2240,
            'Team Liquid': 98,
            'OG': 1400,
            'G2.iG': 42,
            'Shopify Rebellion': 840,
            'Aurora': 560,
            'Team Secret': 175,
            'Tundra Esports': 350,
            'HEROIC': 98,
            'Virtus.pro': 350,
            '1win': 42,
            'Azure Ray': 175
        }

        # Placeholder 0 EPT point teams in qualifier
        self.qualifier_teams = {
            # 'NA team': 0,
            'nouns': 0,
            # 'SA team': 0,
            'Estar_Backs': 0,
            'WEU team 1': 0,
            'WEU team 2': 0,
            # 'EEU team': 0,
            'Natus Vincere': 0,
            # 'MENA team': 0,
            'Nigma Galaxy': 0,
            # 'China team': 0,
            'Team Zero': 0,
            # 'SEA team': 0
            'Geek Fam': 0
        }
        self.qualifier_teams.pop('Geek Fam')
        self.qualifier_teams.pop('WEU team 1')
        self.qualifier_teams.pop('WEU team 2')
        self.qualifier_teams.pop('nouns')
        self.qualifier_teams.pop('Team Zero')
        self.qualifier_teams.pop('Nigma Galaxy')
        self.qualifier_teams.pop('Estar_Backs')

        self.points_s22_birmingham = {}

        self.points_birmingham_s23 = {
            # Roster submission issue ahead of Birmingham
            'Tundra Esports': -35,
        }

        # Any changes after S23
        self.points_s23_riyadh = {
            # Palos, Mjz -> Natsumi, Jaunuel
            'Blacklist International': -126
        }

        self.currentpoints = Counter_tweaked(self.points_s21) + Counter_tweaked(self.points_s21_kl) + \
                             Counter_tweaked(self.points_kl) + Counter_tweaked(self.points_kl_s22) + \
                             Counter_tweaked(self.points_s22) + Counter_tweaked(self.points_s22_birmingham) + \
                             Counter_tweaked(self.points_birmingham_s23) + Counter_tweaked(self.points_s23_riyadh) + \
                             Counter_tweaked(self.qualifier_teams)
        self.teams = len(self.currentpoints)
        self.teamlist = list(self.currentpoints.keys())
        for ti in self.teamlist:
            print(ti)

        self.na_qualifier = ['Shopify Rebellion', 'nouns']
        self.na_qualifier.remove('nouns')
        self.na_qualifier.remove('Shopify Rebellion')
        self.sa_qualifier = ['HEROIC', 'Estar_Backs']
        self.sa_qualifier.remove('HEROIC')
        self.sa_qualifier.remove('Estar_Backs')
        self.weu_qualifier = ['Team Liquid', 'OG', 'Team Secret', 'Entity', 'Tundra Esports', 'WEU team 1',
                              'WEU team 2']
        self.weu_qualifier.remove('Team Secret')
        self.weu_qualifier.remove('WEU team 1')
        self.weu_qualifier.remove('WEU team 2')
        self.weu_qualifier.remove('Team Liquid')
        self.weu_qualifier.remove('Entity')
        self.weu_qualifier.remove('OG')
        self.weu_qualifier.remove('Tundra Esports')
        self.eeu_qualifier = ['Team Spirit', 'Virtus.pro', '1win', 'Natus Vincere']
        self.eeu_qualifier.remove('Team Spirit')
        self.eeu_qualifier.remove('1win')
        self.eeu_qualifier.remove('Virtus.pro')
        self.mena_qualifier = ['PSG Quest', 'Nigma Galaxy']
        self.mena_qualifier.remove('Nigma Galaxy')
        self.mena_qualifier.remove('PSG Quest')
        self.china_qualifier = ['G2.iG', 'LGD Gaming', 'Azure Ray', 'Team Zero']
        self.china_qualifier.remove('LGD Gaming')
        self.china_qualifier.remove('G2.iG')
        self.china_qualifier.remove('Team Zero')
        self.sea_qualifier = ['Aurora', 'Talon Esports', 'Blacklist International', 'Geek Fam']
        self.sea_qualifier.remove('Blacklist International')
        self.sea_qualifier.remove('Geek Fam')
        self.sea_qualifier.remove('Talon Esports')
        self.sea_qualifier.remove('Aurora')

        self.r_s21 = (2400, 2000, 1600, 1280, 880, 880, 400, 400, 200, 200, 100, 100)
        self.r_kl = (4800, 3600, 3000, 2400, 1680, 1680, 780, 780, 420, 420, 210, 210)
        self.r_s22 = (4200, 3500, 2800, 2240, 1680, 1680, 1400, 1400, 840, 560, 350, 350, 175, 175, 98, 98, 42, 42)
        self.r_birmingham = (6400, 4800, 4000, 3200, 2240, 2240, 1040, 1040, 560, 560, 280, 280)
        self.r_s23 = (6000, 5000, 4000, 3200, 2200, 2200, 1000, 1000, 500, 500, 250, 250)
        self.placements = 12

        self.birmingham_teams = ['BetBoom Team', 'Xtreme Gaming', 'Team Falcons', 'Gaimin Gladiators',
                                 'Team Spirit', 'Team Liquid', 'G2.iG', 'Shopify Rebellion', 'Tundra Esports', 'HEROIC',
                                 '1win', 'Talon Esports']
        # 1win visa issues
        self.birmingham_teams.append('OG')
        self.birmingham_teams.remove('1win')
        self.s23_teams = ['BetBoom Team', 'Xtreme Gaming', 'Team Falcons', 'Gaimin Gladiators',
                          'Aurora', 'Natus Vincere', 'Shopify Rebellion', 'Team Liquid', 'Azure Ray', 'Tundra Esports',
                          'PSG Quest', 'HEROIC']

        self.birmingham_highest = [-1 for i in range(self.teams)]
        self.s23_highest = [-1 for i in range(self.teams)]

        self.model = cp_model.CpModel()

    def team_index(self, t):
        return list(self.currentpoints.keys()).index(t)

    def build(self):
        model = self.model
        teams = self.teams
        teamlist = self.teamlist
        placements = self.placements
        currentpoints = self.currentpoints

        x_birmingham = [[model.NewBoolVar(f'x_birmingham_{i}_{j}') for j in range(placements)] for i in range(teams)]
        x_s23 = [[model.NewBoolVar(f'x_s23_{i}_{j}') for j in range(placements)] for i in range(teams)]
        d_birmingham = [model.NewIntVar(0, 99999, f'd_birmingham_{i}') for i in range(teams)]
        d_s23 = [model.NewIntVar(0, 99999, f'd_s23_{i}') for i in range(teams)]
        d = [model.NewIntVar(0, 99999, f'd_{i}') for i in range(teams)]

        def team_can_finish_between(tournament, tournament_enum, team, best, worst):
            t = teamlist.index(team)
            sum = 0
            for i in range(best, worst + 1):
                sum += tournament[t][i - 1]
            model.Add(sum == 1)

            if tournament_enum == Tournament.BIRMINGHAM:
                self.birmingham_highest[t] = self.r_birmingham[best - 1]
            elif tournament_enum == Tournament.S23:
                self.s23_highest[t] = self.r_s23[best - 1]

        def one_of_these_teams_finishes_in(tournament, group, position):
            sum = 0
            for group_team in group:
                t = teamlist.index(group_team)
                sum += tournament[t][position - 1]
            model.Add(sum == 1)

        # It is not possible for these teams to provide the winner *and* runner-up
        def guaranteed_lb_or_eliminated(tournament, group):
            sum = 0
            for i in [0, 1]:
                for team in group:
                    sum += tournament[teamlist.index(team)][i]
            model.Add(sum <= 1)

        #############################
        # ESL One Birmingham
        #############################
        team_can_finish_between(x_birmingham, Tournament.BIRMINGHAM, 'BetBoom Team', 2, 2)
        team_can_finish_between(x_birmingham, Tournament.BIRMINGHAM, 'Xtreme Gaming', 7, 8)
        team_can_finish_between(x_birmingham, Tournament.BIRMINGHAM, 'Team Falcons', 1, 1)
        team_can_finish_between(x_birmingham, Tournament.BIRMINGHAM, 'Gaimin Gladiators', 11, 12)
        team_can_finish_between(x_birmingham, Tournament.BIRMINGHAM, 'Team Spirit', 9, 10)
        team_can_finish_between(x_birmingham, Tournament.BIRMINGHAM, 'Team Liquid', 5, 6)
        team_can_finish_between(x_birmingham, Tournament.BIRMINGHAM, 'OG', 4, 4)
        team_can_finish_between(x_birmingham, Tournament.BIRMINGHAM, 'G2.iG', 5, 6)
        team_can_finish_between(x_birmingham, Tournament.BIRMINGHAM, 'Shopify Rebellion', 11, 12)
        team_can_finish_between(x_birmingham, Tournament.BIRMINGHAM, 'Tundra Esports', 3, 3)
        team_can_finish_between(x_birmingham, Tournament.BIRMINGHAM, 'HEROIC', 7, 8)
        team_can_finish_between(x_birmingham, Tournament.BIRMINGHAM, 'Talon Esports', 9, 10)

        # Group A
        birmingham_group_a = ['BetBoom Team', 'Team Liquid', 'G2.iG', 'Talon Esports', 'Team Falcons',
                              'Shopify Rebellion']
        one_of_these_teams_finishes_in(x_birmingham, birmingham_group_a, 9)
        one_of_these_teams_finishes_in(x_birmingham, birmingham_group_a, 11)

        # Group B
        birmingham_group_b = ['HEROIC', 'OG', 'Tundra Esports', 'Team Spirit', 'Gaimin Gladiators', 'Xtreme Gaming']
        one_of_these_teams_finishes_in(x_birmingham, birmingham_group_b, 10)
        one_of_these_teams_finishes_in(x_birmingham, birmingham_group_b, 12)

        # 7th-8th - force matchups to avoid, say, Liquid and HEROIC both finishing 7th-8th (impossible as they play each other)
        one_of_these_teams_finishes_in(x_birmingham, ['Team Liquid', 'HEROIC'], 7)
        one_of_these_teams_finishes_in(x_birmingham, ['Xtreme Gaming', 'G2.iG'], 8)

        # 5th-6th - we know how teams drop from the upper bracket
        one_of_these_teams_finishes_in(x_birmingham, ['Team Falcons', 'Tundra Esports', 'Team Liquid', 'HEROIC'], 5)
        one_of_these_teams_finishes_in(x_birmingham, ['OG', 'BetBoom Team', 'Xtreme Gaming', 'G2.iG'], 6)

        #############################
        # DreamLeague Season 23
        #############################
        team_can_finish_between(x_s23, Tournament.S23, 'BetBoom Team', 1, 3)
        team_can_finish_between(x_s23, Tournament.S23, 'Xtreme Gaming', 4, 4)
        team_can_finish_between(x_s23, Tournament.S23, 'Team Falcons', 1, 3)
        team_can_finish_between(x_s23, Tournament.S23, 'Gaimin Gladiators', 1, 2)
        team_can_finish_between(x_s23, Tournament.S23, 'Team Liquid', 9, 10)
        team_can_finish_between(x_s23, Tournament.S23, 'Shopify Rebellion', 9, 10)
        team_can_finish_between(x_s23, Tournament.S23, 'Aurora', 7, 8)
        team_can_finish_between(x_s23, Tournament.S23, 'Tundra Esports', 5, 6)
        team_can_finish_between(x_s23, Tournament.S23, 'HEROIC', 7, 8)
        team_can_finish_between(x_s23, Tournament.S23, 'Azure Ray', 5, 6)
        team_can_finish_between(x_s23, Tournament.S23, 'PSG Quest', 11, 12)
        team_can_finish_between(x_s23, Tournament.S23, 'Natus Vincere', 11, 12)

        # Group A
        s23_group_a = ['Aurora', 'Gaimin Gladiators', 'HEROIC', 'PSG Quest', 'Team Liquid', 'Xtreme Gaming']
        one_of_these_teams_finishes_in(x_s23, s23_group_a, 9)
        one_of_these_teams_finishes_in(x_s23, s23_group_a, 11)

        # Group B
        s23_group_b = ['Azure Ray', 'BetBoom Team', 'Natus Vincere', 'Shopify Rebellion', 'Team Falcons',
                       'Tundra Esports']
        one_of_these_teams_finishes_in(x_s23, s23_group_b, 10)
        one_of_these_teams_finishes_in(x_s23, s23_group_b, 12)

        # LB teams
        guaranteed_lb_or_eliminated(x_s23,
                                    ['Aurora', 'HEROIC', 'Azure Ray', 'BetBoom Team', 'Tundra Esports', 'Xtreme Gaming',
                                     'Team Falcons'])

        # 7th-8th
        one_of_these_teams_finishes_in(x_s23, ['Aurora', 'BetBoom Team'], 7)
        one_of_these_teams_finishes_in(x_s23, ['Azure Ray', 'HEROIC'], 8)

        # 5th-6th
        one_of_these_teams_finishes_in(x_s23, ['Aurora', 'BetBoom Team', 'Gaimin Gladiators', 'Tundra Esports'], 5)
        one_of_these_teams_finishes_in(x_s23, ['Azure Ray', 'HEROIC', 'Team Falcons', 'Xtreme Gaming'], 6)

        # ESL One Birmingham constraints
        # Qualified teams
        for t in self.birmingham_teams:
            model.Add(sum(x_birmingham[self.team_index(t)]) == 1)

        # DreamLeague Season 23 constraints
        # Already-qualified teams
        for t in self.s23_teams:
            model.Add(sum(x_s23[self.team_index(t)]) == 1)

        # Regional constraints
        # Basically, within each region, only one team can qualify and thus place
        # So if there are two qualified teams for a region, there are two rows, but only one 1 in both rows
        def add_regional_constraint(regionalqualifier, numberofqualifedteams, decisionvariable, model):
            regional_sum = 0
            for t in regionalqualifier:
                teamindex = self.team_index(t)
                model.Add(sum(decisionvariable[teamindex]) <= 1)
                regional_sum += sum(decisionvariable[teamindex])
            model.Add(regional_sum == numberofqualifedteams)

        # add_regional_constraint(self.na_qualifier, 1, x_s23, model)
        # add_regional_constraint(self.sa_qualifier, 1, x_s23, model)
        # add_regional_constraint(self.weu_qualifier, 2, x_s23, model)
        # add_regional_constraint(self.eeu_qualifier, 1, x_s23, model)
        # add_regional_constraint(self.mena_qualifier, 1, x_s23, model)
        # add_regional_constraint(self.china_qualifier, 1, x_s23, model)
        # add_regional_constraint(self.sea_qualifier, 1, x_s23, model)

        # One placement per team
        for p in range(placements):
            model.Add(sum(x_birmingham[i][p] for i in range(teams)) == 1)
            model.Add(sum(x_s23[i][p] for i in range(teams)) == 1)

        # Points
        for t in self.currentpoints:
            teamindex = self.team_index(t)
            d_birmingham[teamindex] = sum(x_birmingham[teamindex][p] * self.r_birmingham[p] for p in range(placements))
            d_s23[teamindex] = sum(x_s23[teamindex][p] * self.r_s23[p] for p in range(placements))
            d[teamindex] = self.currentpoints[self.teamlist[teamindex]] + d_birmingham[teamindex] + d_s23[teamindex]

        # Ranks
        aux = {(i, j): model.NewBoolVar(f'aux_{i}_{j}') for i in range(teams) for j in range(teams)}
        ranks = {team: model.NewIntVar(1, teams, f'ranks_{team}') for team in range(teams)}
        M = 20000
        for i in range(teams):
            for j in range(teams):
                if i == j:
                    model.Add(aux[(i, j)] == 1)
                else:
                    model.Add(d[i] - d[j] <= (1 - aux[(i, j)]) * M)
                    model.Add(d[j] - d[i] <= aux[(i, j)] * M)
            ranks[i] = sum(aux[(i, j)] for j in range(teams))

        return [model, x_birmingham, x_s23, d_birmingham, d_s23, d, aux, ranks]

    def optimise(self, team_to_optimise, show_all, maxobjectivevalue):
        teamlist = self.teamlist

        [model, _, _, d_birmingham, d_s23, d, _, ranks] = self.build()

        model.Add(ranks[team_to_optimise] > 8)
        model.Maximize(d[team_to_optimise])

        # If this team can't breach the best maximum so far, don't bother
        if not show_all:
            teamname = teamlist[team_to_optimise]
            maxpointsobtainable = 0
            if teamname in self.birmingham_teams:
                if self.birmingham_highest[team_to_optimise] > 0:
                    maxpointsobtainable += self.birmingham_highest[team_to_optimise]
                else:
                    maxpointsobtainable += self.r_birmingham[0]

            if teamname in self.s23_teams:
                if self.s23_highest[team_to_optimise] > 0:
                    maxpointsobtainable += self.s23_highest[team_to_optimise]
                else:
                    maxpointsobtainable += self.r_s23[0]
            elif teamname in self.na_qualifier or teamname in self.sa_qualifier or teamname in self.weu_qualifier or teamname in self.eeu_qualifier or teamname in self.mena_qualifier or teamname in self.china_qualifier or teamname in self.sea_qualifier:
                maxpointsobtainable += self.r_s23[0]

            maxpointsobtainable += self.currentpoints[self.teamlist[team_to_optimise]]
            if maxpointsobtainable < maxobjectivevalue:
                print(f"Skipping {teamlist[team_to_optimise]} as {maxpointsobtainable} < {maxobjectivevalue}")
                return self.tounsolvedmodel(team_to_optimise)

        solver = cp_model.CpSolver()
        status = solver.Solve(model)
        if status == cp_model.OPTIMAL:
            objectivevalue = solver.ObjectiveValue()
            print("Objective value:", objectivevalue)
            return self.tosolvedmodel(team_to_optimise, d_birmingham, d_s23, d, solver, objectivevalue)
        else:
            print("No optimal solution found, probably unable to finish outside of top 8.")
            return self.tounsolvedmodel(team_to_optimise)

    def tosolvedmodel(self, team_to_optimise, d_birmingham, d_s23, d, solver, objectivevalue):
        return SolvedModel(self.model, self.teamlist,
                           self.r_s21, self.r_kl, self.r_s22, self.r_birmingham, self.r_s23,
                           self.points_s21, self.points_s21_kl, self.points_kl, self.points_kl_s22, self.points_s22,
                           self.points_s22_birmingham, d_birmingham, self.points_birmingham_s23, d_s23,
                           self.points_s23_riyadh, d,
                           self.currentpoints, solver, objectivevalue, team_to_optimise)

    def tounsolvedmodel(self, team_to_optimise):
        return self.tosolvedmodel(team_to_optimise, None, None, None, None, -1)


def main():
    # Final constraint
    max_team = -1
    max_solution = -1
    max_model = None
    # for t in [Model().teamlist.index('PSG Quest')]:
    for t in range(len(Model().currentpoints)):
        model = Model()
        print(f"Optimising for {list(model.currentpoints.keys())[t]}")
        ninth = model.optimise(t, False, max_solution)
        if ninth.maxpoints > 0:
            old_max_solution = max_solution
            if old_max_solution < ninth.maxpoints:
                max_team = t
                max_solution = round(max(old_max_solution, ninth.maxpoints))
                max_model = ninth
        print()

    max_model.printsolution()

    print("Done")


if __name__ == "__main__":
    main()
