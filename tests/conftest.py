import pytest
import pexpect


@pytest.fixture
def ambiente_virtuale():

    processo = pexpect.spawn(
        "umvu",
        ["bash", "--noprofile", "--norc"],
        encoding="utf-8",
        echo=False,
        timeout=10
    )

    try:
        processo.expect(r"[$#] ")
        yield processo

    finally:
        processo.close(force=True)