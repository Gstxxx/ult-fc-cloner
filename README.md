# 🏆 EA FC 25 Web App Scraper

Um scraper automatizado para coletar dados dos jogadores do seu clube no EA FC 25 Web App.

## 📋 Descrição

Este projeto permite coletar automaticamente informações de todos os jogadores do seu clube no EA FC 25 Web App, incluindo:
- **Nome do jogador**
- **Overall/Rating**
- **Posição**
- **Clube**
- **Dados exportados em CSV**

## ✨ Funcionalidades

- 🔐 **Login automático** (opcional) ou manual
- 📄 **Paginação automática** - coleta todos os jogadores de todas as páginas
- 🎯 **Seletores precisos** - coleta apenas dados válidos dos jogadores
- 📊 **Exportação CSV** - dados organizados e prontos para análise
- 🛡️ **Tratamento de erros** - robusto e confiável
- 🔄 **Navegação automática** - vai até a página de jogadores automaticamente

## 🚀 Como Funciona

### 1. **Acesso ao Web App**
- Abre o Chrome automaticamente
- Acessa o EA FC 25 Web App
- Configura o navegador para evitar detecção de automação

### 2. **Sistema de Login**
- **Opção 1**: Login automático com credenciais
- **Opção 2**: Login manual (recomendado)
- **Opção 3**: Variáveis de ambiente

### 3. **Navegação Inteligente**
- Detecta automaticamente a página de jogadores
- Navega para "Clube > Jogadores"
- Fallback para navegação manual se necessário

### 4. **Coleta de Dados**
- Identifica cards de jogadores usando seletores precisos
- Extrai dados de cada jogador individualmente
- Filtra apenas jogadores válidos (sem "N/A")
- Processa todas as páginas automaticamente

### 5. **Paginação Automática**
- Detecta botão "Próxima"
- Navega por todas as páginas
- Coleta todos os jogadores do clube
- Para automaticamente na última página

### 6. **Exportação**
- Gera arquivo CSV com todos os dados
- Preview dos dados coletados
- Estatísticas da coleta

## 📦 Instalação

### Pré-requisitos
- Python 3.8+
- Google Chrome
- Conta EA FC 25

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd ult-fc-cloner
```

### 2. Crie um ambiente virtual
```bash
python -m venv .venv
```

### 3. Ative o ambiente virtual
```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 4. Instale as dependências
```bash
pip install -r requirements.txt
```

## 🎯 Como Usar

### Execução Simples
```bash
python fc25_scraper.py
```

### Processo Completo

1. **Execute o script**
   ```bash
   python fc25_scraper.py
   ```

2. **Configure o login** (opcional)
   - Escolha entre login automático ou manual
   - Para login automático, insira email e senha
   - Para login manual, continue com a opção 3

3. **Faça login manualmente**
   - O navegador abrirá o EA FC 25 Web App
   - Faça login na sua conta EA
   - Navegue até "Clube > Jogadores"
   - Pressione ENTER no terminal

4. **Aguarde a coleta**
   - O scraper processará automaticamente todas as páginas
   - Você verá o progresso em tempo real
   - Todos os jogadores serão coletados

5. **Resultado**
   - Arquivo `jogadores_fc25.csv` será gerado
   - Preview dos dados será mostrado
   - Estatísticas da coleta serão exibidas

## 📊 Dados Coletados

### **Dados Básicos:**
- **Nome**: Nome completo do jogador
- **Overall**: Overall rating do jogador
- **Posição**: Posição principal do jogador (ex: ST, CM, CB)
- **Clube**: Clube atual do jogador
- **Rating**: Rating geral (mesmo que Overall)

### **Dados Expandidos:**
- **Qualidade**: Tipo do card (Base, Special, Hero, Icon, TOTS, etc.)
- **Nação**: Nacionalidade do jogador
- **Liga**: Liga do jogador (ex: Icon, Premier League, etc.)
- **Status**: Se o jogador é tradeable ou untradeable
- **Posições_Alternativas**: Outras posições que o jogador pode jogar

### **Estatísticas Detalhadas:**
- **PAC**: Pace (Velocidade)
- **SHO**: Shooting (Finalização)
- **PAS**: Passing (Passe)
- **DRI**: Dribbling (Drible)
- **DEF**: Defending (Defesa)
- **PHY**: Physical (Físico)

### **Traits:**
- **Traits**: Características especiais do jogador (ex: Pinged Pass, First Touch)

## 📊 Exemplo de Saída

### Arquivo CSV gerado:
```csv
Nome,Overall,Posição,Clube,Rating,Qualidade,Nação,Liga,PAC,SHO,PAS,DRI,DEF,PHY,Traits,Status,Posições_Alternativas
Essien,97,CDM,N/A,97,Icon,Gana,Icon,85,73,89,85,90,91,Pinged Pass,First Touch,Tradeable,CM
Kanu,97,ST,N/A,97,Icon,Nigéria,Icon,87,95,78,88,45,82,Power Header,Untradeable,
Yıldız,96,LW,N/A,96,TOTS,Turquia,Super Lig,92,88,85,94,45,78,Flair,Untradeable,RW
...
```

### Estatísticas típicas:
```
Total de jogadores coletados: 199
Páginas processadas: 10
Taxa de sucesso: 100%
```

## ⚙️ Configuração

### Login Automático

#### Opção 1: Inserir credenciais
```bash
python fc25_scraper.py
# Escolha opção 1 e insira email/senha
```

#### Opção 2: Variáveis de ambiente
```bash
# Windows
set EA_EMAIL=seu_email@exemplo.com
set EA_PASSWORD=sua_senha

# Linux/Mac
export EA_EMAIL=seu_email@exemplo.com
export EA_PASSWORD=sua_senha
```

### Configurações Avançadas

Edite o arquivo `config.py` para personalizar:
- Timeouts
- Seletores CSS
- Configurações do navegador

## 🔧 Estrutura do Projeto

```
ult-fc-cloner/
├── fc25_scraper.py      # Script principal
├── config.py            # Configurações e credenciais
├── requirements.txt     # Dependências Python
├── setup.py            # Configuração do projeto
├── README.md           # Este arquivo
├── .gitignore          # Arquivos ignorados pelo Git
├── .venv/              # Ambiente virtual
├── __pycache__/        # Cache Python
├── fc25_scraper.log    # Log de execução
└── jogadores_fc25.csv  # Dados coletados
```

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+** - Linguagem principal
- **Selenium** - Automação do navegador
- **ChromeDriver** - Driver do Chrome (gerenciado automaticamente)
- **Pandas** - Manipulação de dados CSV
- **WebDriver Manager** - Gerenciamento automático do driver

## 🔍 Como Funciona Tecnicamente

### 1. **Navegação**
```python
# Navegação para Club > Players
"button.ut-tab-bar-item.icon-club"  # Botão Club na navbar
"div.players-tile"                  # Tile Players no hub
"h1:contains('Players')"           # Header Players
```

### 2. **Detecção de Cards**
```python
# Seletor principal para cards de jogadores
"li.listFUTItem"  # Container principal do card
".name"           # Nome do jogador
".rating"         # Overall/Rating
".position"       # Posição
```

### 3. **Extração de Dados Expandidos**
```python
# Estatísticas detalhadas
".player-stats-data-component li"   # Container de stats
".label"                           # Label da stat (PAC, SHO, etc.)
".value"                           # Valor da stat

# Informações de nação/liga
".ut-item-view--bio .ut-item-row"  # Seção bio
".ut-item-row-label--left"         # Labels (IRE, ICN, etc.)

# Traits
".ut-item-view--traits .ut-item-row .ut-item-row-label--left"

# Qualidade do card
card.get_attribute('class')        # Classes CSS para determinar qualidade
```

### 4. **Paginação**
```python
# Detecta botão "Próxima"
"button.pagination.next"
"button.flat.pagination.next"
```

### 5. **Extração de Dados**
- Usa seletores CSS precisos
- Valida dados antes de adicionar
- Filtra cards vazios ou inválidos
- Trata caracteres especiais
- Extrai dados expandidos (stats, traits, qualidade)

### 6. **Robustez**
- Múltiplos métodos de inicialização do driver
- Fallbacks para diferentes cenários
- Tratamento de erros abrangente
- Logs detalhados para debug

## ⚠️ Limitações e Considerações

### Limitações
- Requer login manual ou credenciais válidas
- Depende da estrutura HTML do EA FC 25 Web App
- Pode ser afetado por mudanças na interface
- Requer conexão estável com a internet

### Considerações de Segurança
- **NUNCA** compartilhe suas credenciais
- Use variáveis de ambiente para credenciais
- O script não armazena senhas permanentemente
- Recomendado usar login manual

### Performance
- Coleta ~200 jogadores em ~5-10 minutos
- Depende da velocidade da internet
- Pode ser mais lento com muitos jogadores

## 🐛 Solução de Problemas

### Problema: "ChromeDriver não encontrado"
```bash
# Reinstale as dependências
pip install --upgrade webdriver-manager selenium
```

### Problema: "Nenhum jogador encontrado"
- Verifique se está na página correta
- Aguarde o carregamento completo
- Tente navegar manualmente para "Clube > Jogadores"

### Problema: "Botão Próxima não encontrado"
- Verifique se há mais páginas
- O script para automaticamente na última página
- Isso é normal quando todos os jogadores foram coletados

### Problema: "Erro de encoding"
- O script trata caracteres especiais automaticamente
- Verifique se o terminal suporta UTF-8

## 📈 Melhorias Futuras

- [ ] Coleta de estatísticas detalhadas dos jogadores
- [ ] Suporte a múltiplos clubes
- [ ] Interface gráfica (GUI)
- [ ] Análise automática dos dados
- [ ] Comparação entre jogadores
- [ ] Recomendações de formação
- [ ] Exportação para outros formatos (JSON, Excel)

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto é para uso educacional e pessoal. Respeite os termos de uso do EA FC 25.

## ⚖️ Disclaimer

Este scraper é para uso pessoal e educacional. Respeite os termos de serviço do EA e não use para fins comerciais ou maliciosos. O autor não se responsabiliza pelo uso inadequado.

---

**Desenvolvido com ❤️ para a comunidade EA FC 25**

*Última atualização: Julho 2025* 