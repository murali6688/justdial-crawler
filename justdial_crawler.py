
# coding: utf-8

# In[1]:

from bs4 import BeautifulSoup


# In[2]:

import requests
import urllib2
import json
import re
import pandas as pd
import os
import glob


# In[ ]:




# In[3]:

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Cookie': "ppc=; f5avrbbbbbbbbbbbbbbbb=BEAHLKGHFBDHHKCCFLLKHJBHOEAKEGBKFEDIFHLDKEODPINMKHDCAEHOEJIAJMELLNNADKMOGBOOLAABMKIBMEPDCMAGCCBNEDJJKENJICOHLLDNJEPJIHHAAPLKLACI; AKA_A2=; f5avrbbbbbbbbbbbbbbbb=ADDHBHEHDOONJJLEPHKPNFFCMKHKKBNCEOFFIBOAKEIDMGEJLMCNIOFHHHOAFALGGFFEEMGFJCKCMFGAPJGGDOCECOMNPKPLELFMMDMKICOEICBCHBIPPOGEFFFLFBNM; ppc=; _ga=GA1.2.1691653454.1497519660; _gid=GA1.2.91078670.1497519660; inweb_city=Bangalore; PHPSESSID=ffbainch6v62t3jlecn3sf46d3; profbd=0; www=3356338368.20480.0000; main_city=Bangalore; bdcheck=1; tab=toprs; BDprofile=1; bd_inputs=2|4|Plumbers; view=lst_v; scity=Bangalore; sarea=; dealBackCity=Bangalore; prevcatid=10378025",
    'Host': 'www.justdial.com',
    'Referer': 'https://www.justdial.com/Bangalore/plumbers',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
    'X-Requested-With': 'XMLHttpRequest'
}


# In[4]:

def get_store_name(container):
    try:
        store_name = container.find('h4', {'class': 'store-name'}).text
        return store_name
    except:
        return None


# In[5]:

def get_href(container):
    try:
        href = container.find('h4', {'class': 'store-name'}).a['href']
        return href
    except:
        return None
    


# In[6]:

def get_rating(container):
    try:
        stars = container.find('span',{'class': 'star_m'})
        rating = 0
        for star in stars:
            star = star['class'][0]
            rating += int(re.search(r'\d+', star).group())
        return rating
    except:
        return 0


# In[7]:

def get_votes(container):
    try:
        votes = container.find('span', {'class': 'rt_count'}).text
        votes = int(re.search(r'\d+', votes).group())
        return votes
    except:
        return 0


# In[8]:

def get_contact(container):
    try:
        phone = container.find('p', {'class': 'contact-info'}).text
        return phone
    except:
        return None
    


# In[9]:

def get_addres(container):
    try:
        more_info = container.find('span', {'class': 'mrehover'}).text.strip()
        return more_info
    except:
        return None
    


# In[10]:

def get_otherCats(container):
    try:
        cats = container.find('span', {'class': 'addrinftxt'}).findAll('a')
        cats = ','.join([cat['href'].split('/')[-2] for cat in cats[:-1]])
        return cats
    except:
        return None


# In[11]:

def get_next_page(soup):
    try:
        url = soup.find('a', {'rel': 'next'})['href']
        return url
    except:
        return None


# In[12]:

def get_containers(soup):
    containers = [list for list in soup.findAll('li', {'class':'cntanr'})]
    return containers
    


# In[13]:

def get_soup(url):
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        return soup
    except:
        return None


# In[14]:

def get_start_url(listing):
    url = listing + '/' + city.capitalize() + '/' + category.capitalize() + '-in-' + locality.capitalize()
    return url

def remove_whitespace( x ):
    if isinstance( x, basestring ):
        return x.strip()
    else:
        return x


# In[21]:

if __name__=='__main__':
    listing = 'https://www.justdial.com'
    city = raw_input('City: ')
    category = raw_input('Category: ')
    locality = raw_input('Locality: ')
    search_url = get_start_url(listing)
    df = pd.DataFrame(columns=['Category', 'Store Name', 'Url', 'Rating', 'votes', 'contact', 'address', 'all_cats'])
    while search_url:
        soup = get_soup(search_url)
        if(soup):
            containers = get_containers(soup)
            for container in containers:
                Category = category
                store_name = get_store_name(container)
                url = get_href(container)
                rating = get_rating(container)
                votes = get_votes(container)
                contact = get_contact(container)
                address = get_addres(container)
                all_cats = get_otherCats(container)
                df.loc[len(df)] = [Category, store_name, url, rating, votes, contact, address, all_cats]
            search_url = get_next_page(soup)
    file_name = category + '-' + locality + '.xlsx'
    df = df.applymap(remove_whitespace)
    df.to_excel(file_name, index=False)
    