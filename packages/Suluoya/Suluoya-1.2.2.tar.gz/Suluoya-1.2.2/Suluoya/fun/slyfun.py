def draw_a_heart(name='Suluoya'):
    try:
        print('\n'.join([''.join([(name[(x-y)%len(list(name))]if((x*0.05)**2+(y*0.1)**2-1)**3-(x*0.05)**2*(y*0.1)**3<=0 else' ')for x in range(-30,30)])for y in range(15,-15,-1)]))
    except:
        print('请输入字符串！')
def standard_time(show=True):
    import time
    t=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    if show == True:
        print(t)
    return t
def xkcd():
    import antigravity
def syy():
    draw_a_heart('syy')
def hqy():
    draw_a_heart('hqy')
def wyx():
    draw_a_heart('wyx')
def lsf():
    print('SB')