#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para construir o executável do EA FC 25 Web App Scraper
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def verificar_python():
    """Verifica se a versão do Python é compatível"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 ou superior é necessário")
        print(f"Versão atual: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} - OK")
    return True

def instalar_dependencias():
    """Instala as dependências necessárias"""
    try:
        print("📦 Instalando dependências...")
        
        # Instala as dependências básicas
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

def limpar_builds_anteriores():
    """Remove builds anteriores"""
    try:
        print("🧹 Limpando builds anteriores...")
        
        # Remove diretórios de build
        dirs_para_remover = ['build', 'dist', '__pycache__']
        for dir_name in dirs_para_remover:
            if os.path.exists(dir_name):
                shutil.rmtree(dir_name)
                print(f"   Removido: {dir_name}")
        
        # Remove arquivos .spec antigos (exceto o nosso)
        for file in os.listdir('.'):
            if file.endswith('.spec') and file != 'fc25_scraper.spec':
                os.remove(file)
                print(f"   Removido: {file}")
        
        print("✅ Limpeza concluída!")
        return True
        
    except Exception as e:
        print(f"❌ Erro durante limpeza: {str(e)}")
        return False

def verificar_arquivos_necessarios():
    """Verifica se todos os arquivos necessários existem"""
    arquivos_necessarios = [
        'fc25_scraper.py',
        'config.py',
        'requirements.txt',
        'fc25_scraper.spec',
        'file_version_info.txt'
    ]
    
    print("🔍 Verificando arquivos necessários...")
    for arquivo in arquivos_necessarios:
        if os.path.exists(arquivo):
            print(f"   ✅ {arquivo}")
        else:
            print(f"   ❌ {arquivo} - NÃO ENCONTRADO")
            return False
    
    print("✅ Todos os arquivos necessários encontrados!")
    return True

def construir_executavel():
    """Constrói o executável usando PyInstaller"""
    try:
        print("🔨 Construindo executável...")
        print("   Isso pode levar alguns minutos...")
        
        # Comando PyInstaller
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--clean",
            "--noconfirm",
            "fc25_scraper.spec"
        ]
        
        # Executa o comando
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Executável construído com sucesso!")
            return True
        else:
            print("❌ Erro ao construir executável:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Erro durante construção: {str(e)}")
        return False

def verificar_executavel():
    """Verifica se o executável foi criado corretamente"""
    exe_path = Path("dist/FC25_Scraper.exe")
    
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"✅ Executável criado: {exe_path}")
        print(f"   Tamanho: {size_mb:.1f} MB")
        return True
    else:
        print("❌ Executável não encontrado em dist/FC25_Scraper.exe")
        return False

def criar_arquivo_batch():
    """Cria um arquivo .bat para facilitar a execução"""
    try:
        batch_content = """@echo off
echo ========================================
echo    EA FC 25 Web App Scraper
echo ========================================
echo.
echo Iniciando o scraper...
echo.
FC25_Scraper.exe
echo.
echo Pressione qualquer tecla para sair...
pause >nul
"""
        
        with open("dist/Executar_Scraper.bat", "w", encoding="utf-8") as f:
            f.write(batch_content)
        
        print("✅ Arquivo batch criado: dist/Executar_Scraper.bat")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar arquivo batch: {str(e)}")
        return False

def mostrar_instrucoes():
    """Mostra instruções de uso"""
    print("\n" + "="*60)
    print("🎉 EXECUTÁVEL CRIADO COM SUCESSO!")
    print("="*60)
    print()
    print("📁 Arquivos criados:")
    print("   • dist/FC25_Scraper.exe - Executável principal")
    print("   • dist/Executar_Scraper.bat - Script de execução")
    print()
    print("🚀 Como usar:")
    print("   1. Vá para a pasta 'dist'")
    print("   2. Execute 'FC25_Scraper.exe' ou 'Executar_Scraper.bat'")
    print("   3. Siga as instruções na tela")
    print()
    print("⚠️  IMPORTANTE:")
    print("   • O Google Chrome deve estar instalado")
    print("   • Uma conexão com a internet é necessária")
    print("   • O executável pode ser movido para qualquer pasta")
    print()
    print("📊 Dados coletados serão salvos como 'jogadores_fc25.csv'")
    print("="*60)

def main():
    """Função principal"""
    print("="*60)
    print("🔨 CONSTRUTOR DE EXECUTÁVEL - EA FC 25 SCRAPER")
    print("="*60)
    
    # Verifica Python
    if not verificar_python():
        sys.exit(1)
    
    # Verifica arquivos
    if not verificar_arquivos_necessarios():
        sys.exit(1)
    
    # Instala dependências
    if not instalar_dependencias():
        sys.exit(1)
    
    # Limpa builds anteriores
    if not limpar_builds_anteriores():
        sys.exit(1)
    
    # Constrói executável
    if not construir_executavel():
        sys.exit(1)
    
    # Verifica resultado
    if not verificar_executavel():
        sys.exit(1)
    
    # Cria arquivo batch
    criar_arquivo_batch()
    
    # Mostra instruções
    mostrar_instrucoes()

if __name__ == "__main__":
    main() 