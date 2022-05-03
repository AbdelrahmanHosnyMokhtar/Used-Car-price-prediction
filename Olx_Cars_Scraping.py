# packages that we will work with 
from datetime import time
import time
from bs4 import BeautifulSoup
from bs4.dammit import encoding_res
import pandas as pd
import numpy as np
import csv
from pandas.core.frame import DataFrame 
from tqdm import tqdm 
from itertools import zip_longest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

#Columns lists
Car_name = []
Engine_Capacity= []
Location = []
Date_time = []
Car_Model =[]
Transmission_type = []
Fuel_type = []
Price = []
Color = []
Model_year = []
Kilometer = []
Description = []
Payment_option = []
Condition = []
Body_type = []
Ad_type = []
Extra_Feature = []
Phone = []
Owner_name = []
view = []
pages =[]
links = []
all_links = []
page_num = 70

#function for getting every element 
def get_element(list_of_element,Pa):
   try:
      lists = driver.find_element_by_xpath(Pa)
      list_of_element.append(lists.text.strip())
   except:
      list_of_element.append(np.NaN)
   return list_of_element  

#opening a connection
driver = webdriver.Chrome(executable_path="C:/Users/user/Desktop/chromedriver")

driver.get('https://www.olx.com.eg/en/account/')

#getting my username and password from a hidden file
file = open('config.txt')
lines = file.readlines()
phone = lines[0][:-1]
password = lines[1]

#logging into my account
elementID = driver.find_element_by_id("userEmail")
elementID.send_keys(phone)

elementID = driver.find_element_by_id("userPass")
elementID.send_keys(password)

elementID.submit()

#looping the ain page to get the links and the dates
while True:
    url =f'https://www.olx.com.eg/en/vehicles/cars-for-sale/daewoo/?page={page_num}'
    driver.get(url)
    src = driver.page_source
    #create soup object to parse content
    soup = BeautifulSoup(src, "lxml")
    links = driver.find_elements_by_class_name("ads__item__ad--title")
    Dates = driver.find_elements_by_class_name('ads__item__date')
    Dat = (dat.text.strip() for dat in Dates)
    pages = ([link.get_attribute('href') for link in links])
    for link in pages:
        all_links.append(link)
    for date in Dat:    
        Date_time.append(date)
    page_num+=1
    if page_num > 70:
        break

     
for link in tqdm(all_links):
     driver.get(link)
     src = driver.page_source
    #create soup object to parse content
     soup = BeautifulSoup(src, "lxml")
     time.sleep(3)
     fields = ['Model','Year','Engine Capacity (CC)','Payment Options','Condition','Color',
     'Body Type','Kilometers','Transmission Type','Fuel Type','Ad Type','Extra Features']
     fielddata = {}

     names = soup.find_all('td', attrs={'class' : 'col'})
     for name in names:
         cat = name.find('th').text.strip()
         catval = name.find('td').text.strip()
         fielddata[cat] = catval
     
     for f in fields:
            if f not in fielddata:
                fielddata[f] = np.NAN

     Car_Model.append(fielddata['Model'])
     Color.append(fielddata['Color'])
     Model_year.append(fielddata['Year'])
     Engine_Capacity.append(fielddata['Engine Capacity (CC)'])
     Payment_option.append(fielddata['Payment Options'])
     Condition.append(fielddata['Condition'])
     Body_type.append(fielddata['Body Type'])
     Kilometer.append(fielddata['Kilometers'])
     Transmission_type.append(fielddata['Transmission Type'])
     Fuel_type.append(fielddata['Fuel Type'])
     Ad_type.append(fielddata['Ad Type'])
     Extra_Feature.append(str(fielddata['Extra Features']).replace('\t','').replace('\n\n',','))
     
     get_element(Car_name,'/html/body/div[4]/section/div/div/div[2]/div[1]/div[1]/div[1]/h1') 
     get_element(Location,'/html/body/div[4]/section/div/div/div[2]/div[1]/div[1]/div[1]/p/span/span[2]/strong') 
     get_element(Price,'/html/body/div[4]/section/div/div/div[2]/div[2]/div[1]/div[1]/div[1]/strong') 
     get_element(Description,'/html/body/div[4]/section/div/div/div[2]/div[1]/div[1]/div[2]/div[3]/div/p')
     get_element(view,'//*[@id="offerbottombar"]/div[3]/strong')   
     get_element(Owner_name,'//*[@id="offeractions"]/div[1]/div[3]/div[2]/p[1]')       

   #  try:
   #     driver.find_element_by_xpath("//*[@id='ad-phone']/div/span").click()
   #     time.sleep(3)
   #     Phones =  driver.find_element_by_xpath('//*[@id="ad-phone"]/div/strong')
   #     Phone.append(Phones.text.strip())
   #  except:
   #    Phone.append(np.NaN)
    
print(len(Car_name),len(Location),len(Date_time),len(Car_Model),len(Model_year),
len(Transmission_type),len(Color),len(Fuel_type),len(Price),len(Engine_Capacity),len(Kilometer),len(Description),len(Payment_option),len(Condition)
,len(Body_type),len(Ad_type),len(Phone),len(Extra_Feature),len(Owner_name))

driver.quit()

data0  = {"Title":Car_name,"Car Brand":"Daewoo","Location":Location,"Posted Date":Date_time}
data1  = {"Ad Description":Description}
data2  = {"Model":Car_Model}
data3  = {"Year":Model_year}
data4  = {"Payment Options":Payment_option}
data5  = {"Engine Capacity (CC)":Engine_Capacity}
data6  = {"Fuel Type":Fuel_type}
data7  = {"Transmission Type":Transmission_type}
data8  = {"Kilometers":Kilometer}
data9  = {"Condition":Condition}
data10 = {"Color":Color}
data11 = {"Body Type":Body_type}
data12 = {"Ad Type":Ad_type}
data13 = {"Views Count":view}
data14 = {"Owner Name" :Owner_name}
data15 = {"Extra Features":Extra_Feature}
data16 = {"Phone Number":Phone}
data17 = {"Price":Price}

df0  = pd.DataFrame(data0 ,columns=["Title","Car Brand", "Location", "Posted Date"])
df1  = pd.DataFrame(data1 ,columns=["Ad Description"])
df2  = pd.DataFrame(data2 ,columns=["Model"])
df3  = pd.DataFrame(data3 ,columns=["Year"])
df4  = pd.DataFrame(data4 ,columns=["Payment Options"])
df5  = pd.DataFrame(data5 ,columns=["Engine Capacity (CC)"])
df6  = pd.DataFrame(data6 ,columns=["Fuel Type"])
df7  = pd.DataFrame(data7 ,columns=["Transmission Type"])
df8  = pd.DataFrame(data8 ,columns=["Kilometers"])
df9  = pd.DataFrame(data9 ,columns=["Condition"])
df10 = pd.DataFrame(data10,columns=["Color"])
df11 = pd.DataFrame(data11,columns=["Body Type"])
df12 = pd.DataFrame(data12,columns=["Ad Type"])
df13 = pd.DataFrame(data13,columns=["Views Count"])
df14 = pd.DataFrame(data14,columns=["Owner Name"])
df15 = pd.DataFrame(data15,columns=["Extra Features"])
df16 = pd.DataFrame(data16,columns=["Phone Number"])
df17 = pd.DataFrame(data17,columns=["Price"])

df0.transpose()
df1.transpose()
df2.transpose()
df3.transpose()
df4.transpose()
df5.transpose()
df6.transpose()
df7.transpose()
df8.transpose()
df9.transpose()
df10.transpose()
df11.transpose()
df12.transpose()
df13.transpose()
df14.transpose()
df15.transpose()
df16.transpose()
df17.transpose()

Last = pd.concat([df0,df1,df2,df3,df4,df5,df6,df7,df8,df9,df10,df11,df12,df13,df14,df15,df16,df17], axis = 1)
Last.to_csv("C:/Users/user/Desktop/Olx_Cars8.csv")














 
