from loguru import logger
import sys
from pathlib import Path

log_path = Path(__file__).parent.parent / "logs"
log_path.mkdir(exist_ok=True)

logger.remove()
logger.add(sys.stdout, level="INFO", format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>")
logger.add(log_path / "test_{time:YYYY-MM-DD}.log", rotation="00:00", retention="30 days", level="DEBUG")

def get_logger():
    return logger
