# QA Automation Project - Python + Selenium + PyTest + Allure

Este é um framework robusto e escalável de automação de testes Web desenvolvido em **Python**, utilizando **Selenium WebDriver** para interação com o navegador, **PyTest** para orquestração e asserções de testes, a arquitetura **Page Object Model (POM)** para facilidade de manutenção e **Allure Report** para geração de relatórios interativos com evidências visuais e logs.

---

## Funcionalidades Principais

- **Arquitetura Page Object Model (POM):** Separação clara entre a lógica de negócio dos testes (`tests/`) e o mapeamento/interação com elementos da interface (`pages/`).
- **Gerenciamento Automático do Driver:** Utilização do `webdriver-manager` para baixar e atualizar automaticamente a versão correta do Chrome Driver no sistema.
- **Interações Seguras com Esperas Explícitas:** Métodos encapsulados na `BasePage` com `WebDriverWait` e `ExpectedConditions` para evitar falhas por tempo de carregamento (*flaky tests*).
- **Captura Automática de Evidências em Falhas:** Hook customizado no `conftest.py` que tira um print automático da tela no exato momento do erro e o salva na pasta `logs/`.
- **Relatórios Interativos com Allure:** Anexo de screenshots e logs detalhados diretamente nas etapas do relatório gráfico do Allure.
- **Gerenciamento de Logs Estruturados:** Registro detalhado de cada ação no console e em arquivos de log diários na pasta `logs/execution_YYYYMMDD.log`.

---

## Estrutura do Projeto

```text
QA_Selenium_Project/
├── logs/                   # Capturas de tela (.png) e arquivos de log (.log) gerados em falhas
├── pages/                  # Camada do Page Object Model
│   ├── __init__.py
│   ├── base_page.py        # Métodos genéricos do Selenium (esperas, cliques, digitação, screenshots)
│   └── login_page.py       # Mapeamento de elementos e fluxos específicos da tela de login
├── tests/                  # Suíte de testes automatizados
│   ├── __init__.py
│   └── test_login.py       # Casos de teste funcionais com PyTest e anotações Allure
├── conftest.py             # Setup/Teardown do WebDriver e captura automática de erros
├── requirements.txt        # Dependências do projeto (Selenium, PyTest, Allure, etc.)
└── README.md               # Documentação e instruções de uso do projeto
```

---

## Pré-requisitos

Antes de executar os testes, certifique-se de possuir em sua máquina:

1. **Python 3.10 ou superior:** Verifique a instalação com:
   ```bash
   python --version
   ```
2. **Navegador Google Chrome:** Instalado e atualizado.
3. **Allure CLI (Opcional para visualização gráfica):** Instruções de instalação em [Allure Docs](https://allurereport.org/).

---

## Instalação das Dependências

1. **Clone este repositório:**
   ```bash
   git clone https://github.com/Robson-37/QA_Selenium_Project.git
   cd QA_Selenium_Project
   ```

2. **Instale as bibliotecas necessárias:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Como Executar os Testes

### 1. Execução Padrão (com interface gráfica do navegador)

```bash
pytest
```

### 2. Execução com Logs Detalhados no Terminal

```bash
pytest -v -s
```

### 3. Execução no Modo Headless (Sem abrir a janela do navegador)

```bash
pytest --headless
```

### 4. Execução e Geração do Relatório Allure

Execute os testes salvando os dados do relatório na pasta `allure-results`:

```bash
pytest --alluredir=allure-results
```

Em seguida, abra o relatório interativo no seu navegador:

```bash
allure serve allure-results
```

---

## Relatório de Testes e Evidências

Durante e após a execução, o projeto gera automaticamente:

1. **Capturas de Tela em Falhas (`logs/`):** Imagens no formato `FAIL_<nome_do_teste>_<data_hora>.png`.
2. **Logs de Execução (`logs/`):** Arquivos `execution_YYYYMMDD.log` contendo o histórico de passos.
3. **Dashboard Allure:** Gráficos de taxa de sucesso/falha, tempos de execução e prints anexados em cada falha.

---

## 📄 Licença

Este projeto é mantido para fins de automação de testes de qualidade de software (QA). Sinta-se à vontade para utilizar e expandir a arquitetura!
