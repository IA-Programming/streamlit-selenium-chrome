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
    from selenium.webdriver.chrome.options import Options
    
    options = Options()
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
    def ExtrayendoHTML(Url: str, driver: webdriver=driver):
        response = requests.get(Url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print('\33[1;32m' + 'Using BeautifulSoup' + '\33[0m')
            return response
        else:
            print('\33[1;33m' + 'Using Selenium' + '\33[0m')
            driver = web_driver()
    
            # Cargar la página web
            driver.get(Url)
    
            # Esperar a que la página se cargue completamente
            WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
            )  # Esperar hasta x segundos
    
            html_code = driver.page_source
    
            # Get the status code using requests library
            response = requests.get(driver.current_url)
            # driver.close()
            if response.status_code == 200:
                print("HTML code extracted successfully")
                return html_code
            else:
    
                print('\33[1;34m' + 'Using Selenium Script method' + '\33[0m')
    
                # Get the HTML content directly from the browser's DOM
                page_source = driver.execute_script("return document.body.outerHTML;")
    
                html_code = driver.page_source
    
                # Get the status code using requests library
                response = requests.get(driver.current_url)
    
                # Validate the status code
                if response.status_code == 200:
                    print("HTML code extracted successfully")
                    return html_code
                else:
                    print(f"Failed to extract HTML code")
                    return html_code
    
    if url := st.text_input(label="put the url that you want you extract the html code", value="http://example.com", max_chars=100, help="pruepa"):
    
        start_time = time()
        st.code(ExtrayendoHTML(Url=url))
        elapsed_time = time() - start_time
        st.markdown(f"### for the extraction of the html code is loaded in {elapsed_time:.2f} seconds")
