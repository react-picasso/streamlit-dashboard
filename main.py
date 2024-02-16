from standings.standings import Standings

def stats():
    standings = Standings()

    return standings.drop(), standings.table()

if __name__ == '__main__':
    stats()