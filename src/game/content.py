AIR = 0
GRASS = 1
DIRT = 2
STONE = 3
LOG = 4
LEAVES = 5
WATER = 6
SAND = 7
CRAFTING_TABLE = 8
PLANKS = 9

BLOCK_NAMES = {
    AIR: 'Воздух', GRASS: 'Трава', DIRT: 'Земля', STONE: 'Камень',
    LOG: 'Бревно', LEAVES: 'Листва', WATER: 'Вода', SAND: 'Песок',
    CRAFTING_TABLE: 'Верстак', PLANKS: 'Доски',
}

SOLID = {GRASS, DIRT, STONE, LOG, LEAVES, SAND, CRAFTING_TABLE, PLANKS}

ITEM_STICK = 100
ITEM_WOOD_PICKAXE = 101
ITEM_WOOD_AXE = 102
ITEM_WOOD_SHOVEL = 103
ITEM_WOOD_SWORD = 104

ITEM_NAMES = {
    ITEM_STICK: 'Палка',
    ITEM_WOOD_PICKAXE: 'Деревянная кирка',
    ITEM_WOOD_AXE: 'Деревянный топор',
    ITEM_WOOD_SHOVEL: 'Деревянная лопата',
    ITEM_WOOD_SWORD: 'Деревянный меч',
}

def max_stack(item):
    if item in (ITEM_WOOD_PICKAXE, ITEM_WOOD_AXE, ITEM_WOOD_SHOVEL, ITEM_WOOD_SWORD):
        return 1
    return 64

BREAK_TIMES = {
    GRASS: 1.0, DIRT: 1.0, STONE: 4.0, LOG: 2.5, LEAVES: 0.25,
    SAND: 0.5, CRAFTING_TABLE: 2.0, PLANKS: 1.5,
}

def break_time_for(block, tool):
    base = BREAK_TIMES.get(block, 1.0)
    if block == STONE and tool == ITEM_WOOD_PICKAXE:
        return base / 4.0
    if block in (LOG, CRAFTING_TABLE, PLANKS) and tool == ITEM_WOOD_AXE:
        return base / 4.0
    if block in (GRASS, DIRT, SAND) and tool == ITEM_WOOD_SHOVEL:
        return base / 4.0
    if block == LEAVES and tool == ITEM_WOOD_SWORD:
        return base / 4.0
    return base

DROPS = {
    GRASS: DIRT, DIRT: DIRT, STONE: STONE, LOG: LOG, LEAVES: None,
    SAND: SAND, CRAFTING_TABLE: CRAFTING_TABLE, PLANKS: PLANKS,
}

BLOCK_COLORS = {
    GRASS: (95, 159, 53), DIRT: (134, 96, 67), STONE: (128, 128, 128),
    LOG: (110, 80, 50), LEAVES: (60, 130, 50), WATER: (50, 100, 200),
    SAND: (220, 200, 130), CRAFTING_TABLE: (160, 120, 80), PLANKS: (180, 140, 90),
}

RECIPES = [
    ([[LOG]], PLANKS, 4),
    ([[PLANKS], [PLANKS]], ITEM_STICK, 4),
    ([[PLANKS, PLANKS], [PLANKS, PLANKS]], CRAFTING_TABLE, 1),
    ([[PLANKS, PLANKS, PLANKS],
      [None, ITEM_STICK, None],
      [None, ITEM_STICK, None]], ITEM_WOOD_PICKAXE, 1),
    ([[PLANKS, PLANKS, None],
      [PLANKS, ITEM_STICK, None],
      [None, ITEM_STICK, None]], ITEM_WOOD_AXE, 1),
    ([[None, PLANKS, None],
      [None, ITEM_STICK, None],
      [None, ITEM_STICK, None]], ITEM_WOOD_SHOVEL, 1),
    ([[None, PLANKS, None],
      [None, PLANKS, None],
      [None, ITEM_STICK, None]], ITEM_WOOD_SWORD, 1),
]

def normalize_pattern(grid):
    rows, cols = len(grid), len(grid[0])
    min_r, max_r = rows, -1
    min_c, max_c = cols, -1
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] is not None:
                min_r, max_r = min(min_r, r), max(max_r, r)
                min_c, max_c = min(min_c, c), max(max_c, c)
    if max_r < 0:
        return []
    return [[grid[r][c] for c in range(min_c, max_c + 1)] for r in range(min_r, max_r + 1)]

def match_recipe(grid):
    norm = normalize_pattern(grid)
    if not norm:
        return None
    for recipe, result, count in RECIPES:
        if norm == normalize_pattern(recipe):
            return (result, count)
    return None
