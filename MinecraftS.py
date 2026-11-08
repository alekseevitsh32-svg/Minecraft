import os
import sys

_BASE = os.path.dirname(os.path.abspath(__file__))
if _BASE not in sys.path:
    sys.path.insert(0, _BASE)

from src import config

if not os.path.exists(config.asset('dirt.png')):
    print('[MyCraft] Ассеты не найдены, генерирую...')
    from tools import generate_assets
    generate_assets.main()

from src.app import App


if __name__ == '__main__':
    App().run()
