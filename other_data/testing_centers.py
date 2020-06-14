import requests
from bs4 import BeautifulSoup
import pymongo
import geocoder
from geopy.geocoders import Nominatim


# get current location
def getCity(coords):
    g = geocoder.ip('me')
    locator = Nominatim(user_agent="myGeocoder")
    #coordinates = str(g.latlng[0]) + ','  + str(g.latlng[1])
    coordinates = coords['lat'] + ','  + coords['lon']
    location = locator.reverse(coordinates)
    return location.raw['address']['city'].lower()


def run(coords):
    # Desktop user-agent
    #USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"

    # Specify user-agent
    #USER_AGENT = coords['agent']
    #print(USER_AGENT)
    #print(coords['agent'])

    if coords['agent'] == True:
        USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"
        return runMobile(coords)
    else:
        USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
        return runDesktop(coords)

    #print(USER_AGENT)


def runDesktop(coords):
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"

    headers = {"user-agent" : USER_AGENT}
    city = getCity(coords)

    # Link to Google search for nearby COVID-19 testing centers
    response = requests.get("https://www.google.com/search?q=covid+19+testing+centers" + city + "&tbm=lcl&tbs=lrf:!3sIAE,lf:1,lf_ui:16&rldoc=1", headers=headers)
    response = response.text.strip()
    soup = BeautifulSoup(response, "html.parser")

    # All data to be scraped is in divs of this class
    data = soup.find_all('div', {"class": "cXedhc"})


    results = [] # array to be returned
    i = 0
    for loc in data:
        # Get names of testing centers
        nameDivs = loc.find_all('div', {"class": "dbg0pd"})
        for div in nameDivs:
            names = div.find_all('div')[0].text.strip()
            d = dict(name=names)
            results.append(d)

        # Get details of testing centers (location, phone number)
        details = loc.find_all('div', {"class": "f5Sf1"})[0].text.strip()
        results[i]['details'] = details

        # Get appointment, referral, testing, and drive-through info, as well as instructions
        info = loc.find_all('span', {'class': "gqguwf X0w5lc"})
        if info != []:
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
    # Get links to testing center websites
    links = soup.find_all('a', {"class": "yYlJEf L48Cpd"})
    for link in links:
        results[i]['link'] = link['href']
        i += 1

    return results


def runMobile(coords):
    USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"

    headers = {"user-agent" : USER_AGENT}
    city = getCity(coords)

    # Link to Google search for nearby COVID-19 testing centers
    response = requests.get("https://www.google.com/search?q=covid+19+testing+centers+" + city + "&ie=UTF-8&oe=UTF-8&hl=en-us&dlnr=1&sei=C3bVXpPXBOSFggectJ-QDw#dlnr=1&trex=m_r:1,m_t:gwp,rc_q:covid%" + "252019%" + "2520testing%" + "2520centers%2520" + city + ",rc_ui:16,ru_gwp:8%252C6,ru_q:covid%" + "252019%" + "2520testing%" + "2520centers%2520" + city, headers=headers)
    print("https://www.google.com/search?q=covid+19+testing+centers+" + city + "&ie=UTF-8&oe=UTF-8&hl=en-us&dlnr=1&sei=C3bVXpPXBOSFggectJ-QDw#dlnr=1&trex=m_r:1,m_t:gwp,rc_q:covid%" + "252019%" + "2520testing%" + "2520centers%2520" + city + ",rc_ui:16,ru_gwp:8%252C6,ru_q:covid%" + "252019%" + "2520testing%" + "2520centers%2520" + city)
    response = response.text.strip()
    soup = BeautifulSoup(response, "html.parser")

    # All data to be scraped is in a's of this class
    data = soup.find_all('a', {"class": "bdw3Ld rl-lhs"})

    print(data)

    results = [] # array to be returned
    i = 0
    for loc in data:
        # Get names of testing centers
        nameDivs = loc.find_all('div', {"class": "kR1eme rllt__wrapped gsrt"})
        for div in nameDivs:
            names = div.find_all('div')[0].text.strip()
            d = dict(name=names)
            results.append(d)

        # Get details of testing centers (location, phone number)
        #details = loc.find_all('div', {"class": "f5Sf1"})[0].text.strip()
        #results[i]['details'] = details
        results[i]['details'] = ""

        # Get appointment, referral, testing, and drive-through info, as well as instructions
        info = loc.find_all('span', {'class': "bOxIrc cqtb4"})
        if info != []:
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
            
            '''
            if loc.find_all('div', {"class": "rxSVje rllt__wrapped"}) != []:
                instructions = loc.find_all('div', {"class": "rxSVje rllt__wrapped"})[0].text.strip()
            else:
                instructions = "Instructions:N/A"
            results[i]['instructions'] = 'Instructions: ' + instructions[instructions.index('Instructions:') + len('Instructions:'):]
            '''
            results[i]['instructions'] = ""
            results[i]['link'] = ""
            i += 1

    '''
    i = 0
    # Get links to testing center websites
    links = soup.find_all('a', {"class": "yYlJEf L48Cpd"})
    for link in links:
        results[i]['link'] = link['href']
        i += 1
    '''
    print(results)
    return results

#run()