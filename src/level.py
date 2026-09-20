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
    ]
    blocks = [
        # Première énigme : pousser cette poutre dans le vide pour créer un pont.
        MetalBlock(pygame.Rect(300, 606, 150, 34), mass=1.8),
        MetalBlock(pygame.Rect(800, 582, 58, 58), mass=1.25),
        MetalBlock(pygame.Rect(1860, 447, 58, 58), mass=1.1),
        MetalBlock(pygame.Rect(685, 445, 42, 195), mass=3.0),
        MetalBlock(pygame.Rect(930, 525, 150, 24), mass=2.0),
        MetalBlock(pygame.Rect(1245, 430, 38, 210), mass=3.0),
        MetalBlock(pygame.Rect(1515, 340, 38, 300), mass=3.5),
        MetalBlock(pygame.Rect(1283, 340, 270, 24), mass=2.8),
        MetalBlock(pygame.Rect(1780, 505, 150, 24), mass=2.0),
        MetalBlock(pygame.Rect(2050, 395, 40, 245), mass=3.2),
        MetalBlock(pygame.Rect(2280, 465, 42, 175), mass=3.0),
    ]
    cells = [
        EnergyCell(pygame.Vector2(984, 477)),
        EnergyCell(pygame.Vector2(1398, 300)),
    ]
    return solids, blocks, cells, Generator(pygame.Rect(2600, 420, 190, 220))
