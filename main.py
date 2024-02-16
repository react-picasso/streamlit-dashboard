from standings.standings import Standings

def stats():
    standings = Standings()

    return standings.table(), standings.graph()

if __name__ == '__main__':
    stats()