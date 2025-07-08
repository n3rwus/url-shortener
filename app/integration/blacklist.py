import aiohttp
from pathlib import Path
from app.core.logging_config import setup_logger

logger = setup_logger()

CERT_URL = "https://hole.cert.pl/domains/v2/domains.txt"
LOCAL_BACKUP = Path("data/blacklist.txt")

class BlacklistUnavailableError(Exception):
    """Raised when the blacklist cannot be fetched or loaded."""

async def fetch_blacklist() -> set[str]:
    try:
        timeout = aiohttp.ClientTimeout(total=5)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(CERT_URL) as response:
                if response.status == 200:
                    text = await response.text()
                    domains = {
                        line.strip().lower()
                        for line in text.splitlines()
                        if line and not line.startswith("#")
                    }
                    LOCAL_BACKUP.write_text(text)
                    logger.info(f"Fetched {len(domains)} domains from CERT URL")
                    return domains
                else:
                    logger.warning(f"Remote fetch failed with status {response.status}")
    except Exception as e:
        logger.error(f"Unable to fetch live blacklist: {e}")

    if LOCAL_BACKUP.exists():
        logger.info("Loading blacklist from local backup")
        text = LOCAL_BACKUP.read_text()
        return {
            line.strip().lower()
            for line in text.splitlines()
            if line and not line.startswith("#")
        }

    logger.error("No backup available; cannot validate domains")
    raise BlacklistUnavailableError("Unable to fetch or load blacklist")

