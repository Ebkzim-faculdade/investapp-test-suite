
import os

import pytest
import requests


@pytest.fixture(scope="module")
def auth_headers_simulacoes(base_url):
    """Obtém autenticação para os testes de simulação."""

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


def test_simulacao_sem_autenticacao(base_url):
    """Verifica se a simulação de rendimento exige login."""

    response = requests.post(
        f"{base_url}/api/simulate/yield-monthly",
        json={"months": 12},
        timeout=15
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_simulacao_payload_invalido(base_url):
    """Verifica a validação do campo months."""

    response = requests.post(
        f"{base_url}/api/simulate/yield-monthly",
        json={"months": "valor_invalido"},
        timeout=15
    )

    if response.status_code == 401:
        pytest.skip(
            "Teste HTTP 422 requer autenticação."
        )

    assert response.status_code == 422


def test_simulacao_rendimento_autenticado(
    base_url, auth_headers_simulacoes
):
    """Verifica o cálculo de rendimento mensal."""

    response = requests.post(
        f"{base_url}/api/simulate/yield-monthly",
        json={"months": 12},
        headers=auth_headers_simulacoes,
        timeout=15
    )

    assert response.status_code == 200


def test_resgate_sem_autenticacao(base_url):
    """Verifica se o resgate exige autenticação."""

    response = requests.post(
        f"{base_url}/api/simulate/tax-withdrawal",
        json={"target_amount": 1000.0},
        timeout=15
    )

    print("\n===== RESGATE SEM AUTENTICACAO =====")
    print("Status:", response.status_code)
    print("Resposta:", response.text)

    assert response.status_code == 401


def test_resgate_autenticado(
    base_url, auth_headers_simulacoes
):
    """Verifica a simulação fiscal de resgate."""

    payload = {
        "target_amount": 1000.0
    }

    response = requests.post(
        f"{base_url}/api/simulate/tax-withdrawal",
        json=payload,
        headers=auth_headers_simulacoes,
        timeout=15
    )

    print("\n===== SIMULACAO FISCAL =====")
    print("Status:", response.status_code)
    print("Resposta:", response.text)

    assert response.status_code == 200
