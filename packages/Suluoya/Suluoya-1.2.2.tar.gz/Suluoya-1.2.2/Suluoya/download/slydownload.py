def download(url):
    import wget
    try:
        wget.download(url)
    except:
        print('Something went wrong!')
def download_music(path='d:\\'):
    import requests
    import urllib.parse as parse
    from urllib.request import urlretrieve
    import json
    import urllib.request
    w=parse.urlencode({'w':input('请输入歌名:')})
    url='https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.song&searchid=63229658163010696&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=10&%s&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0'%(w)
    content=requests.get(url=url)
    str_1=content.text
    dict_1=json.loads(str_1)
    song_list=dict_1['data']['song']['list']
    str_3='''https://u.y.qq.com/cgi-bin/musicu.fcg?-=getplaysongvkey5559460738919986&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&data={"req":{"module":"CDN.SrfCdnDispatchServer","method":"GetCdnDispatch","param":{"guid":"1825194589","calltype":0,"userip":""}},"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"1825194589","songmid":["%s"],"songtype":[0],"uin":"0","loginflag":1,"platform":"20"}},"comm":{"uin":0,"format":"json","ct":24,"cv":0}}'''
    url_list=[]
    music_name=[]
    for i in range(len(song_list)):
        music_name.append(song_list[i]['name']+'-'+song_list[i]['singer'][0]['name'])
        print('{}.{}-{}'.format(i+1,song_list[i]['name'],song_list[i]['singer'][0]['name']))
        url_list.append(str_3 % (song_list[i]['mid']))
    id=int(input('请输入你想下载的音乐序号:'))
    content_json=requests.get(url=url_list[id-1])
    dict_2=json.loads(content_json.text)
    url_ip=dict_2['req']['data']['freeflowsip'][1]
    purl=dict_2['req_0']['data']['midurlinfo'][0]['purl']
    downlad=url_ip+purl    
    try:
        print('开始下载...')
        urlretrieve(url=downlad,filename=r'{}{}.mp3'.format(path,music_name[id-1]))
        print('{}{}.mp3下载完成!'.format(path,music_name[id-1]))
    except Exception as e:
        print('没有{}的版权'.format(music_name[id-1]))
def download_video(url):
    import os
    try:
        os.system(f'you-get {url}')
    except:
        print('Something went wrong!')       
