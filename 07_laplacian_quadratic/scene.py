from manim import *
import numpy as np

# Consistent color palette
FRAUD = "#E05252"
LEGIT = "#52A8E0"
NEUTRAL = "#888888"
ACCENT = "#F5A623"
SOFT = "#CCCCCC"
GREEN = "#2ECC71"


def val_color(v):
    """Map value 0-1 to blue-red gradient."""
    red = np.array(color_to_rgb(FRAUD))
    blue = np.array(color_to_rgb(LEGIT))
    return rgb_to_color(blue + (red - blue) * v)


class LaplacianQuadratic(Scene):
    def construct(self):
        # Formula
        formula = MathTex(r"x^\top L x = \sum_{(i,j)\in E}(x_i-x_j)^2", font_size=24, color=SOFT).to_edge(UP, buff=0.35)
        formula_meaning = Text("measures signal smoothness on the graph", font_size=14, color=ACCENT).next_to(formula, DOWN, buff=0.1)
        self.play(FadeIn(formula), FadeIn(formula_meaning), run_time=0.5)
        self.wait(0.4)

        # Graph with two clusters
        npos = {
            0: np.array([-3.8, 0.8, 0]),
            1: np.array([-3.8, -0.5, 0]),
            2: np.array([-2.5, 0.15, 0]),
            3: np.array([2.5, 0.15, 0]),
            4: np.array([3.8, 0.8, 0]),
            5: np.array([3.8, -0.5, 0]),
        }

        intra = [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5)]
        bridge = (2, 3)

        # Smooth signals: cluster 1 high, cluster 2 low
        smooth = {0: 0.90, 1: 0.85, 2: 0.88, 3: 0.12, 4: 0.15, 5: 0.10}

        # Create edges
        intra_lines = VGroup(*[Line(npos[a], npos[b], color=SOFT, stroke_width=2) for a, b in intra])
        bridge_line = Line(npos[bridge[0]], npos[bridge[1]], color=SOFT, stroke_width=2.5)

        # Create nodes
        node_circles = {}
        node_labels = {}
        for i, pos in npos.items():
            circle = Circle(0.32, color=val_color(smooth[i]), fill_color=val_color(smooth[i]), fill_opacity=0.9).move_to(pos)
            label = Text(f"{smooth[i]:.2f}", font_size=12, color=WHITE).move_to(pos)
            node_circles[i] = circle
            node_labels[i] = label

        all_nodes = VGroup(*node_circles.values(), *node_labels.values())

        caption = Text(
            "Smooth signal: similar values within each cluster",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)

        cluster_labels = VGroup(
            Text("Cluster 1", font_size=14, color=FRAUD).move_to(LEFT * 3.2 + UP * 1.8),
            Text("Cluster 2", font_size=14, color=LEGIT).move_to(RIGHT * 3.2 + UP * 1.8),
        )

        self.play(
            Create(intra_lines), Create(bridge_line),
            FadeIn(all_nodes), FadeIn(cluster_labels), FadeIn(caption),
            run_time=0.5
        )
        self.wait(0.4)

        # === COMPUTE EDGE COSTS ===
        cost_caption = Text(
            "Compute (x_i - x_j)² for each edge",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, cost_caption), run_time=0.5)
        self.wait(0.4)

        # Intra-cluster edges: small costs
        intra_costs = VGroup()
        for a, b in intra[:3]:  # Left cluster
            diff = abs(smooth[a] - smooth[b])
            cost = diff ** 2
            midpoint = (npos[a] + npos[b]) / 2
            cost_txt = Text(f"{cost:.4f}", font_size=10, color=GREEN).move_to(midpoint + UP * 0.25)
            intra_costs.add(cost_txt)
            # Highlight edge
            highlight = Line(npos[a], npos[b], color=GREEN, stroke_width=4)
            self.play(Create(highlight), FadeIn(cost_txt), run_time=0.34)
            self.play(FadeOut(highlight), run_time=0.34)

        small_note = Text("Small costs — similar values!", font_size=14, color=GREEN).move_to(LEFT * 3.2 + DOWN * 1.3)
        self.play(FadeIn(small_note), run_time=0.5)
        self.wait(0.4)

        # Bridge edge: large cost
        bridge_caption = Text(
            "The bridge edge has huge disagreement",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, bridge_caption), run_time=0.5)

        bridge_diff = abs(smooth[bridge[0]] - smooth[bridge[1]])
        bridge_cost = bridge_diff ** 2

        bridge_highlight = Line(npos[bridge[0]], npos[bridge[1]], color=FRAUD, stroke_width=6)
        bridge_cost_txt = Text(f"{bridge_cost:.4f}", font_size=12, color=FRAUD).move_to(
            (npos[bridge[0]] + npos[bridge[1]]) / 2 + DOWN * 0.35
        )

        self.play(Create(bridge_highlight), FadeIn(bridge_cost_txt), run_time=0.5)

        dominates_note = Text("This one edge dominates the total!", font_size=14, color=FRAUD).move_to(DOWN * 1.0)
        self.play(FadeIn(dominates_note), run_time=0.5)

        # Total cost
        total = sum((smooth[a] - smooth[b]) ** 2 for a, b in intra + [bridge])
        total_txt = Text(f"Total x⊤Lx ≈ {total:.3f}", font_size=18, color=ACCENT).move_to(RIGHT * 3.0 + DOWN * 1.8)
        self.play(FadeIn(total_txt), run_time=0.5)
        self.wait(0.32)

        # === ADD MORE BRIDGES ===
        more_caption = Text(
            "Add more cross-cluster edges — cost increases",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        self.play(
            Transform(caption, more_caption),
            FadeOut(VGroup(intra_costs, small_note, dominates_note, bridge_cost_txt)),
            run_time=0.5
        )
        self.wait(0.4)

        # Add more bridge edges
        new_bridges = [(0, 4), (1, 5)]
        running_total = total

        for a, b in new_bridges:
            new_line = Line(npos[a], npos[b], color=FRAUD, stroke_width=3)
            diff = abs(smooth[a] - smooth[b])
            cost = diff ** 2
            running_total += cost

            # Update total
            new_total = Text(f"Total x⊤Lx ≈ {running_total:.3f}", font_size=18, color=ACCENT).move_to(RIGHT * 3.0 + DOWN * 1.8)

            self.play(
                Create(new_line),
                Transform(total_txt, new_total),
                run_time=0.5
            )

        self.wait(0.4)

        # === SCRAMBLED SIGNALS ===
        scramble_caption = Text(
            "Scramble the values — disagreement everywhere!",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, scramble_caption), FadeOut(bridge_highlight), run_time=0.5)

        scrambled = {0: 0.85, 1: 0.12, 2: 0.55, 3: 0.30, 4: 0.90, 5: 0.18}

        anims = []
        for i in range(6):
            anims.append(node_circles[i].animate.set_color(val_color(scrambled[i])).set_fill(val_color(scrambled[i])))
            new_label = Text(f"{scrambled[i]:.2f}", font_size=12, color=WHITE).move_to(npos[i])
            anims.append(Transform(node_labels[i], new_label))

        self.play(*anims, run_time=0.5)

        # Recompute total
        all_edges = intra + [bridge] + new_bridges
        total_scrambled = sum((scrambled[a] - scrambled[b]) ** 2 for a, b in all_edges)

        scrambled_total = Text(f"Total x⊤Lx ≈ {total_scrambled:.3f}", font_size=18, color=FRAUD).move_to(RIGHT * 3.0 + DOWN * 1.8)
        self.play(Transform(total_txt, scrambled_total), run_time=0.5)
        self.wait(0.4)

        # Final caption
        final = Text(
            "Low x⊤Lx = smooth signal · High x⊤Lx = rough signal",
            font_size=18, color=ACCENT,
        ).to_edge(DOWN, buff=0.4)

        self.play(Transform(caption, final), run_time=0.5)
        self.wait(0.4)
