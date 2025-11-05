import logging
import sys
from pathlib import Path

# 创建logs目录
log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(exist_ok=True)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(log_dir / "test.log", encoding='utf-8')
    ]
)

logger = logging.getLogger(__name__)

def get_logger():
    return logger