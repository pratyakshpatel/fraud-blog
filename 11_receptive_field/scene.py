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

HOP_COLORS = [FRAUD, ACCENT, "#FFE066", GREEN]  # 0-hop (target), 1-hop, 2-hop, 3-hop


class ReceptiveField(Scene):
    def construct(self):
        np.random.seed(3)

        # Create a graph with clear hop structure
        # Center node (target) surrounded by 1-hop, 2-hop, 3-hop neighbors
        npos = {0: np.array([0, 0, 0])}  # Target node at center

        # 1-hop neighbors (4 nodes)
        for i in range(4):
            angle = np.pi / 2 + 2 * np.pi * i / 4
            npos[i + 1] = np.array([1.4 * np.cos(angle), 1.4 * np.sin(angle), 0])

        # 2-hop neighbors (6 nodes)
        for i in range(6):
            angle = 2 * np.pi * i / 6
            npos[i + 5] = np.array([2.6 * np.cos(angle), 2.6 * np.sin(angle), 0])

        # 3-hop neighbors (4 nodes at corners)
        for i in range(4):
            angle = np.pi / 4 + np.pi / 2 * i
            npos[i + 11] = np.array([3.8 * np.cos(angle), 3.8 * np.sin(angle), 0])

        # Edges connecting hops
        edges = (
            # Center to 1-hop
            [(0, 1), (0, 2), (0, 3), (0, 4)]
            # 1-hop to 2-hop
            + [(1, 5), (1, 6), (2, 6), (2, 7), (3, 8), (3, 9), (4, 9), (4, 10)]
            # 2-hop to 3-hop
            + [(5, 11), (7, 12), (9, 13), (10, 14)]
            # Some intra-layer connections
            + [(5, 6), (7, 8), (9, 10)]
        )

        edge_lines = VGroup(*[Line(npos[a], npos[b], color=SOFT, stroke_width=1.6) for a, b in edges])

        # All nodes start gray
        node_circles = {
            i: Circle(0.25, color=NEUTRAL, fill_color=NEUTRAL, fill_opacity=0.85).move_to(npos[i])
            for i in range(15)
        }

        # Hop assignments
        hops = {0: 0}  # Target
        for i in range(1, 5):
            hops[i] = 1
        for i in range(5, 11):
            hops[i] = 2
        for i in range(11, 15):
            hops[i] = 3

        caption = Text(
            "Each GNN layer expands the receptive field by one hop",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)

        # Move everything slightly left to make room
        graph_group = VGroup(edge_lines, VGroup(*node_circles.values()))

        self.play(Create(edge_lines), FadeIn(VGroup(*node_circles.values())), FadeIn(caption), run_time=0.5)
        self.wait(0.4)

        # Highlight target node
        self.play(
            node_circles[0].animate.set_color(HOP_COLORS[0]).set_fill(HOP_COLORS[0]),
            run_time=0.5
        )

        self.wait(0.4)

        # Layer counter
        layer_counter = VGroup(
            Text("Layers:", font_size=16, color=ACCENT),
            Text("0", font_size=22, color=ACCENT)
        ).arrange(RIGHT, buff=0.15).move_to(RIGHT * 5.0 + UP * 2.0)
        self.play(FadeIn(layer_counter), run_time=0.5)

        hop_groups = {1: range(1, 5), 2: range(5, 11), 3: range(11, 15)}
        hop_labels = {
            1: "Layer 1: direct neighbors join",
            2: "Layer 2: 2-hop neighbors reached",
            3: "Layer 3: almost the whole graph!",
        }

        for layer in [1, 2, 3]:
            # Update caption
            new_caption = Text(hop_labels[layer], font_size=18, color=SOFT).to_edge(DOWN, buff=0.4)
            new_layer_count = Text(str(layer), font_size=22, color=ACCENT)
            new_layer_count.move_to(layer_counter[1].get_center())

            self.play(
                Transform(caption, new_caption),
                Transform(layer_counter[1], new_layer_count),
                run_time=0.5
            )
            self.wait(0.4)

            # Pulse animation - messages flowing from previous layer to current
            pulse_dots = []
            pulse_anims = []
            for a, b in edges:
                if (hops.get(a, 99) < layer and hops.get(b, 99) == layer) or \
                   (hops.get(b, 99) < layer and hops.get(a, 99) == layer):
                    src = a if hops.get(a, 99) < layer else b
                    dst = b if src == a else a
                    dot = Circle(radius=0.1, color=HOP_COLORS[layer - 1], fill_color=HOP_COLORS[layer - 1], fill_opacity=0.9).move_to(npos[src])
                    pulse_dots.append(dot)
                    pulse_anims.append(MoveAlongPath(dot, Line(npos[src], npos[dst]), rate_func=smooth))

            if pulse_anims:
                for dot in pulse_dots:
                    self.add(dot)
                self.play(*pulse_anims, run_time=0.5)
                for dot in pulse_dots:
                    self.remove(dot)

            # Color the new hop nodes
            self.play(
                *[
                    node_circles[i].animate.set_color(HOP_COLORS[layer]).set_fill(HOP_COLORS[layer])
                    for i in hop_groups[layer]
                ],
                run_time=0.5,
            )

            self.wait(0.4)

        # === OVER-SMOOTHING WARNING ===
        smooth_caption = Text(
            "Too many layers → all nodes look the same (over-smoothing)",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, smooth_caption), run_time=0.5)
        self.wait(0.4)

        # Continue layers until everything becomes gray
        for extra_layer in range(4, 8):
            new_layer_count = Text(str(extra_layer), font_size=22, color=FRAUD)
            new_layer_count.move_to(layer_counter[1].get_center())
            self.play(Transform(layer_counter[1], new_layer_count), run_time=0.34)

        # Fade all to same gray
        self.play(
            *[node_circles[i].animate.set_color(NEUTRAL).set_fill(NEUTRAL) for i in range(15)],
            run_time=0.5,
        )

        identity_lost = Text("Identity lost!", font_size=16, color=FRAUD).move_to(RIGHT * 5.0 + DOWN * 0.5)
        self.play(FadeIn(identity_lost), run_time=0.5)
        self.wait(0.4)

        # === SIDE-BY-SIDE COMPARISON ===
        compare_caption = Text(
            "2-3 layers optimal: enough context, distinct embeddings",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, compare_caption), FadeOut(identity_lost), run_time=0.5)
        self.wait(0.4)

        # Split screen boxes
        left_box = VGroup(
            Rectangle(width=3, height=2.5, color=GREEN, stroke_width=2),
            Text("2 Layers", font_size=14, color=GREEN),
        )
        left_box[1].next_to(left_box[0], UP, buff=0.1)
        left_box.move_to(LEFT * 4.5 + DOWN * 1.0)

        right_box = VGroup(
            Rectangle(width=3, height=2.5, color=FRAUD, stroke_width=2),
            Text("8 Layers", font_size=14, color=FRAUD),
        )
        right_box[1].next_to(right_box[0], UP, buff=0.1)
        right_box.move_to(RIGHT * 4.5 + DOWN * 1.0)

        # Mini graphs inside boxes
        mini_nodes_left = VGroup(*[
            Circle(0.1, color=[GREEN, LEGIT, ACCENT, FRAUD][i % 4], fill_color=[GREEN, LEGIT, ACCENT, FRAUD][i % 4], fill_opacity=0.9).move_to(
                LEFT * 4.5 + DOWN * 1.0 + np.array([0.5 * np.cos(2 * np.pi * i / 6), 0.5 * np.sin(2 * np.pi * i / 6), 0])
            )
            for i in range(6)
        ])

        mini_nodes_right = VGroup(*[
            Circle(0.1, color=NEUTRAL, fill_color=NEUTRAL, fill_opacity=0.9).move_to(
                RIGHT * 4.5 + DOWN * 1.0 + np.array([0.5 * np.cos(2 * np.pi * i / 6), 0.5 * np.sin(2 * np.pi * i / 6), 0])
            )
            for i in range(6)
        ])

        self.play(
            FadeIn(left_box), FadeIn(right_box),
            FadeIn(mini_nodes_left), FadeIn(mini_nodes_right),
            run_time=0.5
        )
        self.wait(0.4)

        # Final caption
        final = Text(
            "A few layers add context — too many wash away identity",
            font_size=18, color=ACCENT,
        ).to_edge(DOWN, buff=0.4)

        self.play(Transform(caption, final), run_time=0.5)
        self.wait(0.4)
