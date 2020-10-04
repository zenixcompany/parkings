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


   # def __del__(self):
   #     self.conn.close()


#   def set_spaces_amount(self, id, spaces_amount):
#     with self.connection:
#       query = f'UPDATE parkings SET spaces_amount = ? WHERE id = ?'
#       self.cursor.execute(query, (spaces_amount, id))


    def get_parkings(self):
        with self.conn:
            query = f'SELECT * FROM _parkings'
            self.cursor.execute(query)

            return self.cursor.fetchall()