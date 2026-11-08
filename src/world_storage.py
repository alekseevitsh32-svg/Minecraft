import json
import os
import time
from src import config

SAVES_DIR = os.path.join(config.data_dir(), 'saves')


def _ensure_dir():
    os.makedirs(SAVES_DIR, exist_ok=True)


def _path(index):
    return os.path.join(SAVES_DIR, f'world{index}.json')


def next_index():
    _ensure_dir()
    i = 1
    while os.path.exists(_path(i)):
        i += 1
    return i


def list_worlds():
    _ensure_dir()
    result = []
    for fname in os.listdir(SAVES_DIR):
        if not (fname.startswith('world') and fname.endswith('.json')):
            continue
        try:
            idx = int(fname[5:-5])
        except ValueError:
            continue
        try:
            with open(os.path.join(SAVES_DIR, fname), encoding='utf-8') as f:
                data = json.load(f)
        except Exception:
            continue
        result.append({
            'index': idx,
            'name': data.get('name', f'Мир {idx}'),
            'seed': data.get('seed', 0),
            'last_played': data.get('last_played', ''),
        })
    result.sort(key=lambda w: w['index'])
    return result


def new_world(name=None, seed=None):
    _ensure_dir()
    idx = next_index()
    seed = seed if seed is not None else int(time.time() * 1000) & 0xFFFFFFFF
    now = time.strftime('%Y-%m-%dT%H:%M:%S')
    data = {
        'version': 1,
        'name': name or f'Новый мир {idx}',
        'created': now,
        'last_played': now,
        'seed': seed,
        'gamemode': 'survival',
        'player': {
            'x': 0.5, 'y': 64.0, 'z': 0.5,
            'yaw': 0.0, 'pitch': 0.0,
            'hp': 20, 'hunger': 20,
        },
        'world': {
            'time': 1000,
            'chunks': {},
        },
    }
    _write(idx, data)
    return idx, data


def load_world(index):
    p = _path(index)
    if not os.path.exists(p):
        return None
    try:
        with open(p, encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        return None
    data['last_played'] = time.strftime('%Y-%m-%dT%H:%M:%S')
    _write(index, data)
    return data


def save_world(index, data):
    data['last_played'] = time.strftime('%Y-%m-%dT%H:%M:%S')
    _write(index, data)


def delete_world(index):
    p = _path(index)
    if os.path.exists(p):
        os.remove(p)


def _write(index, data):
    _ensure_dir()
    with open(_path(index), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
