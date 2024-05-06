from bs4 import BeautifulSoup
import urllib.request
import re, pyinputplus as pyip
import time, datetime, openpyxl, docx, subprocess
#2024-03-31
#Andrei Fridrikhsen
#Final project, scraping prices off eBay


#open doc
doc = docx.Document(r"C:\Users\stewa\AppData\Local\Programs\Python\Python312\Scripts\prices.docx")
#ask the numberOfItems the user wants to track
itemNames = []


        
numOfItems = pyip.inputInt("How many items do you wish to track? \n")
    
#ask the user for how many days they want to track the prices for

numberOfDays = pyip.inputInt("For how many days do you wish to track the average price? \n")

#ask the user for the item's name
while numOfItems!=0:
    
    
    itemToSearch = input("Enter the name of the item: \n")
    itemNames.append(itemToSearch)
    numOfItems -=1



#filter Item string (remove all spaces to pass to the path)
itemFirstPart = ""
def filterInput(itemToSearch):
    
    filteredString = ""
    itemToSearchList = itemToSearch.split()
    itemFirstPart = itemToSearchList[0]
    for item in itemToSearchList:
        filteredString += item
    return filteredString.strip()




#dayCounter
counter = 0

def trackAveragePrice(itemToSearch, counter):
    path = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2499337.m570.l1313&_nkw=" + filterInput(itemToSearch) + "&_sacat=0&rt=nc&LH_ItemCondition=1000"
    

    responseObj = urllib.request.urlopen(path)
    print(responseObj.getcode())
    data = responseObj.read()

    print(path)
    #parse html
    soup = BeautifulSoup(data, "html.parser")
    text = soup.get_text()
    #split the text to a list
    textList = text.split()
    #write regex for matching prices
    prices = []
   


    matchedPrice = ""


    #match prices in $000.00 or $0,000.00 format
    regexPrice = re.compile(r"(\$\d\d\d\.\d\d)|(\$\d\,\d\d\d.\d\d)")
    #search for names
    for item in textList:
        
        matchPrice = regexPrice.search(item)
        if matchPrice!=None:
            matchedPrice = matchPrice.group()
            prices.append(matchedPrice)
            #remove prices for delivery or scam prices
            if "," not in matchedPrice:
                if float(matchedPrice[1:]) < 200.00:
                    prices.remove(matchedPrice)
                                                                          
            
            

          


    #calculate average
    total = 0
    for item in prices:
        
            
        priceWithoutComma = ""
        if "," in item:
            priceWithoutCommaList = item.split(",")
            for i in priceWithoutCommaList:
                priceWithoutComma += i
                cleanPrice = float(priceWithoutComma[1:])
        else:
            cleanPrice = float(item[1:])

     
        total += cleanPrice
    average = 0
    #if prices is 0
    try:
        average = total//len(prices)
    except ZeroDivisionError:
        print("No items found")
        numberOfDays = 0
    print(average)
    print(prices)
    if average > 0:
        currentDate = datetime.datetime.now()
        
        
        doc.add_paragraph("The average price for " + itemToSearch + " is $" + str(average) + " on " + str(currentDate))
        doc.save('prices.docx')
    
    
    

while numberOfDays!=0:
    
    for i in range(0, numberOfDays):
        doc.add_heading("Day " + str(counter+1), 0)
        doc.save('prices.docx')
        for name in itemNames:
                trackAveragePrice(name, counter)
        
        time.sleep(1)
        #time.sleep(86400)
        counter+=1
        numberOfDays -=1
    
