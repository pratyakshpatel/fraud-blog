from manim import *
import numpy as np

# Consistent color palette
FRAUD = "#E05252"
LEGIT = "#52A8E0"
NEUTRAL = "#888888"
ACCENT = "#F5A623"
SOFT = "#CCCCCC"
GREEN = "#2ECC71"


class ImageVsGraph(Scene):
    def construct(self):
        # === IMAGE GRID STRUCTURE ===
        title = Text("Images vs Graphs", font_size=28, color=WHITE).to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.8)

        # Create 5x5 grid for better CNN demonstration
        SIZE = 0.55
        cells = VGroup()
        nums = VGroup()
        grid_center = LEFT * 3.5
        for r in range(5):
            for c in range(5):
                sq = Square(SIZE, color=LEGIT, fill_color=LEGIT, fill_opacity=0.2, stroke_width=2)
                sq.move_to(grid_center + np.array([(c - 2) * SIZE, (2 - r) * SIZE, 0]))
                cells.add(sq)
                n = Text(str(r * 5 + c + 1), font_size=14, color=WHITE)
                n.move_to(sq.get_center())
                nums.add(n)

        grid = VGroup(cells, nums)
        img_label = Text("Image (5×5 pixels)", font_size=18, color=LEGIT).next_to(grid, UP, buff=0.3)

        caption = Text(
            "Every pixel has exactly 8 neighbors in the same arrangement",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)

        self.play(Create(cells), Write(nums), FadeIn(img_label), FadeIn(caption), run_time=1.2)
        self.wait(0.8)

        # 3x3 filter demonstration
        filter_caption = Text(
            "A 3×3 filter slides across — fixed neighborhood at every position",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, filter_caption), run_time=0.8)
        self.wait(0.5)

        # Highlight 3x3 region
        def get_filter_rect(row, col):
            group = VGroup(*[cells[r * 5 + c] for r in range(row, row + 3) for c in range(col, col + 3)])
            return SurroundingRectangle(group, color=ACCENT, buff=0, stroke_width=4)

        fbox = get_filter_rect(0, 0)
        # Show aggregation dots
        agg_dots = VGroup()
        for r in range(3):
            for c in range(3):
                dot = Dot(radius=0.06, color=ACCENT).move_to(cells[r * 5 + c].get_center())
                agg_dots.add(dot)

        self.play(Create(fbox), FadeIn(agg_dots), run_time=0.8)

        # Fixed 9 neighbors annotation
        fixed_label = Text("Always 9 inputs", font_size=14, color=ACCENT).next_to(fbox, RIGHT, buff=0.2)
        self.play(FadeIn(fixed_label), run_time=0.8)

        # Slide filter across grid
        for row, col in [(0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]:
            new_fbox = get_filter_rect(row, col)
            new_dots = VGroup()
            for r in range(row, row + 3):
                for c in range(col, col + 3):
                    dot = Dot(radius=0.06, color=ACCENT).move_to(cells[r * 5 + c].get_center())
                    new_dots.add(dot)
            self.play(
                Transform(fbox, new_fbox),
                Transform(agg_dots, new_dots),
                fixed_label.animate.next_to(new_fbox, RIGHT, buff=0.2),
                run_time=0.5,
                rate_func=smooth
            )

        self.wait(0.5)
        self.play(FadeOut(VGroup(fbox, agg_dots, fixed_label)), run_time=0.8)

        # === GRAPH STRUCTURE (side by side) ===
        # Keep grid on left, show graph on right
        self.play(grid.animate.scale(0.7).move_to(LEFT * 4.5 + UP * 0.5), img_label.animate.scale(0.7).move_to(LEFT * 4.5 + UP * 2.2), run_time=1.0)
        self.wait(0.5)

        graph_center = RIGHT * 2.0
        npos = {
            0: graph_center + np.array([-2.2, 0.8, 0]),
            1: graph_center + np.array([-0.8, 1.5, 0]),
            2: graph_center + np.array([-0.8, -0.8, 0]),
            3: graph_center + np.array([0.8, 0.8, 0]),
            4: graph_center + np.array([0.8, -1.0, 0]),
            5: graph_center + np.array([2.2, 0.0, 0]),
        }
        edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 4), (3, 4), (3, 5), (4, 5)]

        edge_lines = VGroup(*[Line(npos[a], npos[b], color=SOFT, stroke_width=2) for a, b in edges])
        node_grp = {}
        for i, p in npos.items():
            circ = Circle(0.28, color=NEUTRAL, fill_color=NEUTRAL, fill_opacity=0.85).move_to(p)
            ltext = Text(str(i + 1), font_size=18, color=WHITE).move_to(p)
            node_grp[i] = VGroup(circ, ltext)

        all_nodes = VGroup(*node_grp.values())
        graph_label = Text("Graph (6 nodes)", font_size=18, color=GREEN).move_to(graph_center + UP * 2.2)

        graph_caption = Text(
            "No fixed grid — each node has a different number of neighbors",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)

        self.play(
            Create(edge_lines),
            FadeIn(all_nodes),
            FadeIn(graph_label),
            Transform(caption, graph_caption),
            run_time=1.0
        )
        self.wait(1.0)

        # Highlight variable neighborhood
        var_caption = Text(
            "Node 2 has 3 neighbors, Node 6 has only 2",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, var_caption), run_time=0.8)

        # Highlight node 2's neighborhood
        ring1 = Circle(radius=0.4, color=ACCENT, stroke_width=4).move_to(npos[1])
        nb_arrows1 = VGroup(*[
            Arrow(npos[j], npos[1], buff=0.3, color=ACCENT, stroke_width=3, max_tip_length_to_length_ratio=0.2)
            for j in [0, 2, 3]
        ])
        self.play(Create(ring1), Create(nb_arrows1), run_time=1.0)
        self.wait(0.8)

        # Then node 6's neighborhood (only 2 neighbors)
        ring2 = Circle(radius=0.4, color=GREEN, stroke_width=4).move_to(npos[5])
        nb_arrows2 = VGroup(*[
            Arrow(npos[j], npos[5], buff=0.3, color=GREEN, stroke_width=3, max_tip_length_to_length_ratio=0.2)
            for j in [3, 4]
        ])
        self.play(Create(ring2), Create(nb_arrows2), run_time=1.0)
        self.wait(0.8)

        self.play(FadeOut(VGroup(ring1, ring2, nb_arrows1, nb_arrows2)), run_time=0.8)
        self.wait(0.5)

        # === PERMUTATION INVARIANCE ===
        perm_caption = Text(
            "Relabel nodes — the graph structure is identical",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, perm_caption), run_time=0.8)

        # Show relabeling with animation
        remap = {0: "4", 1: "1", 2: "6", 3: "2", 4: "5", 5: "3"}
        new_labels = []
        for i, vg in node_grp.items():
            new_t = Text(remap[i], font_size=18, color=ACCENT).move_to(npos[i])
            new_labels.append(Transform(vg[1], new_t))
            new_labels.append(vg[0].animate.set_stroke(ACCENT, width=3))

        self.play(*new_labels, run_time=1.0)
        self.wait(0.8)

        # Final caption
        final_caption = Text(
            "Model must produce the same output regardless of node numbering",
            font_size=18, color=ACCENT,
        ).to_edge(DOWN, buff=0.4)

        self.play(Transform(caption, final_caption), run_time=0.8)
        self.wait(2.0)
