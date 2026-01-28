Uma ferramenta que ajude usuários a:
Rastrear atividades diárias de forma intuitiva
Visualizar padrões de produtividade através de gráficos
Identificar horários mais produtivos e distrações frequentes
Tomar decisões baseadas em dados para melhorar o foco

Funcionalidades Principais:
Gerenciamento de Tarefas
Criar, editar, excluir e categorizar atividades
Definir estimativas de tempo vs. tempo real gasto
Classificar por projetos, prioridades e tags
Arrastar e soltar para reordenar
Dashboard Inteligente
Gráficos de produtividade diária/semanal/mensal
Métricas de conclusão (% de tarefas finalizadas)
"Calor de produtividade" por horários do dia
Design totalmente responsivo
Segurança & Usuário
Autenticação JWT com refresh tokens
Senhas hasheadas com bcrypt
Dados isolados por usuário
Performance otimizada

Arquitetura do Sistema:

KairoFlow/
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── api/            # Endpoints REST
│   │   ├── core/           # Configurações e segurança
│   │   ├── models/         # SQLModel + Pydantic
│   │   ├── schemas/        # Esquemas de validação
│   │   └── services/       # Lógica de negócio
│   ├── tests/              # Testes unitários e de integração
│   └── alembic/            # Migrações de banco
├── frontend/               # Aplicação Next.js
│   ├── app/                # App Router (Next.js 14)
│   │   ├── dashboard/      # Páginas principais
│   │   ├── api/            # API routes do frontend
│   │   └── components/     # Componentes React
│   ├── lib/                # Utilitários e hooks
│   ├── styles/             # Estilos Tailwind
│   └── types/              # Tipos TypeScript
└── docker-compose.yml      # Containerização


Tecnologias & Escolhas Técnicas:
Backend (FastAPI + PostgreSQL)
FastAPI: Escolhido pela performance (ASGI), geração automática de docs (Swagger/OpenAPI) e tipagem estática com Pydantic

SQLModel: Combina SQLAlchemy (ORM) + Pydantic (validação) para menos boilerplate

PostgreSQL: Dados relacionais com suporte a JSONB para flexibilidade

JWT: Autenticação stateless e escalável

Frontend (Next.js 14 + TypeScript)
Next.js 14 (App Router): Server-side rendering, melhor SEO, loading states nativos

TypeScript: Segurança de tipos em todo o projeto

Tailwind CSS: Desenvolvimento rápido com design consistente

Recharts: Biblioteca leve e customizável para visualizações

React Hook Form + Zod: Validação de formulários otimizada

Como Executar o Projeto
Opção 1: Docker (Recomendada)
bash
# Clone o repositório
git clone [https://github.com/seu-usuario/KairoFlow.git](https://github.com/NicolasDeNigris91/KairoFlow)
cd KairoFlow

# Configure as variáveis de ambiente
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local

# Inicie os containers
docker-compose up -d

# Acesse:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs


# 2 Backend
cd backend
python -m venv venv
source venv/bin/activate  # ou `venv\Scripts\activate` no Windows
pip install -r requirements.txt

# Configure o .env (veja .env.example)
cp .env.example .env

# Execute
uvicorn main:app --reload --port 8000

# 3. Frontend
cd ../frontend
npm install
npm run dev

API Endpoints Principais
Método	Endpoint	Descrição
POST	/api/auth/register	Registrar novo usuário
POST	/api/auth/login	Login e obtenção de token
GET	/api/activities	Listar atividades do usuário
POST	/api/activities	Criar nova atividade
GET	/api/analytics/daily	Estatísticas diárias
GET	/api/analytics/weekly	Relatório semanal
📚 Documentação completa da API: http://localhost:8000/docs

Testes
bash
# Backend
cd backend
pytest -v
pytest --cov=app tests/  # Com cobertura de código

# Frontend (se tiver testes)
cd frontend
npm test
npm run test:coverage
