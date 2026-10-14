
import requests


def test_login_credenciais_invalidas(base_url):
    """Verifica se a API rejeita credenciais incorretas."""

    payload = {
        "username": "usuario_teste_inexistente_xyz",
        "password": "senha_invalida_xyz"
    }

    response = requests.post(
        f"{base_url}/api/login",
        json=payload,
        timeout=15
    )

    print("\n===== TESTE DE CREDENCIAIS INVALIDAS =====")
    print("Status recebido:", response.status_code)
    print("Resposta da API:", response.text)

    assert response.status_code == 400
    assert response.json()["detail"] == "Usuário ou senha incorretos"


def test_login_payload_invalido(base_url):
    """Verifica se a API trata dados com formato inválido."""

    payload = {
        "username": 12345,
        "password": ["senha_invalida"]
    }

    response = requests.post(
        f"{base_url}/api/login",
        json=payload,
        timeout=15
    )

    print("\n===== TESTE DE PAYLOAD INVALIDO =====")
    print("Status esperado: 422")
    print("Status recebido:", response.status_code)
    print("Resposta da API:", response.text)

    assert response.status_code == 422
