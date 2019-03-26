from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
req= Request('https://scholar.google.com/scholar?start=20&q=emnlp+2018&hl=en&as_sdt=0,5',headers={'User-Agent': 'Mozilla/5.0'})

page_html=urlopen(req).read()
page_soup=soup(page_html,"html.parser")
finders=page_soup.findAll("div",{"class" : "gs_ri"})
#print(len(finders))
#print(soup.prettify(finders[0]))
finder=finders[0]
citation=finder.findAll("div",{"class": "gs_fl"})
print(citation[0].text)
print(finder.a.text)
 
filename="prod.csv"
f=open(filename,"a")
headers="Name_of_paper,Citations \n"
f.write(headers)
for finder in finders:
    name_of_paper=finder.a.text
    no_of_citations=finder.findAll("div",{"class": "gs_fl"})
    
    citation=no_of_citations[0].text.strip() 
    
    trim_cite= citation.split(' ')
    final_cite=trim_cite[2]
    if(final_cite.isdigit()):
        print( name_of_paper+" ,"+ final_cite+"\n")
        f.write(name_of_paper+" ,"+ final_cite+"\n")
    else:
        final_cite='0'
        print( name_of_paper+" ,"+ final_cite+"\n")
        f.write(name_of_paper+" ,"+ final_cite+"\n")
f.close()