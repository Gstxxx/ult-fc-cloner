#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para Web Scraping dos Jogadores do EA FC 25 Web App
Autor: Sistema de Web Scraping
Data: 2024
"""

import time
import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import logging
from config import Config

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fc25_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class FC25Scraper:
    """
    Classe para fazer web scraping dos jogadores do EA FC 25 Web App
    """
    
    def __init__(self):
        """Inicializa o scraper com configurações do Chrome"""
        self.driver = None
        self.wait = None
        self.jogadores = []
        self.config = Config()
        
    def setup_driver(self):
        """Configura o driver do Chrome com opções otimizadas"""
        try:
            # Configurações do Chrome
            chrome_options = Options()
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Tenta diferentes abordagens para inicializar o driver
            try:
                # Método 1: Usando ChromeDriverManager
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
            except Exception as e1:
                logger.warning(f"ChromeDriverManager falhou: {str(e1)}")
                try:
                    # Método 2: Driver automático sem service
                    self.driver = webdriver.Chrome(options=chrome_options)
                except Exception as e2:
                    logger.warning(f"Driver automático falhou: {str(e2)}")
                    # Método 3: Usando webdriver-manager com configurações específicas
                    from webdriver_manager.chrome import ChromeDriverManager
                    import os
                    
                    # Força download do driver
                    driver_path = ChromeDriverManager().install()
                    logger.info(f"Driver baixado em: {driver_path}")
                    
                    service = Service(driver_path)
                    self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Remove indicadores de automação
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # Configura wait explícito
            self.wait = WebDriverWait(self.driver, 20)
            
            logger.info("Driver do Chrome configurado com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao configurar driver: {str(e)}")
            logger.error("Verifique se o Google Chrome está instalado e atualizado")
            return False
    
    def acessar_webapp(self):
        """Acessa o EA FC 25 Web App"""
        try:
            url = "https://www.ea.com/ea-sports-fc/ultimate-team/web-app/"
            logger.info(f"Acessando: {url}")
            
            self.driver.get(url)
            logger.info("Página carregada com sucesso")
            
            # Aguarda carregamento inicial
            time.sleep(5)
            return True
            
        except Exception as e:
            logger.error(f"Erro ao acessar webapp: {str(e)}")
            return False
    
    def fazer_login_automatico(self):
        """Faz login automático usando as credenciais configuradas"""
        try:
            logger.info("Tentando login automático...")
            
            # Aguarda carregamento da página de login
            time.sleep(3)
            
            # Procura pelo campo de email
            seletores_email = [
                'input[type="email"]',
                'input[name="email"]',
                'input[id*="email"]',
                'input[placeholder*="email"]',
                'input[placeholder*="Email"]'
            ]
            
            campo_email = None
            for seletor in seletores_email:
                try:
                    campo_email = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, seletor)))
                    logger.info(f"Campo de email encontrado: {seletor}")
                    break
                except TimeoutException:
                    continue
            
            if not campo_email:
                logger.warning("Campo de email não encontrado, tentando login manual")
                return False
            
            # Preenche email
            campo_email.clear()
            campo_email.send_keys(self.config.email)
            logger.info("Email preenchido")
            
            # Procura pelo campo de senha
            seletores_senha = [
                'input[type="password"]',
                'input[name="password"]',
                'input[id*="password"]',
                'input[placeholder*="password"]',
                'input[placeholder*="Password"]'
            ]
            
            campo_senha = None
            for seletor in seletores_senha:
                try:
                    campo_senha = self.driver.find_element(By.CSS_SELECTOR, seletor)
                    logger.info(f"Campo de senha encontrado: {seletor}")
                    break
                except NoSuchElementException:
                    continue
            
            if not campo_senha:
                logger.warning("Campo de senha não encontrado, tentando login manual")
                return False
            
            # Preenche senha
            campo_senha.clear()
            campo_senha.send_keys(self.config.senha)
            logger.info("Senha preenchida")
            
            # Procura pelo botão de login
            seletores_botao = [
                'button[type="submit"]',
                'button:contains("Sign In")',
                'button:contains("Login")',
                'input[type="submit"]',
                'button[id*="login"]',
                'button[id*="signin"]'
            ]
            
            botao_login = None
            for seletor in seletores_botao:
                try:
                    botao_login = self.driver.find_element(By.CSS_SELECTOR, seletor)
                    logger.info(f"Botão de login encontrado: {seletor}")
                    break
                except NoSuchElementException:
                    continue
            
            if not botao_login:
                # Tenta pressionar Enter no campo de senha
                campo_senha.send_keys(Keys.RETURN)
                logger.info("Pressionando Enter para fazer login")
            else:
                botao_login.click()
                logger.info("Botão de login clicado")
            
            # Aguarda redirecionamento ou carregamento
            time.sleep(5)
            
            # Verifica se o login foi bem-sucedido
            if self.verificar_login_sucesso():
                logger.info("✅ Login automático realizado com sucesso!")
                return True
            else:
                logger.warning("❌ Login automático falhou, tentando login manual")
                return False
                
        except Exception as e:
            logger.error(f"Erro durante login automático: {str(e)}")
            return False
    
    def verificar_login_sucesso(self):
        """Verifica se o login foi bem-sucedido"""
        try:
            # Aguarda um pouco para a página carregar
            time.sleep(3)
            
            # Verifica se ainda está na página de login
            if "login" in self.driver.current_url.lower() or "signin" in self.driver.current_url.lower():
                return False
            
            # Verifica se há elementos que indicam que está logado
            indicadores_logado = [
                '.user-profile',
                '.account-menu',
                '.logout',
                '[data-testid*="user"]',
                '.ut-navigation'
            ]
            
            for indicador in indicadores_logado:
                try:
                    elemento = self.driver.find_element(By.CSS_SELECTOR, indicador)
                    if elemento.is_displayed():
                        return True
                except NoSuchElementException:
                    continue
            
            # Se não encontrou indicadores específicos, verifica se não há campos de login
            try:
                self.driver.find_element(By.CSS_SELECTOR, 'input[type="email"]')
                return False  # Ainda na página de login
            except NoSuchElementException:
                return True  # Provavelmente logado
            
        except Exception as e:
            logger.error(f"Erro ao verificar login: {str(e)}")
            return False
    
    def aguardar_login(self):
        """Aguarda o usuário fazer login manualmente ou tenta login automático"""
        try:
            # Carrega credenciais se disponíveis
            if self.config.carregar_credenciais():
                # Tenta login automático
                if self.fazer_login_automatico():
                    logger.info("Login automático realizado com sucesso!")
                    return True
            
            # Se não conseguiu login automático, aguarda manual
            logger.info("Aguardando login manual do usuário...")
            logger.info("Por favor, faça login na sua conta EA e navegue até 'Clube > Jogadores'")
            
            # Aguarda até que o usuário confirme que está logado
            input("Pressione ENTER após fazer login e navegar para 'Clube > Jogadores'...")
            
            logger.info("Login confirmado pelo usuário")
            
            # Tenta navegar automaticamente para a página de jogadores
            if self.navegar_para_jogadores():
                logger.info("Navegação automática para jogadores realizada!")
                return True
            else:
                logger.info("Navegação automática falhou, aguardando navegação manual...")
                input("Pressione ENTER quando estiver na página 'Clube > Jogadores'...")
                return True
            
        except Exception as e:
            logger.error(f"Erro durante aguardo do login: {str(e)}")
            return False
    
    def navegar_para_jogadores(self):
        """Tenta navegar automaticamente para a página de jogadores"""
        try:
            logger.info("Tentando navegar para a página de jogadores...")
            
            # Aguarda carregamento da página principal
            time.sleep(3)
            
            # Procura por links/menus que levam ao clube
            seletores_clube = [
                'a[href*="club"]',
                'a[href*="squad"]',
                'button:contains("Club")',
                'button:contains("Clube")',
                '[data-testid*="club"]',
                '.ut-club-link',
                '.club-link'
            ]
            
            link_clube = None
            for seletor in seletores_clube:
                try:
                    link_clube = self.driver.find_element(By.CSS_SELECTOR, seletor)
                    logger.info(f"Link do clube encontrado: {seletor}")
                    break
                except NoSuchElementException:
                    continue
            
            if link_clube:
                link_clube.click()
                logger.info("Clicou no link do clube")
                time.sleep(3)
            
            # Procura por links/menus que levam aos jogadores
            seletores_jogadores = [
                'a[href*="players"]',
                'a[href*="squad"]',
                'button:contains("Players")',
                'button:contains("Jogadores")',
                '[data-testid*="players"]',
                '.ut-players-link',
                '.players-link'
            ]
            
            link_jogadores = None
            for seletor in seletores_jogadores:
                try:
                    link_jogadores = self.driver.find_element(By.CSS_SELECTOR, seletor)
                    logger.info(f"Link dos jogadores encontrado: {seletor}")
                    break
                except NoSuchElementException:
                    continue
            
            if link_jogadores:
                link_jogadores.click()
                logger.info("Clicou no link dos jogadores")
                time.sleep(3)
                return True
            
            logger.warning("Não foi possível navegar automaticamente para jogadores")
            return False
            
        except Exception as e:
            logger.error(f"Erro durante navegação automática: {str(e)}")
            return False
    
    def localizar_cards_jogadores(self):
        """Localiza todos os cards de jogadores na página"""
        try:
            # Aguarda carregamento da página
            time.sleep(2)
            
            # Seletor correto para cards de jogadores (container principal)
            seletores_cards = [
                "li.listFUTItem",
                ".listFUTItem",
                ".ut-item-view--main",
                ".ut-item-view.main",
                ".player-card",
                ".item-view"
            ]
            
            cards_encontrados = []
            
            for seletor in seletores_cards:
                try:
                    cards = self.driver.find_elements(By.CSS_SELECTOR, seletor)
                    if cards:
                        logger.info(f"Encontrados {len(cards)} cards usando seletor: {seletor}")
                        cards_encontrados = cards
                        break
                except NoSuchElementException:
                    continue
            
            if not cards_encontrados:
                # Tenta encontrar por texto que contenha informações de jogador
                logger.info("Tentando localizar jogadores por texto...")
                elementos = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Overall') or contains(text(), 'Rating')]")
                if elementos:
                    logger.info(f"Encontrados {len(elementos)} elementos com informações de jogador")
                    cards_encontrados = elementos
            
            return cards_encontrados
            
        except Exception as e:
            logger.error(f"Erro ao localizar cards de jogadores: {str(e)}")
            return []
    
    def ir_proxima_pagina(self):
        """Navega para a próxima página de jogadores"""
        try:
            # Aguarda um pouco para garantir que a página carregou
            time.sleep(2)
            
            # Procura pelo botão "Próxima"
            seletores_proxima = [
                'button.pagination.next',
                'button.flat.pagination.next',
                '.pagination .next',
                'button:contains("Próxima")',
                'button:contains("Next")',
                '[data-testid*="next"]',
                '.next-page',
                '.pagination-next'
            ]
            
            botao_proxima = None
            for seletor in seletores_proxima:
                try:
                    botao_proxima = self.driver.find_element(By.CSS_SELECTOR, seletor)
                    if botao_proxima.is_displayed() and botao_proxima.is_enabled():
                        logger.info(f"Botão 'Próxima' encontrado: {seletor}")
                        break
                except NoSuchElementException:
                    continue
            
            if botao_proxima:
                # Rola até o botão para garantir que está visível
                self.driver.execute_script("arguments[0].scrollIntoView(true);", botao_proxima)
                time.sleep(1)
                
                # Clica no botão
                botao_proxima.click()
                logger.info("Clicou no botão 'Próxima'")
                
                # Aguarda carregamento da nova página
                time.sleep(3)
                return True
            else:
                logger.info("Botão 'Próxima' não encontrado ou não está visível")
                return False
                
        except Exception as e:
            logger.error(f"Erro ao navegar para próxima página: {str(e)}")
            return False
    
    def extrair_dados_jogador(self, card):
        """Extrai dados de um jogador individual"""
        try:
            jogador = {
                'Nome': 'N/A',
                'Overall': 'N/A',
                'Posição': 'N/A',
                'Clube': 'N/A',
                'Rating': 'N/A'
            }
            
            # Extrai nome do jogador
            try:
                # Seletor correto para nome baseado na estrutura HTML
                seletores_nome = [
                    '.name',  # Seletor principal encontrado no HTML
                    '.name.untradeable',
                    '.player-name', 
                    '.ut-player-name', 
                    '[data-testid*="name"]',
                    '.ut-item-name',
                    '.item-name'
                ]
                for seletor in seletores_nome:
                    try:
                        nome_element = card.find_element(By.CSS_SELECTOR, seletor)
                        if nome_element.text.strip():
                            jogador['Nome'] = nome_element.text.strip()
                            break
                    except NoSuchElementException:
                        continue
                
                # Se não encontrou por seletor, tenta por texto
                if jogador['Nome'] == 'N/A':
                    texto_completo = card.text
                    # Procura por padrões de nome (primeira linha geralmente é o nome)
                    linhas = texto_completo.split('\n')
                    for linha in linhas:
                        linha = linha.strip()
                        # Ignora linhas que são apenas números ou muito curtas
                        if (len(linha) > 2 and 
                            not linha.isdigit() and 
                            not linha in ['GK', 'CB', 'LB', 'RB', 'CDM', 'CM', 'CAM', 'LM', 'RM', 'LW', 'RW', 'ST', 'CF']):
                            jogador['Nome'] = linha
                            break
                
            except Exception as e:
                logger.warning(f"Erro ao extrair nome: {str(e)}")
            
            # Extrai overall/rating
            try:
                seletores_overall = ['.rating', '.overall', '.ut-rating', '[data-testid*="rating"]']
                for seletor in seletores_overall:
                    try:
                        overall_element = card.find_element(By.CSS_SELECTOR, seletor)
                        if overall_element.text.strip():
                            jogador['Overall'] = overall_element.text.strip()
                            break
                    except NoSuchElementException:
                        continue
                
                # Se não encontrou por seletor, procura por números no texto
                if jogador['Overall'] == 'N/A':
                    texto_completo = card.text
                    import re
                    numeros = re.findall(r'\b\d{2,3}\b', texto_completo)
                    if numeros:
                        # Assume que o primeiro número de 2-3 dígitos é o overall
                        jogador['Overall'] = numeros[0]
                
            except Exception as e:
                logger.warning(f"Erro ao extrair overall: {str(e)}")
            
            # Extrai posição
            try:
                seletores_posicao = ['.position', '.ut-position', '[data-testid*="position"]']
                for seletor in seletores_posicao:
                    try:
                        posicao_element = card.find_element(By.CSS_SELECTOR, seletor)
                        if posicao_element.text.strip():
                            jogador['Posição'] = posicao_element.text.strip()
                            break
                    except NoSuchElementException:
                        continue
                
                # Se não encontrou por seletor, procura por posições conhecidas no texto
                if jogador['Posição'] == 'N/A':
                    texto_completo = card.text
                    posicoes = ['GK', 'CB', 'LB', 'RB', 'CDM', 'CM', 'CAM', 'LM', 'RM', 'LW', 'RW', 'ST', 'CF']
                    for pos in posicoes:
                        if pos in texto_completo:
                            jogador['Posição'] = pos
                            break
                
            except Exception as e:
                logger.warning(f"Erro ao extrair posição: {str(e)}")
            
            # Extrai clube/time
            try:
                seletores_clube = ['.club', '.team', '.ut-club', '[data-testid*="club"]']
                for seletor in seletores_clube:
                    try:
                        clube_element = card.find_element(By.CSS_SELECTOR, seletor)
                        if clube_element.text.strip():
                            jogador['Clube'] = clube_element.text.strip()
                            break
                    except NoSuchElementException:
                        continue
                
            except Exception as e:
                logger.warning(f"Erro ao extrair clube: {str(e)}")
            
            # Copia overall para rating se rating estiver vazio
            if jogador['Rating'] == 'N/A' and jogador['Overall'] != 'N/A':
                jogador['Rating'] = jogador['Overall']
            
            return jogador
            
        except Exception as e:
            logger.error(f"Erro ao extrair dados do jogador: {str(e)}")
            return {
                'Nome': 'Erro',
                'Overall': 'N/A',
                'Posição': 'N/A',
                'Clube': 'N/A',
                'Rating': 'N/A'
            }
    
    def coletar_dados_jogadores(self):
        """Coleta dados de todos os jogadores usando paginação"""
        try:
            logger.info("Iniciando coleta de dados dos jogadores...")
            
            pagina_atual = 1
            max_paginas = 50  # Limite de segurança
            
            while pagina_atual <= max_paginas:
                logger.info(f"Processando página {pagina_atual}...")
                
                # Localiza cards da página atual
                cards = self.localizar_cards_jogadores()
                
                if not cards:
                    logger.warning(f"Nenhum card de jogador encontrado na página {pagina_atual}")
                    break
                
                logger.info(f"Encontrados {len(cards)} jogadores na página {pagina_atual}")
                
                # Processa todos os jogadores da página atual
                for i, card in enumerate(cards):
                    try:
                        indice_global = len(self.jogadores) + 1
                        logger.info(f"Processando jogador {indice_global} (página {pagina_atual}, posição {i+1})")
                        
                        # Rola até o card para garantir que está visível
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", card)
                        time.sleep(0.5)
                        
                        jogador = self.extrair_dados_jogador(card)
                        
                        # Só adiciona se tem dados válidos
                        if (jogador['Nome'] != 'Erro' and 
                            jogador['Nome'] != 'N/A' and 
                            jogador['Overall'] != 'N/A' and
                            jogador['Overall'].strip() != ''):
                            
                            self.jogadores.append(jogador)
                            logger.info(f"Jogador coletado: {jogador['Nome']} - {jogador['Overall']}")
                        else:
                            logger.info(f"Card ignorado - dados insuficientes")
                        
                    except Exception as e:
                        logger.error(f"Erro ao processar card {indice_global}: {str(e)}")
                        continue
                
                # Tenta ir para a próxima página
                if not self.ir_proxima_pagina():
                    logger.info("Não há mais páginas ou botão 'Próxima' não encontrado")
                    break
                
                pagina_atual += 1
                
                # Aguarda carregamento da nova página
                time.sleep(3)
            
            logger.info(f"Coleta concluída. Total de jogadores coletados: {len(self.jogadores)}")
            return True
            
        except Exception as e:
            logger.error(f"Erro durante coleta de dados: {str(e)}")
            return False
    
    def exportar_csv(self, filename="jogadores_fc25.csv"):
        """Exporta os dados coletados para CSV"""
        try:
            if not self.jogadores:
                logger.warning("Nenhum jogador para exportar")
                return False
            
            # Cria DataFrame
            df = pd.DataFrame(self.jogadores)
            
            # Exporta para CSV
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            
            logger.info(f"Dados exportados com sucesso para {filename}")
            logger.info(f"Total de jogadores exportados: {len(self.jogadores)}")
            
            # Mostra preview dos dados
            print("\n" + "="*50)
            print("PREVIEW DOS DADOS COLETADOS:")
            print("="*50)
            print(df.head(10).to_string(index=False))
            print("="*50)
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao exportar CSV: {str(e)}")
            return False
    
    def executar_scraping(self):
        """Executa o processo completo de scraping"""
        try:
            logger.info("Iniciando processo de scraping do EA FC 25 Web App")
            
            # 1. Configura driver
            if not self.setup_driver():
                return False
            
            # 2. Acessa webapp
            if not self.acessar_webapp():
                return False
            
            # 3. Aguarda login manual
            if not self.aguardar_login():
                return False
            
            # 4. Coleta dados dos jogadores
            if not self.coletar_dados_jogadores():
                return False
            
            # 5. Exporta para CSV
            if not self.exportar_csv():
                return False
            
            logger.info("Processo de scraping concluído com sucesso!")
            return True
            
        except Exception as e:
            logger.error(f"Erro durante execução do scraping: {str(e)}")
            return False
        
        finally:
            # Limpa credenciais da memória
            self.config.limpar_credenciais()
            
            if self.driver:
                logger.info("Fechando navegador...")
                self.driver.quit()

def main():
    """Função principal"""
    print("="*60)
    print("SCRAPER EA FC 25 WEB APP")
    print("="*60)
    print("Este script irá:")
    print("1. Abrir o navegador Chrome")
    print("2. Acessar o EA FC 25 Web App")
    print("3. Aguardar seu login manual")
    print("4. Coletar dados dos jogadores do seu clube")
    print("5. Exportar para jogadores_fc25.csv")
    print("="*60)
    
    scraper = FC25Scraper()
    sucesso = scraper.executar_scraping()
    
    if sucesso:
        print("\n✅ Scraping concluído com sucesso!")
        print("📁 Arquivo gerado: jogadores_fc25.csv")
    else:
        print("\n❌ Erro durante o scraping. Verifique os logs para mais detalhes.")
    
    input("\nPressione ENTER para sair...")

if __name__ == "__main__":
    main() 