import requests
from bs4 import BeautifulSoup
import pandas as pd
import time 

with open('ny_times_email.txt', 'r', encoding = 'utf8') as file:
        html_content = file.read()

soup = BeautifulSoup(html_content, 'lxml')

alist = soup.find('body').find_all('a')
h = []
values = ['google','http']
for link in alist:
    if link.get('href') == None or \
        link.get('href') == '#inbox' or link.get('href') == '':
        continue
    if values[0] not in link.get('href') and values[1] in link.get('href'):
        h.append(link.get('href'))
    
api = "https://www.virustotal.com/api/v3/urls"
rows = []



for i in h:
    payload = {"url": i}
    headers = {
        "accept": "application/json",
        "x-apikey": "e12014e04e5b1b6bc2aa4d65fb9639804657a2f9a4c04887678f520569ad7e55",
        "content-type": "application/x-www-form-urlencoded"
    }
    
    response = requests.post(api, data=payload, headers=headers)
    
    status = response.status_code
    
    if status == 200:
        
        print('\n' + i)
        
        print("\nWebsite has been accessed successfully")
    
        id = response.json()['data']['id']
        
        url_2 = "https://www.virustotal.com/api/v3/analyses/" + id
        
        response_2 = requests.get(url_2, headers=headers)
        
        if response_2.json()['data']['attributes']['stats']['malicious'] > 0:
            print("Alert: Website has been reported as being malicious.")
            
        elif response_2.json()['data']['attributes']['stats']['suspicious'] > 0:
            print("Alert: Website had been reported as being suspicous.")
        
        elif response_2.json()['data']['attributes']['stats']['harmless'] > 30:
            print(f"Note: Website has been reported as harmless {response_2.json()['data']['attributes']['stats']['harmless']} times and should be safe.")
            
        elif response_2.json()['data']['attributes']['stats']['malicious'] + \
                 response_2.json()['data']['attributes']['stats']['suspicious'] + \
                 response_2.json()['data']['attributes']['stats']['harmless'] == 0:
            print("Alert: The software did not return any detections.")
            
        else:
            print("Alert: Something went wrong.")
        
        rows.append({'url': i} | response_2.json()['data']['attributes']['stats'])
        time.sleep(16)
        
    
    else:
        print('Website error')
        
    
    
scans = pd.DataFrame.from_dict(rows, orient='columns')