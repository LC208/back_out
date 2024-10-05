'''Wait for mysql container up'''
import time
import MySQLdb
from django.core.management.base import BaseCommand
import out.settings as db

class Command(BaseCommand):
    help = 'Ожидание до поднятия бд'

    def add_arguments(self, parser):
        parser.add_argument('timeout', type=int, help='Количество попыток для подключения')

    def handle(self, *args, **kwargs):
        # Get the database connection characteristics.
        (HOST, PORT, USERNAME, PASSWORD, DATABASE, TIMEOUT) = (db.DATABASES['default']['HOST'], db.DATABASES['default']['PORT'], db.DATABASES['default']['USER'],  db.DATABASES['default']['PASSWORD'], db.DATABASES['default']['NAME'], kwargs['timeout'])
        # Ensure timeout is an integer greater than zero, otherwise use 15 secs a default
        try:
            TIMEOUT = int(TIMEOUT)
            if TIMEOUT <= 0:
                raise Exception("Timeout needs to be > 0")
        except:
            TIMEOUT = 60
        # Ensure port is an integer greater than zero, otherwise use 3306 as default
        try:
            PORT = int(PORT)
            if PORT <= 0:
                raise Exception("Port needs to be > 0")
        except:
            PORT = 3306
        # Try to connect to the database TIMEOUT times
        for i in range(0, TIMEOUT):
            try:
                # Try to connect to db
                con = MySQLdb.connect(host=HOST, port=PORT, user=USERNAME, password=PASSWORD, database=DATABASE)
                with con:
                    cur = con.cursor()
                    cur.execute("SELECT VERSION()")
                # If an error hasn't been raised, then exit
                return True

            except Exception as Ex:
                strErr=Ex.args[0]
                print(Ex.args)
                # Sleep for 1 second
                time.sleep(1)
        # If I get here, assume a timeout has occurred
        raise Exception("Timeout")
