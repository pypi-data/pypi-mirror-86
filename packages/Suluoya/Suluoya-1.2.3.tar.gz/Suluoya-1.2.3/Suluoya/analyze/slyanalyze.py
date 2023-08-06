def report(df):
    import pandas_profiling
    a=pandas_profiling.ProfileReport(df)
    a.to_file('report.html')
