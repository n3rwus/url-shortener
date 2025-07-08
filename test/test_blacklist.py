import pytest
import aiohttp
from unittest.mock import patch, AsyncMock, MagicMock
from app.integration.blacklist import fetch_blacklist, BlacklistUnavailableError

# Sample domain text
MOCK_CERT_RESPONSE = "bad.com\nphishing.net\n# comment\n\n"

def test_domains_parsed_correctly():
    """Quick sanity check on what parse logic should return."""
    domains = {
        line.strip().lower()
        for line in MOCK_CERT_RESPONSE.splitlines()
        if line and not line.startswith("#")
    }
    assert "bad.com" in domains
    assert "phishing.net" in domains
    assert "# comment" not in domains

@pytest.fixture
def fake_local_backup(tmp_path):
    backup_file = tmp_path / "blacklist.txt"
    backup_file.write_text("local.com\nbackup.net\n")
    with patch("app.integration.blacklist.LOCAL_BACKUP", backup_file):
        yield backup_file

@pytest.mark.asyncio
async def test_fetch_from_cert(monkeypatch, tmp_path):
    # Mock the response
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.text = AsyncMock(return_value="bad.com\nphishing.net\n")
    mock_response.__aenter__ = AsyncMock(return_value=mock_response)
    mock_response.__aexit__ = AsyncMock(return_value=None)

    # Mock the session
    mock_session = MagicMock()
    mock_session.get.return_value = mock_response
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=None)

    # Mock ClientSession
    mock_client_session = MagicMock(return_value=mock_session)

    # Apply the patch
    monkeypatch.setattr("aiohttp.ClientSession", mock_client_session)

    # Patch LOCAL_BACKUP
    backup_path = tmp_path / "blacklist.txt"
    monkeypatch.setattr("app.integration.blacklist.LOCAL_BACKUP", backup_path)

    domains = await fetch_blacklist()
    assert "bad.com" in domains
    assert "phishing.net" in domains
    assert backup_path.exists()

@pytest.mark.asyncio
async def test_fallback_to_backup(monkeypatch, fake_local_backup):
    # Mock session that raises an exception
    mock_session = MagicMock()
    mock_session.get.side_effect = aiohttp.ClientError("Network error")
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=None)

    # Mock ClientSession
    mock_client_session = MagicMock(return_value=mock_session)

    # Apply the patch
    monkeypatch.setattr("aiohttp.ClientSession", mock_client_session)

    domains = await fetch_blacklist()
    assert "local.com" in domains
    assert "backup.net" in domains

@pytest.mark.asyncio
async def test_failure_no_fetch_no_backup(monkeypatch, tmp_path):
    # Mock session that raises an exception
    mock_session = MagicMock()
    mock_session.get.side_effect = aiohttp.ClientError("Network error")
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=None)

    # Mock ClientSession
    mock_client_session = MagicMock(return_value=mock_session)

    # Apply the patch
    monkeypatch.setattr("aiohttp.ClientSession", mock_client_session)

    # Patch LOCAL_BACKUP to nonexistent file
    monkeypatch.setattr("app.integration.blacklist.LOCAL_BACKUP", tmp_path / "missing.txt")

    with pytest.raises(BlacklistUnavailableError):
        await fetch_blacklist()