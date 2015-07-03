This is Tournament project, it contains: a database schema for postgresql database to store the game matches between players and python code to query this data and determine the winners of various games in Swiss-system tournamet style.

** To run the Application: **
- open command line and create database schema with following command:
```
psql -f tournament.sql  
```
- run as well from command line the python test script to ensure everything works as expected:
```
python tournament_test.py  
```

** The main files of Application: **  
- __tournament.sql__ table definitions for the project
- __db.py__  a class to handle database connection and query execution
- __tournament.py__ implementation of a Swiss-system tournament
- __tournament_test.py__ test script to ensure everything works
