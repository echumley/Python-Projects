from bs4 import BeautifulSoup
import requests

url = 'https://www.newegg.com/acer-kg271u-xbmiipx-27-qhd-240-hz-va-black/p/N82E16824011486?Item=N82E16824011486&cm_sp=Homepage_SS-_-P2_24-011-486-_-12272024'

results = requests.get(url)
doc = BeautifulSoup(results.text, 'html.parser')

print(doc.prettify())


'''
prices = doc.find_all(string='$')
parent = prices[0].parent
strong = parent.find('strong')
print(strong.string)
'''