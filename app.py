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

st.set_page_config(page_title="Selenium Web App", page_icon="🌠", layout="wide", initial_sidebar_state="collapsed")
st.title('🎁 Selenium App To Extract The text', anchor=False)

with st.sidebar:
    st.title('🤗💬 Selenium App')
    '## Settings of the Driver'
    Agents = {'Chrome Windows 10': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.159 Safari/537.36",
              'Chrome macOS': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.159 Safari/537.36",
               'Firefox Windows 10': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
                'Firefox macOS': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
                'Edge Windows 10': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.159 Safari/537.36 Edg/91.0.864.37",
                'Safari iPhone': "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
                'Safari Android': "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.159 Mobile Safari/537.36"}
    lista = list(Agents.keys())
    # Agentes=["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.49 Safari/537.36",
    #         "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0",
    #         "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36",
    #         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
    #         "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    #         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.37"]
    st.session_state['User_Agent'] = Agents.get(st.selectbox('🔌 User Agents', lista, index=0))
    '---'
    '## Settings to Extract Data'
    modo = ['Auto', 'BeautifulSoup', 'Selenium', 'SeleniumScript']
    st.session_state['mode'] = st.selectbox('Select the mode that you wanna look', modo, index=0)
    st.session_state['delay'] = st.number_input("Insert a number", value=10, placeholder="Type a number...", step=10, min_value=10, max_value=60)

@st.cache_resource
def webdriver(user_agent:str = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.49 Safari/537.36'):
    start_time = time()
    if (platform.system() == "Windows"):
        options = Options()
        chrome_service = fs.Service(executable_path=ChromeDriverManager().install())
    else:
        options = Options()
        ua = user_agent
        options.add_argument('--user-agent=' + ua)
        options.add_argument("--headless")
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--enable-javascript")
        options.add_argument("--enable-cookies")
        options.add_argument('--disable-dev-shm-usage')
        chrome_service = fs.Service(executable_path=ChromeDriverManager(chrome_type= ChromeType.CHROMIUM).install())

    browser = WebDriver(options=options,service=chrome_service)
    elapsed_time = time() - start_time
    return elapsed_time, browser

elapsed_time, driver = webdriver(user_agent=st.session_state.get('User_Agent'))
st.write(f"Chrome-driver loaded in {elapsed_time:.2f} seconds")  

import requests
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
    
@st.cache_data
def ExtrayendoHTML(Url: str, mode:str= 'Auto', delay:int= 20, driver=driver):
    response = requests.get(Url)
    # Check if the request was successful (status code 200)
    if response.status_code == 200 and mode=='Auto' or mode=='BeautifulSoup':
        result= 'Using BeautifulSoup'
        print('\33[1;32m' + result + '\33[0m')
        return result, response.text
    else:
        result= 'Using Selenium'
        print('\33[1;33m' + result + '\33[0m')

        # Cargar la página web
        driver.get(Url)

        driver.set_page_load_timeout(delay)

        driver.implicitly_wait(delay)

        # Esperar a que la página se cargue completamente
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.TAG_NAME, "body")))  # Esperar hasta x segundos

        html_code = driver.page_source

        # Get the status code using requests library
        response = requests.get(driver.current_url)
        if response.status_code == 200 and mode=='Auto' or mode=='Selenium':
            result= result + ": HTML code extracted successfully"
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
            if response.status_code == 200 and mode== 'Auto' or mode=='SeleniumScript':
                result= result + ": HTML code extracted successfully"
                print(result)
                return result, html_code
            else:
                result= result + ": Failed to extract HTML code"
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
    result, html = ExtrayendoHTML(Url=Url, mode=st.session_state.get('mode'), delay=st.session_state.get('delay'))
    st.markdown(result)
    st.markdown(f'#### {driver.capabilities["browserVersion"]}')
    with st.expander("📚 Codigo Fuente "):
        st.code(html)
    with st.spinner('extracting the text from html'):
        with st.expander('Getting the Text'):
            st.markdown(getext(html=html))
    elapsed_time = time() - start_time
    st.markdown(f"**Number of open windows: :red[{len(driver.window_handles)}]**")
    st.markdown(f"### for the extraction of the html code is loaded in {elapsed_time:.2f} seconds")