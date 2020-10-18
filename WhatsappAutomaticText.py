
from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
import time 

#the URL in the function needs to be replaced by the path of the Chrome Driver in your computer
driver = webdriver.Chrome('C:\Users\Pooja Gera\Downloads\chromedriver')
driver.get("https://web.whatsapp.com") 
wait = WebDriverWait(driver,500)

target = "contact/group name"
message = "WhatsApp Message Jutsu!"

x_arg = '//span[contains(@title,' + target + ')]'
group_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg))) 
group_title.click() 
inp_xpath = '//div[@class="input"][@dir="auto"][@data-tab="1"]'
input_box = wait.until(EC.presence_of_element_located((By.XPATH, inp_xpath))) 
for i in range(100): 
    input_box.send_keys(message + Keys.ENTER) 
    time.sleep(1) 