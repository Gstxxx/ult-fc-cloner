#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scraping de jogadores do EA FC 25 Web App
"""

import time
import logging
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

logger = logging.getLogger(__name__)

class PlayerScraper:
    """Scraper principal para jogadores do EA FC 25"""
    
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
        self.jogadores = []
    
    def localizar_cards_jogadores(self):
        """Localiza todos os cards de jogadores na página atual"""
        try:
            # Aguarda carregamento dos cards
            time.sleep(2)
            
            # Procura pelos cards de jogadores
            seletores_cards = [
                'li.listFUTItem',
                'div.ut-item-view',
                'div.player-card',
                'li[data-testid="player-card"]'
            ]
            
            cards = []
            for seletor in seletores_cards:
                try:
                    cards = self.driver.find_elements(By.CSS_SELECTOR, seletor)
                    if cards:
                        logger.info(f"Encontrados {len(cards)} cards com seletor: {seletor}")
                        break
                except NoSuchElementException:
                    continue
            
            if not cards:
                logger.warning("Nenhum card de jogador encontrado")
                return []
            
            # Filtra apenas cards válidos (com dados)
            cards_validos = []
            for card in cards:
                if self._card_valido(card):
                    cards_validos.append(card)
            
            logger.info(f"Cards válidos encontrados: {len(cards_validos)}")
            return cards_validos
            
        except Exception as e:
            logger.error(f"Erro ao localizar cards: {str(e)}")
            return []
    
    def _card_valido(self, card):
        """Verifica se o card contém dados válidos"""
        try:
            # Verifica se tem nome do jogador
            seletores_nome = ['.name', '.player-name', '[data-testid="player-name"]']
            for seletor in seletores_nome:
                try:
                    nome = card.find_element(By.CSS_SELECTOR, seletor)
                    if nome.text.strip():
                        return True
                except NoSuchElementException:
                    continue
            
            return False
            
        except Exception:
            return False
    
    def extrair_dados_jogador(self, card):
        """Extrai dados de um jogador específico"""
        try:
            jogador = {}
            
            # Dados básicos
            jogador.update(self._extrair_dados_basicos(card))
            
            # Dados expandidos
            jogador.update(self._extrair_dados_expandidos(card))
            
            # Estatísticas detalhadas
            jogador.update(self._extrair_estatisticas(card))
            
            # Traits
            jogador.update(self._extrair_traits(card))
            
            # Valida dados obrigatórios
            if self._validar_dados_jogador(jogador):
                return jogador
            else:
                logger.warning(f"Dados inválidos para jogador: {jogador.get('nome', 'N/A')}")
                return None
                
        except Exception as e:
            logger.error(f"Erro ao extrair dados do jogador: {str(e)}")
            return None
    
    def _extrair_dados_basicos(self, card):
        """Extrai dados básicos do jogador"""
        dados = {}
        
        # Nome
        seletores_nome = ['.name', '.player-name', '[data-testid="player-name"]']
        dados['nome'] = self._extrair_texto(card, seletores_nome)
        
        # Overall/Rating
        seletores_overall = ['.rating', '.overall', '[data-testid="player-rating"]']
        dados['overall'] = self._extrair_texto(card, seletores_overall)
        dados['rating'] = dados['overall']  # Mesmo valor
        
        # Posição
        seletores_posicao = ['.position', '.player-position', '[data-testid="player-position"]']
        dados['posicao'] = self._extrair_texto(card, seletores_posicao)
        
        # Clube
        seletores_clube = ['.club', '.team', '[data-testid="player-club"]']
        dados['clube'] = self._extrair_texto(card, seletores_clube)
        
        return dados
    
    def _extrair_dados_expandidos(self, card):
        """Extrai dados expandidos do jogador"""
        dados = {}
        
        # Qualidade do card
        dados['qualidade'] = self._determinar_qualidade(card)
        
        # Nação
        seletores_nacao = ['.nation', '.country', '[data-testid="player-nation"]']
        dados['nacao'] = self._extrair_texto(card, seletores_nacao)
        
        # Liga
        seletores_liga = ['.league', '[data-testid="player-league"]']
        dados['liga'] = self._extrair_texto(card, seletores_liga)
        
        # Status (tradeable/untradeable)
        dados['status'] = self._determinar_status(card)
        
        # Posições alternativas
        dados['posicoes_alternativas'] = self._extrair_posicoes_alternativas(card)
        
        return dados
    
    def _extrair_estatisticas(self, card):
        """Extrai estatísticas detalhadas do jogador"""
        stats = {}
        
        # Lista de estatísticas
        estatisticas = ['PAC', 'SHO', 'PAS', 'DRI', 'DEF', 'PHY']
        
        for stat in estatisticas:
            seletores_stat = [
                f'.{stat.lower()}',
                f'[data-testid="{stat.lower()}"]',
                f'.stat-{stat.lower()}'
            ]
            stats[stat.lower()] = self._extrair_texto(card, seletores_stat)
        
        return stats
    
    def _extrair_traits(self, card):
        """Extrai traits do jogador"""
        traits = []
        
        try:
            # Procura pela seção de traits
            seletores_traits = [
                '.ut-item-view--traits .ut-item-row .ut-item-row-label--left',
                '.traits .trait',
                '[data-testid="player-traits"]'
            ]
            
            for seletor in seletores_traits:
                try:
                    elementos_traits = card.find_elements(By.CSS_SELECTOR, seletor)
                    for elemento in elementos_traits:
                        trait = elemento.text.strip()
                        if trait and trait not in traits:
                            traits.append(trait)
                except NoSuchElementException:
                    continue
            
        except Exception as e:
            logger.warning(f"Erro ao extrair traits: {str(e)}")
        
        return {'traits': ', '.join(traits) if traits else ''}
    
    def _extrair_texto(self, elemento, seletores):
        """Extrai texto de um elemento usando múltiplos seletores"""
        for seletor in seletores:
            try:
                el = elemento.find_element(By.CSS_SELECTOR, seletor)
                texto = el.text.strip()
                if texto:
                    return texto
            except NoSuchElementException:
                continue
        return ''
    
    def _determinar_qualidade(self, card):
        """Determina a qualidade do card baseado nas classes CSS"""
        try:
            classes = card.get_attribute('class')
            if not classes:
                return 'Base'
            
            classes = classes.lower()
            
            if 'icon' in classes:
                return 'Icon'
            elif 'hero' in classes:
                return 'Hero'
            elif 'tots' in classes:
                return 'TOTS'
            elif 'special' in classes:
                return 'Special'
            else:
                return 'Base'
                
        except Exception:
            return 'Base'
    
    def _determinar_status(self, card):
        """Determina se o jogador é tradeable ou untradeable"""
        try:
            classes = card.get_attribute('class')
            if not classes:
                return 'Tradeable'
            
            classes = classes.lower()
            
            if 'untradeable' in classes:
                return 'Untradeable'
            else:
                return 'Tradeable'
                
        except Exception:
            return 'Tradeable'
    
    def _extrair_posicoes_alternativas(self, card):
        """Extrai posições alternativas do jogador"""
        try:
            seletores_alt = ['.alt-positions', '.secondary-positions']
            for seletor in seletores_alt:
                try:
                    elemento = card.find_element(By.CSS_SELECTOR, seletor)
                    return elemento.text.strip()
                except NoSuchElementException:
                    continue
        except Exception:
            pass
        
        return ''
    
    def _validar_dados_jogador(self, jogador):
        """Valida se os dados do jogador são válidos"""
        # Verifica se tem nome
        if not jogador.get('nome') or jogador['nome'] == 'N/A':
            return False
        
        # Verifica se tem overall
        if not jogador.get('overall') or jogador['overall'] == 'N/A':
            return False
        
        return True
    
    def coletar_dados_jogadores(self):
        """Coleta dados de todos os jogadores de todas as páginas"""
        try:
            pagina = 1
            total_jogadores = 0
            
            logger.info("Iniciando coleta de dados dos jogadores...")
            
            while True:
                logger.info(f"Processando página {pagina}...")
                
                # Localiza cards na página atual
                cards = self.localizar_cards_jogadores()
                
                if not cards:
                    logger.info(f"Nenhum jogador encontrado na página {pagina}")
                    break
                
                # Extrai dados de cada jogador
                jogadores_pagina = 0
                for card in cards:
                    dados_jogador = self.extrair_dados_jogador(card)
                    if dados_jogador:
                        self.jogadores.append(dados_jogador)
                        jogadores_pagina += 1
                
                total_jogadores += jogadores_pagina
                logger.info(f"Página {pagina}: {jogadores_pagina} jogadores coletados")
                
                # Tenta ir para próxima página
                from .navigation import NavigationManager
                nav = NavigationManager(self.driver, self.wait)
                
                if not nav.ir_proxima_pagina():
                    logger.info("Última página alcançada")
                    break
                
                pagina += 1
            
            logger.info(f"Coleta concluída! Total: {total_jogadores} jogadores em {pagina} páginas")
            return True
            
        except Exception as e:
            logger.error(f"Erro durante coleta: {str(e)}")
            return False
    
    def get_jogadores(self):
        """Retorna a lista de jogadores coletados"""
        return self.jogadores 