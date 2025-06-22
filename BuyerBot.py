import requests
from bs4 import BeautifulSoup
from time import sleep
import json
import csv


def reCaptcha(captchaLink):
    try:
        res = ss.get(captchaLink, verify=False).content
        with open('image.jpg', 'wb') as img:
            img.write(res)

        files = {'file': open('image.jpg', 'rb')}
        ss = requests.Session()
        API_Key = '31e344b88486f046e57066ee24aa3192'

        captcha_id = ss.post("http://2captcha.com/in.php?key={}".format(
            API_Key), files=files, verify=False).text.split('|')[1]

        recaptcha_answer = ss.get(
            "http://2captcha.com/res.php?key={}&action=get&id={}".format(API_Key, captcha_id)).text
        print("Solving ref Captcha...")
        while 'CAPCHA_NOT_READY' in recaptcha_answer:
            sleep(5)
            recaptcha_answer = ss.get(
                "http://2captcha.com/res.php?key={}&action=get&id={}".format(API_Key, captcha_id)).text
        recaptcha_answer = recaptcha_answer.split('|')[1]
        return recaptcha_answer
    except Exception as e:
        print(e)


def pay_load(locator):
    data = locator.find_all('input', type='hidden')
    load = {}
    for row in data:
        if 'name' in str(row) and 'value' in str(row):
            load.update({row['name']: row['value']})
    return load


def Add_to_Cart():
    userData = []
    # with open('userData.txt', 'r') as f:
    #     userData.extend(f.readlines())
    # email = userData[0].replace('\n', '')
    # password = userData[1].replace('\n', '')
    # asin = userData[2]
    ss = requests.Session()

    head = requests.utils.default_headers()

    # First Go to Amazon URL

    Url = 'https://www.amazon.com/'
    # productUrl = 'https://www.amazon.com/dp/'+asin
    pr = '78327+US+78327:botmart123@us-1-sticky.botmart.co:14627'
    pr = '127.0.0.1:8888'
    # pr = '78327+US+78327:botmart123@us-1-sticky.botmart.co:10674'
    # pr = '78327+US+78327:botmart123@us-1-sticky.botmart.co:19391'
    # pr = '78327+US+78327:botmart123@us-1-sticky.botmart.co:10295'
    # pr = '78327+US+78327:botmart123@us-1-sticky.botmart.co:16042'
    # pr = 'manuelsicubtw:qWmxXbTqsw077vJy_country-Italy_session-wEmY6Mra@proxy.btwproxy.io:8080'
    # pr = 'manuelsicubtw:qWmxXbTqsw077vJy_country-Italy_session-RsHqs9Vz@proxy.btwproxy.io:8080'
    # pr = 'manuelsicubtw:qWmxXbTqsw077vJy_country-Italy_session-dtoRb5PB@proxy.btwproxy.io:8080'

    # ss.proxies = {
    #     'http': 'http://'+pr,
    #     'https': 'https://'+pr}
    head.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
    })

    # Go to SignIn Page and the corresponding pages to complete login procedures
    signIn = ss.get('https://www.amazon.com/gp/sign-in.html',
                    verify=True, headers=head)

    soup = BeautifulSoup(signIn.content)
    signInpage = soup.find('form', method='post')['action']
    payload = pay_load(soup)
    payload.pop('ue_back')
    payload.update({'email': email, 'password': '', 'metadata1': ''})
    head['Referer'] = signIn.url
    cookie = {'ubid-main': signIn.cookies['ubid-main']}
    signIn2 = ss.post(signInpage, verify=False, headers=head,
                      cookies=cookie, data=payload)

    soup = BeautifulSoup(signIn2.content)
    payload = pay_load(soup)

    md = ''

    head1 = {
        'Origin': 'https://www.amazon.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://www.amazon.com/ap/signin',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    payload.pop('ue_back')
    payload.update(
        {'email': [email, email], 'password': password, 'metadata1': md})
    head['Referer'] = signInpage
    loginUrl = ss.post(signInpage, verify=False, headers=head1, data=payload)

    if 'Enter the characters you see' in loginUrl.text and 'https://www.amazon.com/ap/signin' == loginUrl.url:
        print('It\'s a CAPTCHA')
        sleep(2)
        # break
        head.pop('Referer')
        soup = BeautifulSoup(loginUrl.content)
        captchaLink = soup.find('img', id="auth-captcha-image")["src"]
        payload = pay_load(soup)

        if 'subPageType' in payload:
            payload.pop('subPageType')
        if 'ue_back' in payload:
            payload.pop('ue_back')
        payload.update({'metadata1': '', 'email': [
                       email, email], 'password': password})

        recaptcha_answer = reCaptcha(captchaLink)

        payload.update({'guess': recaptcha_answer})

        loginUrl = ss.post(signInpage, verify=False,
                           headers=head, data=payload)

        if loginUrl.url == signInpage:
            soup = BeautifulSoup(loginUrl.content)
            captchaLink = soup.find('img', id="auth-captcha-image")["src"]
            payload = pay_load(soup)

            res = ss.get(captchaLink, verify=False).content
            with open('image.jpg', 'wb') as img:
                img.write(res)

            files = {'file': open('image.jpg', 'rb')}
            recaptcha_answer = reCaptcha(files)

            payload.update({'guess': recaptcha_answer})

    if 'https://www.amazon.com/ap/cvf/request?arb=' not in loginUrl.url:
        soup = BeautifulSoup(loginUrl.content)
        payload = pay_load(soup)
        if 'ue_back' in payload:
            payload.pop('ue_back')
        payload.update({'metadata1': '', 'email': [
                       email, email], 'password': password})
        loginUrl = ss.post('https://www.amazon.com/ap/signin',
                           verify=False, headers=head, data=payload)

    if 'https://www.amazon.com/ap/cvf/request?arb=' in loginUrl.url:
        soup = BeautifulSoup(loginUrl.content)
        load = pay_load(soup)

        load.update(
            {'openid.ns.pape':	'http://specs.openid.net/extensions/pape/1.0', 'ignoreAuthState':	'1'})
        auth1 = ss.post('https://www.amazon.com/ap/cvf/verify',
                        verify=False, headers=head, data=load)

        if 'Anti-Automation Challenge' in auth1.text or 'Enter the characters above' in auth1.text:
            soup = BeautifulSoup(auth1.content)
            load = pay_load(soup)
            captchaLink = soup.find('img', alt="captcha")["src"]
            recaptcha_answer = reCaptcha(captchaLink)

            load.update({'cvf_captcha_input': recaptcha_answer})
            auth1 = ss.post('https://www.amazon.com/ap/cvf/verify',
                            verify=False, headers=head, data=load)

        # Type the OTP, if sent to your registered email
        if "One Time Password (OTP) sent" in auth1.text:
            soup = BeautifulSoup(auth1.content)
            code = ''
            code = input('Enter OTP sent to your Email : ')
            load = {'code': code}
            load.update(pay_load(soup))

            print('Initial Action ', load['action'])
            load['action'] = 'code'
            authUrl = ss.post('https://www.amazon.com/ap/cvf/verify',
                              verify=False, headers=head, data=load)

            if authUrl.status_code == 200:
                print(
                    '****************************\n\nYou are Successfully logged In\n\n*****************************')
    # Go to the product page usin the product asin no.
    else:
        raise Exception('You are unable to login via bot')

    productPage = ss.get(productUrl, verify=False, headers=head)

    soup = BeautifulSoup(productPage.content)
    # refererUrl = soup.find('div', id = 'huc-page-state')['data-url']
    addingUrl = soup.find('form', method="post", id="addToCart")["action"]
    cartload = pay_load(soup)
    del(head)
    head = requests.utils.default_headers()
    head.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
    })
    addingUrl = 'https://www.amazon.com'+addingUrl
    addItemUrl = ss.post(addingUrl, verify=False, headers=head, data=cartload)

    # head.update({'Referer': refererUrl})
    soup = BeautifulSoup(addItemUrl.content)
    cartUrl = soup.find('a', id='hlb-ptc-btn-native')['href']
    CheckOutUrl = ss.get('https://www.amazon.com'+cartUrl,
                         verify=False, headers=head)

    soup1 = BeautifulSoup(CheckOutUrl.content)
    placeOrderUrl = soup1.find('form', id='spc-form')['action']
    orderLoad = pay_load(soup1)
    orderLoad.update(
        {'switchCurrency': 'transactional', 'placeYourOrder1': '1'})
    if 'ue_back' in orderLoad:
        orderLoad.pop('ue_back')
    data1 = soup.find_all('input', type='text')
    for row in data1:
        if 'name' in row:
            if row['name'] == 'storeZip2':
                orderLoad.update({row['name']: row['value']})
            if row['name'] == 'storeZip':
                orderLoad.update({row['name']: row['value']})
    for i in orderLoad:
        if 'RCX_CHECKOUT' in i:
            popKey = i
    orderLoad.pop(popKey)
    if 'primeCoOptState' in orderLoad:
        orderLoad.pop('primeCoOptState')
    data2 = soup.find('input', type='radio')
    orderLoad.update({data2['name']: data2['value']})
    if 'paymentInstrumentID' in orderLoad:
        orderLoad.pop('paymentInstrumentID')
    if 'offerToken' in orderLoad:
        orderLoad.pop('offerToken')
    orderLoad['currencyChanged'] = 'False'
    orderLoad['claimCode'] = ''

    # orderLoad.update(pay_load(soup))
    orderUrl = ss.post('https://www.amazon.com'+placeOrderUrl,
                       verify=False, headers=head, data=orderLoad)
    if orderUrl.status_code == 200:
        print('Your order hasbeen Successfully placed ')
        pass


Add_to_Cart()
pass
