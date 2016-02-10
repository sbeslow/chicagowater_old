from datetime import datetime

from mwrd_csos.database_methods import insert_cso_into_db, select_from_db
from mwrd_csos.helpers import find_overlapping_times
from scraper import scrape_date
import sqlite3

sqlite_file = 'cso-data.db'


def scrape_by_date(date_str):

    events = scrape_date(date_str)

    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()

    for event in events:

        try:

            insert_cso_into_db(c, event)

        except Exception as e:
            print('Exception: %s' % e.message)

    conn.commit()
    conn.close()


def search_for_overlap(event):
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()

    a = find_overlapping_times(c, event)
    conn.close()
    return a


event = {"date": "2015-9-18", "location": 'DS-M15',
         "start": datetime.strptime("3:30", "%H:%M"),
         "stop": datetime.strptime("3:45", "%H:%M"),}
a = search_for_overlap(event)
for b in a:
    print("ID=" + str(b["id"]))