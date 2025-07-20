#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EA FC 25 Web App Scraper
Script automatizado para coletar dados dos jogadores do EA FC 25 Web App
"""

import time
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    """Configura o driver do Chrome"""
    try:
        chrome_options = Options()
        
        # Configurações de performance
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Remove indicadores de automação
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Tenta usar ChromeDriver Manager
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
        except:
            # Fallback: usa Chrome sem service
            driver = webdriver.Chrome(options=chrome_options)
        
        # Remove indicadores de automação
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver, WebDriverWait(driver, 20)
    except Exception as e:
        print(f"Erro ao configurar driver: {e}")
        print("Tentando configuração alternativa...")
        
        try:
            # Configuração alternativa
            chrome_options = Options()
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
            driver = webdriver.Chrome(options=chrome_options)
            return driver, WebDriverWait(driver, 20)
        except Exception as e2:
            print(f"Erro na configuração alternativa: {e2}")
            return None, None

def aguardar_login():
    """Aguarda o usuário fazer login manualmente"""
    print("\n" + "="*50)
    print("LOGIN MANUAL REQUERIDO")
    print("="*50)
    print("1. Faça login na sua conta EA no navegador")
    print("2. Pressione ENTER quando estiver logado")
    print("3. O programa fará a navegação e coleta automaticamente")
    print("="*50)
    
    input("Pressione ENTER quando estiver logado...")
    return True

def navegar_para_clube(driver, wait):
    """Navega para a seção Clube"""
    try:
        print("Navegando para Clube...")
        
        # Procura pelo botão Clube na navbar
        botao_clube = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.ut-tab-bar-item.icon-club')))
        botao_clube.click()
        
        time.sleep(3)
        print("✅ Navegação para Clube concluída")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao navegar para Clube: {e}")
        return False

def navegar_para_jogadores(driver, wait):
    """Navega para a seção de jogadores"""
    try:
        print("Navegando para Jogadores...")
        
        # Procura pelo tile de jogadores
        tile_jogadores = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.tile.col-1-1-md.players-tile')))
        tile_jogadores.click()
        
        time.sleep(3)
        print("✅ Navegação para Jogadores concluída")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao navegar para Jogadores: {e}")
        return False

def extrair_dados_jogador(card):
    """Extrai dados completos de um jogador"""
    try:
        # Dados básicos
        nome = card.find_element(By.CSS_SELECTOR, 'div.name').text.strip()
        overall = card.find_element(By.CSS_SELECTOR, 'div.rating').text.strip()
        posicao = card.find_element(By.CSS_SELECTOR, 'div.position').text.strip()
        
        # Verifica se é untradeable
        try:
            nome_element = card.find_element(By.CSS_SELECTOR, 'div.name.untradeable')
            status = 'Untradeable'
        except:
            status = 'Tradeable'
        
        # Extrai estatísticas
        stats = {}
        try:
            stats_container = card.find_element(By.CSS_SELECTOR, 'div.player-stats-data-component ul')
            stats_items = stats_container.find_elements(By.CSS_SELECTOR, 'li')
            
            for item in stats_items:
                label = item.find_element(By.CSS_SELECTOR, 'span.label').text.strip()
                value = item.find_element(By.CSS_SELECTOR, 'span.value').text.strip()
                stats[label] = value
        except:
            pass
        
        # Extrai informações bio
        bio_info = {'nacao': 'N/A', 'liga': 'N/A', 'clube': 'N/A'}
        try:
            bio_section = card.find_element(By.CSS_SELECTOR, 'div.ut-item-view--bio')
            bio_rows = bio_section.find_elements(By.CSS_SELECTOR, 'div.ut-item-row')
            
            for i, row in enumerate(bio_rows):
                try:
                    label = row.find_element(By.CSS_SELECTOR, 'span.ut-item-row-label--left').text.strip()
                    if i == 0:  # Primeira linha é nação
                        bio_info['nacao'] = label
                    elif i == 1:  # Segunda linha é liga
                        bio_info['liga'] = label
                    elif i == 2:  # Terceira linha é clube
                        bio_info['clube'] = label
                except:
                    continue
        except:
            pass
        
        # Extrai posições alternativas
        posicoes_alt = 'N/A'
        try:
            pos_header = card.find_element(By.CSS_SELECTOR, 'div.ut-item-view--positions-header')
            posicoes_alt = pos_header.find_element(By.CSS_SELECTOR, 'span.otherPositions').text.strip()
            if posicoes_alt.startswith(', '):
                posicoes_alt = posicoes_alt[2:]
        except:
            pass
        
        # Extrai traits
        traits = []
        try:
            traits_section = card.find_element(By.CSS_SELECTOR, 'div.ut-item-view--traits')
            traits_items = traits_section.find_elements(By.CSS_SELECTOR, 'div.ut-item-row span.ut-item-row-label--left')
            
            for item in traits_items:
                trait = item.text.strip()
                if trait and trait != 'Traits':
                    traits.append(trait)
        except:
            pass
        
        # Determina qualidade do card
        qualidade = 'Base'
        try:
            classes = card.get_attribute('class')
            if 'specials' in classes:
                qualidade = 'Special'
            elif 'icon' in classes:
                qualidade = 'Icon'
            elif 'hero' in classes:
                qualidade = 'Hero'
        except:
            pass
        
        # Verifica se está ativo
        ativo = False
        try:
            ativo_indicator = card.find_element(By.CSS_SELECTOR, 'div.ut-list-tag-view.ut-list-active-tag-view')
            ativo = True
        except:
            pass
        
        return {
            'nome': nome,
            'overall': overall,
            'posicao': posicao,
            'clube': bio_info['clube'],
            'rating': overall,
            'qualidade': qualidade,
            'nacao': bio_info['nacao'],
            'liga': bio_info['liga'],
            'PAC': stats.get('RIT', 'N/A'),
            'SHO': stats.get('FIN', 'N/A'),
            'PAS': stats.get('PAS', 'N/A'),
            'DRI': stats.get('CON', 'N/A'),
            'DEF': stats.get('DEF', 'N/A'),
            'PHY': stats.get('FÍS', 'N/A'),
            'traits': ', '.join(traits) if traits else 'N/A',
            'status': status,
            'posicoes_alternativas': posicoes_alt,
            'ativo': 'Sim' if ativo else 'Não'
        }
        
    except Exception as e:
        print(f"Erro ao extrair dados do jogador: {e}")
        return None

def coletar_jogadores(driver, wait):
    """Coleta dados de todos os jogadores"""
    jogadores = []
    pagina = 1
    
    print("Iniciando coleta de dados...")
    
    while True:
        print(f"Processando página {pagina}...")
        
        # Aguarda carregamento dos cards
        time.sleep(3)
        
        # Procura pelos cards de jogadores
        try:
            cards = driver.find_elements(By.CSS_SELECTOR, 'div.small.player.item')
            if not cards:
                print("Nenhum jogador encontrado nesta página")
                break
            
            print(f"Encontrados {len(cards)} jogadores na página {pagina}")
            
            # Extrai dados de cada jogador
            for card in cards:
                try:
                    dados = extrair_dados_jogador(card)
                    if dados and dados['nome'] and dados['overall']:
                        jogadores.append(dados)
                except Exception as e:
                    continue
            
            # Tenta ir para próxima página
            try:
                botao_proxima = driver.find_element(By.CSS_SELECTOR, 'button.pagination.next')
                if botao_proxima.is_enabled():
                    botao_proxima.click()
                    time.sleep(3)
                    pagina += 1
                else:
                    print("Última página alcançada")
                    break
            except:
                print("Botão próxima não encontrado - fim das páginas")
                break
                
        except Exception as e:
            print(f"Erro ao processar página {pagina}: {e}")
            break
    
    print(f"Coleta concluída! Total: {len(jogadores)} jogadores")
    return jogadores

def gerar_estatisticas(jogadores):
    """Gera estatísticas da coleta"""
    if not jogadores:
        return {}
    
    df = pd.DataFrame(jogadores)
    
    stats = {
        'total_jogadores': len(df),
        'overall_medio': df['overall'].astype(str).str.extract(r'(\d+)').astype(float).mean(),
        'posicoes_unicas': df['posicao'].nunique(),
        'clubes_unicos': df['clube'].nunique(),
        'qualidades_unicas': df['qualidade'].nunique(),
        'tradeable': len(df[df['status'] == 'Tradeable']),
        'untradeable': len(df[df['status'] == 'Untradeable']),
        'ativos': len(df[df['ativo'] == 'Sim'])
    }
    
    return stats

def exportar_csv(jogadores, filename="jogadores_fc25.csv"):
    """Exporta dados para CSV"""
    try:
        if not jogadores:
            print("Nenhum jogador para exportar")
            return False
        
        df = pd.DataFrame(jogadores)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        # Gera estatísticas
        stats = gerar_estatisticas(jogadores)
        
        print(f"\nCSV exportado: {filename}")
        print(f"Total de jogadores: {stats['total_jogadores']}")
        print(f"Overall médio: {stats['overall_medio']:.1f}")
        print(f"Posições únicas: {stats['posicoes_unicas']}")
        print(f"Clubes únicos: {stats['clubes_unicos']}")
        print(f"Qualidades únicas: {stats['qualidades_unicas']}")
        print(f"Tradeable: {stats['tradeable']}")
        print(f"Untradeable: {stats['untradeable']}")
        print(f"Ativos: {stats['ativos']}")
        
        print("\nPrimeiros jogadores:")
        print(df.head().to_string(index=False))
        
        return True
        
    except Exception as e:
        print(f"Erro ao exportar CSV: {e}")
        return False

def main():
    """Função principal"""
    driver = None
    
    try:
        print("="*60)
        print("EA FC 25 WEB APP SCRAPER")
        print("="*60)
        
        # 1. Configura driver
        print("1. Configurando driver do Chrome...")
        driver, wait = setup_driver()
        if not driver:
            return
        
        # 2. Acessa web app
        print("2. Acessando EA FC 25 Web App...")
        driver.get("https://www.ea.com/ea-sports-fc/ultimate-team/web-app/")
        time.sleep(5)
        
        # 3. Aguarda login manual
        print("3. Aguardando login manual...")
        if not aguardar_login():
            return
        
        # 4. Navega para Clube
        print("4. Navegando para Clube...")
        if not navegar_para_clube(driver, wait):
            return
        
        # 5. Navega para Jogadores
        print("5. Navegando para Jogadores...")
        if not navegar_para_jogadores(driver, wait):
            return
        
        # 6. Coleta dados
        print("6. Coletando dados dos jogadores...")
        jogadores = coletar_jogadores(driver, wait)
        
        # 7. Exporta dados
        print("7. Exportando dados...")
        if exportar_csv(jogadores):
            print("\n🎉 Scraping concluído com sucesso!")
            print("📊 Verifique o arquivo 'jogadores_fc25.csv'")
        else:
            print("\n❌ Erro ao exportar dados")
        
    except KeyboardInterrupt:
        print("\n⚠️ Operação cancelada pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main() 