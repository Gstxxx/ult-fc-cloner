#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configurações para o EA FC 25 Web App Scraper
Versão simplificada - apenas configurações básicas
"""

import os

class Config:
    """Classe para gerenciar configurações do scraper"""
    
    def __init__(self):
        # Configurações básicas
        self.timeout = 20
        self.delay_pagina = 3
        self.delay_elemento = 2
        
        # URLs
        self.webapp_url = "https://www.ea.com/ea-sports-fc/ultimate-team/web-app/"
        
        # Configurações do Chrome
        self.chrome_options = [
            "--start-maximized",
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-dev-shm-usage"
        ]
        
        # Seletores CSS (pode ser personalizado se necessário)
        self.seletores = {
            'cards_jogadores': ['li.listFUTItem', 'div.ut-item-view'],
            'nome': ['.name', '.player-name'],
            'overall': ['.rating', '.overall'],
            'posicao': ['.position', '.player-position'],
            'clube': ['.club', '.team'],
            'botao_proxima': ['button.pagination.next', 'button.flat.pagination.next']
        }
    
    def get_timeout(self):
        """Retorna o timeout configurado"""
        return self.timeout
    
    def get_delay_pagina(self):
        """Retorna o delay entre páginas"""
        return self.delay_pagina
    
    def get_delay_elemento(self):
        """Retorna o delay para elementos"""
        return self.delay_elemento
    
    def get_webapp_url(self):
        """Retorna a URL do web app"""
        return self.webapp_url
    
    def get_chrome_options(self):
        """Retorna as opções do Chrome"""
        return self.chrome_options
    
    def get_seletores(self):
        """Retorna os seletores CSS"""
        return self.seletores 