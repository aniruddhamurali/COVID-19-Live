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

    response = requests.get("https://www.google.com/search?sa=X&rlz=1C5CHFA_enUS559US559&biw=1680&bih=870&sxsrf=ALeKk03axWVxKZgGpBr1XwC8ZbjRI5PNYg:1588735669996&q=covid+19+testing+center&npsic=0&rflfq=1&rlha=0&rllag=41153517,-73314179,13078&tbm=lcl&ved=2ahUKEwiC3YHKpZ7pAhUKg3IEHaRbC5MQjGp6BAgNEBU&tbs=lrf:!3sIAE,lf:1,lf_ui:16&rldoc=1",
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

        info = loc.find_all('span', {"class": "gqguwf X0w5lc"})
        appt = info[0].text.strip()
        ref = info[1].text.strip()
        test = info[2].text.strip()
        results[i]['appointment'] = appt
        results[i]['referral'] = ref
        results[i]['testing'] = test
        results[i]['drive_through'] = 'Not drive-through'

        if len(info) > 3:
            dt = info[3].text.strip()
            results[i]['drive_through'] = dt

        instructions = loc.find_all('div', {"class": "rxSVje rllt__wrapped"})[0].text.strip()
        results[i]['instructions'] = 'Instructions: ' + instructions[instructions.index('Instructions:') + len('Instructions:'):]

        i += 1


    i = 0
    links = soup.find_all('a', {"class": "yYlJEf L48Cpd"})
    for link in links:
        results[i]['link'] = link['href']
        i += 1

    return results

    #newcol = mycol.insert_many(results)
