import psycopg2

class Database:
    def __init__(self, url: str):
        self.url = url

    def connect(self):
        self.conn = psycopg2.connect(
            host=self.url.split(':')[2].split('@')[1],
            database=self.url.split('/')[3],
            user=self.url.split(':')[1].split('/')[2],
            password=self.url.split(':')[2].split('@')[0],
        )
    
    def insert(self, schema: str, app_id: str):
        with self.conn.cursor() as cursor:
            cursor.execute(f"INSERT INTO {schema} (video_id) VALUES ('{app_id}')")

        self.conn.commit()

    def get_all_ids(self, schema: str):
        with self.conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {schema}")
            return cursor.fetchall()
    


def get_db_connection(url: str):
    return Database(url)
