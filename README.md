# EA FC 25 Web App Scraper

Script automatizado para coletar dados dos jogadores do EA FC 25 Web App.

## 🚀 Funcionalidades

- **Navegação Automática**: Clube → Jogadores
- **Coleta Completa**: Todos os dados dos jogadores
- **Exportação CSV**: Dados organizados em planilha
- **Estatísticas**: Resumo da coleta

## 📊 Dados Coletados

### Informações Básicas
- **Nome**: Nome do jogador
- **Overall**: Rating geral
- **Posição**: Posição principal (VOL, MC, etc.)
- **Clube**: Clube atual
- **Nação**: País de origem
- **Liga**: Liga atual
- **Qualidade**: Tipo do card (Base, Special, Icon, Hero)

### Estatísticas
- **RIT**: Ritmo
- **FIN**: Finalização  
- **PAS**: Passe
- **CON**: Controle
- **DEF**: Defesa
- **FÍS**: Físico

### Status e Detalhes
- **Status**: Tradeable/Untradeable
- **Ativo**: Se está no elenco ativo
- **Traits**: Características especiais
- **Posições Alternativas**: Outras posições que pode jogar

## 🛠️ Instalação

### Pré-requisitos
- Python 3.8+
- Google Chrome
- Conta EA FC 25

### Dependências
```bash
pip install -r requirements.txt
```

## 🎯 Como Usar

### 1. Execução Manual
```bash
python fc25_scraper.py
```

### 2. Executável Windows
```bash
# Execute o arquivo
dist/fc25_scraper.exe
```

## 📋 Fluxo de Uso

1. **Execute o script**
2. **Faça login manual** na sua conta EA
3. **Pressione ENTER** quando estiver logado
4. **Aguarde** a navegação e coleta automática
5. **Verifique** o arquivo `jogadores_fc25.csv`

## 📁 Arquivos Gerados

- `jogadores_fc25.csv`: Dados completos dos jogadores
- Estatísticas no console: Resumo da coleta

## 🔧 Build do Executável

```bash
python build_exe.py
```

O executável será criado em `dist/fc25_scraper.exe`

## 📈 Exemplo de Saída

```
============================================================
EA FC 25 WEB APP SCRAPER
============================================================
1. Configurando driver do Chrome...
2. Acessando EA FC 25 Web App...
3. Aguardando login manual...

==================================================
LOGIN MANUAL REQUERIDO
==================================================
1. Faça login na sua conta EA no navegador
2. Pressione ENTER quando estiver logado
3. O programa fará a navegação e coleta automaticamente
==================================================

4. Navegando para Clube...
✅ Navegação para Clube concluída
5. Navegando para Jogadores...
✅ Navegação para Jogadores concluída
6. Coletando dados dos jogadores...
Iniciando coleta de dados...
Processando página 1...
Encontrados 24 jogadores na página 1
Coleta concluída! Total: 254 jogadores
7. Exportando dados...

CSV exportado: jogadores_fc25.csv
Total de jogadores: 254
Overall médio: 78.2
Posições únicas: 8
Clubes únicos: 15
Qualidades únicas: 4
Tradeable: 180
Untradeable: 74
Ativos: 23

🎉 Scraping concluído com sucesso!
📊 Verifique o arquivo 'jogadores_fc25.csv'
```

## 🎮 Compatibilidade

- ✅ EA FC 25 Web App
- ✅ Windows 10/11
- ✅ Google Chrome
- ✅ Conta EA válida

## 📝 Notas

- **Login Manual**: Sempre necessário fazer login manualmente
- **Navegação Automática**: Após login, tudo é automatizado
- **Dados Completos**: Coleta todas as informações disponíveis
- **Exportação CSV**: Formato compatível com Excel/Google Sheets

## 🔄 Atualizações

- **v2.0**: Fluxo automatizado completo
- **v1.0**: Versão inicial com coleta manual

## 📞 Suporte

Para dúvidas ou problemas, abra uma issue no GitHub.

---

**Desenvolvido para facilitar a análise de elencos do EA FC 25** ⚽ 