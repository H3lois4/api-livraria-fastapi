"""API RESTful da Livraria com FastAPI.

Documentação interativa gerada automaticamente em /docs.
"""
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field

app = FastAPI(title="API Livraria", version="1.0.0",
              description="CRUD de livros da livraria, rodando em um contêiner Docker.")


class LivroEntrada(BaseModel):
    titulo: str = Field(min_length=1, examples=["Vidas Secas"])
    autor: str = Field(min_length=1, examples=["Graciliano Ramos"])
    preco: float = Field(ge=0, examples=[45.0])
    estoque: int = Field(ge=0, examples=[4])


class LivroAtualizacao(BaseModel):
    titulo: str | None = Field(default=None, min_length=1)
    autor: str | None = Field(default=None, min_length=1)
    preco: float | None = Field(default=None, ge=0)
    estoque: int | None = Field(default=None, ge=0)


class Livro(LivroEntrada):
    id: int


livros: dict[int, Livro] = {
    1: Livro(id=1, titulo="Dom Casmurro", autor="Machado de Assis", preco=29.90, estoque=3),
    2: Livro(id=2, titulo="A Hora da Estrela", autor="Clarice Lispector", preco=39.90, estoque=5),
    3: Livro(id=3, titulo="Grande Sertão: Veredas", autor="João Guimarães Rosa", preco=89.00, estoque=2),
}
proximo_id = 4


def obter_ou_404(livro_id: int) -> Livro:
    if livro_id not in livros:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return livros[livro_id]


@app.get("/")
def inicio():
    return {"api": "Livraria", "documentacao": "/docs", "recurso": "/api/livros"}


@app.get("/api/livros", response_model=list[Livro])
def listar(autor: str = ""):
    return [l for l in livros.values() if autor.lower() in l.autor.lower()]


@app.get("/api/livros/{livro_id}", response_model=Livro)
def buscar(livro_id: int):
    return obter_ou_404(livro_id)


@app.post("/api/livros", response_model=Livro, status_code=status.HTTP_201_CREATED)
def criar(dados: LivroEntrada):
    global proximo_id
    livro = Livro(id=proximo_id, **dados.model_dump())
    livros[proximo_id] = livro
    proximo_id += 1
    return livro


@app.put("/api/livros/{livro_id}", response_model=Livro)
def atualizar(livro_id: int, dados: LivroAtualizacao):
    livro = obter_ou_404(livro_id)
    atualizado = livro.model_copy(update=dados.model_dump(exclude_unset=True))
    livros[livro_id] = atualizado
    return atualizado


@app.delete("/api/livros/{livro_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover(livro_id: int):
    obter_ou_404(livro_id)
    del livros[livro_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)
