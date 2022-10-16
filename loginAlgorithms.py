from selenium import webdriver
import requests
import time
import base64
from selenium.webdriver.common.by import By
def loginner(url, email, password):
    # Start Chrome Driver
    chromedriver = '/Users/niroren/Documents/chromedriver/chromedriver'

    option = webdriver.ChromeOptions() # Option to not open chrome window
    # option.add_argument('headless')

    
    #driver = webdriver.Chrome(chromedriver, options=option)
    driver = webdriver.Chrome(chromedriver)
    # Open the URL you want to execute JS
    #print(url)
    driver.get(url)

    # Execute JS
    script ='document.getElementById("email").value="' + email + '";document.getElementById("password").value="' + password + '";document.forms[0].submit()'
    #print(script)
    driver.execute_script(script)
    time.sleep(4)

    # Get page source
    text = driver.page_source
    path = '/Users/niroren/Desktop/temp.png'
    # S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
    # driver.set_window_size(S('Width'),S('Height')) # May need manual adjustment
    # driver.find_element_by_tag_name('body').screenshot(path)
    

    return text

def ramapo(url, email, password):
    chromedriver = '/Users/niroren/Documents/chromedriver/chromedriver'

    option = webdriver.ChromeOptions() # Option to not open chrome window
    option.add_argument('headless')
    option.add_argument("start-maximized")

    
    #driver = webdriver.Chrome(chromedriver, options=option)
    driver = webdriver.Chrome(chromedriver)
    # Open the URL you want to execute JS
    #print(url)
    driver.get(url)

    # Execute JS
    script ='document.getElementById("email").value="' + email + '";document.getElementById("password").value="' + password + '";document.forms[0].submit()'
    #print(script)
    driver.execute_script(script)

    # Get page source
    time.sleep(10)
    text = driver.page_source
    # path = '/Users/niroren/Desktop/temp.png'
    # S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
    # driver.set_window_size(S('Width'),S('Height')) # May need manual adjustment
    # driver.find_element_by_tag_name('body').screenshot(path)
    return text


txt = ramapo('https://apply.ramapo.edu/apply/status','niroren04@gmail.com','Sisma!1234ramapo')
print(txt)
w = open('test.html','w')
w.write(txt)
w.close()