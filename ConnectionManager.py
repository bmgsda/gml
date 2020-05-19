import pyodbc

class Connection():
    def __init__(self):
        DRIVER = '{PostgreSQL Unicode}'
        DATABASE = 'projects'
        UID = 'postgres'
        PWD = 'postgres'
        SERVER = 'localhost'
        PORT = 5432
        conn_str = f'DRIVER={DRIVER};DATABASE={DATABASE};UID={UID};PWD={PWD};SERVER={SERVER};PORT={PORT};'
        self.connection = pyodbc.connect(conn_str)

    def execute_query(self, query):
        try:
            self.connection.execute(query)
            self.connection.commit()
            return True
        except Exception as e:
            return e