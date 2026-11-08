from src.game import content


class Inventory:
    def __init__(self):
        self.slots = [None] * 36  # [item, count] or None
        self.selected = 0

    def add(self, item, count=1):
        ms = content.max_stack(item)
        if ms > 1:
            for i in range(36):
                if self.slots[i] and self.slots[i][0] == item:
                    space = ms - self.slots[i][1]
                    if space > 0:
                        take = min(count, space)
                        self.slots[i][1] += take
                        count -= take
                        if count <= 0:
                            return True
        for i in range(36):
            if self.slots[i] is None:
                self.slots[i] = [item, count]
                return True
        return False

    def remove(self, item, count=1):
        for i in range(36):
            if self.slots[i] and self.slots[i][0] == item:
                take = min(count, self.slots[i][1])
                self.slots[i][1] -= take
                count -= take
                if self.slots[i][1] <= 0:
                    self.slots[i] = None
                if count <= 0:
                    return True
        return False

    def selected_item(self):
        s = self.slots[self.selected]
        return s[0] if s else None


class CraftingGrid:
    def __init__(self, size):
        self.size = size
        self.grid = [[None] * size for _ in range(size)]

    def result(self):
        return content.match_recipe(self.grid)

    def consume(self):
        for row in self.grid:
            for i in range(len(row)):
                if row[i] is not None:
                    row[i] = None
