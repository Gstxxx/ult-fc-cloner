#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configurações para o EA FC 25 Web App Scraper
"""

import os
from getpass import getpass

class Config:
    """Classe para gerenciar configurações do scraper"""
    
    def __init__(self):
        self.email = None
        self.senha = None
        self.auto_login = False
    
    def carregar_credenciais(self):
        """Carrega credenciais das variáveis de ambiente ou solicita ao usuário"""
        
        # Tenta carregar das variáveis de ambiente primeiro
        self.email = os.getenv('EA_EMAIL')
        self.senha = os.getenv('EA_SENHA')
        
        if self.email and self.senha:
            print("✅ Credenciais encontradas nas variáveis de ambiente")
            self.auto_login = True
            return True
        
        # Se não encontrou, pergunta ao usuário
        print("\n" + "="*50)
        print("CONFIGURAÇÃO DE LOGIN AUTOMÁTICO")
        print("="*50)
        print("Você pode configurar login automático de duas formas:")
        print("1. Inserir credenciais agora (serão salvas temporariamente)")
        print("2. Configurar variáveis de ambiente (mais seguro)")
        print("3. Continuar com login manual")
        print("="*50)
        
        opcao = input("Escolha uma opção (1/2/3): ").strip()
        
        if opcao == "1":
            return self.solicitar_credenciais()
        elif opcao == "2":
            self.mostrar_instrucoes_variaveis()
            return False
        else:
            print("Continuando com login manual...")
            return False
    
    def solicitar_credenciais(self):
        """Solicita credenciais ao usuário"""
        try:
            print("\n📧 Digite suas credenciais EA:")
            self.email = input("Email: ").strip()
            self.senha = getpass("Senha: ").strip()
            
            if not self.email or not self.senha:
                print("❌ Email e senha são obrigatórios")
                return False
            
            # Confirma se quer usar login automático
            confirmar = input(f"\nUsar login automático para {self.email}? (s/n): ").strip().lower()
            
            if confirmar in ['s', 'sim', 'y', 'yes']:
                self.auto_login = True
                print("✅ Login automático ativado!")
                return True
            else:
                print("Continuando com login manual...")
                return False
                
        except KeyboardInterrupt:
            print("\n❌ Operação cancelada pelo usuário")
            return False
    
    def mostrar_instrucoes_variaveis(self):
        """Mostra instruções para configurar variáveis de ambiente"""
        print("\n" + "="*60)
        print("CONFIGURAÇÃO DE VARIÁVEIS DE AMBIENTE")
        print("="*60)
        print("Para configurar login automático de forma segura:")
        print()
        print("1. Abra o PowerShell como administrador")
        print("2. Execute os comandos:")
        print()
        print("   [Environment]::SetEnvironmentVariable('EA_EMAIL', 'seu_email@exemplo.com', 'User')")
        print("   [Environment]::SetEnvironmentVariable('EA_SENHA', 'sua_senha', 'User')")
        print()
        print("3. Feche e abra novamente o terminal")
        print("4. Execute o script novamente")
        print("="*60)
        print()
        print("⚠️  IMPORTANTE: As credenciais ficam salvas no sistema")
        print("   Use apenas em computadores pessoais e seguros!")
        print("="*60)
    
    def limpar_credenciais(self):
        """Limpa credenciais da memória"""
        self.email = None
        self.senha = None
        self.auto_login = False 