import tradingagents.default_config as default_config
from typing import Dict, Optional

# 使用預設設定，但允許被覆寫
_config: Optional[Dict] = None


def initialize_config():
    """以預設值初始化設定。"""
    global _config
    if _config is None:
        _config = default_config.DEFAULT_CONFIG.copy()


def set_config(config: Dict):
    """以自訂值更新設定。"""
    global _config
    if _config is None:
        _config = default_config.DEFAULT_CONFIG.copy()
    _config.update(config)


def get_config() -> Dict:
    """取得目前的設定。"""
    if _config is None:
        initialize_config()
    return _config.copy()


# 以預設設定進行初始化
initialize_config()
