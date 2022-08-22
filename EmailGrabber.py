import requests,re
from urllib.parse import urlparse
from bs4 import BeautifulSoup as bs

def getFbEmail(link, s=''):
        if '//' == link[:2]:
            url = link[2:]
        elif 'http://' not in link[:10] and 'https://' not in link[:10]:
            url = 'https://'+link
        else:
            url = link
        Link = urlparse(url)
        email = getEmail("https://web.facebook.com/{user}/about".format(user=Link.path.split('/')[1].split('?')[0]), search=s)
        if email:
            return email.split('?')[0]
        else:
            return ''
        

def getEmail(link, fb='', search=''):
    if 'http://' not in link[:10].lower() and 'https://' not in link[:10].lower():
        link = 'http://'+link
        
    a = urlparse(link)
    aFb = ''
    cPage = ''
    ses = requests.Session()
    co = {}
    if search in ['fb', 'aFb']:
        Url = link
    else:
        Url ="{s}://{d}".format(s=a.scheme,d=a.netloc)
    r = ses.get(Url, headers={'User-Agent': 'Chrome'})
    if search == 'fb':
        with open('test.html', 'w', encoding='utf-8') as file:
            file.write(r.text)
    soup = bs(r.content, 'lxml')
    body = soup.find('body')
    [s.extract() for s in body.find_all('script')]
    links = body.find_all('a')
    contactPage = ''

    for link in links:
        try:
            url = link.attrs['href'].lower()
            if 'mailto' in url:
                return url.split(':')[1]
            elif '@' in link.get_text():
                match = re.findall(r'[\w\.-]+@[\w\.-]+', link.get_text())
                if match:
                    return match
            elif 'contact' in url and not search=='fb' and not search == 'contact':
                cPage = url 
            elif 'facebook' in url or 'fb' in url:
                aFb = url.split(':')[1]                    
        except:
            pass

    text = body.get_text()
    match = re.findall(r'[\w\.-]+@[\w\.-]+', text)
    if match:
        return match
    try:
        if '/' in cPage[0] and not search:
            print("\t[=] Visiting Contact Page")
            email = getEmail(link+'/'+cPage, search='contact')
            if len(email) > 4:
                return email
        elif ('http://' in cPage[:10] or 'https://' in cPage[:10]) and not search:
            print("\t[=] Visiting Contact Page")
            email = getEmail(cPage, search='contact')
            if len(email) > 4:
                return email
    except:
        pass
    if fb and not search:
        print("\t[=] Visiting Facebook Page")
        email = getFbEmail(fb, 'fb')
        if len(email) > 4:
            return email
        else:
            return 'NULL'
    elif aFb and not search:
        print("\t[=] Visiting Facebook Page")
        email = getFbEmail(aFb,'aFb')
        if len(email) > 4:
            return email
        else:
            return 'NULL'

    return 'NULL'


# EXAMPLES
print(getEmail('https://www.muhaddis.info/'))
# EXAMPLE2
print(getEmail('https://www.muhaddis.info/','https://web.facebook.com/MuhaddiMu'))
# EXAMPLE3
print(getEmail('https://web.facebook.com/MuhaddiMu/about', search='fb'))


# OUTPUTS
# ask@muhaddis.info -> Example 1
# ask@muhaddis.info -> Example 2
# NULL -> Example 3 (Email is Publicely not available)
