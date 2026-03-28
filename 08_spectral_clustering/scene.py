from manim import *
import numpy as np

# Consistent color palette
FRAUD = "#E05252"
LEGIT = "#52A8E0"
GREEN = "#2ECC71"
NEUTRAL = "#888888"
ACCENT = "#F5A623"
SOFT = "#CCCCCC"

CLUSTER_COLORS = [FRAUD, LEGIT, GREEN]


class SpectralClustering(Scene):
    def construct(self):
        title = Text("Spectral Clustering", font_size=28, color=WHITE).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.8)

        np.random.seed(7)

        # Create 3 clusters of 6 nodes each (18 total)
        n_per = 6
        centers = [LEFT * 3.5 + UP * 0.3, ORIGIN + UP * 0.3, RIGHT * 3.5 + UP * 0.3]
        npos = {}

        for ci, cent in enumerate(centers):
            for j in range(n_per):
                angle = 2 * np.pi * j / n_per
                radius = 0.9
                npos[ci * n_per + j] = cent + np.array([radius * np.cos(angle), radius * np.sin(angle), 0])

        # Intra-cluster edges (ring + some cross)
        edges = []
        for ci in range(3):
            base = ci * n_per
            # Ring edges
            for j in range(n_per):
                edges.append((base + j, base + (j + 1) % n_per))
            # Cross edges within cluster
            edges.append((base, base + 3))
            edges.append((base + 1, base + 4))

        # Sparse inter-cluster edges (just 1-2)
        edges.append((n_per - 1, n_per))  # Cluster 0 to 1
        edges.append((2 * n_per - 1, 2 * n_per))  # Cluster 1 to 2

        edge_lines = VGroup(*[Line(npos[a], npos[b], color=SOFT, stroke_width=1.8) for a, b in edges])
        node_dots = {i: Circle(0.18, color=NEUTRAL, fill_color=NEUTRAL, fill_opacity=0.85).move_to(npos[i]) for i in range(3 * n_per)}
        all_nodes = VGroup(*node_dots.values())

        caption = Text(
            "18 nodes — structure unknown (all gray)",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        self.play(Create(edge_lines), FadeIn(all_nodes), FadeIn(caption), run_time=1.0)
        self.wait(0.8)

        # === COMPUTE LAPLACIAN ===
        laplacian_caption = Text(
            "Compute Laplacian L = D - A and find its eigenvalues",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, laplacian_caption), run_time=0.8)
        self.wait(0.5)

        # Move graph to side
        graph_group = VGroup(edge_lines, all_nodes)
        self.play(graph_group.animate.scale(0.65).move_to(LEFT * 4.0 + UP * 0.8), run_time=1.0)

        # Eigenvalue bar chart
        eig_vals = [0.0, 0.04, 0.06, 1.1, 1.3, 1.6, 1.9, 2.2]
        eig_colors = [LEGIT, GREEN, GREEN, FRAUD, NEUTRAL, NEUTRAL, NEUTRAL, NEUTRAL]
        bar_h = [max(0.1, v * 1.2) for v in eig_vals]
        bar_origin = RIGHT * 0.5 + DOWN * 1.0
        bar_gap = 0.55

        bars = VGroup()
        btags = VGroup()
        for i, (h, c) in enumerate(zip(bar_h, eig_colors)):
            bar = Rectangle(width=0.4, height=h, color=c, fill_color=c, fill_opacity=0.8)
            bar.align_to(bar_origin + RIGHT * i * bar_gap, DOWN + LEFT)
            bars.add(bar)
            ev = MathTex(rf"\lambda_{{{i + 1}}}", font_size=14, color=SOFT).next_to(bar, DOWN, buff=0.08)
            btags.add(ev)

        self.play(FadeIn(btags), *[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.1, run_time=1.0)
        self.wait(0.5)

        # Highlight small eigenvalues
        eig_caption = Text(
            "3 near-zero eigenvalues → 3 clusters!",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, eig_caption), run_time=0.8)

        bracket = Brace(VGroup(*bars[:3]), direction=UP, color=GREEN)
        btext = Text("3 small = 3 clusters", font_size=14, color=GREEN).next_to(bracket, UP, buff=0.08)
        self.play(Create(bracket), FadeIn(btext), run_time=0.8)

        # Gap annotation
        gap_arrow = Arrow(bars[2].get_top() + RIGHT * 0.3, bars[3].get_top() + LEFT * 0.3, color=ACCENT, stroke_width=3)
        gap_text = Text("eigenvalue gap", font_size=12, color=ACCENT).next_to(gap_arrow, UP, buff=0.05)
        self.play(Create(gap_arrow), FadeIn(gap_text), run_time=0.8)
        self.wait(0.8)

        # === 2D EMBEDDING ===
        embed_caption = Text(
            "Plot nodes by eigenvector values — clusters separate!",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        self.play(
            Transform(caption, embed_caption),
            FadeOut(VGroup(bars, btags, bracket, btext, gap_arrow, gap_text)),
            run_time=0.8
        )
        self.wait(0.5)

        # Embedding scatter plot area
        embed_center = RIGHT * 2.0 + UP * 0.5
        axes = VGroup(
            Arrow(embed_center + LEFT * 2, embed_center + RIGHT * 2, color=SOFT, stroke_width=2),
            Arrow(embed_center + DOWN * 1.5, embed_center + UP * 1.5, color=SOFT, stroke_width=2),
        )
        ax_labels = VGroup(
            MathTex(r"v_2", font_size=18, color=SOFT).next_to(axes[0], RIGHT, buff=0.1),
            MathTex(r"v_3", font_size=18, color=SOFT).next_to(axes[1], UP, buff=0.1),
        )
        self.play(Create(axes), FadeIn(ax_labels), run_time=0.8)

        # Compute fake 2D positions for embedding (clustered)
        embed_pos = {}
        cluster_centers_2d = [
            embed_center + LEFT * 1.2 + UP * 0.8,
            embed_center + RIGHT * 0.5 + DOWN * 0.5,
            embed_center + RIGHT * 1.2 + UP * 0.6,
        ]
        np.random.seed(42)
        for ci in range(3):
            for j in range(n_per):
                idx = ci * n_per + j
                offset = np.array([np.random.uniform(-0.25, 0.25), np.random.uniform(-0.25, 0.25), 0])
                embed_pos[idx] = cluster_centers_2d[ci] + offset

        # Animate nodes flying from graph to embedding
        node_copies = {i: node_dots[i].copy() for i in range(3 * n_per)}
        for c in node_copies.values():
            self.add(c)

        fly_anims = [node_copies[i].animate.move_to(embed_pos[i]) for i in range(3 * n_per)]
        self.play(*fly_anims, run_time=1.0)
        self.wait(0.5)

        # Run k-means (color by cluster)
        kmeans_caption = Text(
            "k-means on 2D coordinates finds the clusters",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, kmeans_caption), run_time=0.8)

        color_anims = []
        for ci in range(3):
            for j in range(n_per):
                idx = ci * n_per + j
                color_anims.append(node_copies[idx].animate.set_color(CLUSTER_COLORS[ci]).set_fill(CLUSTER_COLORS[ci]))

        self.play(*color_anims, run_time=0.8)

        # Draw cluster circles
        for ci in range(3):
            cluster_circle = Circle(radius=0.5, color=CLUSTER_COLORS[ci], stroke_width=2, stroke_opacity=0.6).move_to(cluster_centers_2d[ci])
            self.play(Create(cluster_circle), run_time=0.5)

        self.wait(0.8)

        # === REVEAL ON ORIGINAL GRAPH ===
        reveal_caption = Text(
            "Transfer labels back — fraud rings revealed!",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, reveal_caption), run_time=0.8)

        # Update original graph nodes
        original_color_anims = []
        for ci in range(3):
            for j in range(n_per):
                idx = ci * n_per + j
                original_color_anims.append(
                    node_dots[idx].animate.set_color(CLUSTER_COLORS[ci]).set_fill(CLUSTER_COLORS[ci], opacity=0.9)
                )

        self.play(*original_color_anims, run_time=1.0)
        self.wait(0.5)

        # Final caption
        final = Text(
            "Eigenvalues reveal cluster structure — no labels needed!",
            font_size=18, color=ACCENT,
        ).to_edge(DOWN, buff=0.4)

        self.play(Transform(caption, final), run_time=0.8)
        self.wait(2.0)
