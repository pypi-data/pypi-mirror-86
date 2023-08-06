def translate(text='Welcome to use " sly.apy () "function to make a donation!',show=True):
    import translators as ts
    if text=='Welcome to use "sly.apy ()" to make a donation!':
        print(text)
    else:
        if show==True:
            try:
                print(ts.baidu(text, professional_field='common'))
            except:
                print('Something went wrong!')
        else:
            try:
                return(ts.baidu(text, professional_field='common'))
            except:
                print('Something went wrong!')
def text_compare(text1='suluoya',text2='Suluoya',accurate=True,show=True):
    from fuzzywuzzy import fuzz
    from fuzzywuzzy import process
    if show == True:
        if accurate == True:
            print(f'The similarity of {text1} and {text2} is '+str(fuzz.ratio(text1,text2))+'%.')
        else:
            print(f'The similarity of {text1} and {text2} is '+str(fuzz.partial_ratio(text1,text2))+'%.')
    else:
        if accurate == True:
            return fuzz.ratio(text1,text2)/100
        else:
            return fuzz.partial_ratio(text1,text2)/100
def gender_guess(name='苏洛雅',show=True):
    import ngender as nd
    try:
        if show==True:
            print(f'{round(nd.guess(name)[1]*100,2)}% could be a {nd.guess(name)[0]}.')
        else:
            return nd.guess(name)
    except:
        print('The name should be Chinese!')