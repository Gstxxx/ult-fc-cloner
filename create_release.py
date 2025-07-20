#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para criar release no GitHub para o EA FC 25 Web App Scraper
"""

import os
import sys
import subprocess
import zipfile
from pathlib import Path

def verificar_gh_cli():
    """Verifica se o GitHub CLI está instalado"""
    try:
        result = subprocess.run(['gh', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ GitHub CLI encontrado")
            return True
        else:
            print("❌ GitHub CLI não encontrado")
            return False
    except FileNotFoundError:
        print("❌ GitHub CLI não está instalado")
        print("   Instale em: https://cli.github.com/")
        return False

def verificar_login_github():
    """Verifica se está logado no GitHub"""
    try:
        result = subprocess.run(['gh', 'auth', 'status'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Logado no GitHub")
            return True
        else:
            print("❌ Não está logado no GitHub")
            print("   Execute: gh auth login")
            return False
    except Exception as e:
        print(f"❌ Erro ao verificar login: {str(e)}")
        return False

def criar_zip_release():
    """Cria arquivo ZIP com os arquivos do release"""
    try:
        print("📦 Criando arquivo ZIP do release...")
        
        # Nome do arquivo ZIP
        zip_name = "FC25_Scraper_v1.0.0.zip"
        
        # Arquivos para incluir no ZIP
        files_to_include = [
            "dist/FC25_Scraper.exe",
            "dist/Executar_Scraper.bat",
            "dist/INSTRUCOES.txt",
            "README.md",
            "RELEASE_NOTES.md"
        ]
        
        # Cria o ZIP
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in files_to_include:
                if os.path.exists(file_path):
                    # Adiciona o arquivo ao ZIP
                    zipf.write(file_path, os.path.basename(file_path))
                    print(f"   ✅ Adicionado: {file_path}")
                else:
                    print(f"   ⚠️  Arquivo não encontrado: {file_path}")
        
        print(f"✅ ZIP criado: {zip_name}")
        return zip_name
        
    except Exception as e:
        print(f"❌ Erro ao criar ZIP: {str(e)}")
        return None

def criar_release_github():
    """Cria o release no GitHub"""
    try:
        print("🚀 Criando release no GitHub...")
        
        # Cria o release
        cmd = [
            'gh', 'release', 'create', 'v1.0.0',
            '--title', '🎉 Release v1.0.0 - EA FC 25 Web App Scraper',
            '--notes-file', 'RELEASE_NOTES.md',
            '--draft'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Release criado com sucesso!")
            return True
        else:
            print("❌ Erro ao criar release:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Erro durante criação do release: {str(e)}")
        return False

def fazer_upload_assets():
    """Faz upload dos arquivos para o release"""
    try:
        print("📤 Fazendo upload dos arquivos...")
        
        # Upload do ZIP
        zip_name = "FC25_Scraper_v1.0.0.zip"
        if os.path.exists(zip_name):
            cmd = ['gh', 'release', 'upload', 'v1.0.0', zip_name]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Upload do {zip_name} concluído!")
            else:
                print(f"❌ Erro no upload do {zip_name}:")
                print(result.stderr)
                return False
        
        # Upload dos arquivos individuais
        files_to_upload = [
            "dist/FC25_Scraper.exe",
            "dist/Executar_Scraper.bat",
            "dist/INSTRUCOES.txt"
        ]
        
        for file_path in files_to_upload:
            if os.path.exists(file_path):
                cmd = ['gh', 'release', 'upload', 'v1.0.0', file_path]
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"✅ Upload de {os.path.basename(file_path)} concluído!")
                else:
                    print(f"❌ Erro no upload de {file_path}:")
                    print(result.stderr)
        
        return True
        
    except Exception as e:
        print(f"❌ Erro durante upload: {str(e)}")
        return False

def publicar_release():
    """Publica o release (remove o status de draft)"""
    try:
        print("🌐 Publicando release...")
        
        cmd = ['gh', 'release', 'edit', 'v1.0.0', '--draft=false']
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Release publicado com sucesso!")
            return True
        else:
            print("❌ Erro ao publicar release:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Erro ao publicar: {str(e)}")
        return False

def mostrar_instrucoes_manuais():
    """Mostra instruções para criação manual do release"""
    print("\n" + "="*60)
    print("📋 INSTRUÇÕES PARA CRIAÇÃO MANUAL DO RELEASE")
    print("="*60)
    print()
    print("1. Acesse: https://github.com/Gstxxx/ult-fc-cloner/releases")
    print("2. Clique em 'Create a new release'")
    print("3. Configure:")
    print("   • Tag: v1.0.0")
    print("   • Title: 🎉 Release v1.0.0 - EA FC 25 Web App Scraper")
    print("   • Description: Copie o conteúdo de RELEASE_NOTES.md")
    print()
    print("4. Faça upload dos arquivos:")
    print("   • FC25_Scraper.exe")
    print("   • Executar_Scraper.bat")
    print("   • INSTRUCOES.txt")
    print("   • FC25_Scraper_v1.0.0.zip (se criado)")
    print()
    print("5. Clique em 'Publish release'")
    print("="*60)

def main():
    """Função principal"""
    print("="*60)
    print("🚀 CRIADOR DE RELEASE - EA FC 25 SCRAPER")
    print("="*60)
    
    # Verifica GitHub CLI
    if not verificar_gh_cli():
        print("\n⚠️  GitHub CLI não encontrado. Mostrando instruções manuais...")
        mostrar_instrucoes_manuais()
        return
    
    # Verifica login
    if not verificar_login_github():
        print("\n⚠️  Não está logado no GitHub. Mostrando instruções manuais...")
        mostrar_instrucoes_manuais()
        return
    
    # Cria ZIP do release
    zip_name = criar_zip_release()
    
    # Cria release no GitHub
    if not criar_release_github():
        print("\n⚠️  Erro ao criar release. Mostrando instruções manuais...")
        mostrar_instrucoes_manuais()
        return
    
    # Faz upload dos arquivos
    if not fazer_upload_assets():
        print("\n⚠️  Erro no upload. Verifique manualmente...")
        return
    
    # Publica o release
    if not publicar_release():
        print("\n⚠️  Erro ao publicar. Verifique manualmente...")
        return
    
    print("\n" + "="*60)
    print("🎉 RELEASE CRIADO COM SUCESSO!")
    print("="*60)
    print()
    print("📋 Próximos passos:")
    print("1. Verifique o release em: https://github.com/Gstxxx/ult-fc-cloner/releases")
    print("2. Teste o download dos arquivos")
    print("3. Compartilhe o link do release")
    print()
    print("🔗 Link do release: https://github.com/Gstxxx/ult-fc-cloner/releases/tag/v1.0.0")
    print("="*60)

if __name__ == "__main__":
    main() 