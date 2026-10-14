
import requests


def test_listar_ativos_publicos(base_url):
    """Valida a consulta pública de ativos."""

    response = requests.get(
        f"{base_url}/api/assets",
        timeout=15
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0


def test_estrutura_dos_ativos(base_url):
    """Valida os campos dos ativos retornados pela API."""

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
