# SQLiteDb

SQLiteDb is a Python class that provides a simple interface for interacting with SQLite databases in Python. It allows you to easily create, insert, select, update, delete, and drop tables etc. in an SQLite database.

## Features
* Connect to a SQLite database
* Create a new table
* Insert rows into a table
* Select data from a table
* Drop a table from the database
* Delete from a table
* Update a table
* Change a table's name
* Change a column's name

## Usage
To use the SQLiteDb class, you need to import it and create an instance with the name of your database and the table you want to work with:

```python
from sqlite-utils import SQLiteDb

db = SQLiteDb('my_database.db', 'my_table')
```

Then, you can use the class's methods to interact with the database. For example:

### Creating a Table
To create a new table in the database, use the create_table() method and pass in a tuple of strings representing the column names and data types:
```python
db.create_table('id INTEGER PRIMARY KEY', 'name TEXT', 'age INTEGER')

```

### Inserting Data
To insert data into the table, use the insert_table() method and pass in a tuple of values:

```python
db.insert_table(1, 'John', 30)
db.insert_table(2, 'Jane', 25)

```

### Selecting Data
To select data from the table, use the select_from_table() method. You can select all columns by default or specific columns by providing their names as arguments. You can also specify a WHERE clause to filter the results, and an ORDER BY clause to sort the results:
```python
# Select all columns
results = db.select_from_table()
print(results)

# Select specific columns
results = db.select_from_table('name', 'age', where='age > 26', order_by='name')
print(results)
```

### Updating Data
To update data in the table, use the update_table() method and pass in the column names and new values as well as a WHERE clause to specify which rows to update.
```python
db.update_table(column_name="value", column_name2="value2", where="column_name3='value3'")
```

### Drop a Table
This method drops the specified table from the database. It permanently deletes the table and all the data it contains. A warning message is displayed to confirm the action before the table is dropped.
```python
db.drop_table()
```

### Delete from a Table
This method deletes all rows in the specified table. A warning message is displayed to confirm the action before the rows are deleted. You can also specify a WHERE clause when deleting rows from the table:
```python
db.delete_table()

db.delete_table("column_name = value")

```
