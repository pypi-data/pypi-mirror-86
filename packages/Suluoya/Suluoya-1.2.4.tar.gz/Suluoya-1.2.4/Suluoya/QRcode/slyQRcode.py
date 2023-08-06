from MyQR import myqr
def QRcode(content='I Love Suluoya!',name='QRcode'):
    myqr.run(words=content,save_name=name+'.png')
def contact(mode='qq'):
    qq='https://qm.qq.com/cgi-bin/qm/qr?k=SQEky7p_hr1bclCGYHLO9YHGEV2SCcg1&noverify=0'    
    wechat='https://u.wechat.com/ELmeETBV3ihbSWAoJogLLp0'
    print('Thanks for your support!\nMy contact code is already created!\nPlease search for QRcode.png in the current directory!\nThanks again! ')
    if mode=='qq':
        myqr.run(words=qq,save_name='qq_QRcode.png')
    elif mode == 'wechat':
        myqr.run(words=wechat,save_name='wechat_QRcode.png')
    else:
        print('Please choose the a mode:\nqq in default or wechat instead')        
def pay(mode='alipay'):
    pay_alipay='https://qr.alipay.com/fkx08434ltweaydof2wuj4b'
    pay_wechat='wxp://f2f0OpF_yJIY9Iag7-EbFI2cjFsZH3wBQoS7'
    print('Thanks for your support!\nThe payment code is already created!\nPlease search for QRcode.png in the current directory!\nThanks again! ')
    if mode=='wechatpay':
        myqr.run(words=pay_wechat,save_name='wechatpay_QRcode.png')
    elif mode == 'alipay':
        myqr.run(words=pay_alipay,save_name='alipay_QRcode.png')
    else:
        print('Please choose the a mode:\nalipay in default or wechatpay instead')