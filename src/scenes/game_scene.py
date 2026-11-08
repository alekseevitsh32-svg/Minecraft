import math
import pygame
from src.scenes.base_scene import BaseScene
from src.game.world import World
from src.game.player import Player
from src.game import content, renderer, hud
from src.game.raycaster import pick_block
from src.game.inventory import Inventory, CraftingGrid
from src.ui.text import draw_text
from src import world_storage


RW, RH = 320, 180


class _Cam:
    pass


class GameScene(BaseScene):
    def __init__(self, app, world_index, world_data):
        super().__init__(app)
        self.world_index = world_index
        self.world_data = world_data
        self.world = World(world_data)
        self.player = Player(world_data.get('player', {}))
        self.inv = Inventory()
        self.inv.add(content.ITEM_WOOD_PICKAXE, 1)
        self.inv.add(content.ITEM_WOOD_AXE, 1)
        self.inv.add(content.ITEM_WOOD_SHOVEL, 1)
        self.inv.add(content.CRAFTING_TABLE, 1)

        self.breaking = None
        self.break_progress = 0.0
        self.place_cd = 0.0
        self.ui_open = False
        self.craft_grid = CraftingGrid(2)
        self.render_surf = pygame.Surface((RW, RH))

        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        pygame.mouse.get_rel()

    def _camera(self):
        c = _Cam()
        c.x = self.player.pos[0]
        c.z = self.player.pos[2]
        c.eye_y = self.player.eye_y
        c.yaw = self.player.yaw
        c.pitch = self.player.pitch
        return c

    def handle_event(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                if self.ui_open:
                    self.ui_open = False
                    pygame.mouse.set_visible(False)
                    pygame.event.set_grab(True)
                    pygame.mouse.get_rel()
                else:
                    self._save()
                    from src.scenes.world_select import WorldSelect
                    self.app.scene_manager.switch(WorldSelect(self.app))
                    return
            elif e.key == pygame.K_e:
                self.ui_open = not self.ui_open
                pygame.mouse.set_visible(self.ui_open)
                pygame.event.set_grab(not self.ui_open)
                if not self.ui_open:
                    pygame.mouse.get_rel()
            elif pygame.K_1 <= e.key <= pygame.K_9:
                self.inv.selected = e.key - pygame.K_1

        if not self.ui_open:
            if e.type == pygame.MOUSEMOTION:
                dx, dy = e.rel
                self.player.yaw -= dx * 0.003
                self.player.pitch -= dy * 0.003
                self.player.pitch = max(-1.55, min(1.55, self.player.pitch))
            elif e.type == pygame.MOUSEWHEEL:
                self.inv.selected = (self.inv.selected - e.y) % 9

    def update(self, dt):
        if self.ui_open:
            return
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys, dt)
        self.player.update_physics(dt, self.world)
        self.player.pos[0] = max(1.0, min(self.world.size_x - 1.0, self.player.pos[0]))
        self.player.pos[2] = max(1.0, min(self.world.size_z - 1.0, self.player.pos[2]))

        if self.place_cd > 0:
            self.place_cd -= dt

        cam = self._camera()
        hit = pick_block((self.player.pos[0], self.player.eye_y, self.player.pos[2]),
                         self.player.forward(), self.world, 5.0)
        left, _, right = pygame.mouse.get_pressed()

        if left and hit:
            bp = hit['block_pos']
            if self.breaking != bp:
                self.breaking = bp
                self.break_progress = 0.0
            block = self.world.get_block(*bp)
            tool = self.inv.selected_item()
            bt = content.break_time_for(block, tool)
            self.break_progress += dt / bt
            if self.break_progress >= 1.0:
                drop = content.DROPS.get(block)
                if drop is not None:
                    self.inv.add(drop, 1)
                self.world.set_block(*bp, content.AIR)
                self.breaking = None
                self.break_progress = 0.0
        else:
            self.breaking = None
            self.break_progress = 0.0

        if right and self.place_cd <= 0:
            if hit and hit['block'] == content.CRAFTING_TABLE:
                self.ui_open = True
                pygame.mouse.set_visible(True)
                pygame.event.set_grab(False)
                return
            item = self.inv.selected_item()
            if item and item in content.SOLID and hit:
                adj = hit['adjacent']
                if not self._player_blocks(adj):
                    self.world.set_block(*adj, item)
                    self.inv.remove(item, 1)
                    self.place_cd = 0.2

    def _player_blocks(self, bp):
        bx, by, bz = bp
        p = self.player.pos
        hw = self.player.width / 2
        return (p[0] + hw > bx and p[0] - hw < bx + 1
                and p[1] + self.player.height > by and p[1] < by + 1
                and p[2] + hw > bz and p[2] - hw < bz + 1)

    def _save(self):
        self.world_data['player'] = self.player.to_dict()
        self.world_data.setdefault('world', {})['blocks'] = self.world.serialize()
        world_storage.save_world(self.world_index, self.world_data)

    def draw(self, screen):
        cam = self._camera()
        renderer.render_world(self.render_surf, cam, self.world)

        if not self.ui_open:
            hit = pick_block((self.player.pos[0], self.player.eye_y, self.player.pos[2]),
                             self.player.forward(), self.world, 5.0)
            if hit:
                renderer.render_selection(self.render_surf, cam, hit['block_pos'])

        pygame.transform.scale(self.render_surf, screen.get_size(), screen)
        W, H = screen.get_size()

        if not self.ui_open:
            hud.draw_crosshair(screen, W, H)
            hud.draw_hotbar(screen, self.inv, W, H)
            hud.draw_hand(screen, self.player, self.inv, self.break_progress)
            if self.breaking:
                draw_text(screen, f"{int(self.break_progress * 100)}%",
                          W // 2, H // 2 + 40, size=8, scale=2, center=True)
        else:
            self._draw_inventory_ui(screen)

        hud.draw_fps(screen, int(self.app.clock.get_fps()))

    def _draw_inventory_ui(self, screen):
        W, H = screen.get_size()
        ov = pygame.Surface((W, H), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 160))
        screen.blit(ov, (0, 0))
        pw, ph = 560, 420
        px = (W - pw) // 2
        py = (H - ph) // 2
        pygame.draw.rect(screen, (120, 120, 120), (px, py, pw, ph))
        pygame.draw.rect(screen, (30, 30, 30), (px, py, pw, ph), 3)
        draw_text(screen, "Инвентарь", W // 2, py + 25, size=12, scale=2, center=True)

        # 2x2 crafting grid
        cs = 44
        cx0 = px + 40
        cy0 = py + 80
        draw_text(screen, "Крафт", cx0, cy0 - 22, size=8, scale=2)
        for gy in range(2):
            for gx in range(2):
                sx = cx0 + gx * cs
                sy = cy0 + gy * cs
                pygame.draw.rect(screen, (80, 80, 80), (sx, sy, cs, cs))
                pygame.draw.rect(screen, (40, 40, 40), (sx, sy, cs, cs), 1)
        # Arrow
        pygame.draw.polygon(screen, (255, 255, 255),
                            [(cx0 + cs*2 + 15, cy0 + cs),
                             (cx0 + cs*2 + 45, cy0 + cs - 15),
                             (cx0 + cs*2 + 45, cy0 + cs + 15)])
        # Output
        ox = cx0 + cs*2 + 60
        pygame.draw.rect(screen, (80, 80, 80), (ox, cy0, cs, cs))
        pygame.draw.rect(screen, (40, 40, 40), (ox, cy0, cs, cs), 1)

        # Player inventory grid 3x9
        inv_x0 = px + 180
        inv_y0 = py + 80
        for row in range(3):
            for col in range(9):
                idx = 9 + row*9 + col
                sx = inv_x0 + col * cs
                sy = inv_y0 + row * cs
                pygame.draw.rect(screen, (80, 80, 80), (sx, sy, cs, cs))
                pygame.draw.rect(screen, (40, 40, 40), (sx, sy, cs, cs), 1)
                slot = self.inv.slots[idx]
                if slot:
                    icon = hud.get_icon(slot[0], cs - 12)
                    if icon:
                        screen.blit(icon, (sx + 6, sy + 6))
                    if slot[1] > 1:
                        draw_text(screen, str(slot[1]), sx + cs - 4, sy + cs - 16,
                                  size=8, scale=1, right=True)

        # Hotbar row
        hb_y = inv_y0 + 3 * cs + 15
        for col in range(9):
            sx = inv_x0 + col * cs
            pygame.draw.rect(screen, (80, 80, 80), (sx, hb_y, cs, cs))
            pygame.draw.rect(screen, (40, 40, 40), (sx, hb_y, cs, cs), 1)
            slot = self.inv.slots[col]
            if slot:
                icon = hud.get_icon(slot[0], cs - 12)
                if icon:
                    screen.blit(icon, (sx + 6, hb_y + 6))
                if slot[1] > 1:
                    draw_text(screen, str(slot[1]), sx + cs - 4, hb_y + cs - 16,
                              size=8, scale=1, right=True)

        draw_text(screen, "E — закрыть  |  ESC — сохранить и выйти",
                  W // 2, py + ph - 25, size=8, scale=2, center=True,
                  color=(220, 220, 220))
