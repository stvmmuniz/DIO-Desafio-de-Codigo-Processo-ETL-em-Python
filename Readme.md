# 📊 Desafio de Código – Pipeline ETL em Python

Este projeto tem como objetivo demonstrar, de forma prática, a aplicação dos conceitos e boas práticas de **ETL (Extract, Transform, Load)** utilizando Python. O pipeline foi desenvolvido a partir de dados públicos do **Portal da Transparência**, preparando o dataset final para análise no **Power BI**.

A solução foi estruturada de maneira modular e organizada, facilitando a leitura, manutenção e reaproveitamento do código, além de evidenciar a capacidade técnica aplicada na resolução do desafio.

<br>

# ⚙️ Etapa 0 – Configuração do Ambiente

Nesta etapa inicial, o ambiente é preparado para garantir organização e reprodutibilidade do processo:

Importação de bibliotecas padrão do Python (`os`, `zipfile`, `glob`, `unicodedata`) e bibliotecas externas amplamente utilizadas em projetos de dados (`requests` e `pandas`);

Definição de diretórios separados para **dados brutos** (`data_raw`) e **dados processados** (`data_processed`), seguindo boas práticas de organização;

Criação automática dessas pastas, evitando erros em execuções futuras.

Essa estrutura facilita tanto o entendimento do fluxo quanto a escalabilidade do projeto.

<br>

# 📥 Etapa 1 – Extração dos Dados (Extract)

A etapa de extração é responsável por obter os dados diretamente da fonte oficial:

* **Download automatizado** do arquivo ZIP a partir do Portal da Transparência, utilizando requisições HTTP com tratamento de erros;

* **Armazenamento do arquivo bruto localmente**, garantindo rastreabilidade dos dados originais;

* **Extração controlada do conteúdo do ZIP**, evitando duplicidades;

* **Identificação automática do arquivo CSV** para processamento.

Essa abordagem garante **confiabilidade** na origem dos dados e reduz dependências manuais.

<br>

# 🔄 Etapa 2 – Transformação dos Dados (Transform)

Esta é a etapa central do processo, onde os dados brutos são tratados e padronizados para uso analítico.

## 2.1 Padronização dos nomes das colunas

Os nomes das colunas são normalizados para remover acentos, espaços e inconsistências de formatação, facilitando o uso em ferramentas analíticas e evitando erros futuros.

## 2.2 Conversão de valores monetários

A coluna de valores financeiros é convertida corretamente para o tipo numérico, respeitando o padrão brasileiro de separadores decimais, garantindo precisão em cálculos e análises.

## 2.3 Tratamento de datas

A coluna de data é convertida para o formato de data do Python, com tratamento de valores inválidos, assegurando consistência temporal no dataset.

## 2.4 Conversão de códigos numéricos

Colunas que representam códigos administrativos são convertidas para o tipo inteiro, preservando valores nulos quando necessário e garantindo melhor desempenho em análises e relacionamentos.

## 2.5 Padronização de colunas de texto

As colunas textuais passam por limpeza básica, como remoção de espaços extras, garantindo maior qualidade dos dados.

### 🔍 Destaque importante:
A coluna **CodigoFavorecido** foi mantida e tratada como **texto**, pois na base original ela pode conter **valores alfanuméricos**. Essa decisão evita perda de informação e demonstra atenção à natureza real dos dados, uma prática essencial em projetos de dados profissionais.

<br>

# 📈 Etapa 3 – Preparação Final para Análise (Load)

Na etapa final, os dados são preparados para consumo no Power BI:

Garantia dos tipos finais das colunas, assegurando compatibilidade com ferramentas de BI;

Seleção e ordenação das colunas mais relevantes para análise;

Exportação do dataset final em formato CSV, com encoding adequado e separador compatível com o Power BI.

O arquivo final é salvo na pasta de dados processados, pronto para visualizações e análises.

<br>

# ✅ Boas Práticas Aplicadas

Separação clara entre dados brutos e processados;

Código organizado por etapas do ETL;

Tratamento explícito de erros e validações;

Padronização de nomes e tipos de dados;

Decisões técnicas baseadas na natureza real dos dados;

Foco em reprodutibilidade, clareza e qualidade dos dados.

<br>

# 🧩 Código do Pipeline ETL

A seguir estão os arquivos com o código completo utilizado neste projeto, organizado por etapas e com comentários que facilitam o entendimento do fluxo de Extração, Transformação e Preparação dos Dados:

<br>

# 📝 Arquivos

- [X] Projeto Completo (formato Colab .ipynb): [Clique aqui para visualizar o arquivo.](stvmmuniz_Desafio_de_Codigo_Processo_ETL_em_Python.ipynb)

- [X] Python (formato .py): [Clique aqui para visualizar o arquivo.](stvmmuniz_Desafio_de_Codigo_Processo_ETL_em_Python.py)
<br><br>

# 🎯 Conclusão

Este projeto demonstra a aplicação prática de um pipeline ETL completo, desde a extração de dados públicos até a entrega de um dataset pronto para análise. A solução equilibra **qualidade técnica, clareza de implementação e boas práticas de engenharia de dados**, sendo adequada tanto para avaliação técnica quanto para apresentação em um portfólio profissional.