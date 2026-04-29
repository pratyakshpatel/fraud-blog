from manim import *
import numpy as np

# Consistent color palette
FRAUD = "#E05252"
LEGIT = "#52A8E0"
NEUTRAL = "#888888"
ACCENT = "#F5A623"
SOFT = "#CCCCCC"
GREEN = "#2ECC71"
PURPLE = "#9B59B6"


def blend_colors(colors):
    """Blend multiple colors together."""
    r, g, b = 0, 0, 0
    for c in colors:
        rgb = color_to_rgb(c)
        r += rgb[0]
        g += rgb[1]
        b += rgb[2]
    n = len(colors)
    return rgb_to_color([r / n, g / n, b / n])


class EmbeddingPropagation(Scene):
    def construct(self):
        # Graph layout
        center_pos = LEFT * 1.5
        nb_pos = {
            "A": center_pos + np.array([-2.0, 1.0, 0]),
            "B": center_pos + np.array([-2.0, -1.0, 0]),
            "C": center_pos + np.array([2.0, 0.0, 0]),
        }
        far_pos = center_pos + np.array([4.5, 0.0, 0])

        # Edges
        edge_to_A = Line(center_pos, nb_pos["A"], color=SOFT, stroke_width=2)
        edge_to_B = Line(center_pos, nb_pos["B"], color=SOFT, stroke_width=2)
        edge_to_C = Line(center_pos, nb_pos["C"], color=SOFT, stroke_width=2)
        far_edge = Line(nb_pos["C"], far_pos, color=SOFT, stroke_width=1.5, stroke_opacity=0.5)

        # Nodes
        n47 = Circle(0.4, color=LEGIT, fill_color=LEGIT, fill_opacity=0.9).move_to(center_pos)
        t47 = Text("47", font_size=16, color=WHITE).move_to(center_pos)

        nA = Circle(0.32, color=FRAUD, fill_color=FRAUD, fill_opacity=0.9).move_to(nb_pos["A"])
        tA = Text("A", font_size=14, color=WHITE).move_to(nb_pos["A"])

        nB = Circle(0.32, color=GREEN, fill_color=GREEN, fill_opacity=0.9).move_to(nb_pos["B"])
        tB = Text("B", font_size=14, color=WHITE).move_to(nb_pos["B"])

        nC = Circle(0.32, color=ACCENT, fill_color=ACCENT, fill_opacity=0.9).move_to(nb_pos["C"])
        tC = Text("C", font_size=14, color=WHITE).move_to(nb_pos["C"])

        nD = Circle(0.28, color=NEUTRAL, fill_color=NEUTRAL, fill_opacity=0.7).move_to(far_pos)
        tD = Text("D", font_size=12, color=WHITE).move_to(far_pos)

        # Feature bars representing embeddings
        def feature_bar(color, pos, label):
            bar = Rectangle(width=0.6, height=0.15, color=color, fill_color=color, fill_opacity=0.8, stroke_width=0)
            bar.move_to(pos + DOWN * 0.6)
            lbl = Text(label, font_size=10, color=SOFT).next_to(bar, DOWN, buff=0.05)
            return VGroup(bar, lbl)

        bar_47 = feature_bar(LEGIT, center_pos, "h₄₇")
        bar_A = feature_bar(FRAUD, nb_pos["A"], "hₐ")
        bar_B = feature_bar(GREEN, nb_pos["B"], "h_b")
        bar_C = feature_bar(ACCENT, nb_pos["C"], "h_c")

        caption = Text(
            "Each node has a feature vector (embedding)",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)

        self.play(
            Create(VGroup(edge_to_A, edge_to_B, edge_to_C, far_edge)),
            FadeIn(VGroup(n47, t47, nA, tA, nB, tB, nC, tC, nD, tD)),
            FadeIn(VGroup(bar_47, bar_A, bar_B, bar_C)),
            FadeIn(caption),
            run_time=0.5,
        )
        self.wait(0.4)

        # === LAYER 1 AGGREGATION ===
        layer1_caption = Text(
            "Layer 1: Node 47 aggregates neighbors' features",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)

        layer_label = Text("Layer 1", font_size=18, color=ACCENT).move_to(RIGHT * 5.0 + UP * 2.0)
        self.play(Transform(caption, layer1_caption), FadeIn(layer_label), run_time=0.5)
        self.wait(0.4)

        # Animate colored dots flowing from neighbors to center
        dots = [
            Circle(radius=0.12, color=FRAUD, fill_color=FRAUD, fill_opacity=0.9).move_to(nb_pos["A"]),
            Circle(radius=0.12, color=GREEN, fill_color=GREEN, fill_opacity=0.9).move_to(nb_pos["B"]),
            Circle(radius=0.12, color=ACCENT, fill_color=ACCENT, fill_opacity=0.9).move_to(nb_pos["C"]),
        ]
        for d in dots:
            self.add(d)

        self.play(*[MoveAlongPath(d, Line(d.get_center(), center_pos), rate_func=smooth) for d in dots], run_time=0.5)

        for d in dots:
            self.remove(d)

        # Show aggregation (average/sum)
        agg_formula = MathTex(r"h_{47}^{(1)} = \sigma\left(W \cdot \frac{1}{4}(h_{47} + h_A + h_B + h_C)\right)", font_size=18, color=SOFT)
        agg_formula.move_to(RIGHT * 3.5 + UP * 0.5)
        self.play(FadeIn(agg_formula), run_time=0.5)

        # Show W matrix transform
        w_box = VGroup(
            Rectangle(width=0.8, height=1.0, color=PURPLE, fill_color=PURPLE, fill_opacity=0.3, stroke_width=2),
            Text("W", font_size=16, color=PURPLE)
        ).arrange(ORIGIN).move_to(RIGHT * 3.5 + DOWN * 0.8)
        w_label = Text("(learnable)", font_size=10, color=PURPLE).next_to(w_box, DOWN, buff=0.08)
        self.play(FadeIn(w_box), FadeIn(w_label), run_time=0.5)

        # Update node 47's color to show blending
        blended_color_1 = blend_colors([LEGIT, FRAUD, GREEN, ACCENT])
        new_bar_47 = Rectangle(width=0.6, height=0.15, color=blended_color_1, fill_color=blended_color_1, fill_opacity=0.8, stroke_width=0)
        new_bar_47.move_to(center_pos + DOWN * 0.6)

        self.play(
            n47.animate.set_color(blended_color_1).set_fill(blended_color_1),
            Transform(bar_47[0], new_bar_47),
            run_time=0.5
        )

        self.wait(0.4)

        # === LAYER 2 ===
        layer2_caption = Text(
            "Layer 2: Neighbors ALSO updated — 47 gets 2-hop info",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        layer_label_2 = Text("Layer 2", font_size=18, color=ACCENT).move_to(RIGHT * 5.0 + UP * 2.0)

        self.play(Transform(caption, layer2_caption), Transform(layer_label, layer_label_2), run_time=0.5)
        self.wait(0.4)

        # Update formula
        new_formula = MathTex(r"h_{47}^{(2)} = \sigma\left(W \cdot \text{AGG}(h_{47}^{(1)}, h_A^{(1)}, h_B^{(1)}, h_C^{(1)})\right)", font_size=16, color=SOFT)
        new_formula.move_to(RIGHT * 3.5 + UP * 0.5)
        self.play(Transform(agg_formula, new_formula), run_time=0.5)

        # Show neighbors have also updated
        neighbor_update_note = Text("(neighbors now contain THEIR neighbors' info)", font_size=12, color=SOFT)
        neighbor_update_note.move_to(RIGHT * 3.5 + UP * 1.3)
        self.play(FadeIn(neighbor_update_note), run_time=0.5)

        # More message passing animation
        dots2 = [
            Circle(radius=0.12, color=blended_color_1, fill_color=blended_color_1, fill_opacity=0.9).move_to(nb_pos["A"]),
            Circle(radius=0.12, color=blended_color_1, fill_color=blended_color_1, fill_opacity=0.9).move_to(nb_pos["B"]),
            Circle(radius=0.12, color=blended_color_1, fill_color=blended_color_1, fill_opacity=0.9).move_to(nb_pos["C"]),
        ]
        for d in dots2:
            self.add(d)

        self.play(*[MoveAlongPath(d, Line(d.get_center(), center_pos), rate_func=smooth) for d in dots2], run_time=0.5)

        for d in dots2:
            self.remove(d)

        # Node 47 now has even more blended color
        blended_color_2 = blend_colors([blended_color_1, blended_color_1, blended_color_1, blended_color_1])
        self.play(
            n47.animate.set_color(blended_color_2).set_fill(blended_color_2),
            run_time=0.5
        )

        self.wait(0.4)

        # === NODE D IS TOO FAR ===
        far_caption = Text(
            "Node D is 4 hops away — 2 layers can't reach it!",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, far_caption), run_time=0.5)

        # Highlight node D
        d_ring = Circle(radius=0.4, color=FRAUD, stroke_width=4).move_to(far_pos)
        self.play(Create(d_ring), run_time=0.5)

        # Cross mark
        cross = VGroup(
            Line(far_pos + UP * 0.2 + LEFT * 0.2, far_pos + DOWN * 0.2 + RIGHT * 0.2, color=FRAUD, stroke_width=4),
            Line(far_pos + UP * 0.2 + RIGHT * 0.2, far_pos + DOWN * 0.2 + LEFT * 0.2, color=FRAUD, stroke_width=4),
        )
        self.play(Create(cross), run_time=0.5)

        # Show distance
        dist_label = Text("4 hops away", font_size=12, color=FRAUD).next_to(nD, DOWN, buff=0.4)
        self.play(FadeIn(dist_label), run_time=0.5)
        self.wait(0.4)

        # Final caption
        final = Text(
            "k layers = k hops of information flow",
            font_size=18, color=ACCENT,
        ).to_edge(DOWN, buff=0.4)

        self.play(Transform(caption, final), run_time=0.5)
        self.wait(0.4)
