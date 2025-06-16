from manim import *
import numpy as np
import os


class LorenzAttractor(ThreeDScene):
    def construct(self):
        self.create_lorenz_attractor()

    def lorenz_system(self, pos, sigma=10, rho=28, beta=8/3):
        x, y, z = pos
        dxdt = sigma * (y - x)
        dydt = x * (rho - z) - y
        dzdt = x * y - beta * z
        return np.array([dxdt, dydt, dzdt])
