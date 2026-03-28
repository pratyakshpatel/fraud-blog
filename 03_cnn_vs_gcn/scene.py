from manim import *
import numpy as np

# Consistent color palette
FRAUD = "#E05252"
LEGIT = "#52A8E0"
NEUTRAL = "#888888"
ACCENT = "#F5A623"
SOFT = "#CCCCCC"
GREEN = "#2ECC71"

CNN_C = "#3A7BD5"


class CNNvsGCN(Scene):
    def construct(self):
        title = Text("CNN vs GCN: The Parallel", font_size=28, color=WHITE).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.8)

        # Divider
        divider = Line(UP * 2.8, DOWN * 2.8, color=SOFT, stroke_width=1.5)

        # Labels
        cnn_lbl = Text("CNN (Image)", font_size=20, color=CNN_C).move_to(LEFT * 3.5 + UP * 2.5)
        gcn_lbl = Text("GCN (Graph)", font_size=20, color=GREEN).move_to(RIGHT * 3.5 + UP * 2.5)

        caption = Text(
            "Both aggregate local information through learnable weights",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)

        self.play(Create(divider), FadeIn(cnn_lbl), FadeIn(gcn_lbl), FadeIn(caption), run_time=0.8)
        self.wait(0.5)

        # === CNN SIDE ===
        SIZE = 0.52
        cnn_center = LEFT * 3.5 + UP * 0.3
        cells = VGroup()
        cell_vals = VGroup()
        for r in range(5):
            for c in range(5):
                sq = Square(SIZE, color=CNN_C, fill_color=CNN_C, fill_opacity=0.15, stroke_width=1.5)
                sq.move_to(cnn_center + np.array([(c - 2.0) * SIZE, (2.0 - r) * SIZE, 0]))
                cells.add(sq)
                val = Text(f"{np.random.randint(0, 10)}", font_size=12, color=SOFT)
                val.move_to(sq.get_center())
                cell_vals.add(val)

        self.play(Create(cells), FadeIn(cell_vals), run_time=1.0)

        # Show 3x3 filter with weights
        filter_center = LEFT * 3.5 + DOWN * 2.2
        filter_box = VGroup()
        filter_vals = VGroup()
        w_matrix = [[0.1, 0.2, 0.1], [0.2, 0.4, 0.2], [0.1, 0.2, 0.1]]
        for r in range(3):
            for c in range(3):
                sq = Square(0.4, color=ACCENT, fill_color=ACCENT, fill_opacity=0.3, stroke_width=2)
                sq.move_to(filter_center + np.array([(c - 1) * 0.42, (1 - r) * 0.42, 0]))
                filter_box.add(sq)
                wt = Text(f"{w_matrix[r][c]}", font_size=10, color=WHITE)
                wt.move_to(sq.get_center())
                filter_vals.add(wt)

        w_label = Text("W (learnable)", font_size=12, color=ACCENT).next_to(VGroup(filter_box, filter_vals), DOWN, buff=0.15)
        self.play(Create(filter_box), FadeIn(filter_vals), FadeIn(w_label), run_time=0.8)
        self.wait(0.5)

        # Animate filter on grid
        def get_filter_highlight(row, col):
            highlight_cells = VGroup()
            for dr in range(3):
                for dc in range(3):
                    idx = (row + dr) * 5 + (col + dc)
                    highlight_cells.add(cells[idx].copy().set_fill(ACCENT, opacity=0.5).set_stroke(ACCENT, width=3))
            return highlight_cells

        current_highlight = get_filter_highlight(0, 0)
        self.play(FadeIn(current_highlight), run_time=0.8)

        # Show aggregation output
        agg_arrow = Arrow(cnn_center + DOWN * 1.5, cnn_center + DOWN * 1.8 + RIGHT * 0.5, color=ACCENT, stroke_width=2)
        agg_result = Circle(0.2, color=CNN_C, fill_color=CNN_C, fill_opacity=0.8).move_to(cnn_center + DOWN * 2.0 + RIGHT * 0.8)
        agg_text = Text("Σ(w·x)", font_size=14, color=WHITE).move_to(agg_result.get_center())

        # Slide filter
        positions = [(0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
        for row, col in positions:
            new_highlight = get_filter_highlight(row, col)
            self.play(Transform(current_highlight, new_highlight), run_time=0.5)

        self.play(FadeOut(current_highlight), run_time=0.5)

        fixed_note = Text("Fixed 9 inputs always", font_size=14, color=CNN_C).move_to(LEFT * 3.5 + DOWN * 1.2)
        self.play(FadeIn(fixed_note), run_time=0.8)
        self.wait(0.5)

        # === GCN SIDE ===
        gcn_center = RIGHT * 3.5 + UP * 0.3

        # Create graph with variable degree nodes
        npos = {
            0: gcn_center + np.array([0.0, 0.0, 0]),  # center hub
            1: gcn_center + np.array([0.0, 1.3, 0]),
            2: gcn_center + np.array([-1.2, 0.6, 0]),
            3: gcn_center + np.array([-1.2, -0.6, 0]),
            4: gcn_center + np.array([0.0, -1.3, 0]),
            5: gcn_center + np.array([1.2, 0.0, 0]),
        }
        # Node 0 connected to all others (degree 5)
        edges = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5)]

        edge_lines = VGroup(*[Line(npos[a], npos[b], color=SOFT, stroke_width=2) for a, b in edges])

        hub = Circle(0.35, color=GREEN, fill_color=GREEN, fill_opacity=0.9).move_to(npos[0])
        hub_lbl = Text("v", font_size=20, color=WHITE).move_to(npos[0])

        nb_circles = VGroup()
        nb_labels = VGroup()
        for i in range(1, 6):
            c = Circle(0.25, color=GREEN, fill_color=GREEN, fill_opacity=0.4).move_to(npos[i])
            nb_circles.add(c)
            lbl = Text(f"n{i}", font_size=12, color=WHITE).move_to(npos[i])
            nb_labels.add(lbl)

        self.play(Create(edge_lines), FadeIn(hub), FadeIn(hub_lbl), FadeIn(nb_circles), FadeIn(nb_labels), run_time=1.0)

        # Show arrows flowing into center
        nb_arrows = VGroup()
        for i in range(1, 6):
            direction = npos[0] - npos[i]
            direction = direction / np.linalg.norm(direction)
            start = npos[i] + direction * 0.3
            end = npos[0] - direction * 0.4
            arrow = Arrow(start, end, color=GREEN, stroke_width=3, max_tip_length_to_length_ratio=0.25)
            nb_arrows.add(arrow)

        self.play(Create(nb_arrows), run_time=0.8)

        var_note = Text("Variable inputs (here 5)", font_size=14, color=GREEN).move_to(RIGHT * 3.5 + DOWN * 1.2)
        self.play(FadeIn(var_note), run_time=0.8)
        self.wait(0.5)

        # Show weight matrix for GCN too
        gcn_w = VGroup(
            Rectangle(width=0.6, height=0.8, color=ACCENT, fill_color=ACCENT, fill_opacity=0.3, stroke_width=2),
            Text("W", font_size=16, color=WHITE)
        ).arrange(ORIGIN).move_to(RIGHT * 5.5 + DOWN * 0.5)
        gcn_w_label = Text("(learnable)", font_size=12, color=ACCENT).next_to(gcn_w, DOWN, buff=0.08)
        self.play(FadeIn(gcn_w), FadeIn(gcn_w_label), run_time=0.8)
        self.wait(0.5)

        # === COMPARISON ===
        parallel_caption = Text(
            "The key parallel: aggregate local info, then apply learned transform",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, parallel_caption), run_time=0.8)

        # Highlight boxes around both aggregations
        cnn_box = SurroundingRectangle(VGroup(cells, cell_vals), color=ACCENT, buff=0.1, stroke_width=3)
        gcn_box = SurroundingRectangle(VGroup(hub, nb_circles, edge_lines), color=ACCENT, buff=0.15, stroke_width=3)

        self.play(Create(cnn_box), Create(gcn_box), run_time=0.8)
        self.wait(0.8)

        # Show different degree example
        diff_caption = Text(
            "GCN adapts to ANY connectivity — different neighbors, different inputs",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, diff_caption), FadeOut(VGroup(cnn_box, gcn_box, nb_arrows)), run_time=0.8)
        self.wait(0.5)

        # Show a different node with only 2 neighbors
        new_hub = Circle(0.35, color=FRAUD, fill_color=FRAUD, fill_opacity=0.9).move_to(npos[1])
        self.play(
            hub.animate.set_fill(GREEN, opacity=0.4).set_stroke(GREEN),
            FadeIn(new_hub),
            run_time=0.8
        )

        # Arrow from node 0 to node 1
        direction = npos[1] - npos[0]
        direction = direction / np.linalg.norm(direction)
        single_arrow = Arrow(npos[0] + direction * 0.4, npos[1] - direction * 0.4, color=FRAUD, stroke_width=3, max_tip_length_to_length_ratio=0.25)

        deg_note = Text("This node: only 1 neighbor", font_size=14, color=FRAUD).move_to(RIGHT * 3.5 + UP * 2.0)
        self.play(Create(single_arrow), FadeIn(deg_note), run_time=0.8)
        self.wait(0.5)

        # Final caption
        final = Text(
            "CNN needs a fixed grid — GCN naturally handles any graph structure",
            font_size=18, color=ACCENT,
        ).to_edge(DOWN, buff=0.4)

        self.play(Transform(caption, final), run_time=0.8)
        self.wait(2.0)
