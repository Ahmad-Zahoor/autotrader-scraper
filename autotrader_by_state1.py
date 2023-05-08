# coding: utf8
from tkinter.filedialog import askopenfile, askopenfilename, askopenfilenames, askdirectory
from importlib.machinery import all_suffixes
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from asyncio import sleep
from cProfile import label
# from cgitb import text
import csv
from http import server
from itertools import count
import os
from pprint import pprint
# from telnetlib import theNULL
from threading import Thread
import tkinter
from turtle import color
from unicodedata import category, numeric
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from subprocess import CREATE_NO_WINDOW
import time
import re
from selenium.common.exceptions import JavascriptException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import Select
from tkinter import *
from tkinter import messagebox
import pandas as pd
from random import randint
from actions import *
import smtplib
import sys
from datetime import datetime, timedelta
import pytz
import requests
#from PIL import Image, ImageTk
import glob
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.message import EmailMessage
import undetected_chromedriver as uc
import urllib.request
from pathlib import Path
import re
import threading


root = Tk()
root.title("Autotrader-Products-Data-Software")
root.iconbitmap("autotrader.ico")
fram2 = Frame(root)

label6 = Label(fram2, width=55, text="", anchor='w',font=("Helvetica", 10), fg="green")
label6.grid(row=3, column=1, padx=5, pady=5)

running = False


def clock(get_time):
    # pak_date = pytz.timezone("Asia/Karachi")
    # pak_time = datetime.now(pak_date)

    # current_time = pak_time.strftime("%H:%M:%S")
    try:
        root.update()
        label6.config(text=get_time)
        label6.after(1000)
    except Exception as e:
        pass

def call(getind):
    try:
        root.update()
        emptylabel.configure(text = str(getind))
        root.after(1000)
        #return True
    except tkinter.TclError as e:
        root.destroy()

all_phones = []

def autotrader(driver, getlinks,create_path):

    start = time.time()

    label3.grid_forget()
    label4.grid_forget()

    auto_counter = 0
    get_len_autotraders = 0

    for indn in range(1,2):

        wait = WebDriverWait(driver, 3)

        

        for indz, codez in enumerate(getlinks, start=1):

            # if indz==2:
            #     break
        
            driver.get(codez)
            sleep(15)

            if indn==1:
                try:
                    clsoebtn = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,"//button[text()=' Close']")))
                    driver.execute_script("arguments[0].click();", clsoebtn)
                    sleep(1)
                except Exception as e:
                    pass
        
        
            try:
                cars_place = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'//h1[@id="rfTitle"]/span[@id="titleText"]'))).text
            except Exception as e:
                try:
                    cars_place = driver.find_element(By.XPATH,'//*[@id="titleText"]').text
                except Exception as e:
                    print("Cars Place Name not found")
                    break
            

            if "/" in cars_place:
                cars_place = cars_place.replace("/","")
            
            print(f"{cars_place} is in process...")

            # Create State Folder

            folderpath = f"{create_path}\{cars_place}"

            if not os.path.exists(folderpath):
                os.mkdir(folderpath)

            # Code for getting all car links

            place_name = cars_place.split(" ")[-1]

            #Get the current date and time
            now = datetime.now()

            # Format the date and time as a string
            date_string = now.strftime('%Y-%m-%d')

            # # Create the file name with the date string
            # file_name = f'Karachi_leads_{date_string}.xlsx'

            filpathf = f"{create_path}\{place_name}_carlinks_{date_string}_file_no_"+str(indn)+'.csv'

            all_car_links = []

            try:
                if not os.path.exists(filpathf):
                    call("Wait links is scraping...")
                    with open(filpathf,mode='a', newline='') as output_2:
                        writer = csv.writer(output_2)
                        # for indz, codez in enumerate(getlinks, start=1):

                        #     # if indz==2:
                        #     #     break
                        
                        #     driver.get(codez)
                        #     sleep(15)
                        target_n = 5
                            # try:
                            #     get_last_page_number_text = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'//div[@class="srpPager"]/ul/li[last()]'))).get_attribute("data-page")
                            #     get_last_n = int(get_last_page_number_text)
                                
                            # except Exception as e:
                            #     print("Error")

                        counter = 1
                        while(True):
                            try:
                                all_tr = driver.find_elements(By.XPATH, '//div[@id="listingsWrapperMainListing"]//div[@class="photo-area"]/a')
                                for index, tr in enumerate(all_tr,start=1):
                                    get_link = tr.get_attribute("href")
                                    getdata = [get_link]
                                    writer.writerow(getdata)
                                    output_2.flush()
                                    # all_car_links.append(get_link)
                                
                            except Exception as e:
                                print("There is an issue in scraping links")
                                print(e)
                            
                            print(f"Page No:{counter} Scaraping Completed")
                            counter +=1

                            #checknext_btn = check_exists_by_xpath(driver,'//div[@class="srpPager"]//ul[contains(@class,"pagination")]/li[last()]/a[contains(@class,"disabled")]')

                            if counter>target_n:
                                break
                            else:
                                try:
                                    nextbtn = WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH,'//div[@class="srpPager"]/ul/li[contains(@class,"page-item") and @data-page="'+str(counter)+'"]/a')))
                                    nextbtn.click()
                                    sleep(7)
                                except Exception as e:
                                    try:
                                        nextbtn = driver.find_element(By.XPATH,'//div[@class="srpPager"]/ul/li[contains(@class,"page-item") and @data-page="'+str(counter)+'"]/a')
                                        driver.execute_script("arguments[0].click();", nextbtn)
                                        sleep(7)
                                    except Exception as e:
                                        print(e)

                readlinks = pd.read_csv(filpathf,header=None, index_col=0)

                for row in readlinks.index:
                    all_car_links.append(row)
                
                if len(all_car_links)>0:

                    get_len_autotraders += len(all_car_links)

                    #Get the current date and time
                    now = datetime.now()

                    # Format the date and time as a string
                    date_string = now.strftime('%Y-%m-%d')

                    # Create the file name with the date string
                    # file_name = f'Karachi_leads_{date_string}.xlsx'

                    data_filpathf =f"{folderpath}\{place_name}_{date_string}_"+'cars_data_'+str(indn)+'.csv'

                    if not os.path.exists(data_filpathf):

                        headers = ["Sno","Phone Number","Title","Address","Link","Price"]

                        with open(data_filpathf, 'a', newline='',encoding="utf-8") as output:
                            writer = csv.writer(output)
                            writer.writerow(headers)
                    with open(data_filpathf, 'a', newline='',encoding="utf-8") as output:
                        
                        serial_no = 1
                        

                        for pro_ind, prod_link in enumerate(all_car_links, start=1):
                            auto_counter += 1
                            writer = csv.writer(output)

                            # if pro_ind==5:
                            #     break
                            
                            if pro_ind >0: # agar bot ap rok de to last counter ko daikay aor per yaha dalay like pro_ind>300 to 301 say start hoga

                                driver.get(prod_link)
                                sleep(5)

                                # if pro_ind==101:
                                #     break

                                checkdearler = check_exists_by_xpath(driver,'(//a[normalize-space()="Visit Dealer website"])[2]')

                                if checkdearler:
                                    continue

                                else:

                                    try:
                                        try:
                                            title = wait.until(EC.presence_of_element_located((By.XPATH, '//p[@class="hero-title"]'))).text
                                            #leads_data["Name"] = wait.until(EC.presence_of_element_located((By.XPATH, "//table[@class='list']//tbody/tr["+str(index)+"]/td[2]"))).text
                                        except Exception as e:
                                            title = 'Null'
                                            print("Name not found")

                                        try:
                                            get_price = wait.until(EC.presence_of_element_located((By.XPATH, '//p[@class="hero-price"]'))).text
                                            curr_price = "$"+get_price
                                        except Exception as e:
                                            curr_price = "Null"
                                            print("Email not found")
                                        
                                        try:
                                            check_click_toshow = check_exists_by_xpath(driver,'//vdp-private-lead-phone//div[@class="card-body"]/a[text()="Click to show"]')
                                            if check_click_toshow:
                                                try:
                                                    clcshow = driver.find_element(By.XPATH,'//vdp-private-lead-phone//div[@class="card-body"]/a[text()="Click to show"]')
                                                    clcshow.click()
                                                    sleep(1)
                                                except Exception as e:
                                                    try:
                                                        clcshow = driver.find_element(By.XPATH,'//vdp-private-lead-phone//div[@class="card-body"]/a[text()="Click to show"]')
                                                        driver.execute_script("arguments[0].click();", clcshow)
                                                        sleep(1)
                                                    except Exception as e:
                                                        print("Click to show path has an issue")
                                                        print(e)
                                                try:
                                                    phone = wait.until(EC.presence_of_element_located((By.XPATH, '//vdp-private-lead-phone//div[@class="card-body"]/p'))).text
                                                    phone = phone.replace('-','')

                                                    if "X" in phone:
                                                        try:
                                                            clcshow = driver.find_element(By.XPATH,'//vdp-private-lead-phone//div[@class="card-body"]/a[text()="Click to show"]')
                                                            clcshow.click()
                                                            sleep(1)
                                                        except Exception as e:
                                                            try:
                                                                clcshow = driver.find_element(By.XPATH,'//vdp-private-lead-phone//div[@class="card-body"]/a[text()="Click to show"]')
                                                                driver.execute_script("arguments[0].click();", clcshow)
                                                                sleep(1)
                                                            except Exception as e:
                                                                print("Click to show path has an issue")
                                                                print(e)
                                                        
                                                        phone = wait.until(EC.presence_of_element_located((By.XPATH, '//vdp-private-lead-phone//div[@class="card-body"]/p'))).text
                                                        phone = phone.replace('-','')

                                                except Exception as e:
                                                    try:
                                                        phone = driver.find_element(By.XPATH, '//vdp-private-lead-phone//div[@class="card-body"]/p').text
                                                        phone = phone.replace('-','')
                                                    except Exception as e:
                                                        print("Phone number path has an issue")
                                            else:
                                                phone = ""
                                        except Exception as e:
                                            phone = ""
                                            print("Phone number not found")

                                        try:
                                            address = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@id="privateLeadContainer"]//div[@class="private-title"]/p'))).text
                                            seller = driver.find_element(By.XPATH,'//div[@id="privateLeadContainer"]//div[@class="private-title"]/p/b').text
                                            newaddress = address.replace(seller,'').strip()                
                                        except Exception as e:
                                            newaddress = 'Null'
                                            print("Address not found")
                                    except Exception as e:
                                        print("Error in Scraping data")
                                        print(e)
                                    
                                    if phone=="" or phone in all_phones:
                                        # auto_counter +=1
                                        call(pro_ind)
                                        # pass
                                    else:
                                        all_phones.append(phone)
                                        get_new_data = [serial_no,phone,title,newaddress,prod_link,curr_price]
                                        writer.writerow(get_new_data)
                                        output.flush()
                                        call(pro_ind)

                                        print("Phone Counter: " + str(serial_no) + " | Link Counter:"+str(pro_ind))
                                        serial_no +=1


                else:
                    print("Products are not found")
                    break
            
            except Exception as e:
                print("Issue in Scraping Categories List")
                # print(e)
            
            stop = time.time()
            duration = stop-start
            my_time = time.strftime('%H:%M:%S', time.localtime(duration))
            clock(my_time)

            # print("Scraping Completed.")

    if auto_counter == get_len_autotraders:
        get_val2 = messagebox.showinfo("Autotrader", "Program Completed Successfully.")
        # complete_work(driver)
        try:
            driver.close()
        except (WebDriverException,NoSuchWindowException) as e:
            pass
    # else:
    #     pass
    # try:
    #     driver.close()
    # except (WebDriverException,NoSuchWindowException) as e:
    #     pass


def stop_w(driver):

    global running
    
    get_val = messagebox.askquestion("Exit", "Do you want to close the program",icon = 'warning')
    try:
        if get_val=='yes':
            root.destroy()
            driver.close()
        else:
            pass
    except (NoSuchWindowException,WebDriverException) as e:
        pass

# def complete_work(driver):

#     global running

#     get_val2 = messagebox.showinfo("Autotrader", "Program Completed Successfully.")
    
#     try:
#         if get_val2=='ok':
#             root.destroy()
#             # driver.close()
#         else:
#             print("These is something wrong")
#     except (WebDriverException,NoSuchWindowException) as e:
#         print(e)
        # pass

def close_window():

    global running

    get_val = messagebox.askquestion("Exit", "Do you want to close the program",icon = 'warning')

    try:
        if get_val=='yes' and running:
            root.destroy()
            running.close()
        elif get_val=='yes':
            root.destroy()
    except (WebDriverException,NoSuchWindowException) as e:
        pass


def startBot(ents, root):

    global running

    b1.config(state="disabled")
    
    # startIndex    = ents['Start Index'].get()
    get_file   = ents['Add files'].get()
    get_dir = ents['Output folder'].get()

    # if startIndex=="":
    #     messagebox.showerror('Start Index', "Pleas Enter Value")
    #     b1.config(state="normal")

    # elif startIndex.isnumeric()==False:
    #     messagebox.showerror('Start Index', "Pleas Enter Only Positive Number")
    #     b1.config(state="normal")
    
    if get_file=="":
        messagebox.showerror('Add files', "Pleas Enter File Name")
        b1.config(state="normal")
    
    elif get_file.isnumeric()==True:
        messagebox.showerror('Add files', "Pleas Enter correct file name")
        b1.config(state="normal")
    elif os.path.exists(get_file)==False:
        messagebox.showerror('Add files', "File not found in the direcotry")
        b1.config(state="normal")
    
    elif get_dir=="":
        messagebox.showerror('Folder', "Pleas Select Output Folder")
        b1.config(state="normal")
    
    elif get_dir.isnumeric()==True:
        messagebox.showerror('Folder', "Pleas Enter Correct output path")
        b1.config(state="normal")
    elif os.path.exists(get_file)==False:
        messagebox.showerror('Folder', "Folder path not found")
        b1.config(state="normal")
    
    else:

    
    # else:
    #     startIndex = int(ents['Start Index'].get())

    #     if startIndex <=0:
    #         messagebox.showerror('Start Index', "Pleas Enter greater then 0 Number")
    #         b1.config(state="normal")
        
    #     else:
    #         startIndex = int(ents['Start Index'].get())

        name, extensionf = os.path.splitext(get_file)

        data = []

        if extensionf=='.xlsx':
            excel_data = pd.read_excel(get_file, header=None, index_col=0)
            
            for row in excel_data.index:
                if row not in data:
                    # sentence = ' '.join(row.split())
                    data.append(row)

        else:
            csv_data = pd.read_csv(get_file, header=None, index_col=0)
            for row in csv_data.index:
                if row not in data:
                    # sentence = ' '.join(row.split())
                    data.append(row)


        # data = []
            
        # # Open Products file
        # with open(get_file, 'r') as txt_file:
        #     txt_reader = txt_file.readlines()
        #     for row in txt_reader:
        #         if row not in data:
        #             sentence = ' '.join(row.split())
        #             data.append(sentence)
        
        # get_lenght = len(data)
        # if startIndex >get_lenght:
        #     messagebox.showerror("Start Index", "Please Enter number between 1 and {}".format(get_lenght))
        #     b1.config(state="normal")
        
        print("Total Links are: ")
        print(len(data))
        sleep(1)


        #driver = uc.Chrome(use_subprocess=True,service_creationflags=CREATE_NO_WINDOW)
        driver = uc.Chrome(use_subprocess=True)
        driver.maximize_window()
        time.sleep(5)

        # chrome_options = Options()
        # chrome_options.add_experimental_option("debuggerAddress","localhost:9014")
        # service = Service(executable_path=ChromeDriverManager().install())
        # driver = webdriver.Chrome(service=service,options=chrome_options)
        # #service.creationflags = CREATE_NO_WINDOW
        # driver = webdriver.Chrome(executable_path=r"F:\Furniture\chromedriver.exe",options=chrome_options)
        # driver.maximize_window()
        # sleep(2)

        running = driver

        b1.grid_forget()
        b2 = Button(fram2, text='Stop', command=lambda: stop_w(driver)) #command=root.destroy
        b2.grid(row=4, column=0, padx=5, pady=5)
        
        autotrader(driver,data,get_dir)
    
def open_file(get_field):
    #os.getcwd()
    # downloads_path = str(Path.home() / "Downloads")
    fileobj = askopenfilename(initialdir=os.getcwd(),title="Open File", filetypes=[('Text Files','*.txt'),('CSV Files', '*.csv'),('Xlsx Files', '*.xlsx')])
    
    if fileobj:
        get_field.set(fileobj)

def open_dir(get_dir):
    # downloads_path = str(Path.home() / "Downloads")
    filedir = askdirectory(initialdir=os.getcwd(),title="Select Folder")
    if filedir:
        get_dir.set(filedir)


def makeform(root, fields):
    
    all_ents = {}

    for field in fields:
        fram1 = Frame(root)
        if field=="Add files":
            label1 = Label(fram1, width=15, text=field + " :", anchor='w')
            label1.pack(side=LEFT, padx=5, pady=5)
            my_str = StringVar()
            ent = Entry(fram1, width=40, textvariable=my_str)
            ent.insert(0, "")
            browsebtn = Button(fram1, text="Browse",state="normal", command=lambda: open_file(my_str))
            browsebtn.pack(side=RIGHT, padx=5, pady=5)
            ent.pack(side=RIGHT, expand=YES, fill=X, padx=50, pady=5)
            fram1.pack(side=TOP, fill=X, padx=5, pady=5)
            all_ents[field] = ent
        elif field=="Output folder":
            label1 = Label(fram1, width=15, text=field + " :", anchor='w')
            label1.pack(side=LEFT, padx=5, pady=5)
            my_dir = StringVar()
            ent = Entry(fram1, width=40, textvariable=my_dir)
            ent.insert(0, "")
            browsebtn = Button(fram1, text="Browse",state="normal", command=lambda: open_dir(my_dir))
            browsebtn.pack(side=RIGHT, padx=5, pady=5)
            ent.pack(side=RIGHT, expand=YES, fill=X, padx=50, pady=5)
            fram1.pack(side=TOP, fill=X, padx=5, pady=5)
            all_ents[field] = ent
        else:
            label1 = Label(fram1, width=15, text=field + " :", anchor='w')
            ent = Entry(fram1, width=40)
            ent.insert(0, "")
            fram1.pack(side=TOP, fill=X, padx=5, pady=5)
            label1.pack(side=LEFT, padx=5, pady=5)
            ent.pack(side=RIGHT, expand=YES, fill=X, padx=50, pady=5)
            all_ents[field] = ent

        
    return all_ents


fields = (["Add files","Output folder"])

# root = Tk()

entries = makeform(root, fields)


label2 = Label(fram2, width=10, text="Start Counter:", anchor='w')
label2.grid(row=1, column=0, padx=5, pady=5)

emptylabel = Label(fram2, width=30)
emptylabel.grid(row=1, column=1, padx=10, pady=5)

label3 = Label(fram2, width=10, text="Note:", anchor='w', foreground='red')
label3.grid(row=2, column=0, padx=5, pady=5)

label4 = Label(fram2, width=55, text="After You Hit the start button it will start after minimum 50 seconds", anchor='w')
label4.grid(row=2, column=1, padx=5, pady=5)

label5 = Label(fram2, width=10, text="Current Time:", anchor='w')
label5.grid(row=3, column=0, padx=5, pady=5)



# threading.Thread(target=clock()).start()

fram2.pack(side=BOTTOM, padx=5, pady=5)

#command=lambda: threading.Thread(target=run_weekly, args=(parent,), daemon=True).start()

b1 = Button(fram2, text='Start',state="normal", command=lambda: threading.Thread(target=startBot, args=(entries,  root,)).start()) #, daemon=True

#b1 = Button(fram2, text='Start', command=lambda: startBot(entries,  root))
b1.grid(row=4, column=0, padx=5, pady=5)

# b2 = Button(fram2, text='Stop', command=root.destroy)
# b2.grid(row=4, column=1, padx=5, pady=5)

root.protocol("WM_DELETE_WINDOW",close_window)
root.mainloop()