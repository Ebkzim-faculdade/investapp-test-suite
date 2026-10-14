
import pytest
import requests


def test_simulacao_sem_autenticacao(base_url):
    """Verifica se a API exige autenticação."""

    payload = {
        "months": 12
    }

    response = requests.post(
        f"{base_url}/api/simulate/yield-monthly",
        json=payload,
        timeout=15
    )

    print("\n===== SIMULACAO SEM AUTENTICACAO =====")
    print("Status recebido:", response.status_code)
    print("Resposta da API:", response.text)

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_simulacao_payload_invalido(base_url):
    """Verifica a validação de um payload inválido."""

    payload = {
        "months": "valor_invalido"
    }

    response = requests.post(
        f"{base_url}/api/simulate/yield-monthly",
        json=payload,
        timeout=15
    )

    print("\n===== SIMULACAO COM PAYLOAD INVALIDO =====")
    print("Status recebido:", response.status_code)
    print("Resposta da API:", response.text)

    if response.status_code == 401:
        pytest.skip(
            "Teste HTTP 422 depende de autenticação válida."
        )

    assert response.status_code == 422
