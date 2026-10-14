
import csv
from pathlib import Path

import pytest
import requests


def test_listar_investimentos_sem_token(base_url):
    """Verifica se a API exige autenticação."""

    response = requests.get(
        f"{base_url}/api/investments",
        timeout=15
    )

    assert response.status_code == 401


def carregar_dados_investimentos_csv():
    """Lê os cenários de investimento do arquivo CSV."""

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


def test_leitura_dados_investimentos_csv():
    """Verifica a leitura dos três cenários do CSV."""

    casos = carregar_dados_investimentos_csv()

    print("\n===== DADOS LIDOS DO CSV =====")

    for caso in casos:
        print(caso)

    assert len(casos) == 3

    assert casos[0][0] == "Poupança"
    assert casos[0][1] == 1000.0

    assert casos[1][0] == "CDB"
    assert casos[1][1] == 5000.0

    assert casos[2][0] == "CDB"
    assert casos[2][1] == -100.0

    print("\nLeitura do CSV realizada com sucesso!")


@pytest.mark.parametrize(
    "asset, amount, price, days, planned, status_esperado",
    carregar_dados_investimentos_csv()
)
def test_dados_investimentos_parametrizados(
    asset, amount, price, days, planned, status_esperado
):
    """Verifica os cenários parametrizados do CSV."""

    payload = {
        "asset_name": asset,
        "amount": amount,
        "purchase_price": price,
        "days_invested": days,
        "planned_days": planned
    }

    print("\n===== CENARIO DDT =====")
    print("Investimento:", payload)
    print("Status esperado no CSV:", status_esperado)

    assert isinstance(asset, str)
    assert isinstance(amount, float)
    assert isinstance(price, float)
    assert isinstance(days, int)
    assert isinstance(planned, int)
    assert isinstance(status_esperado, int)
