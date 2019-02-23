from asynctest import CoroutineMock
from soda_client.soda_client.main import Soda


async def test_does_not_report_if_threshold():

    soda_cli = Soda(host="/test", threshold=3, session_factory=CoroutineMock)

    dummy_data = {
        "start": 4,
        "end": 5
    }
    await soda_cli.report(dummy_data)
    assert not soda_cli.client_session.post.called
