#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EA FC 25 Web App Scraper - Versão Refatorada
Script principal para coletar dados dos jogadores do EA FC 25 Web App
"""

import time
from config import Config
from utils.logger import setup_logger
from utils.data_processor import DataProcessor
from drivers.chrome_driver import ChromeDriverManager
from auth.login_manager import LoginManager
from scrapers.navigation import NavigationManager
from scrapers.player_scraper import PlayerScraper
from exporters.csv_exporter import CSVExporter

class FC25Scraper:
    """
    Classe principal para fazer web scraping dos jogadores do EA FC 25 Web App
    Versão refatorada com módulos separados
    """
    
    def __init__(self):
        """Inicializa o scraper com todos os componentes"""
        # Configura logging
        self.logger = setup_logger()
        
        # Inicializa componentes
        self.config = Config()
        self.driver_manager = ChromeDriverManager()
        self.login_manager = None
        self.navigation_manager = None
        self.player_scraper = None
        self.data_processor = DataProcessor()
        self.csv_exporter = CSVExporter()
        
        # URL do web app
        self.webapp_url = "https://www.ea.com/ea-sports-fc/ultimate-team/web-app/"
    
    def setup_driver(self):
        """Configura o driver do Chrome"""
        return self.driver_manager.setup_driver()
    
    def acessar_webapp(self):
        """Acessa o EA FC 25 Web App"""
        return self.driver_manager.navigate_to(self.webapp_url)
    
    def configurar_componentes(self):
        """Configura todos os componentes após inicialização do driver"""
        try:
            driver = self.driver_manager.get_driver()
            wait = self.driver_manager.get_wait()
            
            if not driver or not wait:
                self.logger.error("Driver não configurado corretamente")
                return False
            
            # Inicializa componentes
            self.login_manager = LoginManager(driver, wait, self.config)
            self.navigation_manager = NavigationManager(driver, wait)
            self.player_scraper = PlayerScraper(driver, wait)
            
            self.logger.info("Componentes configurados com sucesso")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao configurar componentes: {str(e)}")
            return False
    
    def fazer_login(self):
        """Gerencia o processo de login"""
        try:
            # Tenta login automático se credenciais estiverem configuradas
            if self.config.auto_login:
                self.logger.info("Tentando login automático...")
                if self.login_manager.fazer_login_automatico():
                    if self.login_manager.verificar_login_sucesso():
                        self.logger.info("Login automático bem-sucedido")
                        return True
            
            # Se login automático falhou, faz login manual
            self.logger.info("Fazendo login manual...")
            return self.login_manager.aguardar_login()
            
        except Exception as e:
            self.logger.error(f"Erro durante login: {str(e)}")
            return False
    
    def navegar_para_jogadores(self):
        """Navega para a página de jogadores"""
        return self.navigation_manager.navegar_para_jogadores()
    
    def coletar_dados(self):
        """Coleta dados de todos os jogadores"""
        return self.player_scraper.coletar_dados_jogadores()
    
    def processar_dados(self):
        """Processa e valida os dados coletados"""
        try:
            jogadores_raw = self.player_scraper.get_jogadores()
            if not jogadores_raw:
                self.logger.warning("Nenhum jogador coletado")
                return False
            
            # Processa dados
            jogadores_processados = self.data_processor.processar_dados(jogadores_raw)
            if not jogadores_processados:
                self.logger.error("Erro ao processar dados")
                return False
            
            # Atualiza lista de jogadores processados
            self.player_scraper.jogadores = jogadores_processados
            
            # Gera estatísticas
            stats = self.data_processor.gerar_estatisticas()
            self.logger.info(f"Estatísticas: {stats}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao processar dados: {str(e)}")
            return False
    
    def exportar_dados(self, filename="jogadores_fc25.csv"):
        """Exporta dados para CSV"""
        try:
            jogadores = self.player_scraper.get_jogadores()
            if not jogadores:
                self.logger.warning("Nenhum jogador para exportar")
                return False
            
            # Exporta CSV
            if self.csv_exporter.exportar_csv(jogadores, filename):
                # Mostra preview
                self.csv_exporter.mostrar_preview()
                
                # Gera relatório
                self.csv_exporter.gerar_relatorio()
                
                return True
            else:
                return False
                
        except Exception as e:
            self.logger.error(f"Erro ao exportar dados: {str(e)}")
            return False
    
    def executar_scraping(self):
        """Executa o processo completo de scraping"""
        try:
            self.logger.info("="*60)
            self.logger.info("INICIANDO EA FC 25 WEB APP SCRAPER")
            self.logger.info("="*60)
            
            # 1. Configura driver
            self.logger.info("1. Configurando driver do Chrome...")
            if not self.setup_driver():
                return False
            
            # 2. Configura componentes
            self.logger.info("2. Configurando componentes...")
            if not self.configurar_componentes():
                return False
            
            # 3. Acessa web app
            self.logger.info("3. Acessando EA FC 25 Web App...")
            if not self.acessar_webapp():
                return False
            
            # 4. Faz login
            self.logger.info("4. Fazendo login...")
            if not self.fazer_login():
                return False
            
            # 5. Navega para jogadores
            self.logger.info("5. Navegando para página de jogadores...")
            if not self.navegar_para_jogadores():
                return False
            
            # 6. Coleta dados
            self.logger.info("6. Coletando dados dos jogadores...")
            if not self.coletar_dados():
                return False
            
            # 7. Processa dados
            self.logger.info("7. Processando dados...")
            if not self.processar_dados():
                return False
            
            # 8. Exporta dados
            self.logger.info("8. Exportando dados...")
            if not self.exportar_dados():
                return False
            
            self.logger.info("="*60)
            self.logger.info("SCRAPING CONCLUÍDO COM SUCESSO!")
            self.logger.info("="*60)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Erro durante execução: {str(e)}")
            return False
        
        finally:
            # Fecha driver
            self.driver_manager.close_driver()
    
    def get_estatisticas(self):
        """Retorna estatísticas da coleta"""
        return self.data_processor.gerar_estatisticas()

def main():
    """Função principal"""
    try:
        # Carrega configurações
        config = Config()
        config.carregar_credenciais()
        
        # Cria e executa scraper
        scraper = FC25Scraper()
        scraper.config = config
        
        # Executa scraping
        sucesso = scraper.executar_scraping()
        
        if sucesso:
            print("\n🎉 Scraping concluído com sucesso!")
            print("📊 Verifique o arquivo 'jogadores_fc25.csv'")
        else:
            print("\n❌ Erro durante o scraping")
            print("📋 Verifique os logs para mais detalhes")
        
    except KeyboardInterrupt:
        print("\n⚠️ Operação cancelada pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {str(e)}")

if __name__ == "__main__":
    main() 