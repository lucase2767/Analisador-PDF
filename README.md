# PDF Chat RAG

Este é um aplicativo web interativo criado com [Streamlit](https://streamlit.io/) que permite o upload de arquivos PDF e a realização de perguntas e respostas (Q&A) baseadas no conteúdo do documento. O projeto utiliza a arquitetura RAG (Retrieval-Augmented Generation) suportada pelo [LangChain](https://www.langchain.com/) e a API do Google Generative AI (Gemini).

## 🚀 Funcionalidades

- **Upload de PDF:** Envie um documento PDF diretamente pela interface da barra lateral.
- **Processamento Automático:** O documento é lido, dividido em partes menores (chunks) e indexado automaticamente em um banco de dados vetorial local (ChromaDB).
- **Chatbot Inteligente:** Interaja com um assistente virtual baseado no modelo `gemini-pro` que responde às suas perguntas referenciando exclusivamente o conteúdo do PDF fornecido.
- **Gerenciamento de Contexto:** Ao enviar um novo PDF, o contexto e o banco de dados do documento anterior são limpos para evitar cruzamento de informações.

## 📋 Pré-requisitos

- Python (versão recomendada: 3.10 a 3.14)
- Chave de API do Google Gemini (obtida no Google AI Studio)

## 🔧 Como Instalar e Rodar


### Passo 0.5 (Opcional): **Crie e ative um ambiente virtual:**
   ```bash
   python -m venv .venv
   
   # No Windows
   .\.venv\Scripts\activate
   
   # No Linux/MacOS
   source .venv/bin/activate
   ```

### Passo 1: **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

### Passo 2: **Configuração da Variável de Ambiente:**
   Copie e cole o arquivo .env.example e renomeie para .env, apos isso adicione sua chave de API do Google, ou:
   ```env
   GOOGLE_API_KEY=sua_chave_de_api_aqui
   ```

### Passo 3: **Execute o aplicativo:**
   ```bash
   streamlit run app.py
   ```

## 🤝 Como Usar

1. No menu lateral da página web que foi aberta, na área de Upload, clique em **Browse files** (ou "Escolher arquivo") e faça o upload de um PDF.
2. Clique no botão **Processar Documento**. O sistema irá ler o arquivo, carregar as partes na memória e disponibilizar no bot.
3. Após aparecer a mensagem verde de sucesso ("Pronto! Pode começar a perguntar."), escreva suas perguntas sobre o assunto do PDF na caixa de texto na parte inferior do aplicativo.

## Objetivos

Esse projeto foi feito para aprender a usa RAG e separar um unico prompt "nesse caso o PDF" e separa-lo em pedaços menores o documento possa ser ingerido pela IA.

Esses parametros são então salvos em um banco de dados vetorial local (ChromaDB), e ao mesmo tempo, são guardadas as coordenadas de cada parte do documento, e quando o usuário faz uma pergunta, a IA busca os pedaços mais relevantes do documento, analisa e responde de acordo.

Essa separação inteligente é o nucleo que separa esse projeto do projeto de Analisador de issues.