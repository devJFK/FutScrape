import datetime
import codecs
import csv

def write_csv(player_list, name):
    with codecs.open(f'{name}.csv', 'w', encoding='utf-8', errors='ignore') as w:
        csvwriter = csv.writer(w)

        csvwriter.writerow(['NAME', 'POSITION', 'VERSION', 'RATING', 'VOLUME', 'HIGH', 'HIGH DAY', 'LOW', 'LOW DAY', 'ONE DAY AVG', 'FIVE DAY AVG', 'TEN DAY AVG', 'ONE DAY MEDIAN', 'FIVE DAY MEDIAN', 'TEN DAY MEDIAN'])

        for player in player_list:
            csvwriter.writerow([player.NAME, player.POSITION, player.VERSION, player.RATING, player.STATS['VOLUME'], player.STATS['HIGH'], player.STATS['HIGH_DAY'], player.STATS['LOW'], player.STATS['LOW_DAY'], player.STATS['AVERAGE']['ONE'], player.STATS['AVERAGE']['FIVE'], player.STATS['AVERAGE']['TEN'], player.STATS['MEDIAN']['ONE'], player.STATS['MEDIAN']['FIVE'], player.STATS['MEDIAN']['TEN']])