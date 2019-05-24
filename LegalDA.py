from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from selenium.common.exceptions import NoSuchElementException
# example option: add 'incognito' command line arg to options
option = webdriver.ChromeOptions()
option.add_argument("--incognito")

# create new instance of chrome in incognito mode
browser = webdriver.Chrome(executable_path=r'C:/Users/Sunmarg Das/Downloads/chromedriver_win32/chromedriver.exe', chrome_options=option)
chrome_path  = r"C:/Users/Sunmarg Das/Downloads/chromedriver_win32/chromedriver.exe"
driver = webdriver.Chrome(chrome_path)
# go to website of interest
browser.get("https://njdg.ecourts.gov.in/njdgnew/index.php")
timeout = 15
try:
    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='report_body']/tr[27]/td[4]")))
except TimeoutException:
    print("Timed out waiting for page to load")
    browser.quit()
browser.maximize_window()
print("  STAGE WISE CRIMINAL CASES  ")

for i in range(16,20):
    titles_element = browser.find_elements_by_xpath("//*[@id='report_body']/tr["+str(i)+"]/td[1]")
    values_element = browser.find_elements_by_xpath("//*[@id='report_body']/tr["+str(i)+"]/td[3]/a")
    values = [x.text for x in values_element]
    titles = []
    i=i+1;
    for x in titles_element:
        titles.append(x.text)
    for title, value in zip(titles, values):
        print(title + ' : ' + value)

for k in range(16,20):
    try:
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='report_body']/tr["+str(k)+"]/td[3]")))
    except TimeoutException:
        print("Timed out waiting for page to load")
        browser.quit()
    browser.find_element_by_xpath("//*[@id='report_body']/tr["+str(k)+"]/td[3]/a").click()
    time.sleep(5)
    row_count1 = len(browser.find_elements_by_xpath("//*[@id='caseDetails_report_body']/tr"))
    
    
    for j in range(1,row_count1+1):
        titles_element = browser.find_elements_by_xpath("//*[@id='caseDetails_report_body']/tr["+str(j)+"]/td[1]")
        values_element = browser.find_elements_by_xpath("//*[@id='caseDetails_report_body']/tr["+str(j)+"]/td[2]/a")
        values = [x.text for x in values_element]
        titles = []
        j=j+1
        for k in titles_element:
            titles.append(k.text)
        for title, value in zip(titles, values):
            print(title + ' : ' + value)
    
    
    for m in range(1,row_count1+1):      
        
        try:
            WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='caseDetails_report_body']/tr["+str(m)+"]/td[2]/a")))
        except TimeoutException:
            print("Timed out waiting for page to load")
            browser.quit()
        time.sleep(3)
        browser.find_element_by_xpath("//*[@id='caseDetails_report_body']/tr["+str(m)+"]/td[2]/a").click()
        time.sleep(5)
        row_count2 = len(browser.find_elements_by_xpath("//*[@id='stateWise_caseDetails_report_body']/tr"))
        time.sleep(3)
        
        for i in range(1,row_count2+1):
            titles_element = browser.find_elements_by_xpath("//*[@id='stateWise_caseDetails_report_body']/tr["+str(i)+"]/td[1]")
            values_element = browser.find_elements_by_xpath("//*[@id='stateWise_caseDetails_report_body']/tr["+str(i)+"]/td[2]/a")
            values = [x.text for x in values_element]
            titles = []
            for x in titles_element:
                titles.append(x.text)
            for title, value in zip(titles, values):
                print(title + ' : ' + value)
        
       
            
            
            
        for n in range(1,row_count2+1):
            
            try:
                WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='stateWise_caseDetails_report_body']/tr["+str(n)+"]/td[2]/a")))
            except TimeoutException:
                print("Timed out waiting for page to load")
                browser.quit()
            time.sleep(2)
            browser.find_element_by_xpath("//*[@id='stateWise_caseDetails_report_body']/tr["+str(n)+"]/td[2]/a").click()
            time.sleep(2)       
            row_count3 = len(browser.find_elements_by_xpath("//*[@id='distWise_caseDetails_report_body']/tr"))
            time.sleep(2)
            
            
            for i in range(1,row_count3+1):
                    titles_element = browser.find_elements_by_xpath("//*[@id='distWise_caseDetails_report_body']/tr["+str(i)+"]/td[1]")
                    values_element = browser.find_elements_by_xpath("//*[@id='distWise_caseDetails_report_body']/tr["+str(i)+"]/td[2]/a")
                    values = [x.text for x in values_element]
                    titles = []
                    for x in titles_element:
                        titles.append(x.text)
                    for title, value in zip(titles, values):
                        print(title + ' : ' + value)
            
            for n in range(1,row_count3+1):
                 
                try:
                    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='distWise_caseDetails_report_body']/tr["+str(n)+"]/td[2]/a")))
                except TimeoutException:
                    print("Timed out waiting for page to load")
                    browser.quit()
                time.sleep(2)
                browser.find_element_by_xpath("//*[@id='distWise_caseDetails_report_body']/tr["+str(n)+"]/td[2]/a").click()
            
                time.sleep(2)            
                row_count4 = len(browser.find_elements_by_xpath("//*[@id='estCodeWise_caseDetails_report_body']/tr"))
      
                for i in range(1,row_count4+1):
                            titles_element = browser.find_elements_by_xpath("//*[@id='estCodeWise_caseDetails_report_body']/tr["+str(i)+"]/td[1]")
                            values_element = browser.find_elements_by_xpath("//*[@id='estCodeWise_caseDetails_report_body']/tr["+str(i)+"]/td[2]/a")
                            values = [x.text for x in values_element]
                            titles = []
                            for x in titles_element:
                                titles.append(x.text)
                            for title, value in zip(titles, values):
                                print(title + ' : ' + value)
                
                for n in range(1,row_count4+1):
                 
                    try:
                        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='estCodeWise_caseDetails_report_body']/tr["+str(n)+"]/td[2]/a")))
                    except TimeoutException:
                        print("Timed out waiting for page to load")
                        browser.quit()
                    time.sleep(2)
                    browser.find_element_by_xpath("//*[@id='estCodeWise_caseDetails_report_body']/tr["+str(n)+"]/td[2]/a").click()
            
                    time.sleep(2)
                    row_count5 = len(browser.find_elements_by_xpath("//*[@id='regYearWise_caseDetails_report_body']/tr"))
                    
                    for i in range(1,row_count5+1):
                            titles_element = browser.find_elements_by_xpath("//*[@id='regYearWise_caseDetails_report_body']/tr["+str(i)+"]/td[1]")
                            values_element = browser.find_elements_by_xpath("//*[@id='regYearWise_caseDetails_report_body']/tr["+str(i)+"]/td[2]/a")
                            values = [x.text for x in values_element]
                            titles = []
                            for x in titles_element:
                                titles.append(x.text)
                            for title, value in zip(titles, values):
                                print(title + ' : ' + value)
                    for n in range(1,row_count5+1): 
                        try:
                             WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='regYearWise_caseDetails_report_body']/tr["+str(n)+"]/td[2]/a")))
                        except TimeoutException:
                             print("Timed out waiting for page to load")
                             browser.quit()
                        time.sleep(2)
                        browser.find_element_by_xpath("//*[@id='regYearWise_caseDetails_report_body']/tr["+str(n)+"]/td[2]/a").click()
                        
                        time.sleep(2)
                        row_count6 = len(browser.find_elements_by_xpath("//*[@id='regnoWise_caseDetails_report_body']/tr"))
                    
                        for i in range(1,row_count6+1):
                                titles_element = browser.find_elements_by_xpath("//*[@id='regnoWise_caseDetails_report_body']/tr["+str(i)+"]/td/a")
                                values_element = browser.find_elements_by_xpath("//*[@id='regnoWise_caseDetails_report_body']/tr["+str(i)+"]/td/a")
                                values = [x.text for x in values_element]
                                titles = []
                                for x in titles_element:
                                    titles.append(x.text)
                                for title, value in zip(titles, values):
                                    print(title)
                    
                        try:
                             WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='regno_Wise_caseDetails_tab']/a")))
                        except TimeoutException:
                            print("Timed out waiting for page to load")
                            browser.quit()
                        browser.find_element_by_xpath("//*[@id='regno_Wise_caseDetails_tab']/a").click()
                    try:
                        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='regYearWise_caseDetails_tab']/a")))
                    except TimeoutException:
                        print("Timed out waiting for page to load")
                        browser.quit()
                    browser.find_element_by_xpath("//*[@id='regYearWise_caseDetails_tab']/a").click()  
                
                
                
                try:
                    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='estCodeWise_caseDetails_tab']/a")))
                    
                except TimeoutException:
                    print("Timed out waiting for page to load")
                    browser.quit()
                time.sleep(5)
                browser.find_element_by_xpath("//*[@id='estCodeWise_caseDetails_tab']/a").click()        
                        
               
            try:
                WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='distWise_caseDetails_tab']/a")))
            except TimeoutException:
                print("Timed out waiting for page to load")
                browser.quit()
            time.sleep(5)   
            browser.find_element_by_xpath("//*[@id='distWise_caseDetails_tab']/a").click()
       
        try:
            WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='stateWise_caseDetails_tab']/a")))
        except TimeoutException:
            print("Timed out waiting for page to load")
            browser.quit()
        browser.find_element_by_xpath("//*[@id='stateWise_caseDetails_tab']/a").click()
    
    
    try:
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='caseDetails_tab']/a")))
    except TimeoutException:
        print("Timed out waiting for page to load")
        browser.quit()
    browser.find_element_by_xpath("//*[@id='caseDetails_tab']/a").click()
               