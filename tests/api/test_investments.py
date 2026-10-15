
import csv
import os
from pathlib import Path

import pytest
import requests


def carregar_dados_investimentos_csv():
    """Carrega os cenários de investimento do CSV."""

    caminho_csv = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "dados_investimentos.csv"
    )

    if not caminho_csv.exists():
        raise FileNotFoundError(
            f"Arquivo CSV não encontrado: {caminho_csv}"
        )

    casos = []

    with open(
        caminho_csv,
        mode="r",
        encoding="utf-8-sig",
        newline=""
    ) as arquivo:
        leitor = csv.DictReader(arquivo)

        for linha in leitor:
            casos.append(
                (
                    linha["asset_name"],
                    float(linha["amount"]),
                    float(linha["purchase_price"]),
                    int(linha["days_invested"]),
                    int(linha["planned_days"]),
                    int(linha["status_esperado"]),
                )
            )

    return casos


@pytest.fixture(scope="module")
def auth_headers_investimentos(base_url):
    """Autentica o usuário para os testes de investimentos."""

    usuario = os.getenv("TEST_USER")
    senha = os.getenv("TEST_PASSWORD")

    if not usuario or not senha or usuario == "userXX":
        pytest.skip("Credenciais válidas não configuradas.")

    response = requests.post(
        f"{base_url}/api/login",
        json={
            "username": usuario,
            "password": senha
        },
        timeout=15
    )

    if response.status_code in (400, 401):
        pytest.skip("Credenciais não aceitas pela API.")

    assert response.status_code == 200

    token = response.json().get("access_token")
    assert token, "Token JWT não retornado."

    return {"Authorization": f"Bearer {token}"}


def test_listar_investimentos_sem_token(base_url):
    """Verifica se a API exige autenticação."""

    response = requests.get(
        f"{base_url}/api/investments",
        timeout=15
    )

    assert response.status_code == 401


def test_leitura_dados_investimentos_csv():
    """Verifica a leitura dos cenários do CSV."""

    casos = carregar_dados_investimentos_csv()

    assert len(casos) == 3
    assert casos[0][0] == "Poupança"
    assert casos[1][0] == "CDB"
    assert casos[2][1] == -100.0


@pytest.mark.parametrize(
    "asset, amount, price, days, planned, status_esperado",
    carregar_dados_investimentos_csv()
)
def test_dados_investimentos_parametrizados(
    asset, amount, price, days, planned, status_esperado
):
    """Valida a parametrização dos dados do CSV."""

    payload = {
        "asset_name": asset,
        "amount": amount,
        "purchase_price": price,
        "days_invested": days,
        "planned_days": planned
    }

    print("\nCenário DDT:", payload)
    print("Status esperado:", status_esperado)

    assert isinstance(asset, str)
    assert isinstance(amount, float)
    assert isinstance(price, float)
    assert isinstance(days, int)
    assert isinstance(planned, int)
    assert isinstance(status_esperado, int)


@pytest.mark.parametrize(
    "asset, amount, price, days, planned, status_esperado",
    carregar_dados_investimentos_csv()
)
def test_criar_investimentos_ddt_csv(
    base_url,
    auth_headers_investimentos,
    asset,
    amount,
    price,
    days,
    planned,
    status_esperado
):
    """Testa a criação de investimentos com massa CSV."""

    payload = {
        "asset_name": asset,
        "amount": amount,
        "purchase_price": price,
        "days_invested": days,
        "planned_days": planned
    }

    response = requests.post(
        f"{base_url}/api/investments",
        json=payload,
        headers=auth_headers_investimentos,
        timeout=15
    )

    assert response.status_code == status_esperado


def test_listar_investimentos_autenticado(
    base_url, auth_headers_investimentos
):
    """Verifica a listagem de investimentos autenticada."""

    response = requests.get(
        f"{base_url}/api/investments",
        headers=auth_headers_investimentos,
        timeout=15
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_excluir_investimento_sem_token(base_url):
    """Verifica se a exclusão exige autenticação."""

    response = requests.delete(
        f"{base_url}/api/investments/999999999",
        timeout=15
    )

    assert response.status_code == 401


def test_excluir_investimento_autenticado(
    base_url, auth_headers_investimentos
):
    """Testa a exclusão de um investimento de teste."""

    pytest.skip(
        "Exclusão pendente: é necessário criar e "
        "identificar um investimento exclusivo do teste."
    )
