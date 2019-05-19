import pandas as pd
import json
import requests
import csv
import time
from datetime import datetime
from bs4 import BeautifulSoup
import seaborn as sns
import re
import matplotlib.pyplot as plt
import random
tag = input()
url = "https://www.instagram.com/tags/"+tag+"/"
url
BURL = 'https://www.instagram.com/accounts/login/'
LURL = BURL + 'ajax/'
headers_list = [
        "Mozilla/5.0 (Windows NT 5.1; rv:41.0) Gecko/20100101"\
        " Firefox/41.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2)"\
        " AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2"\
        " Safari/601.3.9",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0)"\
        " Gecko/20100101 Firefox/15.0.1",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"\
        " (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36"\
        " Edge/12.246"
        ]
USERNAME = '**********Your_insta_Username************'
PASSWD = '**********Your_insta_password**********'
AGENT = headers_list[random.randrange(0,4)]

session = requests.Session()
session.headers = {'User-Agent': AGENT}
session.headers.update({'Referer': BURL})    
req = session.get(BURL)
soup = BeautifulSoup(req.content, 'html.parser') 
body = soup.find('body')

pattern = re.compile('window._sharedData')
script = body.find("script", text=pattern)

script = script.get_text().replace('window._sharedData = ', '')[:-1]
data = json.loads(script)

csrf = data['config'].get('csrf_token')
login_data = {'username': USERNAME, 'password': PASSWD}
session.headers.update({'X-CSRFToken': csrf})
login = session.post(LURL, data=login_data, allow_redirects=True)
session.headers={"Cookie":login.headers['Set-Cookie']}
login.content
# if True :- b'{"authenticated": true, "user": true, "userId": "*******", "oneTapPrompt": false, "status": "ok"}'
r = session.get(url)
soup = BeautifulSoup(r.text, 'lxml')
script = soup.find('script', text=lambda t: t.startswith('window._sharedData'))
page_json = script.text.split(' = ', 1)[1].rstrip(';')
data = json.loads(page_json)
total_post = data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['count']
print("\t\t\t\t\t Your Data Goes As Follows With a total post of "+str(total_post)+" \n\n\n\n\n")
for post in data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['edges']:
    image_src = post['node']['thumbnail_resources'][1]['src']
    likes = post['node']['edge_liked_by']['count']
    comment = post['node']['edge_media_to_comment']['count']
    if comment > 1:
        k = post['node']['shortcode']
        link = "https://www.instagram.com/p/"+k+"/"
        print(str(comment)+"  :   "+str(k)+"  :   "+str(link))
    t = post['node']['taken_at_timestamp']
    tex = post['node']['edge_media_to_caption']['edges'][0]['node']['text']
    tim = time.ctime(t)
    id = post['node']['owner']['id']
    print('likes : '+str(likes)+"; \t \t Comments : "+str(comment)+"; \t \t Post ID : "+str(id)+"; \t \t Timestamp : "+str(tim)+";\n Image Link : "+str(image_src)+"\n \n \t\t\t\t\t\tTEXT\n"+str(tex)+"\n\n\n")
    row = [likes, comment, id, tim, image_src ]
    with open('insta.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)
    csvFile.close()
    dataset = pd.read_csv('insta.csv')
mlik = dataset['LIKES'].max()
mlik
mim = dataset[dataset['LIKES'] == mlik]
mim
plt.figure(figsize=(19,10))
sns.countplot(x = dataset['LIKES'], data=dataset)
plt.xticks(rotation = 'horizontal')
plt.show()
print("\t\t\t\tlikes from HIGH TO LOW")
dataset.sort_values(by='LIKES', ascending=False)
u = mim['IMAGE'].max()
with open('crawldata/pic1.jpg', 'wb') as handle:
        response = session.get(u, stream=True)

        if not response.ok:
            print (response)

        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)
