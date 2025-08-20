# 🖥️ Controle de Estoque de TI

## 📌 Descrição
Este projeto é um **sistema de controle de estoque** para o setor de **Tecnologia da Informação (TI)**, desenvolvido para gerenciar ativos como computadores, monitores, periféricos e outros equipamentos. O sistema permite o **registro e empréstimo de ativos**, além de gerar automaticamente **termos de empréstimo** em formato **PDF**. O banco de dados utilizado é o **MySQL**, com integração via **PyMySQL** para realizar consultas e manipulação dos dados.

---

## 🛠️ Tecnologias Utilizadas

- **Python**: Linguagem de programação utilizada para o desenvolvimento do aplicativo.
- **PyQt5**: Framework para a criação de interfaces gráficas de usuário (GUI).
- **Pandas**: Biblioteca para manipulação e análise de dados.
- **ReportLab**: Biblioteca para gerar documentos em formato **PDF**, incluindo os termos de empréstimo.
- **PDF2Image**: Biblioteca para converter o PDF gerado em imagens, caso necessário.
- **PyMySQL**: Biblioteca para interagir com o banco de dados **MySQL**.
- **MySQL**: Sistema de gerenciamento de banco de dados relacional utilizado para armazenar dados de ativos e empréstimos.

---

## 🎯 Funcionalidades

- **Controle de Estoque de Ativos**: Gerencia os ativos de TI (computadores, monitores, etc.), com a possibilidade de adicionar, editar, excluir e consultar equipamentos.
- **Empréstimo de Ativos**: Registra os empréstimos de equipamentos, incluindo os dados do colaborador, data de empréstimo e data prevista para devolução.
- **Geração de Termos de Empréstimo**: Após o empréstimo, o sistema gera um **termo de empréstimo** em formato **PDF** com todos os dados do ativo e do colaborador.
- **Consulta e Relatórios**: Permite a consulta de ativos disponíveis e emprestados, com a possibilidade de gerar relatórios em formato **PDF** ou **CSV**.
- **Banco de Dados MySQL**: Os dados são armazenados em um banco de dados MySQL, permitindo a persistência e a fácil consulta das informações.

---
