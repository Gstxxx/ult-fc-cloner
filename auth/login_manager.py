#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerenciamento de autenticação para o EA FC 25 Web App Scraper
"""

import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys

logger = logging.getLogger(__name__)

class LoginManager:
    """Gerencia o processo de login no EA FC 25 Web App"""
    
    def __init__(self, driver, wait, config):
        self.driver = driver
        self.wait = wait
        self.config = config
    
    def fazer_login_automatico(self):
        """Faz login automático usando as credenciais configuradas"""
        try:
            logger.info("Tentando login automático...")
            
            # Aguarda carregamento da página de login
            time.sleep(3)
            
            # Procura e preenche campo de email
            campo_email = self._encontrar_campo_email()
            if not campo_email:
                logger.warning("Campo de email não encontrado, tentando login manual")
                return False
            
            # Procura e preenche campo de senha
            campo_senha = self._encontrar_campo_senha()
            if not campo_senha:
                logger.warning("Campo de senha não encontrado, tentando login manual")
                return False
            
            # Tenta fazer login
            return self._tentar_login(campo_senha)
            
        except Exception as e:
            logger.error(f"Erro durante login automático: {str(e)}")
            return False
    
    def _encontrar_campo_email(self):
        """Encontra e preenche o campo de email"""
        seletores_email = [
            'input[type="email"]',
            'input[name="email"]',
            'input[id*="email"]',
            'input[placeholder*="email"]',
            'input[placeholder*="Email"]'
        ]
        
        for seletor in seletores_email:
            try:
                campo_email = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, seletor)))
                logger.info(f"Campo de email encontrado: {seletor}")
                
                # Preenche email
                campo_email.clear()
                campo_email.send_keys(self.config.email)
                logger.info("Email preenchido")
                return campo_email
                
            except TimeoutException:
                continue
        
        return None
    
    def _encontrar_campo_senha(self):
        """Encontra e preenche o campo de senha"""
        seletores_senha = [
            'input[type="password"]',
            'input[name="password"]',
            'input[id*="password"]',
            'input[placeholder*="password"]',
            'input[placeholder*="Password"]'
        ]
        
        for seletor in seletores_senha:
            try:
                campo_senha = self.driver.find_element(By.CSS_SELECTOR, seletor)
                logger.info(f"Campo de senha encontrado: {seletor}")
                
                # Preenche senha
                campo_senha.clear()
                campo_senha.send_keys(self.config.senha)
                logger.info("Senha preenchida")
                return campo_senha
                
            except NoSuchElementException:
                continue
        
        return None
    
    def _tentar_login(self, campo_senha):
        """Tenta fazer login clicando no botão ou pressionando Enter"""
        seletores_botao = [
            'button[type="submit"]',
            'button:contains("Sign In")',
            'button:contains("Login")',
            'input[type="submit"]',
            'button[id*="login"]',
            'button[id*="signin"]'
        ]
        
        for seletor in seletores_botao:
            try:
                botao_login = self.driver.find_element(By.CSS_SELECTOR, seletor)
                logger.info(f"Botão de login encontrado: {seletor}")
                botao_login.click()
                logger.info("Botão de login clicado")
                return True
                
            except NoSuchElementException:
                continue
        
        # Se não encontrou botão, tenta pressionar Enter
        campo_senha.send_keys(Keys.RETURN)
        logger.info("Pressionando Enter para fazer login")
        return True
    
    def verificar_login_sucesso(self):
        """Verifica se o login foi bem-sucedido"""
        try:
            # Aguarda um pouco para o login processar
            time.sleep(5)
            
            # Verifica se ainda está na página de login
            seletores_login = [
                'input[type="email"]',
                'input[type="password"]',
                'form[action*="login"]',
                'div.login-container'
            ]
            
            for seletor in seletores_login:
                try:
                    elemento = self.driver.find_element(By.CSS_SELECTOR, seletor)
                    if elemento.is_displayed():
                        logger.warning("Ainda na página de login - login pode ter falhado")
                        return False
                except NoSuchElementException:
                    continue
            
            # Verifica se há elementos que indicam sucesso
            seletores_sucesso = [
                'div.ut-tab-bar',
                'div.hub-container',
                'div.ut-navigation'
            ]
            
            for seletor in seletores_sucesso:
                try:
                    elemento = self.driver.find_element(By.CSS_SELECTOR, seletor)
                    if elemento.is_displayed():
                        logger.info("Login bem-sucedido - elementos do hub encontrados")
                        return True
                except NoSuchElementException:
                    continue
            
            logger.info("Login parece ter sido bem-sucedido")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao verificar login: {str(e)}")
            return False
    
    def aguardar_login(self):
        """Aguarda o usuário fazer login manualmente"""
        try:
            print("\n" + "="*50)
            print("LOGIN MANUAL REQUERIDO")
            print("="*50)
            print("1. Faça login na sua conta EA no navegador")
            print("2. Navegue até 'Clube > Jogadores'")
            print("3. Pressione ENTER quando estiver pronto")
            print("="*50)
            
            input("Pressione ENTER quando estiver na página de jogadores...")
            logger.info("Usuário confirmou que está pronto")
            return True
            
        except KeyboardInterrupt:
            logger.info("Login manual cancelado pelo usuário")
            return False 