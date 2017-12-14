#Modified
#https://stackoverflow.com/questions/46718043/getting-live-yahoo-finance-data-in-python# import libraries
import requests
from bs4 import BeautifulSoup
import urllib3 as url
import certifi as cert




def scraping(data):
    # specify the url
    http = url.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=cert.where())
    html_doc = http.request('GET', 'https://finance.yahoo.com/quote/%s?p=%s' % (data.index, data.index))
    soup = BeautifulSoup(html_doc.data, 'html.parser')
    # listTags = soup.find_all('span', attrs= {"class" :"Trsdu(0.3s)"})
    # for tag in listTags:
    #       print(str(tag))
    #       if "<!-- react-text: 48 -->" in str(tag):
    #           price = find_between(tag,"<!-- react-text: 48 -->","<!-- /react-text -->" )
    #           print("price",price)
    price = soup.find("span", class_="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)").get_text()
    close = soup.find('span',  class_= 'Trsdu(0.3s) ').get_text()
    data.current = price
    data.close = close


