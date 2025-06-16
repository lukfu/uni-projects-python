import manim
import ffmpeg
from manim import *


## manim -pql scene.py CreateCircle -- do not necessarily have to specify scene to animate, can also use -a to animate all
## manim -pqh scene.py CreateCircle -- high quality
## manim --save_sections scene.py -- saves sections
## quality levels: -ql, -qm, -qh, -qp, -qk, gives low(480p15fps), medium(720p30fps), high(1080p60fps), 2k, and 4k
## --format gif for gif instead of .mp4


class CreateCircle(Scene):
    def construct(self):
        circle = Circle()
        circle.set_fill(PINK, opacity=0.5)
        self.play(Create(circle))


class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        circle.set_fill(PINK, opacity=0.5)

        square = Square()
        square.rotate(PI / 4)

        self.play(Create(square))
        self.play(Transform(square, circle))
        self.play(FadeOut(square))


class SquareAndCircle(Scene):
    def construct(self):
        circle = Circle()
        circle.set_fill(PINK, opacity=0.5)

        square = Square()
        square.set_fill(BLUE, opacity=0.5)

        square.next_to(circle, RIGHT, buff=0.5)
        self.play(Create(circle), Create(square))


class AnimateSquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        square = Square()

        self.play(Create(square))
        self.play(square.animate.rotate(PI / 4))
        self.play(Transform(square, circle))
        self.play(square.animate.set_fill(PINK, opacity=0.5))


class DifferentRotations(Scene):
    def construct(self):
        left_square = Square(color=BLUE, fill_opacity=0.7).shift(2 * LEFT)
        right_square = Square(color=GREEN, fill_opacity=0.7).shift(2 * RIGHT)
        self.play(left_square.animate.rotate(PI), Rotate(right_square, angle=PI), run_time=2)
        self.wait()


class TwoTransforms(Scene):
    def transform(self):
        a = Circle()
        b = Square()
        c = Triangle()
        self.play(Transform(a, b))
        self.play(Transform(a, c))
        self.play(FadeOut(a))

    def replacementtransform(self):
        a = Circle()
        b = Square()
        c = Triangle()
        self.play(ReplacementTransform(a, b))
        self.play(ReplacementTransform(b, c))
        self.play(FadeOut(c))

    def construct(self):
        self.transform()
        self.wait(0.5)
        self.replacementtransform()


class NextSectionTest(Scene):
    def construct(self):
        circle = Circle()
        circle.set_fill(PINK, opacity=0.5)

        square = Square()
        square.rotate(PI / 4)

        self.play(Create(square))
        self.play(Transform(square, circle))
        self.play(FadeOut(square))

        self.wait(0.5)
        self.next_section()

        circle = Circle()
        circle.set_fill(PINK, opacity=0.5)

        square = Square()
        square.set_fill(BLUE, opacity=0.5)

        square.next_to(circle, RIGHT, buff=0.5)
        self.play(Create(circle), Create(square))
        self.play(FadeOut(circle, square))

        self.wait(0.5)
        self.next_section()

        circle = Circle()
        square = Square()

        self.play(Create(square))
        self.play(square.animate.rotate(PI / 4))
        self.play(Transform(square, circle))
        self.play(square.animate.set_fill(PINK, opacity=0.5))


class MobjectPlacement(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        triangle = Triangle()

        circle.move_to(2 * LEFT)
        square.next_to(circle, 2 * LEFT)
        triangle.align_to(circle, LEFT)  ##align the left border of triangle to left border of circle

        self.add(circle, square, triangle)
        self.wait(1)


class MobjectStyling(Scene):
    def construct(self):
        circle = Circle().shift(LEFT)
        square = Square().shift(UP)
        triangle = Triangle().shift(RIGHT)

        circle.set_stroke(color=GREEN, width=20)
        square.set_fill(YELLOW, opacity=1.0)
        triangle.set_fill(PINK, opacity=0.5)

        self.add(circle, square, triangle)  ## order of adding matters
        self.wait(1)


class Count(Animation):
    def __init__(self, number: DecimalNumber, start: float, end: float, **kwargs) -> None:
        # Pass number as the mobject of the animation
        super().__init__(number, **kwargs)
        # Set start and end
        self.start = start
        self.end = end

    def interpolate_mobject(self, alpha: float) -> None:
        # Set value of DecimalNumber according to alpha
        value = self.start + (alpha * (self.end - self.start))
        self.mobject.set_value(value)


class CountingScene(Scene):
    def construct(self):
        # Create Decimal Number and add it to scene
        number = DecimalNumber().set_color(WHITE).scale(5)
        # Add an updater to keep the DecimalNumber centered as its value changes
        number.add_updater(lambda number: number.move_to(ORIGIN))

        self.add(number)

        self.wait()

        # Play the Count Animation to count from 0 to 100 in 4 seconds
        self.play(Count(number, 0, 100), run_time=4, rate_func=linear)

        self.wait()


class MobjectExample(Scene):
    def construct(self):
        p1 = [-1, -1, 0]
        p2 = [1, -1, 0]
        p3 = [1, 1, 0]
        p4 = [-1, 1, 0]
        a = Line(p1, p2).append_points(Line(p2, p3).points).append_points(Line(p3, p4).points)
        point_start = a.get_start()
        point_end = a.get_end()
        point_center = a.get_center()
        self.add(
            Text(f"a.get_start() = {np.round(point_start, 2).tolist()}", font_size=24).to_edge(UR).set_color(YELLOW))
        self.add(Text(f"a.get_end() = {np.round(point_end, 2).tolist()}", font_size=24).next_to(self.mobjects[-1],
                                                                                                DOWN).set_color(RED))
        self.add(Text(f"a.get_center() = {np.round(point_center, 2).tolist()}", font_size=24).next_to(self.mobjects[-1],
                                                                                                      DOWN).set_color(
            BLUE))

        self.add(Dot(a.get_start()).set_color(YELLOW).scale(2))
        self.add(Dot(a.get_end()).set_color(RED).scale(2))
        self.add(Dot(a.get_top()).set_color(GREEN_A).scale(2))
        self.add(Dot(a.get_bottom()).set_color(GREEN_D).scale(2))
        self.add(Dot(a.get_center()).set_color(BLUE).scale(2))
        self.add(Dot(a.point_from_proportion(0.5)).set_color(ORANGE).scale(2))
        self.add(*[Dot(x) for x in a.points])
        self.add(a)


class ExampleTransform(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        m1 = Square().set_color(RED)
        m2 = Rectangle().set_color(RED).rotate(0.2)
        self.play(Transform(m1, m2))


class ExampleRotation(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        m1a = Square().set_color(RED).shift(LEFT)
        m1b = Circle().set_color(RED).shift(LEFT)
        m2a = Square().set_color(BLUE).shift(RIGHT)
        m2b = Circle().set_color(BLUE).shift(RIGHT)

        points = m2a.points
        points = np.roll(points, int(len(points) / 4), axis=0)
        m2a.points = points

        self.play(Transform(m1a, m1b), Transform(m2a, m2b))


class PlotTest(Scene):
    def construct(self):
        ax = Axes(x_range=[-5, 5, 1],
                  y_range=[-1, 5, 1]
                  )

        f1 = ax.plot(lambda x: (1/5)*x**2, color=BLUE)
        f2 = ax.plot(lambda x: x*(1/2) + 1, color=RED)

        self.add(ax, f1, f2)


class PlotTestAnimate(Scene):
    def construct(self):
        vt = ValueTracker(-5)  # parametrised value that changes continuously, input as starting value?

        ax = Axes(x_range=[-5, 5, 1],
                  y_range=[-1, 5, 1]
                  )

        f1 = always_redraw(lambda: ax.plot(lambda x: (1/5)*x**2, color=BLUE, x_range=[-5, vt.get_value()]), )
        f2 = always_redraw(lambda: ax.plot(lambda x: x*(1/2) + 1, color=RED, x_range=[-5, vt.get_value()]))

        f1_dot = always_redraw(lambda: Dot(
            point=ax.c2p(vt.get_value(), f1.underlying_function(vt.get_value())),
            color=YELLOW
        ))

        f2_dot = always_redraw(lambda: Dot(
            point=ax.c2p(vt.get_value(), f2.underlying_function(vt.get_value())),
            color=YELLOW
        ))

        self.play(Write(ax))
        self.wait()
        self.add(f1, f2, f1_dot, f2_dot)
        #  animate the value tracker, from the intial starting point of -5 to 5
        self.play(vt.animate.set_value(5), run_time=6)
