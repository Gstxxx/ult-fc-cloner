#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuração de logging para o EA FC 25 Web App Scraper
"""

import logging
import os
from datetime import datetime

def setup_logger(name='fc25_scraper', level=logging.INFO):
    """Configura o sistema de logging"""
    
    # Cria o logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Evita duplicação de handlers
    if logger.handlers:
        return logger
    
    # Formato das mensagens
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para arquivo
    log_filename = f'fc25_scraper_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    
    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    
    # Adiciona handlers ao logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def get_logger(name='fc25_scraper'):
    """Retorna o logger configurado"""
    return logging.getLogger(name) 