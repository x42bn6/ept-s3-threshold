from region import Region
from teams import Team


class Qualifier:
    def __init__(self, region: Region, teams: [Team], num_qualified: int):
        self.region = region
        self.teams = teams
        self.num_qualified = num_qualified

    def eliminate(self, team: Team):
        self.teams.pop(team)

    def get_remaining_teams(self) -> [Team]:
        return self.teams
