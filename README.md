# API Livraria – FastAPI, Docker e Deploy no Azure (Exercício 9.6)

API RESTful de livros em **FastAPI**, empacotada em uma **imagem Docker** e publicada no
**Azure App Service** por um pipeline de **CI/CD** no GitHub Actions.

## Pipeline (`.github/workflows/deploy.yml`)

A cada push na `main`:

1. **CI – testes:** instala as dependências e roda `pytest`.
2. **Imagem Docker:** constrói a imagem com o `Dockerfile` e publica no GitHub Container Registry
   (`ghcr.io/<usuario>/api-livraria-fastapi`).
3. **CD – deploy:** atualiza o App Service para rodar a nova imagem.

## Endpoints

| Método | Rota | O que faz |
|---|---|---|
| GET | `/api/livros` | Lista os livros (filtro opcional `?autor=`) |
| GET | `/api/livros/{id}` | Busca um livro |
| POST | `/api/livros` | Cria um livro |
| PUT | `/api/livros/{id}` | Atualiza um livro |
| DELETE | `/api/livros/{id}` | Remove um livro |

Documentação interativa: `/docs`.

## Rodar localmente com Docker

```bash
docker build -t api-livraria .
docker run -d -p 8000:8000 --name livraria api-livraria
```

## Coleções do Postman

- `livraria-local.postman_collection.json` – contêiner local (`http://localhost:8000`)
- `livraria-azure.postman_collection.json` – aplicação no Azure
