from manim import *
import random
import numpy as np

# Consistent color palette
FRAUD = "#E05252"
LEGIT = "#52A8E0"
NEUTRAL = "#888888"
ACCENT = "#F5A623"
SOFT = "#CCCCCC"
GREEN = "#2ECC71"
PURPLE = "#9B59B6"

random.seed(42)

TREE_COLORS = ["#3A7BD5", "#2ECC71", "#9B59B6", "#E67E22", "#E05252"]


def mini_tree(root_pos, color, label, seed=0):
    """Create a small tree visualization."""
    random.seed(seed)
    g = VGroup()

    # Root node
    r = RoundedRectangle(
        corner_radius=0.1, width=1.2, height=0.4,
        color=color, fill_color=color, fill_opacity=0.4, stroke_width=2,
    )
    r.move_to(root_pos)
    g.add(r)

    # Two children
    for dx, dy in [(-0.55, -0.7), (0.55, -0.7)]:
        child_pos = root_pos + np.array([dx, dy, 0])
        leaf_c = FRAUD if random.random() > 0.5 else GREEN
        child = Circle(0.18, color=leaf_c, fill_color=leaf_c, fill_opacity=0.85).move_to(child_pos)
        line = Line(root_pos + DOWN * 0.2, child_pos + UP * 0.18, color=SOFT, stroke_width=1.5)
        g.add(line, child)

    # Label
    lbl = Text(label, font_size=12, color=color, weight=BOLD).next_to(r, UP, buff=0.08)
    g.add(lbl)
    return g


class RandomForest(Scene):
    def construct(self):
        # === TRAINING DATA ===
        caption = Text(
            "Training data: many rows of user transactions",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)

        # Show data table
        data_rows = VGroup()
        headers = ["deposit", "age", "label"]
        header_row = VGroup(*[Text(h, font_size=12, color=ACCENT) for h in headers]).arrange(RIGHT, buff=0.5)
        data_rows.add(header_row)

        sample_data = [
            ["$8,000", "3d", "FRAUD"],
            ["$500", "2y", "OK"],
            ["$3,000", "1m", "OK"],
            ["$12,000", "5d", "FRAUD"],
            ["$1,500", "6m", "OK"],
            ["$9,000", "2d", "FRAUD"],
        ]
        for row_data in sample_data:
            row = VGroup(*[
                Text(val, font_size=10, color=FRAUD if val == "FRAUD" else (GREEN if val == "OK" else WHITE))
                for val in row_data
            ]).arrange(RIGHT, buff=0.5)
            data_rows.add(row)

        data_rows.arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to(LEFT * 4 + UP * 0.8).scale(0.9)
        data_box = SurroundingRectangle(data_rows, color=SOFT, buff=0.15, stroke_width=1.5)

        self.play(FadeIn(data_rows), Create(data_box), FadeIn(caption), run_time=0.5)
        self.wait(0.4)

        # === BOOTSTRAP SAMPLING ===
        bootstrap_caption = Text(
            "Bootstrap: randomly sample rows (with replacement) for each tree",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, bootstrap_caption), run_time=0.5)
        self.wait(0.4)

        # Show samples flying to different piles
        sample_piles = VGroup()
        pile_positions = [LEFT * 1.5, LEFT * 0.0, RIGHT * 1.5, RIGHT * 3.0, RIGHT * 4.5]

        for i, pos in enumerate(pile_positions):
            pile_label = Text(f"Sample {i+1}", font_size=11, color=TREE_COLORS[i]).move_to(pos + UP * 2.0)
            sample_piles.add(pile_label)

        self.play(FadeIn(sample_piles), run_time=0.5)

        # Animate a few rows flying to piles
        for pile_idx in range(5):
            # Pick random rows
            row_indices = random.sample(range(1, 7), 3)
            fly_dots = VGroup(*[
                Circle(radius=0.08, color=TREE_COLORS[pile_idx], fill_color=TREE_COLORS[pile_idx], fill_opacity=0.8).move_to(data_rows[idx].get_center())
                for idx in row_indices
            ])
            self.add(fly_dots)
            self.play(
                *[dot.animate.move_to(pile_positions[pile_idx] + UP * (1.0 + 0.2 * j)) for j, dot in enumerate(fly_dots)],
                run_time=0.34
            )

        self.wait(0.4)

        # === GROW TREES IN PARALLEL ===
        tree_caption = Text(
            "Each tree grows on its own sample — slightly different structures",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        self.play(
            Transform(caption, tree_caption),
            FadeOut(data_rows), FadeOut(data_box), FadeOut(sample_piles),
            run_time=0.5
        )
        self.wait(0.4)

        # Create 5 trees
        tree_xs = [LEFT * 4.8, LEFT * 2.4, ORIGIN, RIGHT * 2.4, RIGHT * 4.8]
        trees = VGroup(*[
            mini_tree(x + UP * 0.8, c, f"Tree {i + 1}", seed=i * 7)
            for i, (x, c) in enumerate(zip(tree_xs, TREE_COLORS))
        ])

        # Animate trees growing (fade in with slight delay)
        self.play(FadeIn(trees, lag_ratio=0.2), run_time=0.95)
        self.wait(0.4)

        # === VOTING ===
        vote_caption = Text(
            "New user arrives — every tree votes independently",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, vote_caption), run_time=0.5)
        self.wait(0.4)

        # User enters
        user_dot = Circle(radius=0.15, color=ACCENT, fill_color=ACCENT, fill_opacity=0.9).move_to(UP * 2.8)
        user_label = Text("New User", font_size=12, color=ACCENT).next_to(user_dot, UP, buff=0.1)
        self.play(FadeIn(user_dot), FadeIn(user_label), run_time=0.5)

        # Send user through all trees (simultaneously)
        user_copies = VGroup(*[
            Circle(radius=0.1, color=ACCENT, fill_color=ACCENT, fill_opacity=0.7).move_to(user_dot.get_center())
            for _ in range(5)
        ])
        self.add(user_copies)

        self.play(
            *[user_copies[i].animate.move_to(tree_xs[i] + UP * 0.8) for i in range(5)],
            run_time=0.5
        )
        self.play(FadeOut(user_copies), run_time=0.34)

        # Show votes
        random.seed(42)
        vote_results = ["FRAUD", "FRAUD", "OK", "FRAUD", "OK"]  # 3 fraud, 2 ok
        votes = VGroup()
        for i, (tree, result) in enumerate(zip(trees, vote_results)):
            color = FRAUD if result == "FRAUD" else GREEN
            vote_ball = Circle(radius=0.18, color=color, fill_color=color, fill_opacity=0.9).move_to(tree_xs[i] + DOWN * 1.2)
            vote_text = Text(result, font_size=10, color=WHITE).move_to(vote_ball.get_center())
            votes.add(VGroup(vote_ball, vote_text))

        self.play(FadeIn(votes, lag_ratio=0.15), run_time=0.5)
        self.wait(0.4)

        # === COUNT VOTES ===
        count_caption = Text(
            "Majority vote: 3 FRAUD vs 2 OK → Final prediction: FRAUD",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, count_caption), run_time=0.5)

        # Highlight fraud votes
        fraud_votes = VGroup(votes[0], votes[1], votes[3])
        self.play(
            *[Indicate(v[0], color=FRAUD, scale_factor=1.3) for v in fraud_votes],
            run_time=0.5
        )
        self.wait(0.4)

        # Final result
        result_box = VGroup(
            RoundedRectangle(width=3.5, height=1.0, corner_radius=0.15, color=FRAUD, fill_color=FRAUD, fill_opacity=0.25, stroke_width=3),
            Text("FRAUD", font_size=24, color=FRAUD),
            Text("60% confidence (3/5)", font_size=12, color=SOFT),
        )
        result_box[1].move_to(result_box[0].get_center() + UP * 0.15)
        result_box[2].move_to(result_box[0].get_center() + DOWN * 0.25)
        result_box.move_to(DOWN * 2.5)

        self.play(FadeIn(result_box), run_time=0.5)
        self.wait(0.4)

        # Final caption
        final = Text(
            "Ensemble = more stable predictions + confidence estimates",
            font_size=18, color=ACCENT,
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, final), run_time=0.5)
        self.wait(0.4)
