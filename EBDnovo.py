import pandas as pd 
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

servico = Service(ChromeDriverManager().install())
tabela = pd.read_excel("CPFS.xlsx")

for i, cpf in enumerate(tabela["CPF"]):
    descricao = tabela.loc[i, "DESCRICAO"]

    navegador = webdriver.Chrome(service=servico)  # Novo objeto navegador para cada iteração
    navegador.get("https://www.igrejacristamaranata.org.br/ebd/participacoes/")

    # Espera até que o elemento de entrada do usuário esteja presente na página
    elemento_usuario = WebDriverWait(navegador, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="icmEbdNacionalForm"]/div[2]/div/div[1]/input'))
    )
    elemento_usuario.send_keys(cpf)

    # Clica no botão de participação
    navegador.find_element(By.XPATH, '//*[@id="icmEbdNacionalForm"]/div[5]/div/div[1]/input[2]').click()

    # Espera até que o campo de mensagem esteja presente na página
    elemento_mensagem = WebDriverWait(navegador, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="icmEbdNacionalForm"]/div[5]/div/div[2]/div/div[2]/div[1]/p'))
    )
    elemento_mensagem.send_keys(descricao)

    # Aceita os termos
    navegador.find_element(By.XPATH, '//*[@id="aceitoOsTermos"]').click()

    # Submete o formulário
    navegador.find_element(By.XPATH, '//*[@id="icmEbdNacionalForm"]/button').click()

    # Fecha o navegador após cada iteração
    time.sleep(4)
    navegador.quit()
