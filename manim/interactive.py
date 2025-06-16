from manim import *
from manim.opengl import *


#  manim interactive.py -p --renderer=opengl IntroScene


class IntroScene(Scene):
    def construct(self):
        square = Square(color=RED).shift(LEFT * 2)
        circle = Circle(color=BLUE).shift(RIGHT * 2)

        self.play(Write(square), Write(circle))

        self.play(
            square.animate.shift(UP*0.5),
            circle.animate.shift(DOWN*0.5)
        )
        self.play(
            square.animate.rotate(PI/2).set_fill(opacity=0.8),
            circle.animate.scale(2).set_fill(opacity=0.8)
        )

        self.interactive_embed()
        self.wait()
