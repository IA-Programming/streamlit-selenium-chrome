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
        end_time = time()
        elapsed_time = end_time - start_time
        st.write(f"Chrome-driver loaded in {elapsed_time:.4f} seconds")
        return driver
    
    driver = get_driver()
    driver.get("http://example.com")

    st.code(driver.page_source)
