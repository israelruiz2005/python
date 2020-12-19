# import packages
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from parsel import Selector
import csv

# arquivo csv
writer = csv.writer(open('output.csv', 'w', encoding='utf-8'))
writer.writerow(['Nome', 'Headline', 'URL'])


# Chrome diver
driver = webdriver.Chrome('./chromedriver')

# maximizar janela
# driver.maximize_window()

# LINKEDIN

# acessar LinkedIn
driver.get('https://www.linkedin.com/')
sleep(1)

# clicar no botão de login
# driver.find_element_by_css_selector('a.nav__button-secondary').click()
#driver.find_element_by_xpath('//a[text()="Sign in"]').click()
driver.find_element_by_xpath('//a[text()="Entre"]').click()
sleep(3)

# preencher usuario
# usuario_input = driver.find_element_by_css_selector('input#username')
usuario_input = driver.find_element_by_name('session_key')
usuario_input.send_keys('seu_email_de_login_no_linkedin')

# preencher senha
senha_input = driver.find_element_by_name('session_password')
senha_input.send_keys('sua_senha')

# clicar para logar
# driver.find_element_by_css_selector("button.btn__primary--large").click()
# driver.find_element_by_xpath('//button[text()="Sign in"]').click()

senha_input.send_keys(Keys.RETURN)
sleep(3)

# GOOGLE
driver.get('https://google.com')
sleep(1)

# selecionar campo de busca
# campo_busca = driver.find_element_by_xpath('//input[@name="q"]')
busca_input = driver.find_element_by_name('q')

# fazer busca no google
busca_input.send_keys('site:linkedin.com/in/ AND "data scientist" and "Salvador"')
busca_input.send_keys(Keys.RETURN)
sleep(2)

# extrair lista de perfis
lista_perfil = driver.find_elements_by_xpath('//div[@class="yuRUbf"]/a')
lista_perfil = [perfil.get_attribute('href') for perfil in lista_perfil]

# extrair informacoes individuais
for perfil in lista_perfil:
    driver.get(perfil)
    sleep(10)

    response = Selector(text=driver.page_source)
    nome = response.xpath('//title/text()').extract_first().split(" | ")[1]
    headline = response.xpath('//h2/text()')[2].extract().strip()
    url_perfil = driver.current_url

    # escrever no arquivo csv
    writer.writerow([nome, headline, url_perfil])

# sair do driver
driver.quit()