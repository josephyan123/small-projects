""" module: odbctopy
    return a Pandas DataFrame from SQL query
    class sqlToPy
    method: sqltopy (also property)
    command line arguments: a sql statement with each clause included in double
        quotation mark; separated by space
"""
import pyodbc
import pandas as pd

class sqlToPy:
    ''' constuctor parameters
        ---------------------
            sqlstm:  position argument, multiple line string
            servnam: (optional) keyword argument, server name - only first part (the part before the first dot)
                     default value - 'myserver'
            dbnam:   (optional) keyword argument, database name
                     default value - 'mydatabase'

        method
        ------
            sqltopy: property
                     no additional parameters needed
                     return a Pandas DataFrame

        Warning
        -------
            please don't print the property (or return value of the method) unless you know it only
                contain few lines, assign the dataframe to a variable will be safer

        Example
        -------
            import odbctopy
            sqlstm = """select col1, col2, coln
                        from defaultschema.mytable1
                        where col2 = 7;"""
            df = odbctopy.sqlToPy(sqlstm).sqltopy
            if len(df) <= 100:
                print(df)
            else:
                print("The length of this dataframe is %d, too big for printing" % (len(df)))

    '''
    def __init__(self, sqlstm, servnam='myserver', dbnam='mydatabase'):

        self.servnam = servnam
        self.dbnam = dbnam
        self.sqlstm = sqlstm

    @property
    def sqltopy(self):
        ''' as a method, it return a DataFrame
            or as a property - a DataFrame representing the query result
            example: df = odbctopy.sqlToPy(sqlstm).sqltopy
        '''
        
        conn = pyodbc.connect(\
            'DRIVER={SQL Server};\
            SERVER=%s;\
            DATABASE=%s' % (self.servnam, self.dbnam), \
            autocommit=True)

        df = pd.read_sql(self.sqlstm, conn)

        conn.close()

        return df


if __name__ == "__main__":
    import sys

    import argparse
    parser = argparse.ArgumentParser(description='Execute SQL statements')
    parser.add_argument('-s', '--server', dest='servnam', default='myserver',
                        help='server name')
    parser.add_argument('-d', '--database', dest='dbnam', default='mydatabase',
                        help='database name')
    parser.add_argument('--temp-directory', dest='tmpfldr', default='/home/tmp',
                        help='A temporary folder to store the pickle and csv files')
    
    grp = parser.add_mutually_exclusive_group()
    grp.add_argument('--sqlstm', nargs=argparse.REMAINDER,
                        help="SQL statement, optionally separating clauses by question mark ('?')")
    grp.add_argument('--sqlfile', nargs=argparse.REMAINDER, default='path/to/my/sql/file',
                        help="filepath and filename to the sql file")
    args = parser.parse_args()

    if args.sqlstm:
        sqlstm = " ".join(args.sqlstm).replace("?", "\n")
    elif args.sqlfile:
        with open(args.sqlfile, 'r') as myfile:
            sqlstm = myfile.read()
    else:
        print('You should provide a SQL file or SQL statements at command line!')

    print("\nYour query statement is <\n%s\n>\n" % (sqlstm))
    
    df = sqlToPy(sqlstm, servnam=args.servnam, dbnam=args.dbnam).sqltopy
    
    print("The length of this query result is %d rows.\n" % (len(df)))
    
    from tabulate import tabulate
    
    if len(df) > 100000:
        print("Query result too big, no saving.\n")
    else:
        print("Query result saved.\n")
        df.to_pickle(args.tmpfldr+"/temp.pickle")
        df.to_csv(args.tmpfldr+"/temp.csv")

    if len(df) > 100:
        print("Here is the first 100 rows of the query result.")
        df_head = df[:101]
        print(tabulate(df_head, headers='keys', tablefmt='psql'))
    else:
        print("Here is the query result.")
        print(tabulate(df, headers='keys', tablefmt='psql'))
        
    
