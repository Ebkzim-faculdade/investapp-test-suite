
import os
import pytest


@pytest.fixture(scope="session")
def base_url():
    """Retorna o endereço da API do InvestApp."""
    return os.getenv(
        "API_BASE_URL",
        "https://5bm1nctd1f.execute-api.us-east-1.amazonaws.com"
    )
