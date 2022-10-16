def loginner(url, email, password):
    import screenshot
    # import undetected_chromedriver as uc
    from selenium import webdriver
    import requests
    import time
    import base64
    from PIL import Image
    from selenium.webdriver.common.by import By

    # Start Chrome Driver
    chromedriver = '/Users/niroren/Documents/chromedriver/chromedriver'

    option = webdriver.ChromeOptions() # Option to not open chrome window
    # option.add_argument('headless')
    option.add_argument('--start-maximized')

    
    #driver = webdriver.Chrome(chromedriver, options=option)
    driver = webdriver.Chrome(chromedriver,options=option)
    # driver = uc.Chrome(options=option)
    # Open the URL you want to execute JS
    #print(url)
    driver.get(url)

    # Execute JS
    script ='document.getElementById("email").value="' + email + '";document.getElementById("password").value="' + password + '";document.forms[0].submit()'
    #print(script)
    time.sleep(3)
    driver.execute_script(script)
    time.sleep(5)

    # Get page source
    # text = driver.find_element_by_tag_name('body').text
    text = driver.page_source
    path = '/Users/niroren/Desktop/temp.png'
    w = driver.execute_script('return document.body.parentNode.scrollWidth')
    h = driver.execute_script('return document.body.parentNode.scrollHeight')
    #set to new window size
    # driver.set_window_size(w, h)
    required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
    required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
    
    S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
    print(S("Width"))
    driver.set_window_size(S("Width"), S("Height"))
    body = driver.find_element(By.TAG_NAME, "body")
    # total_height = body.size["height"]+1000
    # body1 = driver.get_element_by_tag_name()
    body.screenshot(path)
    driver.save_screenshot('/Users/niroren/Desktop/temp1.png')
    

    w = open('test.html','w')
    w.write(text)
    w.close()

    return text



# print('-'*50)
dartmouth = 'https://apply.dartmouth.edu/account/login?r=https%3a%2f%2fapply.dartmouth.edu%2fapply%2fstatus'
brown = 'https://apply.college.brown.edu/account/login?r=https%3a%2f%2fapply.college.brown.edu%2fapply%2fstatus'
princeton = 'https://apply.princeton.edu/account/login?r=https%3a%2f%2fapply.princeton.edu%2fapply%2fstatus'
ramapo = 'https://apply.ramapo.edu/apply/status'

# loginner(url = princeton,email = 'niroren04@gmail.com',password='Sisma!1234dartmouth')

