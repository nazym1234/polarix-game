"""Entités et physique du prototype Polarix."""

from __future__ import annotations

from dataclasses import dataclass, field
import math
import pygame

from .settings import (
    CYAN, GRAVITY, INK, JUMP_SPEED, MAGNET_FORCE, MAGNET_RANGE,
    METAL, METAL_DARK, ORANGE, PLAYER_SPEED, YELLOW,
)


@dataclass
class Solid:
    rect: pygame.Rect
    metal: bool = False

    def draw(self, surface: pygame.Surface, camera_x: float) -> None:
        rect = self.rect.move(-camera_x, 0)
        if not self.metal:
            pygame.draw.rect(surface, (26, 42, 50), rect)
            pygame.draw.rect(surface, (38, 59, 68), (rect.x, rect.y, rect.w, 9))
            return
        pygame.draw.rect(surface, METAL_DARK, rect, border_radius=5)
        pygame.draw.rect(surface, METAL, rect.inflate(-6, -6), 3, border_radius=3)
        for y in range(rect.top + 15, rect.bottom - 5, 32):
            for x in range(rect.left + 14, rect.right - 5, 36):
                pygame.draw.circle(surface, (157, 178, 186), (x, y), 3)


@dataclass
class Body:
    rect: pygame.Rect
    velocity: pygame.Vector2 = field(default_factory=pygame.Vector2)
    grounded: bool = False

    def move_and_collide(self, dt: float, solids: list[Solid]) -> None:
        self.rect.x += round(self.velocity.x * dt)
        for solid in solids:
            if not self.rect.colliderect(solid.rect):
                continue
            if self.velocity.x > 0:
                self.rect.right = solid.rect.left
            elif self.velocity.x < 0:
                self.rect.left = solid.rect.right
            self.velocity.x = 0

        self.rect.y += round(self.velocity.y * dt)
        self.grounded = False
        for solid in solids:
            if not self.rect.colliderect(solid.rect):
                continue
            if self.velocity.y > 0:
                self.rect.bottom = solid.rect.top
                self.grounded = True
            elif self.velocity.y < 0:
                self.rect.top = solid.rect.bottom
            self.velocity.y = 0


@dataclass
class MetalBlock(Body):
    mass: float = 1.2
    activated: bool = False

    def update(self, dt: float, solids: list[Solid]) -> None:
        if not self.activated:
            return
        self.velocity.y = min(900, self.velocity.y + GRAVITY * dt)
        self.velocity.x *= math.pow(0.02, dt)
        self.velocity.x = max(-620, min(620, self.velocity.x))
        self.move_and_collide(dt, solids)

    def draw(self, surface: pygame.Surface, camera_x: float) -> None:
        rect = self.rect.move(-camera_x, 0)
        pygame.draw.rect(surface, (51, 75, 87), rect, border_radius=7)
        pygame.draw.rect(surface, (145, 174, 185), rect.inflate(-8, -8), 3)
        pygame.draw.line(surface, METAL, rect.topleft, rect.bottomright, 3)
        pygame.draw.line(surface, METAL, rect.topright, rect.bottomleft, 3)


@dataclass
class MagnetBeam:
    side: str
    mode: str
    target: Solid | MetalBlock
    color: tuple[int, int, int]


class Player(Body):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(pygame.Rect(x, y, 38, 54))
        self.facing = 1
        self.active_beams: list[MagnetBeam] = []

    def jump(self) -> None:
        if self.grounded:
            self.velocity.y = -JUMP_SPEED
            self.grounded = False

    def update(
        self,
        dt: float,
        keys: set[str],
        solids: list[Solid],
        blocks: list[MetalBlock],
    ) -> None:
        move = int("d" in keys or "right" in keys) - int("a" in keys or "q" in keys or "left" in keys)
        if move:
            self.facing = move
        desired = move * PLAYER_SPEED
        response = min(1.0, dt * (13 if self.grounded else 7))
        self.velocity.x += (desired - self.velocity.x) * response
        self.velocity.y = min(950, self.velocity.y + GRAVITY * dt)

        actions = []
        if "j" in keys: actions.append(("left", "attract", CYAN))
        if "k" in keys: actions.append(("left", "repel", CYAN))
        if "o" in keys: actions.append(("right", "attract", ORANGE))
        if "p" in keys: actions.append(("right", "repel", ORANGE))

        self.active_beams.clear()
        for side, mode, color in actions:
            target = self._nearest_metal(side, solids, blocks)
            if target is not None:
                self._apply_magnet(target, side, mode, color, dt)

        self.velocity.x = max(-520, min(520, self.velocity.x))
        self.move_and_collide(dt, solids)
        self._collide_blocks(blocks)

    def _nearest_metal(
        self, side: str, solids: list[Solid], blocks: list[MetalBlock]
    ) -> Solid | MetalBlock | None:
        origin = pygame.Vector2(self.rect.center)
        # Les objets mobiles sont toujours prioritaires. Les plaques fixes ne
        # servent d'ancrage au robot que lorsqu'aucun objet n'est à portée.
        movable = self._nearest_on_side(side, origin, blocks)
        if movable is not None:
            return movable
        return self._nearest_on_side(side, origin, [s for s in solids if s.metal])

    def _nearest_on_side(
        self,
        side: str,
        origin: pygame.Vector2,
        candidates: list[Solid] | list[MetalBlock],
    ) -> Solid | MetalBlock | None:
        best: Solid | MetalBlock | None = None
        best_distance = MAGNET_RANGE
        for target in candidates:
            delta = pygame.Vector2(target.rect.center) - origin
            if side == "left" and delta.x >= -8:
                continue
            if side == "right" and delta.x <= 8:
                continue
            distance = delta.length()
            if distance < best_distance:
                best = target
                best_distance = distance
        return best

    def _apply_magnet(
        self,
        target: Solid | MetalBlock,
        side: str,
        mode: str,
        color: tuple[int, int, int],
        dt: float,
    ) -> None:
        delta = pygame.Vector2(target.rect.center) - pygame.Vector2(self.rect.center)
        distance = max(1.0, delta.length())
        direction = delta / distance
        sign = 1 if mode == "attract" else -1
        force = MAGNET_FORCE * (1 - distance / MAGNET_RANGE * 0.45)
        if isinstance(target, MetalBlock):
            target.activated = True
            target.velocity += -direction * force * sign * dt / target.mass
        else:
            self.velocity += direction * force * sign * dt
        self.active_beams.append(MagnetBeam(side, mode, target, color))

    def _collide_blocks(self, blocks: list[MetalBlock]) -> None:
        for block in blocks:
            if not self.rect.colliderect(block.rect):
                continue
            dx = self.rect.centerx - block.rect.centerx
            dy = self.rect.centery - block.rect.centery
            if abs(dy) > abs(dx) and dy < 0 and self.velocity.y >= 0:
                self.rect.bottom = block.rect.top
                self.velocity.y = 0
                self.grounded = True
            elif dx < 0:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right

    def draw(self, surface: pygame.Surface, camera_x: float) -> None:
        rect = self.rect.move(-camera_x, 0)
        pygame.draw.rect(surface, INK, rect, border_radius=11)
        visor = pygame.Rect(rect.x + 6, rect.y + 10, 26, 18)
        pygame.draw.rect(surface, (23, 42, 51), visor, border_radius=6)
        pygame.draw.rect(surface, CYAN, (visor.x + 5, visor.y + 6, 5, 5))
        pygame.draw.rect(surface, ORANGE, (visor.x + 16, visor.y + 6, 5, 5))
        left_on = any(b.side == "left" for b in self.active_beams)
        right_on = any(b.side == "right" for b in self.active_beams)
        pygame.draw.rect(surface, CYAN if left_on else (83, 102, 110), (rect.x - 8, rect.y + 18, 9, 24), border_radius=4)
        pygame.draw.rect(surface, ORANGE if right_on else (83, 102, 110), (rect.right - 1, rect.y + 18, 9, 24), border_radius=4)


@dataclass
class EnergyCell:
    position: pygame.Vector2
    collected: bool = False

    def draw(self, surface: pygame.Surface, camera_x: float, elapsed: float) -> None:
        if self.collected:
            return
        pulse = 15 + round(math.sin(elapsed * 5) * 2)
        center = (round(self.position.x - camera_x), round(self.position.y))
        pygame.draw.circle(surface, (91, 72, 24), center, pulse + 8)
        pygame.draw.rect(surface, YELLOW, (center[0] - 11, center[1] - 20, 22, 40), border_radius=6)
        pygame.draw.rect(surface, (100, 78, 18), (center[0] - 4, center[1] - 11, 8, 22))


@dataclass
class Generator:
    rect: pygame.Rect

    def draw(self, surface: pygame.Surface, camera_x: float, ready: bool, elapsed: float) -> None:
        rect = self.rect.move(-camera_x, 0)
        border = CYAN if ready else (82, 104, 115)
        pygame.draw.rect(surface, (35, 54, 64), rect, border_radius=14)
        pygame.draw.rect(surface, border, rect.inflate(-16, -16), 4, border_radius=9)
        center = (rect.centerx, rect.y + 80)
        pygame.draw.circle(surface, (16, 28, 34), center, 48)
        pygame.draw.circle(surface, border, center, 42, 9)
        radius = 12 + round(math.sin(elapsed * 6) * 3) if ready else 12
        pygame.draw.circle(surface, CYAN if ready else (51, 69, 76), center, radius)
