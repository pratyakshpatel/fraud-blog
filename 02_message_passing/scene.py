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

# Initial distinct colors for 5 nodes
NODE_COLORS = [FRAUD, LEGIT, GREEN, ACCENT, PURPLE]


def blend_colors(colors, weights=None):
    """Blend multiple colors together."""
    if weights is None:
        weights = [1.0 / len(colors)] * len(colors)
    r, g, b = 0, 0, 0
    for c, w in zip(colors, weights):
        rgb = color_to_rgb(c)
        r += rgb[0] * w
        g += rgb[1] * w
        b += rgb[2] * w
    return rgb_to_color([min(1, r), min(1, g), min(1, b)])


class MessagePassing(Scene):
    def construct(self):
        title = Text("Message Passing in GNNs", font_size=28, color=WHITE).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.8)

        # 5-node graph layout
        npos = {
            0: np.array([0.0, 1.5, 0]),     # top
            1: np.array([-2.0, 0.3, 0]),    # left
            2: np.array([-1.2, -1.8, 0]),   # bottom left
            3: np.array([1.2, -1.8, 0]),    # bottom right
            4: np.array([2.0, 0.3, 0]),     # right
        }
        edge_list = [(0, 1), (0, 4), (1, 2), (2, 3), (3, 4), (1, 4)]

        # Build adjacency
        adj = {i: [] for i in range(5)}
        for a, b in edge_list:
            adj[a].append(b)
            adj[b].append(a)

        # Create edges
        edge_lines = VGroup(*[Line(npos[a], npos[b], color=SOFT, stroke_width=2.5) for a, b in edge_list])

        # Create nodes with initial colors
        node_circles = {}
        node_labels = {}
        color_state = {i: NODE_COLORS[i] for i in range(5)}

        for i, p in npos.items():
            c = Circle(0.4, color=color_state[i], fill_color=color_state[i], fill_opacity=0.9).move_to(p)
            lbl = Text(str(i + 1), font_size=20, color=WHITE).move_to(p)
            node_circles[i] = c
            node_labels[i] = lbl

        all_nodes = VGroup(*node_circles.values(), *node_labels.values())

        caption = Text(
            "Each node starts with a unique color (its initial features)",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)

        self.play(Create(edge_lines), FadeIn(all_nodes), FadeIn(caption), run_time=1.0)
        self.wait(1.0)

        # Track color history for final trace
        color_history = {i: [NODE_COLORS[i]] for i in range(5)}

        def send_messages(round_num):
            """Animate message passing for one round."""
            dots = []
            anims = []

            # Create message dots and animation paths
            for a, b in edge_list:
                # Message from a to b
                d1 = Circle(radius=0.12, color=color_state[a], fill_color=color_state[a], fill_opacity=0.9).move_to(npos[a])
                dots.append(d1)
                anims.append(MoveAlongPath(d1, Line(npos[a], npos[b]), rate_func=smooth))

                # Message from b to a
                d2 = Circle(radius=0.12, color=color_state[b], fill_color=color_state[b], fill_opacity=0.9).move_to(npos[b])
                dots.append(d2)
                anims.append(MoveAlongPath(d2, Line(npos[b], npos[a]), rate_func=smooth))

            # Add dots to scene
            for d in dots:
                self.add(d)

            # Animate messages flowing
            self.play(*anims, run_time=1.0)

            # Compute new colors by averaging self + neighbors
            new_colors = {}
            for i in range(5):
                contributing_colors = [color_state[i]]  # self
                for nb in adj[i]:
                    contributing_colors.append(color_state[nb])
                new_colors[i] = blend_colors(contributing_colors)
                color_history[i].append(new_colors[i])

            # Fade out message dots
            self.play(*[FadeOut(d) for d in dots], run_time=0.5)

            # Update node colors
            update_anims = []
            for i in range(5):
                update_anims.append(node_circles[i].animate.set_color(new_colors[i]).set_fill(new_colors[i]))
                color_state[i] = new_colors[i]

            self.play(*update_anims, run_time=0.8)

        # Round 1
        round1_caption = Text(
            "Round 1: Each node sends its color to neighbors, then averages",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, round1_caption), run_time=0.8)
        self.wait(0.5)

        # Pulse effect before sending
        self.play(*[node_circles[i].animate.scale(1.15) for i in range(5)], run_time=0.5)
        self.play(*[node_circles[i].animate.scale(1/1.15) for i in range(5)], run_time=0.5)

        send_messages(1)
        self.wait(0.5)

        # Round 2
        round2_caption = Text(
            "Round 2: Blended colors spread further — information propagates",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, round2_caption), run_time=0.8)
        self.wait(0.5)

        self.play(*[node_circles[i].animate.scale(1.15) for i in range(5)], run_time=0.5)
        self.play(*[node_circles[i].animate.scale(1/1.15) for i in range(5)], run_time=0.5)

        send_messages(2)
        self.wait(0.5)

        # Round 3
        round3_caption = Text(
            "Round 3: Each node now contains information from 3 hops away",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, round3_caption), run_time=0.8)
        self.wait(0.5)

        self.play(*[node_circles[i].animate.scale(1.15) for i in range(5)], run_time=0.5)
        self.play(*[node_circles[i].animate.scale(1/1.15) for i in range(5)], run_time=0.5)

        send_messages(3)
        self.wait(0.5)

        # Highlight node 1 (index 0)
        highlight_caption = Text(
            "Node 1 now contains traces of ALL original colors",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, highlight_caption), run_time=0.8)

        # Highlight node 1
        ring = Circle(0.55, color=ACCENT, stroke_width=5).move_to(npos[0])
        self.play(Create(ring), run_time=0.8)
        self.wait(0.5)

        # Final caption
        final = Text(
            "After k rounds, each node sees k hops of its neighborhood",
            font_size=18, color=ACCENT,
        ).to_edge(DOWN, buff=0.4)

        self.play(Transform(caption, final), run_time=0.8)
        self.wait(2.0)
