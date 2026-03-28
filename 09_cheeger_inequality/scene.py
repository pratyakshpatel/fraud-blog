from manim import *
import numpy as np

# Consistent color palette
FRAUD = "#E05252"
LEGIT = "#52A8E0"
NEUTRAL = "#888888"
ACCENT = "#F5A623"
SOFT = "#CCCCCC"
GREEN = "#2ECC71"


def cluster_nodes(n, cx, cy, radius=1.0, seed=0):
    """Generate node positions in a circular cluster."""
    np.random.seed(seed)
    positions = []
    for i in range(n):
        angle = 2 * np.pi * i / n
        r = radius * (0.75 + 0.25 * np.random.rand())
        positions.append(np.array([cx + r * np.cos(angle), cy + r * np.sin(angle), 0]))
    return positions


class CheegerInequality(Scene):
    def construct(self):
        title = Text("Cheeger's Inequality", font_size=28, color=WHITE).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.8)

        # Cheeger's inequality formula
        formula = MathTex(r"\frac{h^2}{2} \;\leq\; \lambda_2 \;\leq\; 2h", font_size=26, color=SOFT).next_to(title, DOWN, buff=0.25)
        formula_meaning = Text("(h = Cheeger constant = min cut ratio)", font_size=12, color=ACCENT).next_to(formula, DOWN, buff=0.1)
        self.play(FadeIn(formula), FadeIn(formula_meaning), run_time=0.8)
        self.wait(0.5)

        # Two clusters
        n = 12
        left_pos = cluster_nodes(n, -3.5, 0.0, radius=1.1, seed=1)
        right_pos = cluster_nodes(n, 3.5, 0.0, radius=1.1, seed=2)

        left_dots = VGroup(*[Circle(0.12, color=LEGIT, fill_color=LEGIT, fill_opacity=0.85).move_to(p) for p in left_pos])
        right_dots = VGroup(*[Circle(0.12, color=FRAUD, fill_color=FRAUD, fill_opacity=0.85).move_to(p) for p in right_pos])

        def ring_edges(positions, color):
            edges = VGroup()
            for i in range(len(positions)):
                edges.add(Line(positions[i], positions[(i + 1) % len(positions)], color=color, stroke_width=1.8))
            # Add some internal edges
            for i in range(0, len(positions), 3):
                j = (i + len(positions) // 2) % len(positions)
                edges.add(Line(positions[i], positions[j], color=color, stroke_width=1.2))
            return edges

        left_edges = ring_edges(left_pos, LEGIT)
        right_edges = ring_edges(right_pos, FRAUD)

        # Single bridge edge
        bridge_line = Line(left_pos[3], right_pos[9], color=ACCENT, stroke_width=4)

        caption = Text(
            "Two dense clusters connected by a single edge",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)

        self.play(
            Create(left_edges), Create(right_edges),
            FadeIn(left_dots), FadeIn(right_dots),
            Create(bridge_line), FadeIn(caption),
            run_time=1.0,
        )
        self.wait(0.5)

        # Metrics panel
        panel = VGroup(
            Text("Metrics:", font_size=16, color=ACCENT),
        ).move_to(RIGHT * 5.2 + UP * 1.5)

        h_label = Text("h = ", font_size=14, color=SOFT)
        h_val = DecimalNumber(1 / n, num_decimal_places=3, font_size=14, color=GREEN)
        h_row = VGroup(h_label, h_val).arrange(RIGHT, buff=0.1)

        l2_label = Text("λ₂ = ", font_size=14, color=SOFT)
        l2_val = DecimalNumber(0.04, num_decimal_places=3, font_size=14, color=LEGIT)
        l2_row = VGroup(l2_label, l2_val).arrange(RIGHT, buff=0.1)

        metrics = VGroup(h_row, l2_row).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        metrics.next_to(panel, DOWN, buff=0.2)

        self.play(FadeIn(panel), FadeIn(metrics), run_time=0.8)
        self.wait(0.5)

        # Explain Cheeger constant
        h_caption = Text(
            "h = edges cut / min(|S|, |V-S|) = 1/12 — easy to cut!",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, h_caption), run_time=0.8)

        # Highlight the cut
        cut_line = DashedLine(
            ORIGIN + UP * 2.5, ORIGIN + DOWN * 2.5,
            color=ACCENT, stroke_width=3, dash_length=0.15
        )
        cut_label = Text("cut", font_size=14, color=ACCENT).next_to(cut_line, UP, buff=0.1)
        self.play(Create(cut_line), FadeIn(cut_label), run_time=0.8)
        self.wait(0.8)

        # === ADD MORE BRIDGES ===
        bridge_caption = Text(
            "Add cross-edges — cutting gets harder, both h and λ₂ rise",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, bridge_caption), FadeOut(VGroup(cut_line, cut_label)), run_time=0.8)
        self.wait(0.5)

        # Extra bridge edges
        extra_bridges = [
            (left_pos[0], right_pos[0]),
            (left_pos[6], right_pos[6]),
            (left_pos[9], right_pos[3]),
        ]
        h_series = [2 / n, 3 / n, 4 / n]
        l2_series = [0.10, 0.18, 0.28]

        bridge_lines = [bridge_line]
        for i, ((a, b), hv, l2v) in enumerate(zip(extra_bridges, h_series, l2_series)):
            new_bridge = Line(a, b, color=ACCENT, stroke_width=3)
            bridge_lines.append(new_bridge)

            self.play(
                Create(new_bridge),
                ChangeDecimalToValue(h_val, round(hv, 3)),
                ChangeDecimalToValue(l2_val, round(l2v, 3)),
                run_time=0.8
            )

        self.wait(0.8)

        # === SHOW INEQUALITY BOUNDS ===
        bounds_caption = Text(
            "λ₂ always stays within the Cheeger bounds",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, bounds_caption), run_time=0.8)

        # Create a visual bounds diagram
        bound_center = RIGHT * 0.0 + DOWN * 1.8
        h_current = 4 / n

        lower_bound = h_current ** 2 / 2
        upper_bound = 2 * h_current
        l2_current = 0.28

        # Number line
        num_line = Line(bound_center + LEFT * 2.5, bound_center + RIGHT * 2.5, color=SOFT, stroke_width=2)
        num_labels = VGroup(
            Text("0", font_size=12, color=SOFT).move_to(bound_center + LEFT * 2.5 + DOWN * 0.25),
            Text("0.5", font_size=12, color=SOFT).move_to(bound_center + DOWN * 0.25),
            Text("1.0", font_size=12, color=SOFT).move_to(bound_center + RIGHT * 2.5 + DOWN * 0.25),
        )

        self.play(Create(num_line), FadeIn(num_labels), run_time=0.8)

        # Mark bounds
        scale = 5.0  # 0-1 maps to -2.5 to +2.5
        lower_x = bound_center + LEFT * 2.5 + RIGHT * lower_bound * scale
        upper_x = bound_center + LEFT * 2.5 + RIGHT * upper_bound * scale
        l2_x = bound_center + LEFT * 2.5 + RIGHT * l2_current * scale

        lower_mark = Line(lower_x + UP * 0.15, lower_x + DOWN * 0.15, color=GREEN, stroke_width=4)
        lower_label = MathTex(r"\frac{h^2}{2}", font_size=14, color=GREEN).next_to(lower_mark, UP, buff=0.1)

        upper_mark = Line(upper_x + UP * 0.15, upper_x + DOWN * 0.15, color=FRAUD, stroke_width=4)
        upper_label = MathTex(r"2h", font_size=14, color=FRAUD).next_to(upper_mark, UP, buff=0.1)

        l2_dot = Circle(radius=0.1, color=ACCENT, fill_color=ACCENT, fill_opacity=0.9).move_to(l2_x)
        l2_label = MathTex(r"\lambda_2", font_size=14, color=ACCENT).next_to(l2_dot, DOWN, buff=0.15)

        # Valid region
        valid_region = Rectangle(
            width=upper_x[0] - lower_x[0], height=0.25,
            color=GREEN, fill_color=GREEN, fill_opacity=0.2, stroke_width=0
        ).move_to((lower_x + upper_x) / 2)

        self.play(
            Create(valid_region),
            Create(lower_mark), FadeIn(lower_label),
            Create(upper_mark), FadeIn(upper_label),
            FadeIn(l2_dot), FadeIn(l2_label),
            run_time=1.0
        )
        self.wait(0.5)

        # Final caption
        final = Text(
            "Eigenvalues = cheap proxy for how hard a graph is to cut",
            font_size=18, color=ACCENT,
        ).to_edge(DOWN, buff=0.4)

        self.play(Transform(caption, final), run_time=0.8)
        self.wait(2.0)
