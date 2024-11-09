from teams import TeamDatabase


class TransferWindow:
    def __init__(self, team_database: TeamDatabase):
        self.team_database = team_database
        self.changes = [0] * len(team_database.get_all_teams())

    def add_change(self, team_name: str, delta: int):
        self.changes[self.team_database.get_team_index_by_team_name(team_name)] = delta

    def as_table(self) -> []:
        return self.changes