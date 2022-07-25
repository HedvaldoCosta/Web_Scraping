import streamlit as st
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd


options_site = ['github.com', 'linkedin.com/in']
site = st.selectbox('Site', options=options_site)
area = st.text_input('Área de conhecimento')
locality = st.text_input('Localidade desejada')
if (area != '') & (locality != ''):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    navigator = webdriver.Chrome(service=service, options=options)

    navigator.get("https://google.com.br")
    search = navigator.find_element(by=By.NAME, value='q')
    search.send_keys(f'site:{site} AND "{area}" AND "{locality}"')
    search.send_keys(Keys.ENTER)

    lista_perfis = navigator.find_elements(by=By.XPATH, value='//div[@class="yuRUbf"]/a')
    perfis = [perfil.get_attribute('href') for perfil in lista_perfis if site in perfil.get_attribute('href')]
    dataframe_perfil = pd.DataFrame(perfis)
    dataframe_perfil.rename(columns={0: 'Perfis'}, inplace=True)
    navigator.quit()

    st.dataframe(dataframe_perfil)

