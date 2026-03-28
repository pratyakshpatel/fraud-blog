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
        title = Text("The Adjacency Matrix", font_size=28, color=WHITE).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.8)

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
            run_time=1.0,
        )
        self.wait(0.8)

        # Track edges
        edge_lines = {}
        degree_counts = {i: 0 for i in range(N)}

        # Degree panel
        degree_panel = VGroup(
            Text("Degrees:", font_size=14, color=ACCENT)
        ).move_to(RIGHT * 5.0 + UP * 1.0)
        degree_texts = {}
        for i in range(N):
            dt = Text(f"{names[i]}: 0", font_size=12, color=SOFT)
            degree_texts[i] = dt
        deg_list = VGroup(*degree_texts.values()).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        deg_list.next_to(degree_panel, DOWN, buff=0.15)
        self.play(FadeIn(degree_panel), FadeIn(deg_list), run_time=0.8)

        def add_edge(a, b):
            """Add edge and update matrix."""
            # Draw edge on graph
            line = Line(npos[a], npos[b], color=LEGIT, stroke_width=2.5)
            edge_lines[(a, b)] = line

            # Update matrix cells
            new_ab = Text("1", font_size=18, color=ACCENT).move_to(cell_pos(a, b))
            new_ba = Text("1", font_size=18, color=ACCENT).move_to(cell_pos(b, a))

            # Update degrees
            degree_counts[a] += 1
            degree_counts[b] += 1

            new_deg_a = Text(f"{names[a]}: {degree_counts[a]}", font_size=12, color=ACCENT)
            new_deg_b = Text(f"{names[b]}: {degree_counts[b]}", font_size=12, color=ACCENT)
            new_deg_a.move_to(degree_texts[a].get_center())
            new_deg_b.move_to(degree_texts[b].get_center())

            self.play(
                Create(line),
                Transform(cell_texts[(a, b)], new_ab),
                Transform(cell_texts[(b, a)], new_ba),
                cells[(a, b)].animate.set_fill(ACCENT, opacity=0.4),
                cells[(b, a)].animate.set_fill(ACCENT, opacity=0.4),
                Transform(degree_texts[a], new_deg_a),
                Transform(degree_texts[b], new_deg_b),
                run_time=0.8,
            )
            self.play(
                cells[(a, b)].animate.set_fill(NEUTRAL, opacity=0.1),
                cells[(b, a)].animate.set_fill(NEUTRAL, opacity=0.1),
                run_time=0.5,
            )

        # Add edges one by one
        edge_caption = Text(
            "Each edge creates symmetric 1s — undirected graph",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, edge_caption), run_time=0.8)
        self.wait(0.5)

        add_edge(0, 1)  # A-B
        add_edge(0, 2)  # A-C
        add_edge(1, 3)  # B-D
        add_edge(2, 3)  # C-D

        self.wait(0.8)

        # === MATRIX-VECTOR MULTIPLICATION ===
        ax_caption = Text(
            "Matrix × vector: (Ax)_i = sum of neighbor values",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, ax_caption), run_time=0.8)
        self.wait(0.5)

        # Show x vector
        x_vals = ["1", "2", "3", "4"]
        x_col = VGroup()
        for i, v in enumerate(x_vals):
            txt = Text(v, font_size=16, color=GREEN).move_to(cell_pos(i, N + 0.8))
            x_col.add(txt)
        x_label = Text("x", font_size=18, color=GREEN, weight=BOLD).move_to(cell_pos(-0.7, N + 0.8))
        times_sign = MathTex(r"\times", font_size=24, color=SOFT).move_to(cell_pos(1.5, N + 0.3))

        self.play(FadeIn(x_col), FadeIn(x_label), FadeIn(times_sign), run_time=0.8)

        # Highlight row A (index 0)
        row_highlight = VGroup(*[cells[(0, c)].copy().set_fill(ACCENT, opacity=0.5).set_stroke(ACCENT, width=3) for c in range(N)])
        self.play(FadeIn(row_highlight), run_time=0.8)

        # Show computation for row A
        comp_text = MathTex(r"(Ax)_A = 0 \cdot 1 + 1 \cdot 2 + 1 \cdot 3 + 0 \cdot 4 = 5", font_size=18, color=ACCENT)
        comp_text.move_to(DOWN * 1.8)
        self.play(FadeIn(comp_text), run_time=0.8)

        neighbor_note = Text(
            "= x_B + x_C (neighbors of A)",
            font_size=16, color=ACCENT,
        ).next_to(comp_text, DOWN, buff=0.15)
        self.play(FadeIn(neighbor_note), run_time=0.8)

        self.wait(1.0)

        # Final caption
        final = Text(
            "Ax aggregates neighbor values — the core GNN operation!",
            font_size=18, color=ACCENT,
        ).to_edge(DOWN, buff=0.4)

        self.play(Transform(caption, final), run_time=0.8)
        self.wait(2.0)
