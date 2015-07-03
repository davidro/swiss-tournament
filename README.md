This is Tournament project, it contains a database schema for postgresql database to store the game matches between players and python code to query this data and determine the winners of various games in Swiss-system tournamet style.

**To run the Application:**  
open command line and create database schema with following command:
```
psql -f tournament.sql  
```
run as well from command line the python test script to ensure everything works as expected:
```
python tournament_test.py  
```

**The main files and folders of Application:**  
- _tournament.sql_: table definitions for the project
- _db.py_: a class to handle database connection and query execution
- _tournament.py_: implementation of a Swiss-system tournament
- _tournament_test.py_: test script to ensure everything works as expected
- _/docs_: contains html documentation of python files you can open in your browser
