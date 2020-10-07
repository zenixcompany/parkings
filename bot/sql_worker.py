import json
import psycopg2


try:
    conn = psycopg2.connect(dbname='postgres', 
                            user='postgres', 
                            password='',
                            host='localhost',
                            port='5432'
                            )
except Exception as e:
    print(e)

class SQL:
    def __init__(self):
        self.conn = conn
        self.cursor = self.conn.cursor()



    def get_parkings(self):
        with self.conn:
            query = f'SELECT * FROM _parkings'
            try:
                self.cursor.execute(query)
            except Exception as e:
                print(e)

            return self.cursor.fetchall()