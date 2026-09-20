"""Boucle, rendu et progression du premier niveau de Polarix."""

from __future__ import annotations

import math
import os
import random
import pygame

from .entities import MagnetBeam, Player
from .level import make_level
from .settings import (
    BACKGROUND, CYAN, DANGER, FPS, HEIGHT, INK, MUTED, ORANGE,
    WIDTH, WORLD_WIDTH, YELLOW,
)


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Polarix — Niveau 01")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 25)
        self.small_font = pygame.font.Font(None, 20)
        self.big_font = pygame.font.Font(None, 72)
        self.running = True
        self.reset()

    def reset(self) -> None:
        self.player = Player(90, 560)
        self.solids, self.blocks, self.cells, self.generator = make_level()
        self.camera_x = 0.0
        self.elapsed = 0.0
        self.finished = False
        self.hint = "Avance avec Q et D"
        self.hint_timer = 5.0
        self.shake = 0.0
        self.particles: list[dict[str, object]] = []

    @property
    def collected_cells(self) -> int:
        return sum(cell.collected for cell in self.cells)

    def run(self) -> None:
        test_frames = int(os.getenv("POLARIX_TEST_FRAMES", "0"))
        frame_count = 0
        while self.running:
            dt = min(self.clock.tick(FPS) / 1000.0, 1 / 30)
            self.handle_events()
            self.update(dt)
            self.draw()
            pygame.display.flip()
            frame_count += 1
            if test_frames and frame_count >= test_frames:
                self.running = False
        pygame.quit()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE and not self.finished:
                    self.player.jump()
                elif event.key == pygame.K_r:
                    self.reset()
                elif event.key == pygame.K_e:
                    self.activate_generator()

    def update(self, dt: float) -> None:
        self.elapsed += dt
        self.hint_timer -= dt
        if self.finished:
            self._update_particles(dt)
            return

        keys = pygame.key.get_pressed()
        self.player.update(dt, keys, self.solids, self.blocks)
        for block in self.blocks:
            block.update(dt, self.solids)
        self._collect_cells()

        if self.player.rect.top > HEIGHT + 150:
            x = self.player.rect.x
            checkpoint = 1765 if x > 1650 else 1235 if x > 1100 else 680 if x > 560 else 90
            self.player.rect.topleft = (checkpoint, 520)
            self.player.velocity.update(0, 0)
            self.shake = 12
            self.hint = "Oups ! Retour au dernier point sûr"
            self.hint_timer = 1.8

        if self.player.rect.x > 2480 and self.collected_cells < 2 and self.hint_timer <= 0:
            self.hint = "Il manque des cellules d’énergie"
            self.hint_timer = 2.0

        target_camera = max(0, min(WORLD_WIDTH - WIDTH, self.player.rect.x - WIDTH * 0.36))
        self.camera_x += (target_camera - self.camera_x) * min(1, dt * 4.8)
        self.shake *= math.pow(0.02, dt)
        self._update_particles(dt)

    def _collect_cells(self) -> None:
        for cell in self.cells:
            if cell.collected:
                continue
            if pygame.Vector2(self.player.rect.center).distance_to(cell.position) < 46:
                cell.collected = True
                self.hint = (
                    "Les deux cellules sont chargées !"
                    if self.collected_cells == 2 else "Cellule d’énergie récupérée"
                )
                self.hint_timer = 2.4
                for _ in range(28):
                    angle = random.random() * math.tau
                    speed = 80 + random.random() * 180
                    self.particles.append({
                        "position": cell.position.copy(),
                        "velocity": pygame.Vector2(math.cos(angle), math.sin(angle)) * speed,
                        "life": 1.0,
                        "color": YELLOW,
                    })

    def activate_generator(self) -> None:
        if self.player.rect.x < 2480 or self.finished:
            return
        if self.collected_cells < 2:
            self.hint = "Trouve d’abord les deux cellules"
            self.hint_timer = 2.0
            return
        self.finished = True
        self.hint_timer = 0
        for _ in range(80):
            self.particles.append({
                "position": pygame.Vector2(self.generator.rect.center),
                "velocity": pygame.Vector2(random.uniform(-350, 350), random.uniform(-400, 50)),
                "life": random.uniform(0.6, 1.4),
                "color": random.choice((CYAN, YELLOW, INK)),
            })

    def _update_particles(self, dt: float) -> None:
        for particle in self.particles:
            position = particle["position"]
            velocity = particle["velocity"]
            assert isinstance(position, pygame.Vector2)
            assert isinstance(velocity, pygame.Vector2)
            position += velocity * dt
            velocity.y += 300 * dt
            particle["life"] = float(particle["life"]) - dt * 1.3
        self.particles = [p for p in self.particles if float(p["life"]) > 0]

    def draw(self) -> None:
        shake_x = random.uniform(-self.shake / 2, self.shake / 2)
        camera = self.camera_x - shake_x
        self._draw_background(camera)
        for solid in self.solids:
            solid.draw(self.screen, camera)
        self._draw_guides(camera)
        self.generator.draw(self.screen, camera, self.collected_cells == 2, self.elapsed)
        for cell in self.cells:
            cell.draw(self.screen, camera, self.elapsed)
        for block in self.blocks:
            block.draw(self.screen, camera)
        self._draw_beams(self.player.active_beams, camera)
        self.player.draw(self.screen, camera)
        self._draw_particles(camera)
        self._draw_hud(camera)
        if self.finished:
            self._draw_victory()

    def _draw_background(self, camera: float) -> None:
        self.screen.fill(BACKGROUND)
        for x in range(-round(camera * 0.18) % 220, WIDTH + 220, 220):
            pygame.draw.rect(self.screen, (23, 40, 50), (x, 75, 150, 470), 3)
            pygame.draw.line(self.screen, (23, 40, 50), (x, 75), (x + 150, 545), 3)
        for x in range(-round(camera * 0.35) % 330, WIDTH + 330, 330):
            pygame.draw.rect(self.screen, (15, 32, 41), (x, 545, 210, 18))
            pygame.draw.rect(self.screen, (15, 32, 41), (x + 30, 170, 18, 375))
        for x in range(35, WIDTH, 120):
            alpha = 18 + round(8 * math.sin(self.elapsed + x))
            glow = pygame.Surface((4, 360), pygame.SRCALPHA)
            glow.fill((*CYAN, alpha))
            self.screen.blit(glow, (x, 230))

    def _draw_beams(self, beams: list[MagnetBeam], camera: float) -> None:
        start = pygame.Vector2(self.player.rect.centerx - camera, self.player.rect.centery)
        for beam in beams:
            end = pygame.Vector2(beam.target.rect.centerx - camera, beam.target.rect.centery)
            delta = end - start
            segments = max(3, int(delta.length() / 24))
            for offset in (-7, 0, 7):
                points = []
                for index in range(segments + 1):
                    t = index / segments
                    point = start.lerp(end, t)
                    point.y += math.sin(t * math.pi) * -25 + offset
                    points.append(point)
                step = 2 if beam.mode == "attract" else 3
                for index in range(0, len(points) - 1, step):
                    pygame.draw.line(self.screen, beam.color, points[index], points[min(index + 1, len(points) - 1)], 3)

    def _draw_guides(self, camera: float) -> None:
        guides = [
            (270, 575, "Q / D  AVANCER", MUTED),
            (575, 345, "Z  REPOUSSER À GAUCHE", CYAN),
            (840, 500, "A  ATTIRER À GAUCHE", CYAN),
            (1400, 270, "ATTIRE-TOI ENTRE LES PAROIS", YELLOW),
            (1990, 350, "P  REPOUSSER À DROITE", ORANGE),
        ]
        for x, y, text, color in guides:
            screen_x = x - camera
            if -220 < screen_x < WIDTH + 220:
                self._world_label(screen_x, y, text, color)

    def _world_label(self, x: float, y: float, text: str, color: tuple[int, int, int]) -> None:
        label = self.small_font.render(text, True, color)
        box = label.get_rect(center=(round(x), round(y)))
        panel = box.inflate(24, 14)
        pygame.draw.rect(self.screen, (7, 16, 22), panel, border_radius=7)
        pygame.draw.rect(self.screen, color, panel, 1, border_radius=7)
        self.screen.blit(label, box)

    def _draw_particles(self, camera: float) -> None:
        for particle in self.particles:
            position = particle["position"]
            color = particle["color"]
            assert isinstance(position, pygame.Vector2)
            assert isinstance(color, tuple)
            pygame.draw.rect(self.screen, color, (position.x - camera, position.y, 5, 5))

    def _draw_hud(self, camera: float) -> None:
        panel = pygame.Rect(22, 20, 470, 64)
        pygame.draw.rect(self.screen, (12, 27, 35), panel, border_radius=11)
        pygame.draw.rect(self.screen, (38, 56, 68), panel, 1, border_radius=11)
        mission = self.font.render("MISSION · Réactiver le générateur", True, INK)
        count = self.font.render(f"CELLULES  {self.collected_cells} / 2", True, YELLOW)
        self.screen.blit(mission, (40, 32))
        self.screen.blit(count, (40, 57))

        if self.player.rect.x > 2460:
            ready = self.collected_cells == 2
            text = "[ E ] ACTIVER" if ready else "CELLULES MANQUANTES"
            self._world_label(2695 - camera, 390, text, CYAN if ready else DANGER)

        if self.hint_timer > 0:
            label = self.font.render(self.hint, True, INK)
            panel = label.get_rect(center=(WIDTH // 2, 113)).inflate(34, 18)
            pygame.draw.rect(self.screen, (7, 16, 22), panel, border_radius=9)
            self.screen.blit(label, label.get_rect(center=panel.center))

    def _draw_victory(self) -> None:
        veil = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        veil.fill((5, 11, 15, 215))
        self.screen.blit(veil, (0, 0))
        title = self.big_font.render("NIVEAU TERMINÉ !", True, INK)
        kicker = self.font.render("SECTEUR RÉACTIVÉ", True, CYAN)
        info = self.font.render("Le générateur tourne de nouveau · R pour rejouer", True, MUTED)
        self.screen.blit(kicker, kicker.get_rect(center=(WIDTH // 2, 285)))
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, 345)))
        self.screen.blit(info, info.get_rect(center=(WIDTH // 2, 405)))
