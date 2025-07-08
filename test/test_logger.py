import logging
from app.core.logging_config import setup_logger  # Adjust path to match your structure

def test_logger_output_to_stdout(capsys):
    # Clear existing handlers to avoid duplicates across test runs
    logger = logging.getLogger()
    logger.handlers.clear()

    logger = setup_logger()
    logger.info("Visible message")

    captured = capsys.readouterr()
    assert "Visible message" in captured.out

