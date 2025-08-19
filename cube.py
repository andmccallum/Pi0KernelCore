"""Defines the core N-dimensional lattice and diffusion operators."""

import numpy as np

class HyperdimensionalCube:
    def __init__(self, dimensions: int, size: int, Lp2: float):
        self.dim = dimensions
        self.size = size
        self.Lp2 = Lp2
        self.state = np.zeros((size,) * dimensions, dtype=float)
        self.info = np.zeros_like(self.state)

    def laplacian(self, arr: np.ndarray) -> np.ndarray:
        out = np.zeros_like(arr)
        for axis in range(self.dim):
            rolled_p = np.roll(arr, -1, axis=axis)
            rolled_m = np.roll(arr, +1, axis=axis)
            out += rolled_p + rolled_m - 2 * arr
        return out

    def step(self, D: float, source: np.ndarray = None):
        lap = self.laplacian(self.state)
        lapI = self.laplacian(self.info)
        self.state += D * lap + self.Lp2 * lapI
        if source is not None:
            self.state += source
        return self.state
