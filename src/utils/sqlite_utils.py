import sqlite3
from sqlalchemy import create_engine, text


EMAILS_DB = "emails.db"


class SQLiteUtils:
  def run(self, db_name:str=EMAILS_DB,table_name:str="employees"):
    # Create a connection to a database (or create it if it doesn't exist)
    conn = self.create_connection(db_name)

    # Execute SQL commands
    self.create_table(conn,table_name=table_name)

    # Insert data
    self.insert_data(conn,table_name=table_name, data= ("Michael wang", "michaelwang@163.com"))

    # Commit changes and close
    conn.commit()
    conn.close()

  def create_connection(self, db_file):
    """Create a database connection"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to {db_file}")
    except sqlite3.Error as e:
        print(f"Error: {e}")
    return conn

  def create_table(self, conn, table_name:str="employees"):
      """Create a sample table"""
      create_table_sql = f"""
      CREATE TABLE IF NOT EXISTS {table_name} (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL,
          email TEXT NOT NULL,
          age INTEGER
      );
      """
      try:
          c = conn.cursor()
          c.execute(create_table_sql)
      except sqlite3.Error as e:
          print(f"Error creating table: {e}")

  def insert_data(self, conn, table_name, data):
      """Insert a new employee"""
      sql = f'''INSERT INTO {table_name}(name,email)
                VALUES(?,?) '''
      cur = conn.cursor()
      cur.execute(sql, data)
      conn.commit()
      return cur.lastrowid

  def select_all_data(self, conn,table_name):
      """Query all rows in the employees table"""
      cur = conn.cursor()
      cur.execute(f"SELECT * FROM {table_name}")
      
      rows = cur.fetchall()
      for row in rows:
          print(row)
      return rows
  

def create_sqlite_database_with_alchemy():
  # Connect to SQLite database
  engine = create_engine('sqlite:///example.db')

  with engine.connect() as conn:
      result = conn.execute(text("SELECT * FROM users"))
      for row in result:
          print(row)


if __name__ == "__main__":
  sqlite_utils = SQLiteUtils()
  sqlite_utils.run()