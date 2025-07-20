#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para construir o executável do EA FC 25 Web App Scraper
Versão simplificada - sem config.py
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def verificar_python():
    """Verifica a versão do Python"""
    print("✅ Python {}.{}.{} - OK".format(*sys.version_info[:3]))
    return True

def verificar_arquivos():
    """Verifica se os arquivos necessários existem"""
    print("🔍 Verificando arquivos necessários...")
    
    arquivos_necessarios = [
        'fc25_scraper.py',
        'requirements.txt',
        'fc25_scraper.spec'
    ]
    
    todos_ok = True
    for arquivo in arquivos_necessarios:
        if os.path.exists(arquivo):
            print(f"   ✅ {arquivo}")
        else:
            print(f"   ❌ {arquivo} - NÃO ENCONTRADO")
            todos_ok = False
    
    return todos_ok

def limpar_builds_anteriores():
    """Remove builds anteriores"""
    print("🧹 Limpando builds anteriores...")
    
    pastas_para_limpar = ['build', 'dist', '__pycache__']
    
    for pasta in pastas_para_limpar:
        if os.path.exists(pasta):
            try:
                shutil.rmtree(pasta)
                print(f"   ✅ {pasta} removida")
            except Exception as e:
                print(f"   ⚠️ Erro ao remover {pasta}: {e}")

def instalar_dependencias():
    """Instala as dependências necessárias"""
    print("📦 Instalando dependências...")
    
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True, capture_output=True, text=True)
        print("   ✅ Dependências instaladas")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Erro ao instalar dependências: {e}")
        return False

def construir_executavel():
    """Constrói o executável usando PyInstaller"""
    print("🔨 Construindo executável...")
    
    try:
        # Comando PyInstaller
        cmd = [
            sys.executable, '-m', 'PyInstaller',
            '--onefile',
            '--windowed',
            '--name=fc25_scraper',
            '--add-data=requirements.txt;.',
            'fc25_scraper.py'
        ]
        
        print(f"   Executando: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("   ✅ Executável construído com sucesso!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Erro ao construir executável: {e}")
        print(f"   Erro: {e.stderr}")
        return False

def verificar_executavel():
    """Verifica se o executável foi criado"""
    print("🔍 Verificando executável...")
    
    executavel_path = os.path.join('dist', 'fc25_scraper.exe')
    
    if os.path.exists(executavel_path):
        tamanho = os.path.getsize(executavel_path) / (1024 * 1024)  # MB
        print(f"   ✅ Executável criado: {executavel_path}")
        print(f"   📏 Tamanho: {tamanho:.1f} MB")
        return True
    else:
        print(f"   ❌ Executável não encontrado: {executavel_path}")
        return False

def criar_arquivo_batch():
    """Cria um arquivo .bat para facilitar a execução"""
    print("📝 Criando arquivo batch...")
    
    batch_content = """@echo off
echo ========================================
echo EA FC 25 WEB APP SCRAPER
echo ========================================
echo.
echo Iniciando scraper...
echo.
fc25_scraper.exe
echo.
echo Pressione qualquer tecla para sair...
pause > nul
"""
    
    try:
        with open(os.path.join('dist', 'Executar_Scraper.bat'), 'w', encoding='utf-8') as f:
            f.write(batch_content)
        print("   ✅ Arquivo batch criado: Executar_Scraper.bat")
        return True
    except Exception as e:
        print(f"   ❌ Erro ao criar arquivo batch: {e}")
        return False

def criar_instrucoes():
    """Cria arquivo de instruções"""
    print("📖 Criando instruções...")
    
    instrucoes = """EA FC 25 WEB APP SCRAPER - INSTRUÇÕES

COMO USAR:
1. Execute fc25_scraper.exe ou Executar_Scraper.bat
2. Faça login na sua conta EA no navegador
3. Navegue até 'Clube > Jogadores'
4. Pressione ENTER quando estiver pronto
5. Aguarde a coleta automática
6. Verifique o arquivo jogadores_fc25.csv

REQUISITOS:
- Windows 10/11
- Google Chrome instalado
- Conta EA com acesso ao FC 25 Web App
- Conexão com internet

DADOS COLETADOS:
- Nome, Overall, Posição, Clube
- Nação, Liga, Qualidade do card
- Estatísticas: PAC, SHO, PAS, DRI, DEF, PHY
- Traits, Status, Posições alternativas

SUPORTE:
- GitHub: https://github.com/Gstxxx/ult-fc-cloner
- Issues: https://github.com/Gstxxx/ult-fc-cloner/issues

Desenvolvido com ❤️ para a comunidade EA FC 25
"""
    
    try:
        with open(os.path.join('dist', 'INSTRUCOES.txt'), 'w', encoding='utf-8') as f:
            f.write(instrucoes)
        print("   ✅ Instruções criadas: INSTRUCOES.txt")
        return True
    except Exception as e:
        print(f"   ❌ Erro ao criar instruções: {e}")
        return False

def main():
    """Função principal"""
    print("="*60)
    print("🔨 CONSTRUTOR DE EXECUTÁVEL - EA FC 25 SCRAPER")
    print("="*60)
    
    # 1. Verifica Python
    if not verificar_python():
        return False
    
    # 2. Verifica arquivos
    if not verificar_arquivos():
        print("\n❌ Arquivos necessários não encontrados!")
        return False
    
    # 3. Limpa builds anteriores
    limpar_builds_anteriores()
    
    # 4. Instala dependências
    if not instalar_dependencias():
        print("\n❌ Erro ao instalar dependências!")
        return False
    
    # 5. Constrói executável
    if not construir_executavel():
        print("\n❌ Erro ao construir executável!")
        return False
    
    # 6. Verifica executável
    if not verificar_executavel():
        print("\n❌ Executável não foi criado!")
        return False
    
    # 7. Cria arquivos adicionais
    criar_arquivo_batch()
    criar_instrucoes()
    
    print("\n" + "="*60)
    print("🎉 BUILD CONCLUÍDO COM SUCESSO!")
    print("="*60)
    print("📁 Arquivos criados em: dist/")
    print("   - fc25_scraper.exe (executável principal)")
    print("   - Executar_Scraper.bat (script de execução)")
    print("   - INSTRUCOES.txt (instruções de uso)")
    print("\n🚀 Para usar:")
    print("   1. Vá para a pasta dist/")
    print("   2. Execute fc25_scraper.exe")
    print("   3. Siga as instruções na tela")
    print("="*60)
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ Build cancelado pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1) 