from pathlib import Path

from manim import *
from manim_voiceover import VoiceoverScene

from shared.voiceover import create_speech_service


class DerivativeInstantaneousSlope(VoiceoverScene):
    """Explain instantaneous slope with narration-controlled animation timing.

    Manim Voiceover is the timing authority. The moving secant construction is
    driven by one ValueTracker so its geometry cannot drift out of sync.
    """

    P_X = 0.0
    P_COLOR = BLUE_C
    Q_COLOR = ORANGE
    LINE_COLOR = YELLOW
    DX_COLOR = TEAL_C
    DY_COLOR = GREEN_C
    MUTED_COLOR = GREY_B

    @staticmethod
    def curve_function(x: float) -> float:
        return 0.35 * x**2 + 0.8 * x - 1.1

    @classmethod
    def derivative_at_p(cls) -> float:
        return 0.7 * cls.P_X + 0.8

    def construct(self):
        self.camera.background_color = "#10131A"
        self.set_speech_service(
            create_speech_service(Path(__file__).with_name("voiceover.json"))
        )

        self.show_speed_intuition()
        graph_state = self.show_secant_graph()
        self.show_secant_to_tangent(graph_state)
        self.show_zero_over_zero(graph_state)
        self.show_limit_definition(graph_state)
        self.show_final_distinction(graph_state)

    def show_speed_intuition(self):
        """Beat 1: a lightweight interval-versus-instant comparison."""
        title = Text(
            "Why is the derivative an instantaneous slope?",
            font_size=34,
            weight=MEDIUM,
        ).to_edge(UP, buff=0.38)

        time_line = NumberLine(
            x_range=[0, 10, 10],
            length=7.0,
            include_numbers=False,
            include_tip=False,
            color=self.MUTED_COLOR,
        ).shift(DOWN * 0.55)
        start_dot = Dot(time_line.n2p(0), color=self.P_COLOR)
        end_dot = Dot(time_line.n2p(10), color=self.Q_COLOR)
        start_label = Text("0 s", font_size=24).next_to(start_dot, DOWN, buff=0.25)
        end_label = Text("10 s", font_size=24).next_to(end_dot, DOWN, buff=0.25)

        interval_brace = Brace(time_line, UP, color=self.DX_COLOR)
        average_fraction = MathTex(
            r"\frac{\text{total distance}}{10\ \text{seconds}}",
            font_size=38,
        ).next_to(interval_brace, UP, buff=0.25)
        average_label = Text(
            "average speed  •  over an interval",
            font_size=26,
            color=self.DX_COLOR,
        ).next_to(average_fraction, UP, buff=0.18)

        gauge_arc = Arc(
            radius=0.48,
            start_angle=PI,
            angle=-PI,
            color=self.Q_COLOR,
            stroke_width=5,
        )
        gauge_needle = Line(
            gauge_arc.get_center(),
            gauge_arc.get_center() + 0.37 * normalize(UP + RIGHT),
            color=self.Q_COLOR,
            stroke_width=5,
        )
        gauge_dot = Dot(gauge_arc.get_center(), radius=0.05, color=self.Q_COLOR)
        speedometer = VGroup(gauge_arc, gauge_needle, gauge_dot).next_to(
            end_dot, UP, buff=0.42
        )
        now_label = Text(
            "speed right now  •  at one instant",
            font_size=26,
            color=self.Q_COLOR,
        ).next_to(speedometer, UP, buff=0.2)

        with self.voiceover(text="Imagine driving along a winding road.") as tracker:
            self.play(
                FadeIn(title, shift=DOWN * 0.15),
                Create(time_line),
                FadeIn(start_dot),
                FadeIn(end_dot),
                FadeIn(start_label),
                FadeIn(end_label),
                run_time=tracker.duration * 0.9,
            )

        with self.voiceover(
            text=(
                "Over ten seconds, your average speed is the distance traveled "
                "divided by ten seconds."
            )
        ) as tracker:
            self.play(
                GrowFromCenter(interval_brace),
                Write(average_fraction),
                FadeIn(average_label, shift=UP * 0.1),
                run_time=tracker.duration * 0.9,
            )

        with self.voiceover(
            text=(
                "But your speedometer answers a sharper question: how fast are "
                "you moving right now?"
            )
        ) as tracker:
            self.play(
                FadeOut(interval_brace),
                FadeOut(average_fraction),
                FadeOut(average_label),
                FadeIn(speedometer),
                FadeIn(now_label, shift=UP * 0.1),
                end_dot.animate.scale(1.5),
                run_time=tracker.duration * 0.9,
            )

        self.intro_objects = VGroup(
            title,
            time_line,
            start_dot,
            end_dot,
            start_label,
            end_label,
            speedometer,
            now_label,
        )

    def show_secant_graph(self) -> dict:
        """Beat 2: establish the graph and the average slope construction."""
        axes = Axes(
            x_range=[-1, 3.4, 1],
            y_range=[-2, 4, 1],
            x_length=7.4,
            y_length=5.4,
            tips=False,
            axis_config={"color": GREY_B, "stroke_width": 2},
        ).move_to(LEFT * 2.25 + DOWN * 0.35)
        axis_labels = axes.get_axis_labels(
            Text("x", font_size=24), Text("f(x)", font_size=24)
        )
        graph = axes.plot(
            self.curve_function,
            x_range=[-0.85, 3.25],
            color=BLUE_A,
            stroke_width=4,
        )

        p_point = axes.c2p(self.P_X, self.curve_function(self.P_X))
        p_dot = Dot(p_point, radius=0.09, color=self.P_COLOR)
        p_label = Text("P", font_size=26, color=self.P_COLOR).next_to(
            p_dot, DL, buff=0.12
        )

        with self.voiceover(text="A graph has the same distinction.") as tracker:
            self.play(
                FadeOut(self.intro_objects),
                Create(axes),
                FadeIn(axis_labels),
                Create(graph),
                FadeIn(p_dot),
                FadeIn(p_label),
                run_time=tracker.duration * 0.9,
            )

        q_x = ValueTracker(2.4)

        def secant_slope() -> float:
            q_value = q_x.get_value()
            return (self.curve_function(q_value) - self.curve_function(self.P_X)) / (
                q_value - self.P_X
            )

        q_dot = always_redraw(
            lambda: Dot(
                axes.c2p(q_x.get_value(), self.curve_function(q_x.get_value())),
                radius=0.085,
                color=self.Q_COLOR,
            )
        )
        q_label = Text("Q", font_size=25, color=self.Q_COLOR)
        q_label.add_updater(
            lambda label: label.next_to(
                axes.c2p(q_x.get_value(), self.curve_function(q_x.get_value())),
                UR,
                buff=0.1,
            )
        )
        q_label.update()
        triangle = always_redraw(
            lambda: Polygon(
                p_point,
                axes.c2p(q_x.get_value(), self.curve_function(self.P_X)),
                axes.c2p(q_x.get_value(), self.curve_function(q_x.get_value())),
                fill_color=self.DX_COLOR,
                fill_opacity=0.09,
                stroke_opacity=0,
            )
        )
        delta_x_guide = always_redraw(
            lambda: DashedLine(
                p_point,
                axes.c2p(q_x.get_value(), self.curve_function(self.P_X)),
                color=self.DX_COLOR,
                dash_length=0.09,
                stroke_width=3,
            )
        )
        delta_y_guide = always_redraw(
            lambda: DashedLine(
                axes.c2p(q_x.get_value(), self.curve_function(self.P_X)),
                axes.c2p(q_x.get_value(), self.curve_function(q_x.get_value())),
                color=self.DY_COLOR,
                dash_length=0.09,
                stroke_width=3,
            )
        )
        secant_line = always_redraw(
            lambda: self.line_with_graph_slope(
                axes,
                secant_slope(),
                color=self.LINE_COLOR,
                stroke_width=4,
            )
        )
        secant_label = Text("secant", font_size=24, color=self.LINE_COLOR)
        secant_label.add_updater(
            lambda label: label.next_to(
                axes.c2p(
                    2.35,
                    self.curve_function(self.P_X) + secant_slope() * (2.35 - self.P_X),
                ),
                UP,
                buff=0.12,
            )
        )
        secant_label.update()

        delta_x_label = MathTex(r"\Delta x", color=self.DX_COLOR, font_size=30)
        delta_y_label = MathTex(r"\Delta y", color=self.DY_COLOR, font_size=30)
        slope_fraction = MathTex(
            r"\text{average slope}=",
            r"\frac{\Delta y}{\Delta x}",
            font_size=34,
        )
        slope_fraction.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(
            RIGHT * 4.35 + UP * 1.75
        )

        slope_number = DecimalNumber(
            secant_slope(),
            num_decimal_places=2,
            font_size=38,
            color=self.LINE_COLOR,
        )
        slope_number.add_updater(lambda number: number.set_value(secant_slope()))
        slope_readout_label = Text(
            "secant slope",
            font_size=24,
            color=GREY_A,
        )
        slope_readout = (
            VGroup(slope_readout_label, slope_number)
            .arrange(DOWN, buff=0.1)
            .move_to(RIGHT * 4.35 + DOWN * 0.15)
        )

        with self.voiceover(text="Choose two points on a curve.") as tracker:
            self.play(
                FadeIn(q_dot),
                FadeIn(q_label),
                run_time=tracker.duration * 0.8,
            )

        with self.voiceover(
            text=(
                "The line through them is a secant line, and its slope measures "
                "the average rate of change between those points."
            )
        ) as tracker:
            self.play(
                FadeIn(triangle),
                Create(delta_x_guide),
                Create(delta_y_guide),
                Create(secant_line),
                FadeIn(secant_label),
                run_time=tracker.duration * 0.9,
            )

        delta_x_label.move_to(
            axes.c2p(
                (self.P_X + q_x.get_value()) / 2,
                self.curve_function(self.P_X),
            )
            + DOWN * 0.28
        )
        delta_y_label.next_to(delta_y_guide, RIGHT, buff=0.12)
        with self.voiceover(text="Change in y, divided by change in x.") as tracker:
            self.play(
                FadeIn(delta_x_label),
                FadeIn(delta_y_label),
                Write(slope_fraction),
                FadeIn(slope_readout),
                run_time=tracker.duration * 0.85,
            )

        return {
            "axes": axes,
            "axis_labels": axis_labels,
            "graph": graph,
            "p_point": p_point,
            "p_dot": p_dot,
            "p_label": p_label,
            "q_x": q_x,
            "q_dot": q_dot,
            "q_label": q_label,
            "triangle": triangle,
            "delta_x_guide": delta_x_guide,
            "delta_y_guide": delta_y_guide,
            "secant_line": secant_line,
            "secant_label": secant_label,
            "delta_x_label": delta_x_label,
            "delta_y_label": delta_y_label,
            "slope_fraction": slope_fraction,
            "slope_readout": slope_readout,
            "slope_number": slope_number,
        }

    def show_secant_to_tangent(self, state: dict):
        """Beat 3: the visual centerpiece, driven entirely by q_x."""
        q_x = state["q_x"]
        tangent_label = Text(
            "tangent (the limiting line)",
            font_size=24,
            color=self.LINE_COLOR,
        ).move_to(RIGHT * 4.35 + DOWN * 1.5)
        tangent_value = MathTex(
            r"\text{slope}\ \longrightarrow\ 0.80",
            font_size=33,
            color=self.LINE_COLOR,
        ).next_to(tangent_label, DOWN, buff=0.18)

        tangent_line = self.line_with_graph_slope(
            state["axes"],
            self.derivative_at_p(),
            color=self.LINE_COLOR,
            stroke_width=5,
        )
        tangent_line.set_z_index(2)

        with self.voiceover(
            text="Now keep the first point fixed and slide the second point closer."
        ) as tracker:
            self.play(
                FadeOut(state["delta_x_label"]),
                FadeOut(state["delta_y_label"]),
                q_x.animate.set_value(0.85),
                run_time=tracker.duration * 0.92,
                rate_func=smooth,
            )

        with self.voiceover(text="The interval shrinks.") as tracker:
            self.play(
                q_x.animate.set_value(0.42),
                run_time=tracker.duration * 0.9,
                rate_func=smooth,
            )

        with self.voiceover(
            text=(
                "The average slope describes a smaller and smaller piece of the curve."
            )
        ) as tracker:
            self.play(
                q_x.animate.set_value(0.08),
                FadeOut(state["secant_label"]),
                run_time=tracker.duration * 0.92,
                rate_func=smooth,
            )

        with self.voiceover(
            text=(
                "And the secant line turns toward one limiting position: the "
                "tangent line."
            )
        ) as tracker:
            self.play(
                q_x.animate.set_value(0.01),
                run_time=tracker.duration * 0.55,
                rate_func=smooth,
            )
            self.play(
                Create(tangent_line),
                FadeIn(tangent_label, shift=UP * 0.1),
                FadeIn(tangent_value),
                run_time=tracker.duration * 0.35,
            )

        state["tangent_line"] = tangent_line
        state["tangent_label"] = tangent_label
        state["tangent_value"] = tangent_value

    def show_zero_over_zero(self, state: dict):
        """Beat 4: direct substitution collapses to the undefined 0/0 form."""
        inset_box = RoundedRectangle(
            width=3.5,
            height=2.2,
            corner_radius=0.16,
            color=GREY_C,
            stroke_width=2,
            fill_color=BLACK,
            fill_opacity=0.25,
        ).move_to(RIGHT * 4.35 + DOWN * 0.3)
        inset_title = Text(
            "If Q is placed on P",
            font_size=23,
            color=GREY_A,
        ).next_to(inset_box.get_top(), DOWN, buff=0.18)

        mini_p = inset_box.get_center() + LEFT * 0.75 + DOWN * 0.25
        mini_corner = mini_p + RIGHT * 1.25
        mini_q = mini_corner + UP * 0.68
        mini_triangle = Polygon(
            mini_p,
            mini_corner,
            mini_q,
            fill_color=self.DX_COLOR,
            fill_opacity=0.12,
            stroke_color=GREY_B,
            stroke_width=2,
        )
        mini_dx = Line(mini_p, mini_corner, color=self.DX_COLOR, stroke_width=4)
        mini_dy = Line(mini_corner, mini_q, color=self.DY_COLOR, stroke_width=4)
        mini_q_dot = Dot(mini_q, radius=0.065, color=self.Q_COLOR)
        mini_p_dot = Dot(mini_p, radius=0.065, color=self.P_COLOR)
        mini_fraction = MathTex(r"\frac{\Delta y}{\Delta x}", font_size=34).move_to(
            inset_box.get_center() + RIGHT * 1.08 + DOWN * 0.28
        )

        with self.voiceover(
            text="We cannot simply put the two points in exactly the same place."
        ) as tracker:
            self.play(
                FadeOut(state["slope_fraction"]),
                FadeOut(state["slope_readout"]),
                FadeOut(state["tangent_label"]),
                FadeOut(state["tangent_value"]),
                FadeIn(inset_box),
                FadeIn(inset_title),
                FadeIn(mini_triangle),
                FadeIn(mini_dx),
                FadeIn(mini_dy),
                FadeIn(mini_p_dot),
                FadeIn(mini_q_dot),
                FadeIn(mini_fraction),
                run_time=tracker.duration * 0.9,
            )

        zero_fraction = MathTex(r"\frac{0}{0}", font_size=42, color=RED_C).move_to(
            mini_fraction
        )
        undefined_label = Text(
            "undefined",
            font_size=24,
            color=RED_C,
        ).next_to(zero_fraction, DOWN, buff=0.12)
        with self.voiceover(
            text=("Then both changes would be zero, giving zero divided by zero.")
        ) as tracker:
            self.play(
                mini_triangle.animate.scale(0.02, about_point=mini_p),
                mini_dx.animate.scale(0.02, about_point=mini_p),
                mini_dy.animate.scale(0.02, about_point=mini_p),
                mini_q_dot.animate.move_to(mini_p),
                Transform(mini_fraction, zero_fraction),
                run_time=tracker.duration * 0.65,
            )
            self.play(
                FadeIn(undefined_label, shift=UP * 0.1),
                run_time=tracker.duration * 0.25,
            )

        state["zero_inset"] = VGroup(
            inset_box,
            inset_title,
            mini_triangle,
            mini_dx,
            mini_dy,
            mini_p_dot,
            mini_q_dot,
            mini_fraction,
            undefined_label,
        )

    def show_limit_definition(self, state: dict):
        """Beat 5: reveal the derivative formula in meaningful stages."""
        numerator = MathTex(
            r"f(x+h)-f(x)",
            font_size=38,
            color=self.DY_COLOR,
        )
        fraction_bar = Line(LEFT * 1.65, RIGHT * 1.65, color=WHITE, stroke_width=2)
        denominator = MathTex(r"h", font_size=38, color=self.DX_COLOR)
        difference_quotient = (
            VGroup(
                numerator,
                fraction_bar,
                denominator,
            )
            .arrange(DOWN, buff=0.1)
            .move_to(RIGHT * 4.35 + UP * 0.65)
        )

        with self.voiceover(text="Instead, the derivative uses a limit.") as tracker:
            self.play(
                FadeOut(state["zero_inset"]),
                run_time=tracker.duration * 0.2,
            )
            self.play(Write(numerator), run_time=tracker.duration * 0.32)
            self.play(
                Create(fraction_bar),
                Write(denominator),
                run_time=tracker.duration * 0.32,
            )

        limit_symbol = MathTex(
            r"\lim_{h\to 0}",
            font_size=38,
        ).next_to(difference_quotient, LEFT, buff=0.18)

        moving_geometry = VGroup(
            state["q_dot"],
            state["q_label"],
            state["triangle"],
            state["delta_x_guide"],
            state["delta_y_guide"],
            state["secant_line"],
        )

        with self.voiceover(
            text=("It asks what the secant slopes approach as the gap approaches zero.")
        ) as tracker:
            self.play(
                difference_quotient.animate.shift(RIGHT * 0.38),
                FadeIn(limit_symbol, shift=RIGHT * 0.15),
                run_time=tracker.duration * 0.2,
            )
            self.play(
                Indicate(limit_symbol, color=self.Q_COLOR),
                run_time=tracker.duration * 0.12,
            )
            self.play(
                FadeOut(moving_geometry),
                run_time=tracker.duration * 0.08,
            )
            state["q_x"].set_value(0.9)
            self.play(
                FadeIn(moving_geometry),
                run_time=tracker.duration * 0.08,
            )
            self.play(
                state["q_x"].animate.set_value(0.01),
                run_time=tracker.duration * 0.45,
                rate_func=smooth,
            )

        limit_group = VGroup(limit_symbol, difference_quotient)
        derivative_name = MathTex(r"f'(x)=", font_size=38).next_to(
            limit_group, LEFT, buff=0.18
        )

        correspondence = Text(
            "derivative  =  instantaneous rate  =  tangent slope",
            font_size=23,
            color=self.LINE_COLOR,
        ).move_to(RIGHT * 4.25 + DOWN * 1.15)

        with self.voiceover(
            text=("If those slopes settle to one value, that value is the derivative.")
        ) as tracker:
            self.play(
                limit_group.animate.shift(RIGHT * 0.45),
                FadeIn(derivative_name, shift=RIGHT * 0.15),
                run_time=tracker.duration * 0.42,
            )
            self.play(
                FadeIn(correspondence, shift=UP * 0.12),
                run_time=tracker.duration * 0.42,
            )

        with self.voiceover(
            text=(
                "It captures the curve's rate of change at that exact input: "
                "the slope at an instant."
            )
        ) as tracker:
            self.play(
                Indicate(state["p_dot"], color=self.P_COLOR),
                Indicate(state["tangent_line"], color=self.LINE_COLOR),
                run_time=tracker.duration * 0.8,
            )

        state["formula"] = VGroup(derivative_name, limit_group)
        state["correspondence"] = correspondence
        state["moving_geometry"] = moving_geometry

    def show_final_distinction(self, state: dict):
        """Beat 6: a tiny interval approximates; the limit equals."""
        tiny_interval_label = Text(
            "tiny, but nonzero",
            font_size=23,
            color=self.DX_COLOR,
        ).move_to(RIGHT * 4.3 + UP * 1.25)
        approximation = MathTex(
            r"\text{secant slope}\ \approx\ f'(x)",
            font_size=36,
        ).next_to(tiny_interval_label, DOWN, buff=0.3)

        final_statement = MathTex(
            r"f'(x)=\text{tangent slope at }P",
            font_size=39,
            color=self.LINE_COLOR,
        ).move_to(RIGHT * 4.15 + UP * 0.3)

        with self.voiceover(
            text=(
                "So instantaneous slope is not measured across a tiny fixed interval."
            )
        ) as tracker:
            self.play(
                FadeOut(state["formula"]),
                FadeOut(state["correspondence"]),
                FadeOut(state["moving_geometry"]),
                run_time=tracker.duration * 0.18,
            )
            state["q_x"].set_value(0.46)
            self.play(
                FadeIn(state["moving_geometry"]),
                FadeIn(tiny_interval_label),
                Write(approximation),
                run_time=tracker.duration * 0.55,
            )

        with self.voiceover(
            text=("It is the limit of average slopes as the interval vanishes.")
        ) as tracker:
            self.play(
                state["q_x"].animate.set_value(0.01),
                run_time=tracker.duration * 0.62,
                rate_func=smooth,
            )
            self.play(
                FadeOut(tiny_interval_label),
                ReplacementTransform(approximation, final_statement),
                FadeOut(state["moving_geometry"]),
                run_time=tracker.duration * 0.3,
            )

    def line_with_graph_slope(
        self,
        axes: Axes,
        slope: float,
        color,
        stroke_width: float,
    ) -> Line:
        """Return a graph-panel line through P with the supplied math slope."""
        p_y = self.curve_function(self.P_X)
        left_x = -0.72
        right_x = 2.85
        left_y = p_y + slope * (left_x - self.P_X)
        right_y = p_y + slope * (right_x - self.P_X)
        return Line(
            axes.c2p(left_x, left_y),
            axes.c2p(right_x, right_y),
            color=color,
            stroke_width=stroke_width,
        )
