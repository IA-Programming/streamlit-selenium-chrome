import streamlit as st
import platform
from time import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome import service as fs
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.core.os_manager import ChromeType

st.set_page_config(page_title="Selenium Web App", page_icon="🌠", layout="wide")
st.title('🎁 Selenium App To Extract The text', anchor=False)

@st.cache_resource
def webdriver():
    if (platform.system() == "Windows"):
        options = Options()
        chrome_service = fs.Service(executable_path=ChromeDriverManager().install())
    else:
        options = Options()
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        options.add_argument('--user-agent=' + ua)
        options.add_argument("--headless")
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        chrome_service = fs.Service(executable_path=ChromeDriverManager(chrome_type= ChromeType.CHROMIUM).install())

    browser = WebDriver(options=options,service=chrome_service)

    return browser

start_time = time()
driver = webdriver()
elapsed_time = time() - start_time
st.write(f"Chrome-driver loaded in {elapsed_time:.2f} seconds")  

import requests
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

@st.cache_data
def getext(html):
    if isinstance(html, str):
        soup = BeautifulSoup(html, 'html.parser')
    else:
        soup = html
    text = soup.get_text(separator=" ")
    return text

if Url:= st.text_input(label='Put here your Url', value='http://example.com', max_chars= 100, help='here can you put an url to get the html code'):
    start_time = time()
    result, html = ExtrayendoHTML(Url=Url)
    st.markdown(result)
    with st.expander("📚 Codigo Fuente "):
        st.code(html)
    with st.expander('Getting the Text'):
        st.markdown(getext(html=html))
    elapsed_time = time() - start_time
    st.markdown(f"### for the extraction of the html code is loaded in {elapsed_time:.2f} seconds")