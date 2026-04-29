from manim import *
import numpy as np

# Consistent color palette
FRAUD = "#E05252"
LEGIT = "#52A8E0"
NEUTRAL = "#666666"
ACCENT = "#F5A623"
SOFT = "#CCCCCC"
GREEN = "#2ECC71"


class AdjacencyMatrix(Scene):
    def construct(self):
        N = 4
        names = ["A", "B", "C", "D"]

        # Graph positions
        npos = {
            0: np.array([-5.0, 1.0, 0]),   # A
            1: np.array([-5.0, -0.6, 0]),  # B
            2: np.array([-3.4, 1.0, 0]),   # C
            3: np.array([-3.4, -0.6, 0]),  # D
        }

        # Create nodes
        node_circles = {}
        node_labels = {}
        for i, p in npos.items():
            c = Circle(0.3, color=LEGIT, fill_color=LEGIT, fill_opacity=0.75).move_to(p)
            t = Text(names[i], font_size=18, color=WHITE).move_to(p)
            node_circles[i] = c
            node_labels[i] = t

        graph_lbl = Text("Graph", font_size=18, color=SOFT).move_to(LEFT * 4.2 + UP * 2.0)
        mat_lbl = Text("Adjacency Matrix A", font_size=18, color=SOFT).move_to(RIGHT * 1.5 + UP * 2.0)

        # Matrix setup
        CELL = 0.65
        MAT_ORIGIN = RIGHT * 1.0 + UP * 0.7

        def cell_pos(r, c):
            return MAT_ORIGIN + np.array([c * CELL, -r * CELL, 0])

        cells = {}
        cell_texts = {}
        for r in range(N):
            for c in range(N):
                sq = Square(CELL, color=SOFT, fill_color=NEUTRAL, fill_opacity=0.1, stroke_width=1.5).move_to(cell_pos(r, c))
                cells[(r, c)] = sq
                t = Text("0", font_size=18, color=SOFT).move_to(cell_pos(r, c))
                cell_texts[(r, c)] = t

        row_labels = VGroup(*[Text(names[i], font_size=16, color=LEGIT).move_to(cell_pos(i, -0.7)) for i in range(N)])
        col_labels = VGroup(*[Text(names[j], font_size=16, color=LEGIT).move_to(cell_pos(-0.7, j)) for j in range(N)])

        caption = Text(
            "A_ij = 1 if nodes i and j are connected, 0 otherwise",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)

        self.play(
            FadeIn(graph_lbl), FadeIn(mat_lbl),
            FadeIn(VGroup(*node_circles.values(), *node_labels.values())),
            Create(VGroup(*cells.values())), FadeIn(VGroup(*cell_texts.values())),
            FadeIn(row_labels), FadeIn(col_labels), FadeIn(caption),
            run_time=0.5,
        )
        self.wait(0.4)

        # Track edges
        edge_lines = {}

        def add_edge(a, b, weight="1", directed=False):
            """Add edge and update matrix."""
            # Draw edge on graph
            line = (
                Arrow(npos[a], npos[b], buff=0.32, color=GREEN, stroke_width=2.5, max_tip_length_to_length_ratio=0.16)
                if directed
                else Line(npos[a], npos[b], color=LEGIT, stroke_width=2.5)
            )
            edge_lines[(a, b)] = line

            # Update matrix cells
            new_ab = Text(weight, font_size=18, color=ACCENT).move_to(cell_pos(a, b))
            new_ba = Text(weight, font_size=18, color=ACCENT).move_to(cell_pos(b, a))

            anims = [
                Create(line),
                Transform(cell_texts[(a, b)], new_ab),
                cells[(a, b)].animate.set_fill(ACCENT, opacity=0.4),
            ]
            if directed:
                anims.append(cells[(b, a)].animate.set_fill(GREEN, opacity=0.25))
            else:
                anims.extend([
                    Transform(cell_texts[(b, a)], new_ba),
                    cells[(b, a)].animate.set_fill(ACCENT, opacity=0.4),
                ])
            self.play(*anims, run_time=0.5)
            reset = [cells[(a, b)].animate.set_fill(NEUTRAL, opacity=0.1)]
            if not directed:
                reset.append(cells[(b, a)].animate.set_fill(NEUTRAL, opacity=0.1))
            self.play(*reset, run_time=0.34)

        # Start with one edge so Ax is visually easy to read.
        edge_caption = Text(
            "Add edge A-B: both symmetric cells become 1",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, edge_caption), run_time=0.5)
        self.wait(0.4)

        add_edge(0, 1)  # A-B

        # === MATRIX-VECTOR MULTIPLICATION ===
        ax_caption = Text(
            "Matrix × vector: (Ax)_i = sum of neighbor values",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, ax_caption), run_time=0.5)
        self.wait(0.4)

        # Show x vector
        x_vals = ["1", "2", "3", "4"]
        x_col = VGroup()
        for i, v in enumerate(x_vals):
            txt = Text(v, font_size=16, color=GREEN).move_to(cell_pos(i, N + 0.8))
            x_col.add(txt)
        x_label = Text("x", font_size=18, color=GREEN, weight=BOLD).move_to(cell_pos(-0.7, N + 0.8))
        times_sign = MathTex(r"\times", font_size=24, color=SOFT).move_to(cell_pos(1.5, N + 0.3))

        self.play(FadeIn(x_col), FadeIn(x_label), FadeIn(times_sign), run_time=0.5)

        # Highlight row A (index 0)
        row_highlight = VGroup(*[cells[(0, c)].copy().set_fill(ACCENT, opacity=0.5).set_stroke(ACCENT, width=3) for c in range(N)])
        self.play(FadeIn(row_highlight), run_time=0.5)

        # Show computation for row A
        comp_text = MathTex(r"(Ax)_A = 0 \cdot 1 + 1 \cdot 2 + 0 \cdot 3 + 0 \cdot 4 = 2", font_size=18, color=ACCENT)
        comp_text.move_to(DOWN * 1.8)
        self.play(FadeIn(comp_text), run_time=0.5)

        neighbor_note = Text(
            "= x_B (A's only neighbor)",
            font_size=16, color=ACCENT,
        ).next_to(comp_text, DOWN, buff=0.15)
        self.play(FadeIn(neighbor_note), run_time=0.5)

        self.wait(0.32)

        more_edges_caption = Text(
            "Add more edges: row A collects every connected neighbor",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, more_edges_caption), FadeOut(row_highlight), run_time=0.5)
        add_edge(0, 2)  # A-C
        add_edge(1, 3)  # B-D
        add_edge(2, 3)  # C-D

        row_highlight = VGroup(*[cells[(0, c)].copy().set_fill(ACCENT, opacity=0.5).set_stroke(ACCENT, width=3) for c in range(N)])
        new_comp = MathTex(r"(Ax)_A = x_B + x_C = 2 + 3 = 5", font_size=18, color=ACCENT).move_to(DOWN * 1.8)
        new_note = Text("Matrix multiplication is neighbor aggregation", font_size=16, color=ACCENT).next_to(new_comp, DOWN, buff=0.15)
        self.play(FadeIn(row_highlight), Transform(comp_text, new_comp), Transform(neighbor_note, new_note), run_time=0.5)
        self.wait(0.4)

        directed_caption = Text(
            "Weighted directed edge: only one matrix cell changes",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, directed_caption), FadeOut(row_highlight), run_time=0.5)
        add_edge(3, 0, weight="2.5", directed=True)
        self.wait(0.32)

        # Final caption
        final = Text(
            "Ax aggregates neighbor values — the core GNN operation!",
            font_size=18, color=ACCENT,
        ).to_edge(DOWN, buff=0.4)

        self.play(Transform(caption, final), run_time=0.5)
        self.wait(0.4)
