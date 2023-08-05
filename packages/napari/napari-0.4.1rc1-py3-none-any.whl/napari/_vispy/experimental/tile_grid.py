"""TileGrid class.

Tile grid is a grid draw around/between the tiles for debugging.
"""
from typing import List

import numpy as np
from vispy.scene.node import Node
from vispy.scene.visuals import Line

from ...layers.image.experimental import OctreeChunk

# Draw with lines of this width and color.
GRID_WIDTH = 3
GRID_COLOR = (1, 0, 0, 1)

# Draw grid on top of the tiles.
LINE_VISUAL_ORDER = 10


# Outline for 'segments' point, each pair is one line segment.
_OUTLINE = np.array(
    [[0, 0], [1, 0], [1, 0], [1, 1], [1, 1], [0, 1], [0, 1], [0, 0]],
    dtype=np.float32,
)


def _chunk_outline(chunk: OctreeChunk) -> np.ndarray:
    """Return the verts that outline this single chunk.

    The Line is should be drawn in 'segments' mode.

    Parameters
    ----------
    chunk : OctreeChunk
        Create outline of this chunk.

    Return
    ------
    np.ndarray
        The verts for the outline.
    """
    geom = chunk.geom
    x, y = geom.pos
    h, w = chunk.data.shape[:2]
    w *= geom.scale[1]
    h *= geom.scale[0]

    outline = _OUTLINE.copy()

    # Modify in place.
    outline[:, :2] *= (w, h)
    outline[:, :2] += (x, y)

    return outline


class TileGrid:
    """A grid to show the outline of all the tiles.

    Created for debugging although could be shown for real as well.

    Attributes
    ----------
    parent : Node
        The parent of the grid.
    """

    def __init__(self, parent: Node):
        self.parent = parent
        self.line = self._create_line()

    def _create_line(self) -> Line:
        """Create the Line visual for the grid.

        Return
        ------
        Line
            The new Line visual.
        """
        line = Line(connect='segments', color=GRID_COLOR, width=GRID_WIDTH)
        line.order = LINE_VISUAL_ORDER
        line.parent = self.parent
        return line

    def update_grid(self, chunks: List[OctreeChunk]) -> None:
        """Update grid for this set of chunks.

        Parameters
        ----------
        chunks : List[ImageChunks]
            Add a grid that outlines these chunks.
        """
        # TODO_OCTREE: create in one go without vstack?
        verts = np.zeros((0, 2), dtype=np.float32)
        for octree_chunk in chunks:
            chunk_verts = _chunk_outline(octree_chunk)
            verts = np.vstack([verts, chunk_verts])

        self.line.set_data(verts)

    def clear(self) -> None:
        """Clear the grid so nothing is drawn."""
        data = np.zeros((0, 2), dtype=np.float32)
        self.line.set_data(data)
