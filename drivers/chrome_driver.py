#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerenciamento do driver do Chrome para o EA FC 25 Web App Scraper
"""

import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger(__name__)

class ChromeDriverManager:
    """Gerencia a configuração e inicialização do driver do Chrome"""
    
    def __init__(self):
        self.driver = None
        self.wait = None
    
    def setup_driver(self):
        """Configura o driver do Chrome com opções otimizadas"""
        try:
            # Configurações do Chrome
            chrome_options = self._get_chrome_options()
            
            # Tenta diferentes abordagens para inicializar o driver
            self.driver = self._initialize_driver(chrome_options)
            
            if not self.driver:
                return False
            
            # Remove indicadores de automação
            self._remove_automation_indicators()
            
            # Configura wait explícito
            self.wait = WebDriverWait(self.driver, 20)
            
            logger.info("Driver do Chrome configurado com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao configurar driver: {str(e)}")
            logger.error("Verifique se o Google Chrome está instalado e atualizado")
            return False
    
    def _get_chrome_options(self):
        """Retorna as opções otimizadas do Chrome"""
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        return chrome_options
    
    def _initialize_driver(self, chrome_options):
        """Inicializa o driver usando diferentes métodos"""
        try:
            # Método 1: Usando ChromeDriverManager
            service = Service(ChromeDriverManager().install())
            return webdriver.Chrome(service=service, options=chrome_options)
        except Exception as e1:
            logger.warning(f"ChromeDriverManager falhou: {str(e1)}")
            
            try:
                # Método 2: Driver automático sem service
                return webdriver.Chrome(options=chrome_options)
            except Exception as e2:
                logger.warning(f"Driver automático falhou: {str(e2)}")
                
                try:
                    # Método 3: Usando webdriver-manager com configurações específicas
                    driver_path = ChromeDriverManager().install()
                    logger.info(f"Driver baixado em: {driver_path}")
                    
                    service = Service(driver_path)
                    return webdriver.Chrome(service=service, options=chrome_options)
                except Exception as e3:
                    logger.error(f"Todos os métodos falharam: {str(e3)}")
                    return None
    
    def _remove_automation_indicators(self):
        """Remove indicadores de automação do navegador"""
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
    
    def get_driver(self):
        """Retorna o driver configurado"""
        return self.driver
    
    def get_wait(self):
        """Retorna o WebDriverWait configurado"""
        return self.wait
    
    def close_driver(self):
        """Fecha o driver do Chrome"""
        if self.driver:
            self.driver.quit()
            logger.info("Driver do Chrome fechado")
    
    def navigate_to(self, url):
        """Navega para uma URL específica"""
        try:
            logger.info(f"Navegando para: {url}")
            self.driver.get(url)
            logger.info("Página carregada com sucesso")
            return True
        except Exception as e:
            logger.error(f"Erro ao navegar para {url}: {str(e)}")
            return False 