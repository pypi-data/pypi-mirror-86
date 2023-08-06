def pip():
    import os
    try:
        os.system('pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requests')
        os.system('pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r pandas')
        os.system('pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r beautifulsoup4')
        os.system('pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r translators')
        os.system('pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r fuzzywuzzy')
        os.system('pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r ngender')
        os.system('pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r MyQR')
        os.system('pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r pyforest')
        os.system('pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r wget')
        os.system('pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r urllib3')
        print('Requirements have been installed!')
    except:
        print('Something went wrong!')
