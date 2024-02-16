from src.standings import Standings
from src.locations import Location

def stats():
    standings = Standings()
    locations = Location()

    return standings.drop(), standings.table(), locations.drop(), locations.table()

if __name__ == '__main__':
    stats()