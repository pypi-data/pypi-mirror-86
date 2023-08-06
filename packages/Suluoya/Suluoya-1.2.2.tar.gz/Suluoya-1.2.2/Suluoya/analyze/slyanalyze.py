def report(df):
    a=pandas_profiling.ProfileReport(df)
    a.to_file('report.html')
