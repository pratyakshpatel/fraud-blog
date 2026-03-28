from manim import *
import numpy as np
import random

# Consistent color palette
FRAUD = "#E05252"
LEGIT = "#52A8E0"
NEUTRAL = "#888888"
ACCENT = "#F5A623"
SOFT = "#CCCCCC"
GREEN = "#2ECC71"
PURPLE = "#9B59B6"

random.seed(12)


class RandomWalk(Scene):
    def construct(self):
        title = Text("Random Walks on Graphs", font_size=28, color=WHITE).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.8)

        np.random.seed(5)

        # Graph with fraud cluster and legit cluster
        npos = {
            # Fraud cluster (0-3)
            0: np.array([-3.5, 1.2, 0]),
            1: np.array([-2.5, 0.3, 0]),
            2: np.array([-4.2, 0.0, 0]),
            3: np.array([-3.5, -1.0, 0]),
            # Legit cluster (4-7)
            4: np.array([2.0, 1.3, 0]),
            5: np.array([3.2, 0.3, 0]),
            6: np.array([2.0, -0.8, 0]),
            7: np.array([4.2, 1.0, 0]),
        }
        is_fraud = {0, 1, 2, 3}

        # Dense connections within clusters, sparse between
        edges = [
            (0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (0, 3),  # Fraud cluster (dense)
            (4, 5), (4, 6), (5, 6), (5, 7), (4, 7),  # Legit cluster (dense)
            (1, 4),  # Single bridge
        ]

        adj = {i: [] for i in range(8)}
        for a, b in edges:
            adj[a].append(b)
            adj[b].append(a)

        edge_lines = VGroup(*[Line(npos[a], npos[b], color=SOFT, stroke_width=2) for a, b in edges])

        # Highlight bridge edge
        bridge_edge = Line(npos[1], npos[4], color=ACCENT, stroke_width=3)

        node_circles = {}
        node_labels = {}
        for i in range(8):
            color = FRAUD if i in is_fraud else LEGIT
            c = Circle(0.3, color=color, fill_color=color, fill_opacity=0.85).move_to(npos[i])
            t = Text("F" if i in is_fraud else "L", font_size=12, color=WHITE).move_to(npos[i])
            node_circles[i] = c
            node_labels[i] = t

        all_nodes = VGroup(*node_circles.values(), *node_labels.values())

        cluster_labels = VGroup(
            Text("Fraud Cluster", font_size=14, color=FRAUD).move_to(LEFT * 3.5 + UP * 2.3),
            Text("Legit Cluster", font_size=14, color=LEGIT).move_to(RIGHT * 3.0 + UP * 2.3),
        )

        caption = Text(
            "Red = fraud nodes, Blue = legitimate nodes",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)

        self.play(
            Create(edge_lines), Create(bridge_edge),
            FadeIn(all_nodes), FadeIn(cluster_labels), FadeIn(caption),
            run_time=1.0
        )
        self.wait(0.8)

        # Visit counts
        visit_counts = {i: 0 for i in range(8)}

        # Walker colors
        walker_colors = ["#FFDD44", "#FF88CC", "#88FF88", "#88DDFF"]

        def simulate_walk(start, steps, walker_color, walker_id):
            """Run a single random walk."""
            cur = start
            visit_counts[cur] += 1
            walker = Circle(radius=0.12, color=walker_color, fill_color=walker_color, fill_opacity=0.9).move_to(npos[cur])
            walker_label = Text(str(walker_id), font_size=10, color=BLACK).move_to(npos[cur])
            walker_grp = VGroup(walker, walker_label)
            self.add(walker_grp)

            for _ in range(steps):
                nxt = random.choice(adj[cur])
                self.play(
                    walker_grp.animate.move_to(npos[nxt]),
                    run_time=0.3,
                    rate_func=smooth
                )
                visit_counts[nxt] += 1
                cur = nxt

            self.play(FadeOut(walker_grp), run_time=0.3)
            return cur

        # Run multiple walkers from fraud nodes
        walk_caption = Text(
            "Walkers start from fraud nodes — where do they go?",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, walk_caption), run_time=0.8)
        self.wait(0.5)

        # Start 4 walkers from different fraud nodes
        starts = [0, 1, 2, 3]
        for i, start in enumerate(starts):
            simulate_walk(start, 6, walker_colors[i], i + 1)

        self.wait(0.5)

        # Show visit counts
        heat_caption = Text(
            "Visit counts: walkers mostly stayed in the fraud cluster!",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, heat_caption), run_time=0.8)

        max_v = max(visit_counts.values()) or 1
        heat_anims = []
        visit_labels = VGroup()

        for i in range(8):
            intensity = visit_counts[i] / max_v
            # Scale node by visits
            scale_factor = 1 + 0.4 * intensity
            heat_anims.append(node_circles[i].animate.scale(scale_factor))

            # Visit count label
            vt = Text(str(visit_counts[i]), font_size=12, color=ACCENT, weight=BOLD).move_to(npos[i] + DOWN * 0.55)
            visit_labels.add(vt)

        self.play(*heat_anims, run_time=0.8)
        self.play(FadeIn(visit_labels), run_time=0.8)

        # Show fraud vs legit totals
        fraud_visits = sum(visit_counts[i] for i in is_fraud)
        legit_visits = sum(visit_counts[i] for i in range(8) if i not in is_fraud)

        visit_summary = VGroup(
            Text(f"Fraud visits: {fraud_visits}", font_size=14, color=FRAUD),
            Text(f"Legit visits: {legit_visits}", font_size=14, color=LEGIT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(RIGHT * 0.0 + DOWN * 1.5)

        self.play(FadeIn(visit_summary), run_time=0.8)
        self.wait(0.8)

        # === Node2Vec parameters ===
        n2v_caption = Text(
            "Node2Vec: tune p, q to control exploration style",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, n2v_caption), FadeOut(VGroup(visit_labels, visit_summary)), run_time=0.8)

        # Reset node sizes
        reset_anims = [node_circles[i].animate.scale(1 / (1 + 0.4 * (visit_counts[i] / max_v))) for i in range(8)]
        self.play(*reset_anims, run_time=0.8)
        self.wait(0.5)

        # Parameter box
        param_box = VGroup(
            Text("Node2Vec Parameters:", font_size=14, color=PURPLE),
            Text("q high → BFS-like (local)", font_size=12, color=GREEN),
            Text("q low → DFS-like (explore far)", font_size=12, color=ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(RIGHT * 4.0 + UP * 0.0)

        self.play(FadeIn(param_box), run_time=0.8)

        # Show BFS-like behavior (high q - stay local)
        bfs_walker = Circle(radius=0.15, color=GREEN, fill_color=GREEN, fill_opacity=0.9).move_to(npos[0])
        self.add(bfs_walker)

        bfs_path = [0, 1, 0, 2, 0, 3, 0, 1]  # Stays close to start
        for nxt in bfs_path:
            self.play(bfs_walker.animate.move_to(npos[nxt]), run_time=0.25)

        self.play(FadeOut(bfs_walker), run_time=0.3)
        self.wait(0.5)

        # Show DFS-like behavior (low q - explore far)
        dfs_walker = Circle(radius=0.15, color=ACCENT, fill_color=ACCENT, fill_opacity=0.9).move_to(npos[0])
        self.add(dfs_walker)

        dfs_path = [0, 1, 4, 5, 7, 5, 6, 4]  # Explores outward
        for nxt in dfs_path:
            self.play(dfs_walker.animate.move_to(npos[nxt]), run_time=0.25)

        self.play(FadeOut(dfs_walker), run_time=0.3)
        self.wait(0.5)

        # Final caption
        final = Text(
            "Random walks score nodes by reachability from fraud",
            font_size=18, color=ACCENT,
        ).to_edge(DOWN, buff=0.4)

        self.play(Transform(caption, final), run_time=0.8)
        self.wait(2.0)
