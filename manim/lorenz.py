import numpy as np
import os
from manim import *
from manim.opengl import *
from scipy.integrate import solve_ivp


def lorenz_system(t, state, sigma=10, rho=28, beta=8 / 3):
    x, y, z = state
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z

    return [dxdt, dydt, dzdt]


def ode_solution_point(function, state0, time, dt=0.01):
    solution = solve_ivp(
        function,
        t_span=(0, time),
        y0=state0,
        t_eval=np.arange(0, time, dt)
    )
    return solution.y  # y output is a vector value, not necessarily the y coordinate value, T for transpose


class LorenzAttractor(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=(-50, 50, 5),
            y_range=(-50, 50, 5),
            z_range=(0, 50, 5),
            axis_config={"include_tip": True, "include_ticks": True, "stroke_width": 1}
        )
        #  dot = Sphere(radius=0.05, fill_color=BLUE).move_to(0*RIGHT + 0.1*UP + 0.105*OUT)
        #  axes.set_width()
        axes.center()

        self.add(axes)
        self.set_camera_orientation(phi=65*DEGREES, theta=30*DEGREES)


        #  lorenz solutions
        state = []
        state0 = [1, 1, 1.05]
        time = 10
        dt = 0.01
        points = ode_solution_point(lorenz_system, state0, time)
        print(points)
        curve = ParametricFunction(lambda t: ode_solution_point(lorenz_system, state0, t),
                                   t_range=(0, time)
                                   )

        curve.move_to(ORIGIN)

        self.play(Create(curve), run_time=10, rate_func=linear)

