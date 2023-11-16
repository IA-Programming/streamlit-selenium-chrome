import requests
from time import time
import streamlit as st

"""
## Web scraping on Streamlit Cloud with Selenium

[![Source](https://img.shields.io/badge/View-Source-<COLOR>.svg)](https://github.com/snehankekre/streamlit-selenium-chrome/)

This is a minimal, reproducible example of how to scrape the web with Selenium and Chrome on Streamlit's Community Cloud.

Fork this repo, and edit `/streamlit_app.py` to customize this app to your heart's desire. :heart:
"""

with st.echo():
    from selenium import webdriver
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.chrome.options import Options
    
    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36")
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    options.add_experimental_option("detach", True)
    
    @st.cache_resource
    def get_driver():
        start_time = time()
        driver = webdriver.Chrome(options=options)
        elapsed_time = time() - start_time
        st.write(f"Chrome-driver loaded in {elapsed_time:.2f} seconds")
        return driver
    
    driver = get_driver()

    from bs4 import BeautifulSoup
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    
    @st.cache_data
    def ExtrayendoHTML(Url: str, driver=driver):
        response = requests.get(Url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            result= 'Using BeautifulSoup'
            print('\33[1;32m' + result + '\33[0m')
            return result, response.text
        else:
            result= 'Using Selenium'
            print('\33[1;33m' + result + '\33[0m')
    
            # Cargar la página web
            driver.get(Url)
    
            # Esperar a que la página se cargue completamente
            WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
            )  # Esperar hasta x segundos
    
            html_code = driver.page_source
    
            # Get the status code using requests library
            response = requests.get(driver.current_url)
            if response.status_code == 200:
                result= result + ": " + "HTML code extracted successfully"
                print(result)
                return result, html_code
            else:
    
                result = 'Using Selenium Script method'
                print('\33[1;34m' + result + '\33[0m')
                
                # Get the HTML content directly from the browser's DOM
                html_code = driver.execute_script("return document.body.outerHTML;")
    
                # Get the status code using requests library
                response = requests.get(driver.current_url)
    
                # Validate the status code
                if response.status_code == 200:
                    result= result + ": " + "HTML code extracted successfully"
                    print(result)
                    return result, html_code
                else:
                    result= result + ": " + "Failed to extract HTML code"
                    print(result)
                    return result, html_code
    
    if url := st.text_input(label="put the url that you want you extract the html code", value="http://example.com", max_chars=100, help="pruepa"):
    
        start_time = time()
        result, html = ExtrayendoHTML(Url=url)
        # Get the Chromium version
        version = driver.capabilities['browserVersion']
        # Print the version
        st.markdown(f"### Chromium Version: {version}")
        # Get the ChromeDriver version
        chrome_driver_version = driver.capabilities['chrome']['chromedriverVersion'].split()[0]
        # Print the ChromeDriver version
        st.markdown(f"### ChromeDriver Version: {chrome_driver_version}")
        st.markdown(result)
        st.code(html)
        elapsed_time = time() - start_time
        st.markdown(f"### for the extraction of the html code is loaded in {elapsed_time:.2f} seconds")
