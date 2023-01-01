import os
import sqlite3


class SQLiteDb():
    def __init__(self, db_name, table_name):
        self.db_name = db_name # Database Name
        self.table_name = table_name # Table name
        self.conn = None # connection attribute
        self.cursor = None # cursor attribute
        self.connect_db() # Connect to Database
        
    def connect_db(self):
        """
        This method is used for connecting to database.\n
        'conn' variable is assigned the result of connecting to a SQLite database with the specified 'db_name'. \n
        Then, 'cursor' variable is assigned the result of creating a cursor object from the connection. \n
        The cursor object is used to execute SQL commands and retrieve results from the database.\n
        ---Parameters:---\n
        None\n
        ---Returns:---\n
        conn, cursor\n

        """
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print(f"Connected to Database {self.db_name}.")
            return self.conn, self.cursor
        except Exception as e:
            print(e)
    
    def create_table(self, *args):
        """
        This method is used to create a new table in the database.\n
        ---Parameters:---\n
        *args: tuple of strings, representing the column names and data types for the table.\n
        ---Returns:---\n
        None\n
        """
        try:
            # Check if the table to be created is exists
            if not self.is_table_exists:
                self.execute_db(f"CREATE TABLE {self.table_name} ({','.join(args)})")
            else:
                print("Table already exits.")
        except Exception as e:
            print(e)

    def insert_table(self, *args):
        """
        Insert a new row into the table.\n
        ---Parameters:---\n
        *args (tuple): Tuple of values to be inserted into the table.\n
        ---Returns:---\n
        None
        """
        try:
            # Convert args tuple to string 
            values_str =  ["'{}'".format(arg) for arg in args]
            self.execute_db(f"INSERT INTO {self.table_name} {self.column_names} VALUES ({','.join(values_str)})")
        except Exception as e:
            print(e)

    def select_from_table(self, *args, where=None, order_by=None):
        """
        This method allows you to select data from the table in the database.\n
        You can choose to select all columns (*) or specific columns by providing their names as arguments.\n
        You can also specify a WHERE clause to filter the results, and an ORDER BY clause to sort the results.\n 
        If successful, the method will execute the SELECT command and return the resulting rows.\n
        If an error occurs, it will print the error message.\n
        ---Parameters:---\n
        *args (tuple): Tuple of columns to be retrieved. Default is all columns.\n
        where (str): WHERE clause of the SELECT statement. Default is None.\n
        order_by (str): ORDER BY clause of the SELECT statement. Default is None.\n
        ---Returns:---\n
        List of tuples representing the retrieved rows.
        """
        command = "SELECT "

        try:
            # Check if columns are specified
            if len(args)<1:
                # Select All Columns
                command += "* "
            else:
                # Select Specific Columns
                command += f"{','.join(args)} "
            
            command += f"FROM {self.table_name} "

            # Add Where Clause
            if where != None:
                command += f"WHERE {where} "

            # Add Order By
            if order_by != None:
                command += f"ORDER BY {order_by} "
        
            self.execute_db(command)
            return self.cursor.fetchall()
        except Exception as  e:
            print(e)
        
    def drop_table(self):
        """
        Drop the table from the database.\n
        Note that this will permanently delete the table and all the data it contains.\n
        ---Returns:---\n
        None
        """
        try:
            # Check if the user confirmed to drop table
            if self.__warning_message():
                try: 
                    self.execute_db(f"DROP TABLE {self.table_name}")
                    print(f"Table '{self.table_name}' has been dropped.")
                except Exception as e:
                    print(e)
            else:
                print(f"The drop process has been cancelled.")
        except Exception as e:
            print(e)

    # Get confirmation from the user to make such critical changes as drop, delete
    def __warning_message(self):
        while True:
            warning = input("Note that this will permanently delete the table and all the data it contains. Do you want to continue? y/N:")
            warning = warning.upper()
            if warning in ["Y", "YES"]:
                return True
            elif warning in ["N", "NO"]:
                return False
            else:
                continue

    def delete_table(self, where=None):
        """
        Delete all rows in the table.\n
        ---Parameters:---\n
        None\n
        ---Returns:---\n
        None
        """
        try:
            if self.__warning_message():
                if where != None:
                    self.execute_db(f"DELETE FROM {self.table_name} WHERE {where}")
                else:
                    self.execute_db(f"DELETE FROM {self.table_name}")
        except Exception as e:
            print(e)

    def change_table_name(self, new_table_name):
        """
        Change the name of the table.\n
        ---Parameters:---\n
        new_table_name (str): New name for the table.\n
        ---Returns:---\n
        None
        """
        try:
            self.execute_db(f"ALTER TABLE {self.table_name} RENAME TO {new_table_name};")
            self.table_name = new_table_name
        except Exception as e:
            print(e)

    def change_column_name(self, column_name, new_column_name ):
        """
        Change the name of a column in the table.\n
        ---Parameters:---\n
        column_name (str): The current name of the column that you want to rename.\n
        new_column_name (str): The new name of the column.\n
        ---Returns:---\n
        None
        """
        try:
            self.execute_db(f"ALTER TABLE {self.table_name} RENAME COLUMN {column_name} to {new_column_name};")
        except Exception as e:
            print(e)

    def update_table(self, set, where):
        try:
            self.execute_db(f"UPDATE {self.table_name} SET {set} WHERE {where}")
        except Exception as e:
            print(e)

    def execute_db(self, command):
        """
        Execute an SQL command.\n
        ---Parameters:---\n
        command (str): The SQL command to be executed.\n
        ---Returns:---\n
        None
        """
        try:
            self.cursor.execute(command)
            self.commit_db()    
        except Exception as e:
            print(e) 
    
    def commit_db(self):
        """
        Commit changes to the database.\n
        ---Parameters:---\n
        None\n
        ---Returns:---\n
        None
        """
        try:
            self.conn.commit()
        except Exception as e:
            print(e)

    def close_db(self):
        """
        Close the connection to the database.\n
        ---Returns:---\n
        None
        """
        try:
            self.conn.close()
        except Exception as e:
            print(e)

    @property
    def column_names(self):
        columns = self.table_info
        return tuple(column[1] for column in columns)

    @property
    def table_info(self):
        self.execute_db(f"PRAGMA table_info({self.table_name})")
        columns = self.cursor.fetchall()
        return columns

    @property
    def show_tables(self):
        self.execute_db("SELECT name FROM sqlite_master WHERE type='table'")
        tables = self.cursor.fetchall()
        return tables

    @property
    def is_table_exists(self):
        tables = self.show_tables
        if (self.table_name,) in tables:
            return True
        return False

    @property
    def is_db_exists(self, path=os.listdir(os.path.dirname(__file__))):
        if self.db_name in path:
            return True
        return False

