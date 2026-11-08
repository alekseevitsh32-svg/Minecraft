import json
import os
from src import config

DEFAULTS = {
    'volume': 80,
    'fov': 70,
    'graphics': 1,
    'fullscreen': False,
}


def _path():
    return os.path.join(config.data_dir(), 'settings.json')


def load_settings():
    p = _path()
    if os.path.exists(p):
        try:
            with open(p, encoding='utf-8') as f:
                data = json.load(f)
            for k, v in DEFAULTS.items():
                data.setdefault(k, v)
            return data
        except Exception:
            pass
    return dict(DEFAULTS)


def save_settings(s):
    with open(_path(), 'w', encoding='utf-8') as f:
        json.dump(s, f, indent=2, ensure_ascii=False)
