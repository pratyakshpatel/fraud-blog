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

        caption = Text(
            "Distinct classes: 5 fraud (red) vs 5 legit (blue)",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)

        self.play(
            Create(edge_lines), FadeIn(all_nodes), FadeIn(all_labels),
            FadeIn(caption),
            run_time=0.5
        )
        self.wait(0.4)

        # Simulate over-smoothing over multiple layers
        for layer_num, t_val in enumerate([0.2, 0.45, 0.75, 1.0], start=1):
            nc_anims = []
            for i in range(10):
                r1 = np.array(color_to_rgb(colors_init[i]))
                r2 = np.array(color_to_rgb(NEUTRAL))
                mixed = rgb_to_color(r1 + (r2 - r1) * t_val)
                nc_anims.append(node_c[i].animate.set_color(mixed).set_fill(mixed))

            self.play(*nc_anims, run_time=0.5)
            self.wait(0.4)

        smooth_caption = Text(
            "All nodes converge to same color — classes indistinguishable!",
            font_size=18, color=FRAUD,
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, smooth_caption), run_time=0.5)
        self.wait(0.32)

        residual_caption = Text(
            "Residual connections keep part of the original identity",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        residual_anims = []
        for i in range(10):
            base = np.array(color_to_rgb(colors_init[i]))
            gray = np.array(color_to_rgb(NEUTRAL))
            preserved = rgb_to_color(base + (gray - base) * 0.35)
            residual_anims.append(node_c[i].animate.set_color(preserved).set_fill(preserved))
        skip_arcs = VGroup(*[
            ArcBetweenPoints(npos[i] + UP * 0.3, npos[i + 2] + UP * 0.3, angle=-TAU / 5, color=GREEN, stroke_width=2)
            for i in range(0, 8, 2)
        ])
        self.play(Transform(caption, residual_caption), Create(skip_arcs, lag_ratio=0.1), *residual_anims, run_time=0.5)
        self.wait(0.4)

        # Clear for Over-Squashing
        self.play(
            FadeOut(VGroup(all_nodes, all_labels, edge_lines, skip_arcs)),
            run_time=0.5
        )
        self.wait(0.4)

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
            run_time=0.5,
        )
        self.wait(0.4)

        # Animate signal traveling and fading (squashing)
        signal = Circle(radius=0.15, color=ACCENT, fill_color=ACCENT, fill_opacity=0.9).move_to(cx[0])
        self.add(signal)

        for i in range(1, n_chain):
            new_opacity = max(0.08, 1.0 - i * 0.12)

            self.play(
                signal.animate.move_to(cx[i]).set_opacity(new_opacity),
                run_time=0.5
            )

        squash_result = Text(
            "Signal almost gone by hop 8 — critical info lost!",
            font_size=18, color=FRAUD,
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, squash_result), run_time=0.5)
        self.wait(0.4)

        # === SOLUTION ===
        self.play(FadeOut(signal), run_time=0.34)
        self.wait(0.4)

        sol_caption = Text(
            "Virtual node creates a shortcut: source to hub to target",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, sol_caption), run_time=0.5)

        # Add virtual node
        virtual_pos = np.array([0.0, -1.5, 0])
        virtual_node = Circle(0.35, color=PURPLE, fill_color=PURPLE, fill_opacity=0.9).move_to(virtual_pos)
        virtual_label = Text("V", font_size=14, color=WHITE).move_to(virtual_pos)

        # Edges from virtual to several nodes
        virtual_edges = VGroup(
            DashedLine(virtual_pos, cx[0], color=PURPLE, stroke_width=1.5, dash_length=0.1),
            DashedLine(virtual_pos, cx[4], color=PURPLE, stroke_width=1.5, dash_length=0.1),
            DashedLine(virtual_pos, cx[8], color=PURPLE, stroke_width=1.5, dash_length=0.1),
        )

        self.play(
            Create(virtual_edges), FadeIn(virtual_node), FadeIn(virtual_label),
            run_time=0.5
        )
        self.wait(0.4)

        # Final caption
        final_caption = Text(
            "Balance expressiveness and information flow",
            font_size=18, color=ACCENT,
        ).to_edge(DOWN, buff=0.4)

        self.play(Transform(caption, final_caption), run_time=0.5)
        self.wait(0.4)
