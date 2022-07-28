<p align="center">
  <img width="1000" height="300" src="https://cynoteck.com/wp-content/uploads/2019/07/what-is-selenium-cover.jpg" >
</p>

# Problema de negócio
A área de RH (recursos humanos) deseja automatizar o processo de busca e seleção de novos empregados.

# Resumo
Dando ênfase na automação de processos, a aplicação é utilizada para facilitar a descoberta de perfis e vagas em
determinada área de conhecimento e localidade fornecida pelo usuário.

# Introdução
A aplicação dá a liberdade para o usuário pesquisar a área de conhecimento, localidade e escolher o site desejado para
que os filtros sejam aplicados no framework Selenium, onde os dados da página de pesquisa serão coletados, armazenados
em uma lista que será transformada em um dataframe para que, assim, sejam carregados na aplicação web compartilhável.

# Sobre o código
## Instalando os requerimentos
```
pip install pandas
```

```
pip install selenium
```

```
pip install streamlit
```

```
pip install webdriver-manager
```
## Imports

```python
#Conduz um navegador, em específico, como um usuário faria. O navegador que será utilizado para esse código será o Chrome
#(A escolha de navegadores pode ser aumentada futuramente).
from selenium import webdriver
```

```python
#Com o webdriver_manager, a tarefa de instalar um driver do seu navegador para poder utilizar o selenium passou a ser
#desnecessária. Além de que, se uma nova versão do driver fosse lançada, a versão instalada não poderia ser mais usada.
from webdriver_manager.chrome import ChromeDriverManager
```


```python
#O Service gerencia o início e a parada do driver e fornece um caminho para que o mesmo seja executado.
from selenium.webdriver.chrome.service import Service
```

```python
#O By fornece escolhas para localizar elementos de uma página web. Esses elementos sendo: XPATH, NAME, ID, 
#CSS, CLASS, LINK TEXT e TAG NAME
from selenium.webdriver.common.by import By
```

```python
#A classe Keys possibilita a execução de comandos das teclas no teclado como RETURN, F1, ALT etc
from selenium.webdriver.common.keys import Keys
```

```python
#A biblioteca pandas, nesse código em questão, será utilizada para converter lista em dataframe
import pandas as pd
```

```python
#Transformar o script de dados em um aplicativo web compartilhável 
import streamlit as st
```

## Corpo do código
```python
#Lista de sites que poderão ser escolhidos pelos usuários por meio do web app (A aplicação da lista de 
#de escolha se dá pela variável site.
options_site = ['github.com', 'linkedin.com/in', 'facebook.com', 'instagram.com']
site = st.sidebar.selectbox('Site', options=options_site)
#Fornece a escolha, escrita, pelos usuários, da área de conhecimento e localidade.
area = st.sidebar.text_input('Área de conhecimento')
locality = st.sidebar.text_input('Localidade desejada')
```

```python
#A coleta de dados só é iniciada se a área e a localidade tenham informação
if (area != '') & (locality != ''):
    #Lista vazia que receberá o link de todos os perfis e vagas
    lista_perfil = []
    #options serve para que o navegador não seja aberto durante a coleta dos dados
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    #service faz com que não seja necessária a instalação do driver
    service = Service(ChromeDriverManager().install())
    #Variável utilizada para iniciar o processo de coleta por meio do chrome
    navigator = webdriver.Chrome(service=service, options=options)
```

```python
    #Ordena que a máquina vá para o site google.com e pesquise o que foi desejado pelo usuário
    navigator.get("https://google.com.br")
    search = navigator.find_element(by=By.NAME, value='q')
    search.send_keys(f'site:{site} AND "{area}" AND "{locality}"')
    search.send_keys(Keys.ENTER)
```

```python
    #O laço é utilizado para que a aplicação pegue no máximo 30 links
    for c in range(1, 4):
        #A utilização do try/except se dá pelo fato de que algumas pesquisas não chegam às 3 abas solicitadas no laço
        try:
            perfis = navigator.find_elements(by=By.XPATH, value='//div[@class="yuRUbf"]/a')
            for perfil in perfis:
                #As vezes acabava por aparecer links de anúncios quando fazia algum requerimento, então essa condição é 
                #para que apenas sejam retornados os valores que tenham o link do site requisitado em seu corpo
                if site in perfil.get_attribute('href'):
                    #Insere todos os links dentro da lista 'lista_perfil'
                    lista_perfil.append(perfil.get_attribute('href'))
            #utilizado para que a máquina avance a página de pesquisa
            navigator.find_element(by=By.XPATH, value='//*[@id="pnnext"]/span[2]').click()
        except:
            break
```

```python
    #Transforma 'lista_perfil' em um dataframe para que seja demonstrado no web app
    dataframe_perfil = pd.DataFrame(lista_perfil)
    dataframe_perfil.rename(columns={0: 'Perfis'}, inplace=True)
    #Finaliza o processo da coleta de dados
    navigator.quit()
    #Demonstração dos dados coletado no web app
    st.title('Lista de perfis encontrados')
    st.sidebar.info(f'Total de {len(dataframe_perfil)} perfis encontrados')
    st.dataframe(dataframe_perfil)
```
