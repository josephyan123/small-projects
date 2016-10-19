"""
pivot table while one of the index (the index used as column name) values are not unique

dependencies: Numpy and Pandas

commandline arguments:
    input_file: .csv file containing raw data, first line must be table header.
    output_file: output file to save the pivoted table as csv file
        above two arguments should include the entire file path and name; path separator, use '/' in linux/unix, '/' or '\\' in Windows
    unique_row_index: header of column used as row_index after reshape
    ununique_col_index: header of column used as column index after reshape
    val: header of column used for transpose
               
command-line example:   python this_file.py /home/user/file1.csv /home/user/file2 col_name1 col_name2 col_name3

"""

while True:
    try:
        import sys
        import numpy as np
        import pandas as pd

        input_file = sys.argv[1]
        output_file = sys.argv[2]
        unique_row_index = sys.argv[3]
        ununique_col_index = sys.argv[4]
        val = sys.argv[5]

        df = pd.read_csv(input_file)

        newdf = pd.DataFrame()

        for x in df[unique_row_index].unique():
            df1 = df.ix[df[unique_row_index]==x, [ununique_col_index, val]]
            df2 = df1.set_index(ununique_col_index)
            df3 = df2.T
            df3[unique_row_index] = x
            newdf = newdf.append(df3)

        newdf1 = newdf.set_index(unique_row_index)

        newdf1.to_csv(output_file)

        break

    except:
        print(__doc__)
        print("Oops! Something not correct, please read above docstring and try again...")
        break
