# https://towardsdatascience.com/automate-your-python-scripts-with-task-scheduler-661d0a40b279
import sqlite3
import datetime
from datetime import date  # today = date.today()
import requests
from bs4 import BeautifulSoup
import urllib
import time
import pandas as pd
from scrape import lst
import json
json_format = json.dumps(lst)
print(type(json_format))

conn = ""
db = sqlite3.connect('sec_db.db')
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS sec_data(nameOfIssuer TEXT, entry_date DATE, titleOfClass TEXT, symbol TEXT, value TEXT, sshPrnamt TEXT, sshPrnamtType TEXT, investmentDiscretion TEXT, otherManager TEXT, VA_Sole TEXT, VA_Shared TEXT, VA_None TEXT)")
db.commit()
if __name__ == "__main__":
    print("Starting Scheduler .....")
    while 1:
        print("")
        print("    ########## Scrapping ##########")
        conn = sqlite3.connect('sec_db.db')
        cursor = conn.cursor()
        link = "https://www.sec.gov/cgi-bin/browse-edgar?company=&CIK=&type=13f&owner=include&count=40&action=getcurrent"
        error_link = []  # Link from which we get error

        try:
            page = urllib.request.urlopen(link)
            src = BeautifulSoup(page, 'html.parser')
            link = (src.find_all("a"))
            links = []
            l = []
            for a in link:
                if (a.get('href')).find('.txt') != -1:  # Check for text file
    	            text_data_url = "https://www.sec.gov"+str(a['href'])
    	            # print(text_data_url)
    	            l.append(text_data_url)
        except Exception as e:
            print(e)

        # symbol_data = pd.read_csv("symbol_list.csv", index_col ="c_name")
        for a in l:
            print("")
            print("Scrapping: "+str(a))
            print("|     Company Name        |    Symbol Name    |")
            try:
                r = requests.get(a)
                my_json = r.content.decode('utf8')

                soup = BeautifulSoup(my_json, 'xml')
                titles = soup.find_all('infoTable')
                for x in titles:
                    name_Of_Issuer = (str(x.find('nameOfIssuer').text))
                    cusip_val = (str(x.find('cusip').text))

                    # print(cusip_val)
                    try:
                        sy_name = "None"
                        parameters = {
                            'tickersymbol': cusip_val, 'sopt': 'cusip'}
                        r = requests.post(
                            'https://www.quantumonline.com/search.cfm', data=parameters)
                        so = BeautifulSoup(r.content, "html.parser")
                        so = so.find_all("b")
                        for i in so:
                            if "Ticker Symbol" in i.text:
                                sy_name = (i.text).split(" ")[2]
                        symbol = sy_name
                        
                        from csv import writer
                        def append_list_as_row(file_name, list_of_elem):
                                # Open file in append mode
                                with open(file_name, 'a+', newline='') as write_obj:
                                # Create a writer object from csv module
                                    csv_writer = writer(write_obj)
                                # Add contents of list as last row in the csv file
                                    csv_writer.writerow(list_of_elem)
                            # List of strings
                        row_contents = [name_Of_Issuer,symbol]
                            # Append a list as new line to an old csv file
                        append_list_as_row('symbole.csv', row_contents)
                    except Exception as e:
                        print("Internet connection Error: 'Could not Scrap symbol'")
                        symbol = "####"
                        

                    finally:
                        print("|  {0}          |   {1}  |".format(
                            name_Of_Issuer, symbol))
                        title_Of_Class = (str(x.find('titleOfClass').text))
                        value = (str(x.find('value').text))
                        ssh_Prnamt = (
                            str(x.find('shrsOrPrnAmt').findChildren('sshPrnamt')[0].text))
                        ssh_Prnamt_Type = (
                            str(x.find('shrsOrPrnAmt').findChildren('sshPrnamtType')[0].text))
                        investment_Discretion = (
                            str(x.find('investmentDiscretion').text))
                        if x.find('otherManager'):
                            otherManager = (str(x.find('otherManager').text))
                        else:
                            otherManager = "None"
                        VA_Sole = (
                            str(x.find('votingAuthority').findChildren("Sole")[0].text))
                        VA_Shared = (
                            str(x.find('votingAuthority').findChildren("Shared")[0].text))
                        VA_None = (
                            str(x.find('votingAuthority').findChildren("None")[0].text))
                        with conn:
                            cursor = conn.cursor()
                            cursor.execute('INSERT OR IGNORE INTO  sec_data(nameOfIssuer ,entry_date , titleOfClass, symbol , value , sshPrnamt , sshPrnamtType , investmentDiscretion , otherManager , VA_Sole , VA_Shared , VA_None) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)', (
                                name_Of_Issuer, date.today(), title_Of_Class, symbol, value, ssh_Prnamt, ssh_Prnamt_Type, investment_Discretion, otherManager, VA_Sole, VA_Shared, VA_None))
                    conn.commit()
            except Exception as e:
                    print("!!!!!!!!!!!!!!!!!! Exception Occured !!!!!!!!!!!!!!!!")
                    error_link.append(a)
                    print("Exception: "+str(e))
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("   --------Process Completed-------- ")
        print("We have Scrapped Sec Edger data till now.")
        print("")
        print("")
        print("Run it Again to scrap data. Scrapper will terminate soon.")
        time.sleep(600) #10-min
        break
        # print("Waiting for 10-Min....")
