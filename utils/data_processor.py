#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Processamento de dados para o EA FC 25 Web App Scraper
"""

import pandas as pd
import logging

logger = logging.getLogger(__name__)

class DataProcessor:
    """Processa e valida dados dos jogadores"""
    
    def __init__(self):
        self.df = None
    
    def processar_dados(self, jogadores):
        """Processa e valida os dados dos jogadores"""
        try:
            if not jogadores:
                logger.warning("Nenhum jogador para processar")
                return None
            
            # Cria DataFrame
            self.df = pd.DataFrame(jogadores)
            
            # Remove duplicatas
            self.df = self.df.drop_duplicates(subset=['nome', 'overall', 'posicao'])
            
            # Limpa dados
            self._limpar_dados()
            
            # Valida dados
            self._validar_dados()
            
            # Ordena por overall
            if 'overall' in self.df.columns:
                try:
                    self.df['overall_numeric'] = pd.to_numeric(self.df['overall'], errors='coerce')
                    self.df = self.df.sort_values('overall_numeric', ascending=False)
                    self.df = self.df.drop('overall_numeric', axis=1)
                except:
                    pass
            
            logger.info(f"Dados processados: {len(self.df)} jogadores válidos")
            return self.df.to_dict('records')
            
        except Exception as e:
            logger.error(f"Erro ao processar dados: {str(e)}")
            return None
    
    def _limpar_dados(self):
        """Limpa e padroniza os dados"""
        try:
            # Remove linhas com dados vazios essenciais
            colunas_essenciais = ['nome', 'overall']
            for col in colunas_essenciais:
                if col in self.df.columns:
                    self.df = self.df.dropna(subset=[col])
                    self.df = self.df[self.df[col] != '']
                    self.df = self.df[self.df[col] != 'N/A']
            
            # Padroniza valores
            if 'clube' in self.df.columns:
                self.df['clube'] = self.df['clube'].fillna('N/A')
            
            if 'nacao' in self.df.columns:
                self.df['nacao'] = self.df['nacao'].fillna('N/A')
            
            if 'liga' in self.df.columns:
                self.df['liga'] = self.df['liga'].fillna('N/A')
            
            # Remove espaços extras
            for col in self.df.columns:
                if self.df[col].dtype == 'object':
                    self.df[col] = self.df[col].astype(str).str.strip()
            
        except Exception as e:
            logger.warning(f"Erro ao limpar dados: {str(e)}")
    
    def _validar_dados(self):
        """Valida a qualidade dos dados"""
        try:
            total_inicial = len(self.df)
            
            # Valida overall (deve ser número entre 1-99)
            if 'overall' in self.df.columns:
                try:
                    overall_numeric = pd.to_numeric(self.df['overall'], errors='coerce')
                    self.df = self.df[overall_numeric.between(1, 99)]
                except:
                    pass
            
            # Valida posições conhecidas
            posicoes_validas = ['GK', 'CB', 'LB', 'RB', 'CDM', 'CM', 'CAM', 'LM', 'RM', 'LW', 'RW', 'ST', 'CF']
            if 'posicao' in self.df.columns:
                self.df = self.df[self.df['posicao'].isin(posicoes_validas)]
            
            total_final = len(self.df)
            removidos = total_inicial - total_final
            
            if removidos > 0:
                logger.info(f"Validação: {removidos} registros removidos por dados inválidos")
            
        except Exception as e:
            logger.warning(f"Erro ao validar dados: {str(e)}")
    
    def gerar_estatisticas(self):
        """Gera estatísticas dos dados processados"""
        try:
            if self.df is None or len(self.df) == 0:
                return {}
            
            stats = {
                'total_jogadores': len(self.df),
                'overall_medio': None,
                'overall_max': None,
                'overall_min': None,
                'posicoes': {},
                'qualidades': {},
                'status': {}
            }
            
            # Overall
            if 'overall' in self.df.columns:
                try:
                    overall_numeric = pd.to_numeric(self.df['overall'], errors='coerce')
                    stats['overall_medio'] = overall_numeric.mean()
                    stats['overall_max'] = overall_numeric.max()
                    stats['overall_min'] = overall_numeric.min()
                except:
                    pass
            
            # Posições
            if 'posicao' in self.df.columns:
                stats['posicoes'] = self.df['posicao'].value_counts().to_dict()
            
            # Qualidades
            if 'qualidade' in self.df.columns:
                stats['qualidades'] = self.df['qualidade'].value_counts().to_dict()
            
            # Status
            if 'status' in self.df.columns:
                stats['status'] = self.df['status'].value_counts().to_dict()
            
            return stats
            
        except Exception as e:
            logger.error(f"Erro ao gerar estatísticas: {str(e)}")
            return {} 