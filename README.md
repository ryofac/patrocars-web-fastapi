# Cadastro de Montadoras e Veículos

## Descrição

Este projeto tem como objetivo simular uma experiência de desenvolvimento de sistemas web no estilo dos anos 2000. O sistema implementa um CRUD básico para o cadastro de montadoras e veículos, com persistência de dados em um banco de dados relacional, utilizando PostgreSQL.

### Funcionalidades

- **Montadoras**: Adicionar, Listar, Detalhar, Editar e Remover.
- **Veículos**: Adicionar, Listar, Detalhar, Editar e Remover.

**Obs:** A relação entre modelos de carros e veículos ainda precisa ser implementada.

### Tecnologias Utilizadas

- **Banco de Dados Relacional**: PostgreSQL.
- Persistência de dados pode ser feita diretamente ou através de uma biblioteca ou ORM à sua escolha.
- Deploy está sendo realizado na plataforma Render.

## Instruções para Execução

1. Crie um arquivo .env na raiz do projeto com a estrutura de .env.example
2. Certifique-se de ter o Docker e Docker Compose instalados em sua máquina.
3. Para iniciar o ambiente local, execute o seguinte comando:

   ```bash
   docker compose -f local.yml up
   ```
4. O sistema estará disponível em ```localhost:8000```

## Proximos Passos:
- Implementação do relacionamento entre modelos de carro e carros
- Implementação de validação de formulário
- Melhorias visuais

## Deploy
O deploy do sistema está sendo realizado na plataforma Render, com PostgreSQL configurado para o banco de dados.
- Link: https://patrocars-web-fastapi.onrender.com
