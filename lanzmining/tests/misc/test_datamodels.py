import pytest

from src.misc import Talkshow
from src.misc.datamodels import VaultConfig


def test_vault_config():
    vault_config = VaultConfig(
        markuslanz="./tests/misc/",
        maybritillner="./tests/misc/",
        maischberger="./tests/misc/",
        hartaberfair="./tests/misc/",
        carenmiosga="./tests/misc/",
    )
    assert all(
        [
            k in Talkshow.values() and v.is_dir()
            for k, v in vault_config.model_dump(mode="python").items()
        ]
    )


def test_vault_config_error():
    with pytest.raises(ValueError):
        _ = VaultConfig(
            markuslanz="./tests/misc/",
            maybritillner="./tests/misc/",
            maischberger="./tests/misc/",
            hartaberfair="./tests/misc/",
            carenmiosga="./tests/misc/test_datamodels.py",
        )
