# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 01:11:14 2020

@author: Sunmarg Das
"""


from bs4 import BeautifulSoup
import xlsxwriter
import xlrd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
# example option: add 'incognito' command line arg to options
option = webdriver.ChromeOptions()
#option.add_argument("--incognito")

# create new instance of chrome in incognito mode
web_driver_path=r"C:\Users\horia.clement\Downloads\chromedriver_win32\chromedriver.exe"
browser = webdriver.Chrome(executable_path=web_driver_path, chrome_options=option)
chrome_path  = web_driver_path
driver = webdriver.Chrome(chrome_path)
k=2;


#......UPTO here run only once............



#........for different excel sheets run from next onwards only......


# go to website of interest
browser.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
time.sleep(.05)
username = "jackie.lawrence2020@gmail.com"
password = "Abyabba2013"

elementID = browser.find_element_by_id('username')
elementID.send_keys(username)

elementID = browser.find_element_by_id('password')
elementID.send_keys(password)


elementID.submit()
time.sleep(1)

#give excel location
file_location=r"C:\Users\horia.clement\Desktop\scrape\UK_seriesB_7.5kcleaned.xlsx" #change excel location for different excel files
file_name="UK_seriesB_7.5kcleaned.xlsx"
workbook=xlrd.open_workbook(file_location)
sheet=workbook.sheet_by_index(0)

c=pd.read_excel(file_name)

b=c.dropna(subset=['LinkedIn'],how='any')
row_count=b.shape[0]
#create new excel file
m=6 #for 1st excel file
#......Remember to Update m for different excel sheets............"
excel_name='Data'+str(m)+'.xlsx' #remember to update m for getting values in different profiles

outWork=xlsxwriter.Workbook(excel_name)
outSheet=outWork.add_worksheet()
outSheet.write("A1","Organization");
outSheet.write("B1","Followers");
outSheet.write("C1","Employees")


timeout = 5
a=3
for a in range(0,row_count):
    value=str(c.iloc[a,1])
    browser.get(value)
    name=str(c.iloc[a,0])
    browser.maximize_window()
    browser.execute_script("document.body.style.zoom='100%'")
    elm=browser.find_element_by_tag_name('html')
    src=browser.page_source
    soup=BeautifulSoup(src,'lxml')
    try:
        
        try:
            follow_no=soup.find('div',{'class': 'org-top-card-summary__info-item org-top-card-summary__follower-count'})
            #text1=(browser.find_element_by_class_name('org-top-card-summary__info-item org-top-card-summary__follower-count'))
            text1=follow_no.get_text();
            text1=text1.strip()
            text2=text1.split(" ");
            outSheet.write("B"+str(k),text2[0])
            #except NoSuchElementException:
            #   browser.quit()
            
            outSheet.write("A"+str(k),str(name))
            
            em=soup.findAll('div',{'class':'mt2'})    
            
            try:
                employee_no=em[0].find('span',{'class':'v-align-middle'})
                text3=employee_no.get_text();
                text4=text3.split(" ");
                if text4[2]=='employee':
                    outSheet.write("C"+str(k),text4[1])
                else:
                    outSheet.write("C"+str(k),text4[2])
                k=k+1;
                
            except IndexError or AttributeError:
                employee_no=em[1].find('span',{'class':'v-align-middle'})
                text3=employee_no.get_text();
                text4=text3.split(" ");
                if text4[2]=='employee':
                    outSheet.write("C"+str(k),text4[1])
                else:
                    outSheet.write("C"+str(k),text4[2])
                k=k+1;
                
        except AttributeError:
            k=k+1;
            
    except IndexError:
        k=k+1
    
outWork.close()
browser.quit()








