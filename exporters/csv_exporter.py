#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exportação de dados para CSV
"""

import csv
import pandas as pd
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class CSVExporter:
    """Gerencia a exportação de dados para CSV"""
    
    def __init__(self):
        self.df = None
    
    def exportar_csv(self, jogadores, filename="jogadores_fc25.csv"):
        """Exporta dados dos jogadores para CSV"""
        try:
            if not jogadores:
                logger.warning("Nenhum jogador para exportar")
                return False
            
            logger.info(f"Exportando {len(jogadores)} jogadores para {filename}...")
            
            # Cria DataFrame
            self.df = pd.DataFrame(jogadores)
            
            # Define ordem das colunas
            colunas_ordenadas = [
                'nome', 'overall', 'posicao', 'clube', 'rating',
                'qualidade', 'nacao', 'liga', 'pac', 'sho', 'pas', 'dri', 'def', 'phy',
                'traits', 'status', 'posicoes_alternativas'
            ]
            
            # Reorganiza colunas (mantém apenas as que existem)
            colunas_existentes = [col for col in colunas_ordenadas if col in self.df.columns]
            self.df = self.df[colunas_existentes]
            
            # Exporta para CSV
            self.df.to_csv(filename, index=False, encoding='utf-8-sig')
            
            logger.info(f"CSV exportado com sucesso: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao exportar CSV: {str(e)}")
            return False
    
    def mostrar_preview(self, num_linhas=5):
        """Mostra preview dos dados exportados"""
        try:
            if self.df is None:
                logger.warning("Nenhum dado para mostrar preview")
                return
            
            print("\n" + "="*80)
            print("PREVIEW DOS DADOS COLETADOS")
            print("="*80)
            
            # Mostra informações básicas
            print(f"Total de jogadores: {len(self.df)}")
            print(f"Colunas: {', '.join(self.df.columns)}")
            print()
            
            # Mostra primeiras linhas
            print("Primeiros jogadores:")
            print(self.df.head(num_linhas).to_string(index=False))
            
            # Mostra estatísticas
            self._mostrar_estatisticas()
            
            print("="*80)
            
        except Exception as e:
            logger.error(f"Erro ao mostrar preview: {str(e)}")
    
    def _mostrar_estatisticas(self):
        """Mostra estatísticas dos dados coletados"""
        try:
            print("\n📊 ESTATÍSTICAS:")
            
            # Overall médio
            if 'overall' in self.df.columns:
                try:
                    overall_numerico = pd.to_numeric(self.df['overall'], errors='coerce')
                    media_overall = overall_numerico.mean()
                    if not pd.isna(media_overall):
                        print(f"   Overall médio: {media_overall:.1f}")
                except:
                    pass
            
            # Posições mais comuns
            if 'posicao' in self.df.columns:
                posicoes = self.df['posicao'].value_counts().head(5)
                print(f"   Top 5 posições: {', '.join([f'{pos}({count})' for pos, count in posicoes.items()])}")
            
            # Qualidades
            if 'qualidade' in self.df.columns:
                qualidades = self.df['qualidade'].value_counts()
                print(f"   Qualidades: {', '.join([f'{qual}({count})' for qual, count in qualidades.items()])}")
            
            # Status
            if 'status' in self.df.columns:
                status = self.df['status'].value_counts()
                print(f"   Status: {', '.join([f'{stat}({count})' for stat, count in status.items()])}")
            
        except Exception as e:
            logger.warning(f"Erro ao calcular estatísticas: {str(e)}")
    
    def gerar_relatorio(self, filename="relatorio_scraping.txt"):
        """Gera um relatório detalhado da coleta"""
        try:
            if self.df is None:
                logger.warning("Nenhum dado para gerar relatório")
                return False
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("RELATÓRIO DE SCRAPING - EA FC 25\n")
                f.write("="*50 + "\n")
                f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                f.write(f"Total de jogadores: {len(self.df)}\n")
                f.write(f"Arquivo CSV: {filename}\n\n")
                
                # Estatísticas detalhadas
                f.write("ESTATÍSTICAS DETALHADAS:\n")
                f.write("-" * 30 + "\n")
                
                if 'overall' in self.df.columns:
                    try:
                        overall_numerico = pd.to_numeric(self.df['overall'], errors='coerce')
                        f.write(f"Overall médio: {overall_numerico.mean():.1f}\n")
                        f.write(f"Overall máximo: {overall_numerico.max()}\n")
                        f.write(f"Overall mínimo: {overall_numerico.min()}\n")
                    except:
                        pass
                
                if 'posicao' in self.df.columns:
                    f.write(f"\nDistribuição por posição:\n")
                    posicoes = self.df['posicao'].value_counts()
                    for pos, count in posicoes.items():
                        f.write(f"  {pos}: {count}\n")
                
                if 'qualidade' in self.df.columns:
                    f.write(f"\nDistribuição por qualidade:\n")
                    qualidades = self.df['qualidade'].value_counts()
                    for qual, count in qualidades.items():
                        f.write(f"  {qual}: {count}\n")
                
                f.write(f"\nColunas coletadas: {', '.join(self.df.columns)}\n")
            
            logger.info(f"Relatório gerado: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao gerar relatório: {str(e)}")
            return False 