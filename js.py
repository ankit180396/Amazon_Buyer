import requests 
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def pay_load(locator):
  data = locator.find_all('input', type='hidden')
  load = {}
  for row in data:
    if 'name' in str(row) and 'value' in str(row):
      load.update({row['name']:row['value']})
  return load

def reCaptcha(files):
  try:
    ss = requests.Session()
    API_Key = '31e344b88486f046e57066ee24aa3192'
    
    captcha_id = ss.post("http://2captcha.com/in.php?key={}".format(API_Key), files= files, verify=False).text.split('|')[1]

    recaptcha_answer = ss.get("http://2captcha.com/res.php?key={}&action=get&id={}".format(API_Key, captcha_id)).text
    print("Solving ref Captcha...")
    while 'CAPCHA_NOT_READY' in recaptcha_answer:
      sleep(5)
      recaptcha_answer = ss.get("http://2captcha.com/res.php?key={}&action=get&id={}".format(API_Key, captcha_id)).text
    recaptcha_answer = recaptcha_answer.split('|')[1]
    return recaptcha_answer
  except Exception as e:
    print(e)


def amazon():
  ss = requests.Session()
  url = 'https://www.amazon.com'

  userData = []
  with open('userData.txt','r') as f:
    userData.extend(f.readlines())
  email = userData[0].replace('\n','')
  password = userData[1].replace('\n','')
  asin = userData[2]
  head = requests.utils.default_headers()
  head.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
  })

  productUrl = 'https://www.amazon.com/dp/'+asin

  chrome_options = Options()  
  chrome_options.add_argument('--no-sandbox')
  # chrome_options.add_argument('--disable-gpu')
  # chrome_options.add_argument("--headless")
  chrome_options.add_argument("--start-maximized")
  driver = webdriver.Chrome("chromedriver.exe",chrome_options=chrome_options) 


  driver.get('https://www.amazon.com/gp/sign-in.html')

  driver.find_element_by_id('ap_email').send_keys(email+'\n')
  driver.find_element_by_id('ap_password').send_keys(password+'\n')
  sleep(2)
  
  while driver.current_url=='https://www.amazon.com/ap/signin':
    driver.find_element_by_id('ap_password').send_keys(password)
    try:
      soup = BeautifulSoup(driver.page_source)
      captchaLink = soup.find('img', id = "auth-captcha-image")["src"]

      res = ss.get(captchaLink, verify = False).content
      with open('image.jpg','wb') as img:
        img.write(res)

      files = {'file': open('image.jpg', 'rb')}
      recaptcha_answer = reCaptcha(files)
      driver.find_element_by_id('auth-captcha-guess').send_keys(recaptcha_answer)
      driver.find_element_by_id('signInSubmit').click()
      sleep(2)
    except:
      driver.find_element_by_id('signInSubmit').click()
      sleep(2)

 
    # driver.find_element_by_xpath(r'//*[@id="ap_password"]').send_keys(password+'\n')

  if 'https://www.amazon.com/ap/cvf/request?arb=' in driver.current_url:
    driver.find_element_by_xpath(r'//*[@id="continue"]').click()
    if 'Anti-Automation Challenge' in driver.page_source:
      soup = BeautifulSoup(driver.page_source)
      captchaLink = soup.find('img', id = "auth-captcha-image")["src"]

      res = ss.get(captchaLink, verify = False).content
      with open('image.jpg','wb') as img:
        img.write(res)

      files = {'file': open('image.jpg', 'rb')}
      recaptcha_answer = reCaptcha(files)
      driver.find_element_by_id('auth-captcha-guess').send_keys(recaptcha_answer+'\n')
  if "One Time Password (OTP) sent" in driver.page_source:   
    OTP = input('Enter OTP : ')
    driver.find_element_by_xpath(r'//*[@id="cvf-page-content"]/div/div/div[1]/form/div[2]/input').send_keys(OTP,'\n')

    pass

  #   soup = BeautifulSoup(driver.page_source)
  #   load = pay_load(soup)

  #   load.update({'openid.ns.pape':	'http://specs.openid.net/extensions/pape/1.0', 'ignoreAuthState':	'1'})
  #   auth1 = ss.post('https://www.amazon.com/ap/cvf/verify', verify = False, headers = head, data = load)

  #   if 'Anti-Automation Challenge' in auth1.text:
  #     soup = BeautifulSoup(auth1.content)
  #     load = pay_load(soup)
  #     captchaLink = soup.find('img', alt = "captcha")["src"]
  #     res = ss.get(captchaLink, verify = False).content
  #     with open('image1.jpg','wb') as img:
  #         img.write(res)
  #     files = {'file': open('image1.jpg', 'rb')}
  #     recaptcha_answer = reCaptcha(files)
  #     load.update({'cvf_captcha_input':recaptcha_answer})
  #     auth1 = ss.post('https://www.amazon.com/ap/cvf/verify', verify = False, headers = head, data = load)

  #   # Type the OTP, if sent to your registered email
  #   if "One Time Password (OTP) sent" in auth1.text:
  #     soup = BeautifulSoup(auth1.content)
  #     code = ''
  #     code = input('Enter OTP sent to your Email : ')
  #     load = {'code':code}
  #     load.update(pay_load(soup))

  #     print('Initial Action ', load['action'])
  #     load['action'] = 'code'
  #     authUrl = ss.post('https://www.amazon.com/ap/cvf/verify', verify = False, headers = head, data = load)
      
  #     if authUrl.status_code == 200:
  #         print('****************************\n\nYou are Successfully logged In\n\n*****************************')

  # # Go to the product page usin the product asin no.
  # else:
  #   raise Exception('You are unable to login via bot')

  productPage = ss.get(productUrl, verify = False, headers = head)

  soup = BeautifulSoup(productPage.content)
  # refererUrl = soup.find('div', id = 'huc-page-state')['data-url']
  addingUrl = soup.find('form', method = "post", id = "addToCart")["action"]
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
  addItemUrl = ss.post(addingUrl, verify=False, headers=head, data = cartload)

  # head.update({'Referer': refererUrl})
  soup = BeautifulSoup(addItemUrl.content)
  cartUrl = soup.find('a', id = 'hlb-ptc-btn-native')['href']
  CheckOutUrl = ss.get('https://www.amazon.com'+cartUrl, verify = False, headers = head)

  soup = BeautifulSoup(addItemUrl.content)
  soup1 = BeautifulSoup(CheckOutUrl.content)
  placeOrderUrl = soup1.find('form', id='spc-form')['action']
  orderLoad = pay_load(soup1)
  orderLoad.update({'switchCurrency':'transactional','placeYourOrder1':'1'})
  if 'ue_back' in orderLoad:
    orderLoad.pop('ue_back')
  data1 = soup.find_all('input', type='text')
  for row in data1:
    if 'name' in row:
      if row['name']=='storeZip2':
        orderLoad.update({row['name']:row['value']})
      if row['name']=='storeZip':
        orderLoad.update({row['name']:row['value']})
  for i in orderLoad:
    if 'RCX_CHECKOUT' in i:
      popKey = i
  orderLoad.pop(popKey)
  if 'primeCoOptState' in orderLoad:
    orderLoad.pop('primeCoOptState')
  data2 = soup.find('input', type='radio')
  orderLoad.update({data2['name']:data2['value']})
  if 'paymentInstrumentID' in orderLoad:
    orderLoad.pop('paymentInstrumentID')
  if 'offerToken' in orderLoad:
    orderLoad.pop('offerToken')
  orderLoad['currencyChanged'] = 'False'
  orderLoad['claimCode'] = ''
        
  # orderLoad.update(pay_load(soup))
  orderUrl = ss.post('https://www.amazon.com'+placeOrderUrl, verify = False, headers = head, data = orderLoad)
  if orderUrl.status_code==200:
    print('Your order hasbeen Successfully placed ')        
    pass

pass
amazon()