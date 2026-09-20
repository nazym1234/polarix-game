"""Définition du premier niveau de Polarix."""

import pygame

from .entities import EnergyCell, Generator, MetalBlock, Solid


def make_level() -> tuple[list[Solid], list[MetalBlock], list[EnergyCell], Generator]:
    solids = [
        Solid(pygame.Rect(0, 640, 520, 80)),
        Solid(pygame.Rect(650, 640, 430, 80)),
        Solid(pygame.Rect(1215, 640, 390, 80)),
        Solid(pygame.Rect(1745, 640, 370, 80)),
        Solid(pygame.Rect(2250, 640, 670, 80)),
        Solid(pygame.Rect(455, 410, 38, 230), True),
        Solid(pygame.Rect(685, 445, 42, 195), True),
        Solid(pygame.Rect(930, 525, 150, 24), True),
        Solid(pygame.Rect(1245, 430, 38, 210), True),
        Solid(pygame.Rect(1515, 340, 38, 300), True),
        Solid(pygame.Rect(1283, 340, 270, 24), True),
        Solid(pygame.Rect(1780, 505, 150, 24), True),
        Solid(pygame.Rect(2050, 395, 40, 245), True),
        Solid(pygame.Rect(2280, 465, 42, 175), True),
    ]
    blocks = [
        MetalBlock(pygame.Rect(800, 582, 58, 58), mass=1.25),
        MetalBlock(pygame.Rect(1860, 447, 58, 58), mass=1.1),
    ]
    cells = [
        EnergyCell(pygame.Vector2(984, 477)),
        EnergyCell(pygame.Vector2(1398, 300)),
    ]
    return solids, blocks, cells, Generator(pygame.Rect(2600, 420, 190, 220))
