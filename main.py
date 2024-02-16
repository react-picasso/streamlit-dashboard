from src.standings import Standings
from src.locations import Location
from src.players import Players

def stats():
    standings = Standings()
    locations = Location()
    players = Players()

    return standings.drop(), standings.table(), locations.drop(), locations.table(), players.drop(), players.load()

if __name__ == '__main__':
    stats()