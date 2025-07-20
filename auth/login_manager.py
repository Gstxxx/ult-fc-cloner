#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerenciamento de autenticação para o EA FC 25 Web App Scraper
Versão simplificada - apenas login manual
"""

import time
import logging

logger = logging.getLogger(__name__)

class LoginManager:
    """Gerencia o processo de login manual no EA FC 25 Web App"""
    
    def __init__(self, driver, wait, config):
        self.driver = driver
        self.wait = wait
        self.config = config
    
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
    
    def verificar_login_sucesso(self):
        """Verifica se o login foi bem-sucedido"""
        try:
            # Aguarda um pouco para o login processar
            time.sleep(3)
            
            # Verifica se há elementos que indicam sucesso
            seletores_sucesso = [
                'div.ut-tab-bar',
                'div.hub-container',
                'div.ut-navigation',
                'div.players-list',
                'ul.listFUTItem'
            ]
            
            for seletor in seletores_sucesso:
                try:
                    elemento = self.driver.find_element_by_css_selector(seletor)
                    if elemento.is_displayed():
                        logger.info("Login bem-sucedido - elementos do hub encontrados")
                        return True
                except:
                    continue
            
            logger.info("Login parece ter sido bem-sucedido")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao verificar login: {str(e)}")
            return False 