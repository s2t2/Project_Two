import tkinter as tk
from tkinter import *
import datetime
import tkinter
from PIL import Image, ImageTk
import os
import pprint
from dotenv import load_dotenv
import sendgrid
from sendgrid.helpers.mail import * 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import csv 
# adapted from: https://selenium-python.readthedocs.io/waits.html
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import datetime
import csv
import time
from datetime import timedelta


print("To start, please input your apartment preferences.")
#TNKTR USERINPUTS----------------------------------------------------------
#https://github.com/s2t2/shopping-cart-project/blob/master/shopping_cart.py
#!/usr/bin/python3
#https://www.python-course.eu/tkinter_entry_widgets.php
#https://www.python-course.eu/tkinter_text_widget.php
#https://stackoverflow.com/questions/41211060/how-to-add-scrollbar-to-tkinter
#https://github.com/prof-rossetti/georgetown-opim-243-201901/blob/99ce7522557f0a9c8690e48ac95bcce0d528b380/notes/python/packages/tkinter.md
#https://www.tutorialspoint.com/python/tk_scrollbar.htm
#https://stackoverflow.com/questions/7974849/how-can-i-make-one-python-file-run-another

selections = []

def apartment():
    apartment_value=[l4.get(i) for i in l4.curselection()]
    print("---------------------------------------")
    print("You have selected: ")
    print(apartment_value)
    selections.append(apartment_value)
  
def bed():
    bed_value=[l1.get(i) for i in l1.curselection()]
    print(bed_value)
    selections.append(bed_value)

def bath():
    bath_value=[l2.get(i) for i in l2.curselection()]
    print(bath_value)
    selections.append(bath_value)

def budget():
    print(my_budget.get())
    selections.append(my_budget.get())
    
def notifications():
    notification_value=[l5.get(i) for i in l5.curselection()]
    print(notification_value)
    selections.append(notification_value)

def select():
    print("Your final selections are:")
    #selections.append((my_move.get()))
    
    print(selections)
    budget = (my_budget.get())
    new_budget = int(budget)
    

    print("---------------------------------------")
    user_input = input("Are these values correct? ")
    y = ["Yes","yes","YES"]
    if user_input in y:
        print ("Great, we will save your inputs!")
        t = datetime.datetime.now()
        print("Response recorded at: ", datetime.datetime.now().strftime("%Y-%m-%d %H:%m:%S")) 
        print("---------------------------------------")
        w1.quit
        exit
    else:
        print("Please change your desired inputs and press 'Done'.")
        selections.clear() #https://www.geeksforgeeks.org/list-methods-in-python-set-2-del-remove-sort-insert-pop-extend/
        print("---------------------------------------")
        w1.mainloop()


  
    #Avalon Ballston
    if ['avalon-ballston-square'] in selections and ['One Bedroom'] in selections:  #and ['One Bathroom'] in selections 

        import csv

        with open("apartment3.csv", 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                applicable_apartments =  str(row)

        csvfile.close()
        
        URL = "https://www.avaloncommunities.com/virginia/arlington-apartments/avalon-ballston-square/floor-plans"
        driver = webdriver.Chrome("/usr/local/bin/chromedriver") 
        driver.get(URL)

        csvData =  [['Apartment Number ', 'Move-In ','Budget ']] #to link output to this


        try:
            listings_appear = EC.presence_of_element_located((By.ID, "floor-plan-listing"))
            wait_duration = 3
            div = WebDriverWait(driver, wait_duration).until(listings_appear)
            print("PAGE LOADED!")
        except TimeoutException:
            print("TIME OUT!")
        finally:
            soup = BeautifulSoup(driver.page_source, "html.parser")
            one_br_layouts = soup.find("div", id="bedrooms-1").findAll("div", "row")
            
            print("One Bedroom Apartments:")
            print("                                       ")
            print("Number      Move-in Date        Price")

        #Apartments listings--------------------------------------------------------------------
            for layout in one_br_layouts:
            
            #Apartment Information-------------------------------------------------------------
                one_br=(layout.find("table").find("tbody").text)
                one_br_str= str(one_br)
                one_br_list = one_br_str.split("View Details")

                for listing_str in one_br_list:
                    if listing_str != " ":
                        one_br_listing=(layout.find("h4").text)
                        #budget validation:
                        move_date = listing_str[5: listing_str.find("$")]
                        price = listing_str[listing_str.find("$"):]
                        price_to_int = price[1:6]
                        new_price = price_to_int.replace(',', "")
                        new_new_price = (int(new_price))
                        monthly_budget = new_budget
                        
                        p = []
                        if monthly_budget > new_new_price:
                            p.append(new_new_price)
                            print(listing_str[:5] + "        " + move_date +  "         " +  " "  + str(p))
                            woo_budget = (listing_str[:5] + "        " + move_date +  "         " +  " "  + str(p))

                            csvData.append([woo_budget, one_br_listing])
                            with open('apartment3.csv', 'a+') as csvFile:
                                writer = csv.writer(csvFile)
                                writer.writerows(csvData)
                            csvFile.close()
                        
                        else: 
                            pass
        
        print("You will now receive an email to your inbox")
        
        load_dotenv()

        SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "OOPS, please set env var called 'SENDGRID_API_KEY'")
        MY_EMAIL_ADDRESS = os.environ.get("MY_EMAIL_ADDRESS", "OOPS, please set env var called 'MY_EMAIL_ADDRESS'")

        # AUTHENTICATE

        

        sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)

        # COMPILE REQUEST PARAMETERS (PREPARE THE EMAIL)

        from_email = Email(MY_EMAIL_ADDRESS)
        to_email = Email(MY_EMAIL_ADDRESS)
        subject = "Apartment Update!"
        content = Content("text/plain", "hello, below please find your applicable apartments:"+ applicable_apartments) #https://bytes.com/topic/python/answers/620147-how-execute-python-script-another-python-script)
        mail = Mail(from_email, subject, to_email, content)

        # ISSUE REQUEST (SEND EMAIL)

        response = sg.client.mail.send.post(request_body=mail.get())

        # PARSE RESPONSE

        print(response.status_code)
        print(response.body) 
        print(response.headers)
    
    else:
        pass


    #Ava Ballston
    if ['ava-ballston'] in selections and ['One Bedroom'] in selections and ['One Bathroom'] in selections: 
        scrape = os.system('python ava_ballston_one_bed_one_bath.py') #https://bytes.com/topic/python/answers/620147-how-execute-python-script-another-python-script
    else:
        pass
    


#Tkiner---------------------------------------------------------------------------------
w1= Tk()
w1.title('Apartment Selection App')
frame = Frame(w1)

#Configuring Scrollbar

scrollbar = Scrollbar(w1)
scrollbar.pack( side = RIGHT, fill = Y )

mylist = Listbox(w1, yscrollcommand = scrollbar.set )
for line in range(100):
    line =  1 #to put info in this scrollable section


    l1= Listbox(w1, selectmode= MULTIPLE, width= 20, height=5)
    l2= Listbox(w1, selectmode= MULTIPLE, width= 20, height=5)
    l4= Listbox(w1, selectmode= MULTIPLE, width= 20, height=5)
    l5= Listbox(w1, selectmode= MULTIPLE, width= 20, height=5)

#App Picture--------------------------------------------------------------

    #https://www.slideshare.net/r1chardj0n3s/tkinter-does-not-suck

    image = ImageTk.PhotoImage(Image.open('pic.png')), 
    tk.Label(w1, image=image).pack()

    T = Text(w1, height=1, width=30)
    T.pack()
    T.insert(END, "Welcome to my application!")
 
#Apartment Selection-------------------------------------------------------
    T = Text(w1, height=1, width=30)
    T.pack()
    T.insert(END, "Please select your apartment: ")

    Apartment_Buildings = [
        {"id":1, "name": "avalon-ballston-square", "URL": "https://www.avaloncommunities.com/virginia/arlington-apartments/avalon-ballston-square/floor-plans"},
        {"id":2, "name": "ava-ballston", "URL": "https://www.avaloncommunities.com/virginia/arlington-apartments/ava-ballston/floor-plans"}
        #to add more apartments within Avalon family
    ]

    l = []
    for p in Apartment_Buildings:
        l.append(p["name"])

    Apartment_Buildings = list(set(l))
    Apartment_Buildings = sorted(Apartment_Buildings)

    Apartment= [Apartment_Buildings[0],Apartment_Buildings[1]] #to connect to name on different lines
    for val in Apartment:
        l4.insert(END, val)
    l4.pack()


    b5=Button(text= 'Select', command=apartment)
    b5.pack()

#Bedroom Selection-------------------------------------------------------
    T = Text(w1, height=2, width=30)
    T.pack()
    T.insert(END, "Please select your desired \n number of bedrooms: ")

    bedroom= ['One Bedroom', 'Two Bedrooms']
    for val in bedroom:
        l1.insert(END, val)
    l1.pack()

    b1=Button(text= 'Select', command=bed)
    b1.pack()

#Bathroom Selection-------------------------------------------------------
    #T = Text(w1, height=2, width=30)
    #T.pack()
    #T.insert(END, "Please select your desired \n number of bathrooms: ")

    #bathroom= ['One Bathroom', 'Two Bathrooms', 'More than Two Bathrooms']
    #for val in bathroom:
        #l2.insert(END, val)
    #l2.pack()

    #b2=Button(text= 'Select', command=bath)
    #b2.pack()

#Budget Selection-------------------------------------------------------
    T = Text(w1, height=2, width=30)
    T.pack()
    T.insert(END, "Please input your \n monthly budget: ")

    budget_value = tkinter.StringVar()
    my_budget = tkinter.Entry(textvariable=budget_value)

    my_button = tkinter.Button(text="Select", command=budget)
    my_budget.pack()
    my_button.pack()

#Move-in Date Selection-------------------------------------------------------
    #T = Text(w1, height=2, width=30)
    #T.pack()
    #T.insert(END, "Please input your move in date with \n the following format mm/dd/yyyy ")

    #move_value = tkinter.StringVar()
    #my_move = tkinter.Entry(textvariable=move_value)

    #def movein():
        #print(my_move.get())

    #my_button_two = tkinter.Button(text="Select", command=movein)
    #my_move.pack()
    #my_button_two.pack()

 #Notification Selection------------------------------------------------
    #T = Text(w1, height=2, width=30)
    #T.pack()
    #T.insert(END, "Please select your desired \n notification setting: ")

    #mails= ['One time'] #to add in heroku notifications
    #for val in emails:
        #l5.insert(END, val)
    #l5.pack()

    #b6=Button(text= 'Select', command=notifications)
    #b6.pack()

#Selections Button-----------------------------------------------------------
    b4 = Button(w1, text='Done', command=select)
    b4.pack()

    w1.mainloop()
    mylist.insert(END, (line))

mylist.pack( side = LEFT, fill = BOTH )
scrollbar.config( command = mylist.yview )

breakpoint
