import psycopg2


# a class to make DRY up the code
# and perist connection to the database between diffrent fuction calls
class DB:
    #  A constructor that defines connection to the database
    def __init__(self, db_con="dbname=tournament"):
        """
        Creates a database connection with the connection string provided
        :param str db_con: Contains the database connection string,
        with a default value when no argument is passed to the parameter
        """
        self.conn = psycopg2.connect(db_con)

    # Cursor method
    def cursor(self):
        """
        Returns the current cursor of the database
        """
        return self.conn.cursor()

    # method to exectute sql query, with optional query parametes
    # and optional parameter to close connection
    def execute(self, sql_s, params=False, close_con=False):
        """
        Executes SQL queries
        :param str sql_s: Contain the query string to be executed
        :param tuple params: Passes function params protected against SQL injc.
        :param bool close: If true, closes the database connection
        """
        cursor = self.cursor()
        if params is False:
            cursor.execute(sql_s)
        else:
            cursor.execute(sql_s, params)

        if close_con:
            self.conn.commit()
            self.close()
        return {"conn": self.conn, "cursor": cursor if not close_con else None}

    # method to close connection to the database
    def close(self):
        """
        Closes the current database connection
        """
        return self.conn.close()
