from fastapi.testclient import TestClient

from main import app

cliente = TestClient(app)


def test_listar_e_filtrar():
    assert len(cliente.get("/api/livros").json()) >= 3
    assert [l["titulo"] for l in cliente.get("/api/livros?autor=clarice").json()] == ["A Hora da Estrela"]


def test_crud():
    novo = {"titulo": "Vidas Secas", "autor": "Graciliano Ramos", "preco": 45.0, "estoque": 4}
    criado = cliente.post("/api/livros", json=novo)
    assert criado.status_code == 201
    livro_id = criado.json()["id"]
    assert cliente.put(f"/api/livros/{livro_id}", json={"preco": 39.9}).json()["preco"] == 39.9
    assert cliente.delete(f"/api/livros/{livro_id}").status_code == 204
    assert cliente.get(f"/api/livros/{livro_id}").status_code == 404


def test_validacao():
    assert cliente.post("/api/livros", json={"titulo": "Sem autor"}).status_code == 422
    assert cliente.put("/api/livros/1", json={"preco": -5}).status_code == 422
