from tkinter import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import pyautogui
import time
from selenium.common.exceptions import NoSuchElementException

import winsound as sd


# -*- coding: utf-8 -*-

#비프음소리내기
def beepsound():
    fr = 2000    # range : 37 ~ 32767
    du = 5000     # 1000 ms ==1second
    sd.Beep(fr, du) # winsound.Beep(frequency, duration)

tk = Tk()
tk.title('KTX예매')
tk.geometry("380x380")

label1 = Label(tk,text='아이디').grid(row=0, column=0)
label2 = Label(tk,text='비번').grid(row=1,column=0)
label3 = Label(tk,text='출발').grid(row=2,column=0)
label4 = Label(tk,text='도착').grid(row=3,column=0)
label5 = Label(tk,text='일자').grid(row=4,column=0)
label6 = Label(tk,text='시간').grid(row=5,column=0)
label7 = Label(tk,text='검색결과').grid(row=6,column=0)

# 각 단위 입력받는 부분 만들기
entry1 = Entry(tk)
entry2 = Entry(tk)
entry3 = Entry(tk)
entry4 = Entry(tk)
entry5 = Entry(tk)
entry6 = Entry(tk)
entry7 = Entry(tk)

entry1.grid(row=0,column=1)
entry2.grid(row=1,column=1)
entry3.grid(row=2,column=1)
entry4.grid(row=3,column=1)
entry5.grid(row=4,column=1)
entry6.grid(row=5,column=1)
entry7.grid(row=6,column=1)


#startMacro
def startMacro(driver, startSelct):

    table = driver.find_element(By.CLASS_NAME, 'tbl_h')
    tbody = table.find_element(By.TAG_NAME, 'tbody')
    #검색결과의 TR을 가져와서 체크함 0부터 시작해야 되기 때문에 1 인경우 0
    rows = tbody.find_elements(By.TAG_NAME, 'tr')[int(startSelct)-1]
    body= rows.find_elements(By.TAG_NAME, "td")[5]

    try:
        clickBtn = body.find_element(By.TAG_NAME, 'a')
        clickBtn.click()        
        beepsound()            
        return True        
    except NoSuchElementException:
        return False

def KtxLoginStart():

    driver = webdriver.Chrome('./chromedriver')

    id = entry1.get()
    pw = entry2.get()
    startLoc = entry3.get()
    endLoc = entry4.get()
    startday = entry5.get()
    startTime = entry6.get()
    startSelct = entry7.get()
    driver.get("https://www.letskorail.com/korail/com/login.do")

    # 멤버십로그인
    xpath = '//input[@id="txtMember"]'
    element = driver.find_element(By.ID, 'txtMember').click()
    pyautogui.write(id, interval=0.25)

    pyautogui.press('tab')

    pyautogui.write(pw, interval=0.25)

    pyautogui.press('enter')

    url = "https://www.letskorail.com/ebizprd/prdMain.do"
    driver.get(url)
    time.sleep(3)

    #select main-window
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(1)
    
    #xpath 가 selenium 상위 버전에서는 잘 작동이 안되서 find_element로 변경함
    xpath = '//input[@id="txtGoStart"]'
    driver.find_element(By.ID, 'txtGoStart').clear()
    driver.find_element(By.ID, 'txtGoStart').send_keys(startLoc)
 
    xpath = '//input[@id="txtGoEnd"]'
    driver.find_element(By.ID, 'txtGoEnd').clear()
    driver.find_element(By.ID, 'txtGoEnd').send_keys(endLoc)
    time.sleep(1)

    xpath1 = '//img[@alt="달력"]'
    driver.find_element(By.XPATH, xpath1).click()
    time.sleep(1)

    #move to pop-up
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(1)

    dayCon = '//span[@id="d' + startday + "\"]"
    driver.find_element(By.XPATH, dayCon).click()
    time.sleep(1)

    #move to main-window again
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(1)

    xpath3 = '//select[@id="time"]'
    driver.find_element(By.XPATH, xpath3).click()
    driver.find_element(By.XPATH, xpath3).send_keys(startTime)
    time.sleep(1) 

    driver.execute_script("inqSchedule()")
    driver.implicitly_wait(2)
    driver.execute_script("inqSchedule()")

    time.sleep(3)


    result = startMacro(driver, startSelct)
    while result != True:
        driver.refresh()
        result = startMacro(driver, startSelct)

btn1 = Button(tk,text='예매시작',bg='black',fg='white',command=KtxLoginStart).grid(row=7,column=0)

tk.mainloop()