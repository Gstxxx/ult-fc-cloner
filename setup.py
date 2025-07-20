#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Setup para EA FC 25 Web App Scraper
"""

import subprocess
import sys
import os

def verificar_python():
    """Verifica se a versão do Python é compatível"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 ou superior é necessário")
        print(f"Versão atual: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} - OK")
    return True

def instalar_dependencias():
    """Instala as dependências do projeto"""
    try:
        print("📦 Instalando dependências...")
        
        # Verifica se requirements.txt existe
        if not os.path.exists("requirements.txt"):
            print("❌ Arquivo requirements.txt não encontrado")
            return False
        
        # Instala as dependências
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Dependências instaladas com sucesso!")
            return True
        else:
            print("❌ Erro ao instalar dependências:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Erro durante instalação: {str(e)}")
        return False

def verificar_chrome():
    """Verifica se o Chrome está instalado"""
    try:
        # Tenta importar webdriver-manager para verificar se está instalado
        import webdriver_manager
        print("✅ webdriver-manager instalado - OK")
        return True
    except ImportError:
        print("❌ webdriver-manager não está instalado")
        return False

def main():
    """Função principal do setup"""
    print("="*50)
    print("SETUP - EA FC 25 WEB APP SCRAPER")
    print("="*50)
    
    # Verifica Python
    if not verificar_python():
        sys.exit(1)
    
    # Instala dependências
    if not instalar_dependencias():
        sys.exit(1)
    
    # Verifica Chrome
    if not verificar_chrome():
        print("⚠️  Instale o Google Chrome para usar o script")
        print("   Download: https://www.google.com/chrome/")
    
    print("\n" + "="*50)
    print("✅ SETUP CONCLUÍDO!")
    print("="*50)
    print("Para usar o script:")
    print("1. Execute: python fc25_scraper.py")
    print("2. Siga as instruções na tela")
    print("3. Faça login no EA FC 25 Web App")
    print("4. Navegue até 'Clube > Jogadores'")
    print("5. Pressione ENTER quando estiver pronto")
    print("="*50)

if __name__ == "__main__":
    main() 