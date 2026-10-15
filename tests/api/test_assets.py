
import os

import pytest
import requests


@pytest.fixture(scope="module")
def auth_headers_assets(base_url):
    """Obtém autenticação para atualizar taxas."""

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


def test_listar_ativos_publicos(base_url):
    """Verifica a consulta pública de ativos."""

    response = requests.get(
        f"{base_url}/api/assets",
        timeout=15
    )

    assert response.status_code == 200

    ativos = response.json()

    assert isinstance(ativos, list)
    assert len(ativos) > 0


def test_estrutura_dos_ativos(base_url):
    """Verifica os campos retornados pela API."""

    response = requests.get(
        f"{base_url}/api/assets",
        timeout=15
    )

    assert response.status_code == 200

    ativos = response.json()

    assert isinstance(ativos, list)
    assert len(ativos) > 0

    for ativo in ativos:
        assert isinstance(ativo, dict)
        assert "asset_name" in ativo
        assert "asset_type" in ativo
        assert "annual_rate" in ativo


def test_atualizar_taxa_sem_token(base_url):
    """Verifica se a atualização exige autenticação."""

    payload = {
        "asset_name": "CDB",
        "annual_rate": 10.5
    }

    response = requests.put(
        f"{base_url}/api/assets",
        json=payload,
        timeout=15
    )

    print("\n===== ATUALIZACAO SEM TOKEN =====")
    print("Status recebido:", response.status_code)

    assert response.status_code == 401


def test_atualizar_taxa_autenticado(
    base_url, auth_headers_assets
):
    """Prepara a atualização autenticada de uma taxa."""

    pytest.skip(
        "Atualização pendente: exige ambiente autorizado "
        "e estratégia para restaurar a taxa original."
    )
