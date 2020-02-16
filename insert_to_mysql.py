"""
@author: Phani Kumar Koratamaddi
This script is to read/write data from/to mysql db
"""

import mysql.connector as mysql
from sqlalchemy import create_engine
# import pymysql
import pandas as pd


class MysqlIo:
    """
    This class is to read/write data from/to mysql db
    """

    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.pwd = "root"

    def read_from_db(self, schema='skillenza', table_name='data_set'):
        """function to read data from mysql db and return as a pandas dataframe
        :parameter
         schema - Name of the schema
         table_name - Name of the table
        :return Returns the table as pandas dataframe
        """

        # Create connection
        conn = mysql.connect(host=self.host, user=self.user, passwd=self.pwd)
        mycursor = conn.cursor()

        # Read the data as a list of lists
        sql_query = 'SELECT * FROM ' + schema + '.' + table_name
        mycursor.execute(sql_query)
        my_list = mycursor.fetchall()

        # Convert the list to dataframe
        cols = ['INDEX', 'CIN', 'COMPANY NAME', 'DATE OF REGISTRATION', 'MONTH NAME', 'STATE', 'ROC', 'COMPANY STATUS',
                'CATEGORY', 'CLASS', 'COMPANY TYPE', 'AUTHORIZED CAPITAL', 'PAIDUP CAPITAL', 'ACTIVITY CODE',
                'ACTIVITY DESCRIPTION', 'REGISTERED OFFICE ADDRESS', 'EMAIL', 'x1', 'x2', 'x3', 'x4', 'x5', 'TURN OVER']
        my_df = pd.DataFrame(my_list, columns=cols)

        return my_df

    def write_to_db(self, dataframe, schema='skillenza', table_name='data_set'):
        """function to write data to mysql db
        :parameter
         dataframe - Input csv file as a pandas dataframe
         schema - Name of the schema
         table_name - Name of the table
        :return Returns success or error message
        """

        # Create connection
        conn = 'mysql+pymysql://' + self.user + ':' + self.pwd + '@' + self.host + '/' + schema
        sql_engine = create_engine(conn, pool_recycle=3600)
        db_connection = sql_engine.connect()

        # Push the data to mysql db
        try:
            dataframe.to_sql(table_name, db_connection, if_exists='append')

        except ValueError as vx:
            print(vx)
            return "Oops !! There is an error. We are working on it"
        except Exception as ex:
            print(ex)
            return "Oops !! There is an error. We are working on it"
        else:
            return "Thank you !! File uploaded successfully"
        finally:
            db_connection.close()
