import requests
from bs4 import BeautifulSoup
import pymongo
import json

import sys
sys.path.append("../")
from mongodb_info import getClient

myClient = getClient()
client = pymongo.MongoClient(myClient)
mydb = client['resource_data']
mycol = mydb['testing_centers']


def run():
    # desktop user-agent
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    headers = {"user-agent" : USER_AGENT}

    response = requests.get("https://www.google.com/search?rlz=1C5CHFA_enUS559US559&sxsrf=ALeKk02DeetRUkmRRjNC5Co7B7azzUtGRQ:1589204031549&q=covid+19+testing+centers&npsic=0&rflfq=1&rlha=0&rllag=41153517,-73314179,13078&tbm=lcl&ved=2ahUKEwjtrZqu9qvpAhU1ZDUKHZ-9A0oQjGp6BAgUED8&tbs=lrf:!3sIAE,lf:1,lf_ui:16&rldoc=1#rldoc=1&rlfi=hd:;si:,41.30159486477283,-71.626144996875;mv:[[41.8166219,-72.6467073],[41.00047730000001,-73.6158366]]",
                            headers=headers)
    response = response.text.strip()
    soup = BeautifulSoup(response, "html.parser")
    data = soup.find_all('div', {"class": "cXedhc"})


    results = []
    i = 0
    for loc in data:
        nameDivs = loc.find_all('div', {"class": "dbg0pd"})
        for div in nameDivs:
            names = div.find_all('div')[0].text.strip()
            d = dict(name=names)
            results.append(d)

        details = loc.find_all('div', {"class": "f5Sf1"})[0].text.strip()
        results[i]['details'] = details

        info = loc.find_all('span', {'class': "gqguwf X0w5lc"})
        appt = info[1].text.strip()
        ref = info[2].text.strip()
        test = info[3].text.strip()
        results[i]['appointment'] = appt
        results[i]['referral'] = ref
        results[i]['testing'] = test
        results[i]['drive_through'] = 'Not drive-through'

        if len(info) > 4:
            dt = info[4].text.strip()
            results[i]['drive_through'] = dt

        if loc.find_all('div', {"class": "rxSVje rllt__wrapped"}) != []:
            instructions = loc.find_all('div', {"class": "rxSVje rllt__wrapped"})[0].text.strip()
        else:
            instructions = "Instructions:N/A"
        results[i]['instructions'] = 'Instructions: ' + instructions[instructions.index('Instructions:') + len('Instructions:'):]

        i += 1


    i = 0
    links = soup.find_all('a', {"class": "yYlJEf L48Cpd"})
    for link in links:
        results[i]['link'] = link['href']
        i += 1

    #googleMap = soup.find_all('div', {"class": "bQUiFc"})
    #results.append(googleMap)

    return results

    #newcol = mycol.insert_many(results)
run()