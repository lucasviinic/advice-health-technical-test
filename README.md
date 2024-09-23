# AdviceHealth Technical Test

API RESTful desenvolvida em Python e Flask, que serve como backend para um sistema de gerenciamento de carros e proprietários.

## O problema

> Nork-Town is a weird place. Crows cawk the misty morning while old men squint. It’s a small town, so the mayor had a bright idea 
to limit the number of cars a person may possess. One person may have up to 3 vehicles. The vehicle, registered to a person, may have
one color, ‘yellow’, ‘blue’ or ‘gray’. And one of three models, ‘hatch’, ‘sedan’ or ‘convertible’. Carford car shop want a system where 
they can add car owners and cars. Car owners may not have cars yet, they need to be marked as a sale opportunity. Cars cannot exist in the system without owners.

## Pré-requisitos

- Python
- Docker

## Configuração do projeto
### 1. Clonar o repositório
```
git clone https://github.com/lucasviinic/advice-health-technical-test.git
cd advice-health-technical-test
```

### 2. Configurar variáveis de ambiente
Crie um arquivo .env na raiz do projeto com as seguintes variáveis (confira o .env.example):
```
DATABASE_URL=postgresql://postgres:test1234!@db:5432/AutoRepairShopDB
DB_USER=postgres
DB_PASSWORD=test1234!
DB_NAME=AutoRepairShopDB
```
Essas variáveis irão configurar a conexão com o banco de dados PostgreSQL que será iniciado com o Docker Compose.

### 3. Instalar dependências
As dependências do projeto serão instaladas automaticamente dentro do container Docker, então você não precisa instalá-las manualmente em sua máquina local.

Se quiser rodar o ambiente de desenvolvimento fora do Docker, você pode criar um ambiente virtual Python e instalar as dependências manualmente:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Executar migrações do banco de dados

Se for a primeira vez que está rodando a API, você precisará aplicar as migrações do banco de dados:
```
docker-compose exec web flask db upgrade
```

### 5. Executar os testes

Para rodar os testes automatizados:
```
docker-compose run test
```

### Estrutura do projeto

```
.
├── app
│   ├── database.py              # Configuração do banco de dados
│   ├── models                   # Modelos do banco de dados (Carro, Dono)
│   ├── repositories             # Repositórios para manipulação dos dados
│   ├── routes                   # Rotas de autenticação, carros e donos
│   └── usecases                 # Casos de uso
├── migrations                   # Migrações do banco de dados
├── tests                        # Testes unitários e de integração
├── docker-compose.yml           # Arquivo de configuração do Docker Compose
├── Dockerfile                   # Dockerfile para build da aplicação
├── requirements.txt             # Dependências do projeto
├── start.sh                     # Script para iniciar a aplicação no Docker
└── README.md                    # Instruções para o setup e execução
```

### Diagrama ER

<img src="https://i.imgur.com/YgXIIV9.png" width="700"/>
