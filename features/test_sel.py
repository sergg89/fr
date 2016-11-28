from selenium import webdriver

driver = webdriver.Firefox(executable_path='/Users/gorbanenko_cr/Downloads/geckodriver')
driver.get('http://google.com')