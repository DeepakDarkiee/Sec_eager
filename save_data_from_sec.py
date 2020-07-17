# https://towardsdatascience.com/automate-your-python-scripts-with-task-scheduler-661d0a40b279
import sqlite3
import datetime
from datetime import date #today = date.today()
import requests
from bs4 import BeautifulSoup
import urllib
import time
import pandas as pd 

conn =""
db = sqlite3.connect('sec_db.db')
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS sec_data(nameOfIssuer TEXT, entry_date DATE, titleOfClass TEXT, symbol TEXT, value TEXT, sshPrnamt TEXT, sshPrnamtType TEXT, investmentDiscretion TEXT, otherManager TEXT, VA_Sole TEXT, VA_Shared TEXT, VA_None TEXT)")
db.commit()
if __name__ == "__main__":
    print("Starting Scheduler .....")
    while 1:
        print("")
        print("    ########## Scraping ##########")
        conn = sqlite3.connect('sec_db.db')
        cursor = conn.cursor()
        link = "https://www.sec.gov/cgi-bin/browse-edgar?company=&CIK=&type=13f&owner=include&count=40&action=getcurrent"
        error_link = [] #Link from which we get error
         
        try:
            page = urllib.request.urlopen(link)
            src = BeautifulSoup(page,'html.parser')
            link = (src.find_all("a"))
            links = []
            l = []
            for a in link:
                if (a.get('href')).find('.txt') != -1 :#Check for text file
    	            text_data_url = "https://www.sec.gov"+str(a['href'])
    	            # print(text_data_url)    
    	            l.append(text_data_url)
        except Exception as e:
            print(e)
               
        # symbol_data = pd.read_csv("symbol_list.csv", index_col ="c_name") 
        for a in l:     
            try:
                r = requests.get(a)
                my_json = r.content.decode('utf8')

                soup = BeautifulSoup(my_json, 'xml')
                titles = soup.find_all('infoTable')
                # titles = soup.find('informationTable').find_all("infoTable")
                # print(titles)
                for x in titles:
                    name_Of_Issuer = (str(x.find('nameOfIssuer').text))
                    try: #scraping symbol name
                        query = name_Of_Issuer + " symbol name"
                        query = query.replace(' ', '+')
                        query = query.replace('CHEMS', 'Chemicals')
                        query = query.replace('Co', 'Company')
                        URL = f"https://google.com/search?q={query}"
                        # desktop user-agent
                        USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
                        headers = {"user-agent" : USER_AGENT}
                        resp = requests.get(URL, headers=headers)
                        if resp.status_code == 200:
                            soup = BeautifulSoup(resp.content, "html.parser")
                            sy_name = soup.find("div", {"class": "HfMth"})
                            symbol = (sy_name.text).split(" ")[1] 
                            if not (sy_name is None):
                                sy_name = (sy_name.text).split(" ")[1]
                            if (sy_name is None):
                                sy_name = soup.find("tr", {"class": "ztXv9"})
                                sy_name = (sy_name.find_all("th"))
                                if not (sy_name is None):
                                    sy_name = (sy_name[1].text)
                            if (sy_name is None):
                                sy_name = soup.find("tr", {"class": "ztXv9"})
                                sy_name = (sy_name.find_all("td"))
                                if not (sy_name is None):
                                    sy_name = (sy_name[1].text)
                        symbol = sy_name
                    except Exception as e:
                        symbol = "####"

                    finally:
                        print("{0}   |   {1}".format(name_Of_Issuer,symbol))
                        title_Of_Class = (str(x.find('titleOfClass').text))
                        value = (str(x.find('value').text))
                        ssh_Prnamt = (str(x.find('shrsOrPrnAmt').findChildren('sshPrnamt')[0].text))
                        ssh_Prnamt_Type = (str(x.find('shrsOrPrnAmt').findChildren('sshPrnamtType')[0].text))
                        investment_Discretion = (str(x.find('investmentDiscretion').text))
                        if x.find('otherManager'):
                            otherManager = (str(x.find('otherManager').text))
                        else:
                            otherManager = "None"
                        VA_Sole = (str(x.find('votingAuthority').findChildren("Sole")[0].text))
                        VA_Shared = (str(x.find('votingAuthority').findChildren("Shared")[0].text))
                        VA_None = (str(x.find('votingAuthority').findChildren("None")[0].text))
                        with conn:
                            cursor = conn.cursor()
                            cursor.execute('INSERT OR IGNORE INTO  sec_data(nameOfIssuer ,entry_date , titleOfClass, symbol , value , sshPrnamt , sshPrnamtType , investmentDiscretion , otherManager , VA_Sole , VA_Shared , VA_None) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',(name_Of_Issuer,date.today(), title_Of_Class, symbol, value, ssh_Prnamt, ssh_Prnamt_Type, investment_Discretion, otherManager, VA_Sole, VA_Shared, VA_None))
                    conn.commit()
            except Exception as e:
                    print("!!!!!!!!!!!!!!!!!! Exception Occured !!!!!!!!!!!!!!!!")
                    error_link.append(a)
                    print("Exception: "+str(e))
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("   --------Process Completed-------- ")
        break
        # time.sleep(600) #10-min
        print("")
        print("Waiting for 10-Min....")
