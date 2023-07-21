from bs4 import BeautifulSoup

def parseCode(html):
    soup = BeautifulSoup(html, 'lxml')
    if soup.find('p', class_="ValCode"):
        return soup.find('p', class_="ValCode").text.split()[-1]
