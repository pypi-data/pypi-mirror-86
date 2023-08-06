import pandas as pd
def get_table(url,encoding='utf8',header=None,caption='.+',save=False):
    try:
        dfs=pd.read_html(io=url,encoding=encoding,header=header,match=caption)
        if len(dfs)>1:
            print('='*13)
            print(f'Get {len(dfs)} tables.')
            print('='*13)
            print('\n')
        elif len(dfs)==1:
            pass
        lists=[]
        for df in dfs:
            df.dropna(how='all',inplace=True)
            lists.append(df)
        if save == True:
            k=0
            for i in lists:
                k+=1
                i.to_excel(f'{k}.xlsx',index=False)
        return lists 
    except:
        print('No tables found!')

