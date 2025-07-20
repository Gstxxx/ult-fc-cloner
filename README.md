# EA FC 25 Web App Scraper

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Selenium](https://img.shields.io/badge/Selenium-4.0+-green.svg)](https://selenium-python.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-orange.svg)](https://github.com/Gstxxx/ult-fc-cloner/releases)

Um scraper simples e eficiente para coletar dados dos jogadores do EA FC 25 Web App.

## 🚀 Quick Start

### Download do Executável
- **Windows**: [FC25_Scraper_v1.0.0.zip](https://github.com/Gstxxx/ult-fc-cloner/releases/download/v1.0.0/FC25_Scraper_v1.0.0.zip) (31MB)
- Extraia e execute `fc25_scraper.exe`

### Instalação Python
```bash
# Clone o repositório
git clone https://github.com/Gstxxx/ult-fc-cloner.git
cd ult-fc-cloner

# Instale as dependências
pip install -r requirements.txt

# Execute o scraper
python fc25_scraper.py
```

## 📋 Pré-requisitos

- **Python 3.8+** ou **Windows 10/11**
- **Chrome Browser** instalado
- **Conta EA** com acesso ao FC 25 Web App
- **Conexão com internet** estável

## 🎯 Como Usar

### 1. Execução Simples
```bash
python fc25_scraper.py
```

### 2. Processo de Login
1. O script abrirá o Chrome automaticamente
2. Faça login na sua conta EA
3. Navegue até **Clube > Jogadores**
4. Pressione **ENTER** no terminal quando estiver pronto

### 3. Coleta Automática
- O script coletará dados de todas as páginas automaticamente
- Progresso mostrado no terminal
- Dados exportados para `jogadores_fc25.csv`

## 📊 Dados Coletados

| Campo | Descrição | Exemplo |
|-------|-----------|---------|
| `nome` | Nome do jogador | "Lionel Messi" |
| `overall` | Overall do jogador | "91" |
| `posicao` | Posição no campo | "RW" |
| `clube` | Clube atual | "Inter Miami" |

## 📁 Estrutura do Projeto

```
ult-fc-cloner/
├── fc25_scraper.py          # Script principal (150 linhas)
├── requirements.txt         # Dependências Python
├── README.md               # Este arquivo
├── build_exe.py            # Script para criar executável
├── create_release.py       # Script para criar releases
├── dist/                   # Executável gerado
└── build/                  # Arquivos de build
```

## 🔧 Desenvolvimento

### Instalação para Desenvolvimento
```bash
# Clone o repositório
git clone https://github.com/Gstxxx/ult-fc-cloner.git
cd ult-fc-cloner

# Crie um ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instale dependências
pip install -r requirements.txt
```

### Criando Executável
```bash
# Execute o script de build
python build_exe.py

# Ou use PyInstaller diretamente
pyinstaller fc25_scraper.spec
```

### Criando Release
```bash
# Execute o script de release
python create_release.py

# Ou siga o guia manual
# Ver: GUIA_RELEASE.md
```

## 📦 Dependências

```
selenium>=4.0.0
pandas>=1.3.0
webdriver-manager>=3.8.0
pyinstaller>=5.0.0  # Apenas para build
```

## 🛠️ Funcionalidades

### ✅ Implementadas
- [x] Login manual seguro
- [x] Coleta automática de dados
- [x] Paginação automática
- [x] Exportação CSV
- [x] Preview dos dados
- [x] Executável Windows
- [x] Tratamento de erros
- [x] Logs detalhados

### 🔄 Próximas Funcionalidades
- [ ] Interface gráfica
- [ ] Filtros por posição/overall
- [ ] Exportação JSON/Excel
- [ ] Coleta de preços do mercado
- [ ] Análise estatística avançada

## 🐛 Solução de Problemas

### Erro: "ChromeDriver não encontrado"
```bash
# Reinstale as dependências
pip install --upgrade webdriver-manager selenium
```

### Erro: "Elemento não encontrado"
- Verifique se está na página correta (Clube > Jogadores)
- Aguarde o carregamento completo da página
- Tente novamente

### Erro: "Timeout"
- Verifique sua conexão com a internet
- Feche outros programas que usam Chrome
- Reinicie o script

## 📈 Estatísticas do Projeto

- **Linhas de código**: 150 (vs 829 originais)
- **Arquivos**: 1 script principal
- **Dependências**: 4 pacotes essenciais
- **Tempo de execução**: ~2-5 minutos
- **Dados coletados**: ~100-1000 jogadores

## 🤝 Contribuindo

1. **Fork** o projeto
2. Crie uma **branch** para sua feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. **Push** para a branch (`git push origin feature/AmazingFeature`)
5. Abra um **Pull Request**

### Diretrizes de Contribuição
- Mantenha o código simples e legível
- Adicione comentários explicativos
- Teste suas mudanças
- Siga o padrão de commits

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- **EA Sports** pelo FC 25 Web App
- **Selenium** pela automação web
- **Pandas** pelo processamento de dados
- **PyInstaller** pela criação de executáveis

## 📞 Suporte

- **Issues**: [GitHub Issues](https://github.com/Gstxxx/ult-fc-cloner/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Gstxxx/ult-fc-cloner/discussions)
- **Wiki**: [Documentação](https://github.com/Gstxxx/ult-fc-cloner/wiki)

---

**⭐ Se este projeto te ajudou, considere dar uma estrela no GitHub!** 