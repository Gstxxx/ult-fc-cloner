#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EA FC 25 Web App Scraper
Script simples para coletar dados dos jogadores do EA FC 25 Web App
"""

import time
import pandas as pd
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
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver, WebDriverWait(driver, 20)
    except Exception as e:
        print(f"Erro ao configurar driver: {e}")
        return None, None

def aguardar_login():
    """Aguarda o usuário fazer login manualmente"""
    print("\n" + "="*50)
    print("LOGIN MANUAL REQUERIDO")
    print("="*50)
    print("1. Faça login na sua conta EA no navegador")
    print("2. Navegue até 'Clube > Jogadores'")
    print("3. Pressione ENTER quando estiver pronto")
    print("="*50)
    
    input("Pressione ENTER quando estiver na página de jogadores...")
    return True

def extrair_estatisticas_detalhadas(card):
    """Extrai estatísticas detalhadas do jogador"""
    stats = {}
    
    try:
        # Procura pela seção de estatísticas
        stats_container = card.find_element(By.CSS_SELECTOR, '.player-stats-data-component')
        stats_items = stats_container.find_elements(By.CSS_SELECTOR, 'li')
        
        for item in stats_items:
            try:
                label = item.find_element(By.CSS_SELECTOR, '.label').text.strip()
                value = item.find_element(By.CSS_SELECTOR, '.value').text.strip()
                stats[label] = value
            except:
                continue
                
    except:
        pass
    
    return stats

def extrair_informacoes_bio(card):
    """Extrai informações de nação, liga e qualidade"""
    info = {'nacao': 'N/A', 'liga': 'N/A', 'qualidade': 'N/A'}
    
    try:
        # Procura pela seção bio
        bio_section = card.find_element(By.CSS_SELECTOR, '.ut-item-view--bio')
        bio_rows = bio_section.find_elements(By.CSS_SELECTOR, '.ut-item-row')
        
        for row in bio_rows:
            try:
                label = row.find_element(By.CSS_SELECTOR, '.ut-item-row-label--left').text.strip()
                value = row.find_element(By.CSS_SELECTOR, '.ut-item-row-label--right').text.strip()
                
                if 'IRE' in label or 'Nation' in label:
                    info['nacao'] = value
                elif 'ICN' in label or 'League' in label:
                    info['liga'] = value
                elif 'Quality' in label:
                    info['qualidade'] = value
                    
            except:
                continue
                
    except:
        pass
    
    return info

def extrair_traits(card):
    """Extrai traits do jogador"""
    traits = []
    
    try:
        # Procura pela seção de traits
        traits_section = card.find_element(By.CSS_SELECTOR, '.ut-item-view--traits')
        traits_items = traits_section.find_elements(By.CSS_SELECTOR, '.ut-item-row .ut-item-row-label--left')
        
        for item in traits_items:
            trait = item.text.strip()
            if trait and trait != 'Traits':
                traits.append(trait)
                
    except:
        pass
    
    return ', '.join(traits) if traits else 'N/A'

def determinar_qualidade_card(card):
    """Determina a qualidade do card baseado nas classes CSS"""
    try:
        classes = card.get_attribute('class')
        
        if 'icon' in classes.lower():
            return 'Icon'
        elif 'hero' in classes.lower():
            return 'Hero'
        elif 'tots' in classes.lower():
            return 'TOTS'
        elif 'toty' in classes.lower():
            return 'TOTY'
        elif 'special' in classes.lower():
            return 'Special'
        else:
            return 'Base'
            
    except:
        return 'N/A'

def extrair_posicoes_alternativas(card):
    """Extrai posições alternativas do jogador"""
    posicoes = []
    
    try:
        # Procura por posições alternativas
        alt_positions = card.find_elements(By.CSS_SELECTOR, '.position-alt')
        for pos in alt_positions:
            pos_text = pos.text.strip()
            if pos_text:
                posicoes.append(pos_text)
                
    except:
        pass
    
    return ', '.join(posicoes) if posicoes else 'N/A'

def verificar_status_tradeable(card):
    """Verifica se o jogador é tradeable ou untradeable"""
    try:
        # Procura por indicadores de status
        untradeable_indicators = card.find_elements(By.CSS_SELECTOR, '.untradeable-indicator')
        if untradeable_indicators:
            return 'Untradeable'
        else:
            return 'Tradeable'
    except:
        return 'N/A'

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
            cards = driver.find_elements(By.CSS_SELECTOR, 'li.listFUTItem')
            if not cards:
                print("Nenhum jogador encontrado nesta página")
                break
            
            print(f"Encontrados {len(cards)} jogadores na página {pagina}")
            
            # Extrai dados de cada jogador
            for card in cards:
                try:
                    # Dados básicos
                    nome = card.find_element(By.CSS_SELECTOR, '.name').text.strip()
                    overall = card.find_element(By.CSS_SELECTOR, '.rating').text.strip()
                    posicao = card.find_element(By.CSS_SELECTOR, '.position').text.strip()
                    
                    # Dados adicionais básicos
                    try:
                        clube = card.find_element(By.CSS_SELECTOR, '.club').text.strip()
                    except:
                        clube = 'N/A'
                    
                    # Extrai estatísticas detalhadas
                    stats = extrair_estatisticas_detalhadas(card)
                    
                    # Extrai informações bio
                    bio_info = extrair_informacoes_bio(card)
                    
                    # Extrai traits
                    traits = extrair_traits(card)
                    
                    # Determina qualidade do card
                    qualidade = determinar_qualidade_card(card)
                    
                    # Extrai posições alternativas
                    posicoes_alt = extrair_posicoes_alternativas(card)
                    
                    # Verifica status tradeable
                    status = verificar_status_tradeable(card)
                    
                    # Adiciona jogador se tem dados válidos
                    if nome and overall and posicao:
                        jogador = {
                            'nome': nome,
                            'overall': overall,
                            'posicao': posicao,
                            'clube': clube,
                            'rating': overall,  # Mesmo que overall
                            'qualidade': qualidade,
                            'nacao': bio_info['nacao'],
                            'liga': bio_info['liga'],
                            'PAC': stats.get('PAC', 'N/A'),
                            'SHO': stats.get('SHO', 'N/A'),
                            'PAS': stats.get('PAS', 'N/A'),
                            'DRI': stats.get('DRI', 'N/A'),
                            'DEF': stats.get('DEF', 'N/A'),
                            'PHY': stats.get('PHY', 'N/A'),
                            'traits': traits,
                            'status': status,
                            'posicoes_alternativas': posicoes_alt
                        }
                        jogadores.append(jogador)
                        
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
        'overall_medio': df['overall'].astype(str).str.extract('(\d+)').astype(float).mean(),
        'posicoes_unicas': df['posicao'].nunique(),
        'clubes_unicos': df['clube'].nunique(),
        'qualidades_unicas': df['qualidade'].nunique()
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
        
        # 4. Coleta dados
        print("4. Coletando dados dos jogadores...")
        jogadores = coletar_jogadores(driver, wait)
        
        # 5. Exporta dados
        print("5. Exportando dados...")
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