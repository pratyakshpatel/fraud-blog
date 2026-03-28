from manim import *
import numpy as np

# Consistent color palette
FRAUD = "#E05252"
LEGIT = "#52A8E0"
NEUTRAL = "#888888"
ACCENT = "#F5A623"
SOFT = "#CCCCCC"
PURPLE = "#9B59B6"
GREEN = "#2ECC71"


class OverSmoothingSquashing(Scene):
    def construct(self):
        title = Text("Over-Smoothing & Over-Squashing", font_size=28, color=WHITE).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.8)

        # === OVER-SMOOTHING ===
        # 10 nodes arranged with clear class distinction
        npos = {i: np.array([-4.0 + i * 0.9, 0.8, 0]) for i in range(10)}
        colors_init = [FRAUD] * 5 + [LEGIT] * 5
        node_c = {}
        node_labels = {}
        for i in range(10):
            node_c[i] = Circle(0.25, color=colors_init[i], fill_color=colors_init[i], fill_opacity=0.9).move_to(npos[i])
            node_labels[i] = Text(str(i), font_size=10, color=WHITE).move_to(npos[i])

        edges = [(i, i + 1) for i in range(9)]
        edge_lines = VGroup(*[Line(npos[a], npos[b], color=SOFT, stroke_width=2) for a, b in edges])
        all_nodes = VGroup(*node_c.values())
        all_labels = VGroup(*node_labels.values())

        # Class labels
        fraud_label = Text("Fraud", font_size=12, color=FRAUD).next_to(node_c[2], DOWN, buff=0.25)
        legit_label = Text("Legit", font_size=12, color=LEGIT).next_to(node_c[7], DOWN, buff=0.25)

        caption = Text(
            "Distinct classes: 5 fraud (red) vs 5 legit (blue)",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)

        self.play(
            Create(edge_lines), FadeIn(all_nodes), FadeIn(all_labels),
            FadeIn(fraud_label), FadeIn(legit_label), FadeIn(caption),
            run_time=1.0
        )
        self.wait(0.8)

        # Layer counter
        layer_label = Text("Layer: 0", font_size=16, color=SOFT).move_to(RIGHT * 5.5 + UP * 2.2)
        self.play(FadeIn(layer_label), run_time=0.5)

        # Simulate over-smoothing over multiple layers
        for layer_num, t_val in enumerate([0.2, 0.45, 0.75, 1.0], start=1):
            nc_anims = []
            for i in range(10):
                r1 = np.array(color_to_rgb(colors_init[i]))
                r2 = np.array(color_to_rgb(NEUTRAL))
                mixed = rgb_to_color(r1 + (r2 - r1) * t_val)
                nc_anims.append(node_c[i].animate.set_color(mixed).set_fill(mixed))

            new_layer = Text(f"Layer: {layer_num}", font_size=16, color=SOFT).move_to(RIGHT * 5.5 + UP * 2.2)

            self.play(*nc_anims, Transform(layer_label, new_layer), run_time=0.8)
            self.wait(0.5)

        smooth_caption = Text(
            "All nodes converge to same color — classes indistinguishable!",
            font_size=18, color=FRAUD,
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, smooth_caption), run_time=0.8)
        self.wait(1.0)

        # Clear for Over-Squashing
        self.play(
            FadeOut(VGroup(all_nodes, all_labels, edge_lines, fraud_label, legit_label, layer_label)),
            run_time=0.8
        )
        self.wait(0.5)

        # === OVER-SQUASHING ===
        n_chain = 9
        cx = {i: np.array([-4.5 + i * 1.15, 0.3, 0]) for i in range(n_chain)}
        chain_edges = VGroup(*[Line(cx[i], cx[i + 1], color=SOFT, stroke_width=2.5) for i in range(n_chain - 1)])
        chain_nodes = {}
        for i in range(n_chain):
            col = FRAUD if i == 0 else (LEGIT if i == n_chain - 1 else NEUTRAL)
            chain_nodes[i] = Circle(0.28, color=col, fill_color=col, fill_opacity=0.9).move_to(cx[i])

        src_lbl = Text("source", font_size=12, color=FRAUD).next_to(chain_nodes[0], DOWN, buff=0.12)
        tgt_lbl = Text("target", font_size=12, color=LEGIT).next_to(chain_nodes[n_chain - 1], DOWN, buff=0.12)

        squash_caption = Text(
            "Long-range: important info must travel 8 hops",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        self.play(
            Create(chain_edges), FadeIn(VGroup(*chain_nodes.values())),
            FadeIn(src_lbl), FadeIn(tgt_lbl), Transform(caption, squash_caption),
            run_time=0.8,
        )
        self.wait(0.5)

        # Signal strength bar
        signal_bar_bg = Rectangle(width=3.0, height=0.25, color=SOFT, fill_color=SOFT, fill_opacity=0.2, stroke_width=1)
        signal_bar_bg.move_to(RIGHT * 4.5 + DOWN * 1.0)
        signal_bar = Rectangle(width=3.0, height=0.25, color=ACCENT, fill_color=ACCENT, fill_opacity=0.8, stroke_width=0)
        signal_bar.move_to(signal_bar_bg.get_center())
        signal_label = Text("Signal strength", font_size=10, color=SOFT).next_to(signal_bar_bg, UP, buff=0.08)

        self.play(FadeIn(signal_bar_bg), FadeIn(signal_bar), FadeIn(signal_label), run_time=0.8)

        # Animate signal traveling and fading (squashing)
        signal = Circle(radius=0.15, color=ACCENT, fill_color=ACCENT, fill_opacity=0.9).move_to(cx[0])
        self.add(signal)

        for i in range(1, n_chain):
            new_opacity = max(0.08, 1.0 - i * 0.12)
            new_width = max(0.1, 3.0 * (1.0 - i * 0.12))
            new_bar = Rectangle(width=new_width, height=0.25, color=ACCENT, fill_color=ACCENT, fill_opacity=0.8, stroke_width=0)
            new_bar.align_to(signal_bar_bg, LEFT).move_to(signal_bar_bg.get_center(), coor_mask=[0, 1, 1])

            self.play(
                signal.animate.move_to(cx[i]).set_opacity(new_opacity),
                Transform(signal_bar, new_bar),
                run_time=0.4
            )

        squash_result = Text(
            "Signal almost gone by hop 8 — critical info lost!",
            font_size=18, color=FRAUD,
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, squash_result), run_time=0.8)
        self.wait(0.8)

        # === SOLUTIONS ===
        self.play(FadeOut(signal), FadeOut(signal_bar), FadeOut(signal_bar_bg), FadeOut(signal_label), run_time=0.5)
        self.wait(0.5)

        solutions_label = Text("Solutions", font_size=20, color=GREEN).move_to(UP * 2.2)
        self.play(FadeIn(solutions_label), run_time=0.8)

        # Solution 1: Residual connection
        sol1_caption = Text(
            "Solution 1: Residual connections (skip links)",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, sol1_caption), run_time=0.8)

        # Show skip connection from node 0 to node 4
        skip_arc = ArcBetweenPoints(cx[0] + UP * 0.3, cx[4] + UP * 0.3, angle=-TAU / 4, color=GREEN, stroke_width=3)
        skip_label = Text("skip", font_size=10, color=GREEN).move_to(cx[2] + UP * 0.9)
        self.play(Create(skip_arc), FadeIn(skip_label), run_time=0.8)
        self.wait(0.8)

        # Solution 2: Virtual super-node
        sol2_caption = Text(
            "Solution 2: Virtual super-node (shortcut hub)",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, sol2_caption), run_time=0.8)

        # Add virtual node
        virtual_pos = np.array([0.0, -1.5, 0])
        virtual_node = Circle(0.35, color=PURPLE, fill_color=PURPLE, fill_opacity=0.9).move_to(virtual_pos)
        virtual_label = Text("V", font_size=14, color=WHITE).move_to(virtual_pos)
        virtual_text = Text("virtual", font_size=10, color=PURPLE).next_to(virtual_node, DOWN, buff=0.08)

        # Edges from virtual to several nodes
        virtual_edges = VGroup(
            DashedLine(virtual_pos, cx[0], color=PURPLE, stroke_width=1.5, dash_length=0.1),
            DashedLine(virtual_pos, cx[4], color=PURPLE, stroke_width=1.5, dash_length=0.1),
            DashedLine(virtual_pos, cx[8], color=PURPLE, stroke_width=1.5, dash_length=0.1),
        )

        self.play(
            Create(virtual_edges), FadeIn(virtual_node), FadeIn(virtual_label), FadeIn(virtual_text),
            run_time=0.8
        )
        self.wait(0.8)

        # Final caption
        final_caption = Text(
            "Balance expressiveness and information flow",
            font_size=18, color=ACCENT,
        ).to_edge(DOWN, buff=0.4)

        self.play(Transform(caption, final_caption), run_time=0.8)
        self.wait(2.0)
