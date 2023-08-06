def search_question(question='',again=False,show=False):
    import requests
    import json
    if question !='':
        url='http://api.xmlm8.com/tk.php?t={}'.format(question)
        response = requests.request("GET", url)
        data=json.loads(response.text)
        if show == True:
            print(data['tm']+'\n'+data['da']+'\n')
        else:
            return(data['tm']+'\n'+data['da']+'\n')
    else:
        if again == False:        
            timu=input('Please input the question:')
            url='http://api.xmlm8.com/tk.php?t={}'.format(timu)
            try:
                response = requests.request("GET", url)
                data=json.loads(response.text)
                print(data['tm']+'\n'+data['da']+'\n')
            except:
                mistake='Could not find the answer!'
                print(mistake) 
        else:
            while 1:
                timu=input('请输入题目：')
                url='http://api.xmlm8.com/tk.php?t={}'.format(timu)
                try:
                    response = requests.request("GET", url)
                    data=json.loads(response.text)
                    print(data['tm']+'\n'+data['da']+'\n')                
                except:
                    mistake='Could not find the answer!'
                    print(mistake)
def get_table(url,encoding='utf8',header=None,caption='.+',save=False):
    import pandas as pd
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
def get_soup(url='https://pypi.org/project/Suluoya-pkg/',encoding='utf8',headers={},params={},payload={},show=False):
    import requests
    from bs4 import BeautifulSoup
    try:
        response = requests.request("GET", url, headers=headers, data = payload, params = params)
        response.encoding=encoding
        soup = BeautifulSoup(response.text,'html.parser')
        if show == True:
            print(soup)
        return(soup)
    except:
        try:
            response = requests.request("GET", url, headers=headers, data = payload, params = params)
            if show == True:
                num=str(response)[-5:-2]
                print('HTTP Status Code ='+num)
                print('Please access https://www.cnblogs.com/hao-1234-1234/p/8940079.html')                
        except:
            print('Something went wrong!')    
def get_json(url='',encoding='utf8',headers={},params={},payload={},show=False):
    import json
    import requests
    try:
        if url == '':
            print('Please add an url!')
        else:
            response = requests.request("GET", url, headers=headers, data = payload, params = params)
            response.encoding=encoding
            data=json.loads(response.text)
            if show==True:
                print(data)
            return(data)
    except:
        try:
            response = requests.request("GET", url, headers=headers, data = payload, params = params)
            num=str(response)[-5:-2]
            print('HTTP Status Code ='+num)
            print('Please access https://www.cnblogs.com/hao-1234-1234/p/8940079.html')
        except:
            print('Something went wrong!')
def get_text(url='',useragent='',accurate=True):
    from goose3 import Goose
    if accurate == True:
        from goose3.text import StopWordsChinese
        g = Goose({'stopwords_class': StopWordsChinese,
                'browser_user_agent': useragent
                })
    else:
        g = Goose({'browser_user_agent': useragent
                })
    url = url
    article=g.extract(url=url)
    dic={
    'title':article.title,#标题
    'text':article.cleaned_text,#正文
    'description':article.meta_description,#摘要
    'keywords':article.meta_keywords,#关键词
    'tags':article.tags,#标签
    'image':article.top_image,#主要图片
    'infomation':article.infos,#包含所有信息的 dict
    'raw_html':article.raw_html#原始 HTML 文本
    }
    return dic