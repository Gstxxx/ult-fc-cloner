#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Navegação no EA FC 25 Web App
"""

import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException

logger = logging.getLogger(__name__)

class NavigationManager:
    """Gerencia a navegação no EA FC 25 Web App"""
    
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
    
    def navegar_para_jogadores(self):
        """Navega para a página de jogadores do clube"""
        try:
            logger.info("Navegando para página de jogadores...")
            
            # Tenta navegação automática primeiro
            if self._navegacao_automatica():
                return True
            
            # Se falhar, tenta navegação manual
            logger.info("Navegação automática falhou, tentando manual...")
            return self._navegacao_manual()
            
        except Exception as e:
            logger.error(f"Erro ao navegar para jogadores: {str(e)}")
            return False
    
    def _navegacao_automatica(self):
        """Tenta navegação automática para a página de jogadores"""
        try:
            # Aguarda carregamento do hub
            time.sleep(3)
            
            # Tenta clicar no botão Club
            seletores_club = [
                'button.ut-tab-bar-item.icon-club',
                'button[data-testid="club-tab"]',
                'a[href*="club"]',
                'button:contains("Club")'
            ]
            
            for seletor in seletores_club:
                try:
                    botao_club = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, seletor)))
                    botao_club.click()
                    logger.info("Botão Club clicado")
                    break
                except (TimeoutException, ElementClickInterceptedException):
                    continue
            else:
                logger.warning("Botão Club não encontrado")
                return False
            
            # Aguarda carregamento da página do clube
            time.sleep(2)
            
            # Tenta clicar no tile Players
            seletores_players = [
                'div.players-tile',
                'div[data-testid="players-tile"]',
                'a[href*="players"]',
                'div:contains("Players")'
            ]
            
            for seletor in seletores_players:
                try:
                    tile_players = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, seletor)))
                    tile_players.click()
                    logger.info("Tile Players clicado")
                    break
                except (TimeoutException, ElementClickInterceptedException):
                    continue
            else:
                logger.warning("Tile Players não encontrado")
                return False
            
            # Aguarda carregamento da página de jogadores
            time.sleep(3)
            
            # Verifica se chegou na página correta
            if self._verificar_pagina_jogadores():
                logger.info("Navegação automática bem-sucedida")
                return True
            else:
                logger.warning("Não chegou na página de jogadores")
                return False
                
        except Exception as e:
            logger.error(f"Erro na navegação automática: {str(e)}")
            return False
    
    def _navegacao_manual(self):
        """Instruções para navegação manual"""
        try:
            print("\n" + "="*50)
            print("NAVEGAÇÃO MANUAL REQUERIDA")
            print("="*50)
            print("1. Clique em 'Club' na barra de navegação")
            print("2. Clique em 'Players' no hub do clube")
            print("3. Aguarde carregar a lista de jogadores")
            print("4. Pressione ENTER quando estiver pronto")
            print("="*50)
            
            input("Pressione ENTER quando estiver na página de jogadores...")
            
            # Verifica se chegou na página correta
            if self._verificar_pagina_jogadores():
                logger.info("Navegação manual bem-sucedida")
                return True
            else:
                logger.warning("Página de jogadores não detectada")
                return False
                
        except KeyboardInterrupt:
            logger.info("Navegação manual cancelada pelo usuário")
            return False
    
    def _verificar_pagina_jogadores(self):
        """Verifica se está na página de jogadores"""
        seletores_verificacao = [
            'h1:contains("Players")',
            'div.players-list',
            'ul.listFUTItem',
            'div[data-testid="players-list"]'
        ]
        
        for seletor in seletores_verificacao:
            try:
                elemento = self.driver.find_element(By.CSS_SELECTOR, seletor)
                if elemento.is_displayed():
                    logger.info(f"Página de jogadores confirmada: {seletor}")
                    return True
            except NoSuchElementException:
                continue
        
        return False
    
    def ir_proxima_pagina(self):
        """Vai para a próxima página de jogadores"""
        try:
            # Procura pelo botão "Próxima"
            seletores_proxima = [
                'button.pagination.next',
                'button.flat.pagination.next',
                'button[aria-label="Next"]',
                'button:contains("Next")',
                'a.pagination.next'
            ]
            
            for seletor in seletores_proxima:
                try:
                    botao_proxima = self.driver.find_element(By.CSS_SELECTOR, seletor)
                    
                    # Verifica se o botão está habilitado
                    if botao_proxima.is_enabled() and botao_proxima.is_displayed():
                        # Rola até o botão
                        self.driver.execute_script("arguments[0].scrollIntoView();", botao_proxima)
                        time.sleep(1)
                        
                        # Clica no botão
                        botao_proxima.click()
                        logger.info("Botão Próxima clicado")
                        
                        # Aguarda carregamento da nova página
                        time.sleep(3)
                        return True
                        
                except (NoSuchElementException, ElementClickInterceptedException):
                    continue
            
            logger.info("Botão Próxima não encontrado ou não habilitado - fim das páginas")
            return False
            
        except Exception as e:
            logger.error(f"Erro ao ir para próxima página: {str(e)}")
            return False 