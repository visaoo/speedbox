# 🚚 SpeedBox

SpeedBox é uma aplicação que conecta clientes e empresas a entregadores de forma eficiente e ágil, realizando coletas e entregas em nível municipal, estadual e interestadual. Atuamos como uma ponte entre o remetente e o destinatário.

O projeto possui um backend funcional com frontend básico ainda em desenvolvimento. Nosso objetivo é oferecer uma plataforma completa com múltiplos tipos de usuários: cliente, empresa e entregador.

---

Abaixo estão algumas imagens da interface gráfica da aplicação (em desenvolvimento):

![image](https://github.com/user-attachments/assets/b1b9ed36-30fa-4f01-a6c4-27b0bc7859e7)

Como rodar a interface gráfica da aplicação:

```
bash:

poetry run uvicorn api.main:app --reload
```

---

🖥️ Execução via Terminal
Abaixo uma prévia da aplicação rodando no terminal:

![image](https://github.com/user-attachments/assets/b8d432b8-8325-4e6d-a4ec-3826b05f7fc6)

---

## 🧠 Funcionalidades principais

* Cadastro e login de usuários (cliente, empresa e entregador)
* Criação e visualização de pedidos
* Aceitação de pedidos por entregadores
* Interface de dashboard básica para cada tipo de usuário

---

## 🗂 Estrutura do Projeto

```
├── api/                 # Arquivos da landing page e ponto de entrada da API
├── app/                 # Lógica principal da aplicação (dashboards, login, pedidos)
├── classes/             # Classes e modelos (usuário, pedido, transação, etc.)
├── db/                  # Conexão e operações com o banco de dados
├── validations/         # Validações auxiliares
├── init_db.py           # Script para inicializar o banco de dados
├── populate.py          # Script para popular dados iniciais
├── database.db          # Banco de dados SQLite
├── pyproject.toml       # Gerenciador de dependências (Poetry)
```

---

## ▶️ Como rodar o projeto localmente

1. Instale o Poetry:

   ```bash
   pip install poetry
   ```

2. Ative o ambiente virtual:

   ```bash
   poetry shell
   ```

3. Instale as dependências:

   ```bash
   poetry install
   ```

4. Rode o servidor com Uvicorn:

   ```bash
   poetry run uvicorn api.main:app --reload
   ```

   Caso queira especificar uma porta:

   ```bash
   poetry run uvicorn api.main:app --reload --port 8001
   ```

---

## ⚙️ Comandos úteis

* Rodar linter:

  ```bash
  task lint
  ```

* Formatar código:

  ```bash
  task format
  ```

* Adicionar dependência:

  ```bash
  poetry add nome-da-biblioteca
  ```

* Adicionar dependência apenas para desenvolvimento:

  ```bash
  poetry add --group dev nome-da-biblioteca
  ```

---

## 🔐 Tipos de usuários

* 👤 Cliente: faz pedidos de coleta e entrega
* 🏢 Empresa: solicita entregas de produtos ou documentos
* 🛵 Entregador: aceita pedidos e realiza as entregas

---

## 📌 Observações

* A landing page ainda não está funcional, mas estática, servindo como protótipo visual.
* O backend é o foco atual e pode ser acessado via FastAPI no arquivo `main.py`.

---

## 📜 Licença

Este projeto está licenciado sob a Licença Pública Geral GNU, versão 3 (GPLv3). Veja o arquivo [LICENSE](./LICENSE) para mais detalhes.
