from manim import *
import numpy as np

# Consistent color palette
FRAUD = "#E05252"
LEGIT = "#52A8E0"
NEUTRAL = "#888888"
ACCENT = "#F5A623"
SOFT = "#CCCCCC"
GREEN = "#2ECC71"
ORANGE_ = "#F07820"
MED_RISK = "#E6A832"


def node_box(text, color, width=2.8, height=0.7, font_size=16):
    box = RoundedRectangle(
        corner_radius=0.15, width=width, height=height,
        color=color, fill_color=color, fill_opacity=0.25, stroke_width=2.5,
    )
    lbl = Text(text, font_size=font_size, color=WHITE).move_to(box.get_center())
    return VGroup(box, lbl)


class DecisionTree(Scene):
    def construct(self):
        title = Text("Decision Tree for Fraud Detection", font_size=28, color=WHITE).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.8)

        caption = Text(
            "Each node poses a yes/no question about the transaction",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)

        # === BUILD THE TREE ===
        # Root node
        root = node_box("deposit > $5,000?", NEUTRAL, width=3.4).move_to(UP * 2.2)

        self.play(FadeIn(root), FadeIn(caption), run_time=0.8)
        self.wait(0.8)

        # Build caption
        build_caption = Text(
            "Tree learns to split data by asking discriminative questions",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, build_caption), run_time=0.8)

        # Level 1: Left (No -> LOW RISK) and Right (Yes -> more questions)
        left1_pos = UP * 0.3 + LEFT * 3.8
        right1_pos = UP * 0.3 + RIGHT * 2.0

        edge_no = Line(root.get_bottom(), left1_pos + UP * 0.35, color=GREEN, stroke_width=3)
        edge_yes = Line(root.get_bottom(), right1_pos + UP * 0.35, color=ORANGE_, stroke_width=3)

        no_lbl = Text("No", font_size=14, color=GREEN).move_to(
            (root.get_bottom() + left1_pos + UP * 0.35) / 2 + LEFT * 0.3
        )
        yes_lbl = Text("Yes", font_size=14, color=ORANGE_).move_to(
            (root.get_bottom() + right1_pos + UP * 0.35) / 2 + RIGHT * 0.3
        )

        left1 = node_box("LOW RISK", GREEN, width=2.4).move_to(left1_pos)
        right1 = node_box("account age < 7 days?", NEUTRAL, width=3.6).move_to(right1_pos)

        self.play(Create(edge_no), Create(edge_yes), FadeIn(no_lbl), FadeIn(yes_lbl), run_time=0.8)
        self.play(FadeIn(left1), FadeIn(right1), run_time=0.8)
        self.wait(0.5)

        # Level 2: From right1
        left2_pos = DOWN * 1.5 + RIGHT * 0.0
        right2_pos = DOWN * 1.5 + RIGHT * 4.0

        edge_n2 = Line(right1.get_bottom(), left2_pos + UP * 0.35, color=MED_RISK, stroke_width=3)
        edge_y2 = Line(right1.get_bottom(), right2_pos + UP * 0.35, color=FRAUD, stroke_width=3)

        n2_lbl = Text("No", font_size=14, color=MED_RISK).move_to(
            (right1.get_bottom() + left2_pos + UP * 0.35) / 2 + LEFT * 0.3
        )
        y2_lbl = Text("Yes", font_size=14, color=FRAUD).move_to(
            (right1.get_bottom() + right2_pos + UP * 0.35) / 2 + RIGHT * 0.3
        )

        leaf_med = node_box("MEDIUM RISK", MED_RISK, width=2.8).move_to(left2_pos)
        leaf_high = node_box("HIGH RISK", FRAUD, width=2.4).move_to(right2_pos)

        self.play(Create(edge_n2), Create(edge_y2), FadeIn(n2_lbl), FadeIn(y2_lbl), run_time=0.8)
        self.play(FadeIn(leaf_med), FadeIn(leaf_high), run_time=0.8)

        self.wait(0.8)

        # === CLASSIFICATION DEMO ===
        classify_caption = Text(
            "New user: deposit = $8,000, account age = 3 days",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, classify_caption), run_time=0.8)

        # User info panel
        user_panel = VGroup(
            Text("New User", font_size=16, color=ACCENT),
            Text("deposit: $8,000", font_size=14, color=WHITE),
            Text("acct age: 3 days", font_size=14, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(LEFT * 5.5 + UP * 1.5)
        user_box = SurroundingRectangle(user_panel, color=ACCENT, buff=0.15, stroke_width=2)

        self.play(FadeIn(user_panel), Create(user_box), run_time=0.8)
        self.wait(0.5)

        # User dot
        user_dot = Circle(radius=0.18, color=ACCENT, fill_color=ACCENT, fill_opacity=0.9).move_to(root.get_center() + UP * 1.0)
        self.play(FadeIn(user_dot), run_time=0.8)

        # Move to root
        self.play(user_dot.animate.move_to(root.get_center()), run_time=0.8)
        self.wait(0.5)

        # Check condition: deposit > $5000? YES (8000 > 5000)
        check1 = Text("$8,000 > $5,000? ✓", font_size=12, color=ACCENT).next_to(root, RIGHT, buff=0.2)
        self.play(FadeIn(check1), run_time=0.8)

        # Highlight YES edge
        edge_yes_highlight = edge_yes.copy().set_stroke(ACCENT, width=6)
        self.play(Create(edge_yes_highlight), run_time=0.8)

        # Move to right1
        self.play(user_dot.animate.move_to(right1.get_center()), FadeOut(check1), run_time=0.8)
        self.wait(0.5)

        # Check condition: account age < 7 days? YES (3 < 7)
        check2 = Text("3 days < 7 days? ✓", font_size=12, color=ACCENT).next_to(right1, RIGHT, buff=0.2)
        self.play(FadeIn(check2), run_time=0.8)

        # Highlight YES edge
        edge_y2_highlight = edge_y2.copy().set_stroke(ACCENT, width=6)
        self.play(Create(edge_y2_highlight), run_time=0.8)

        # Move to HIGH RISK leaf
        self.play(user_dot.animate.move_to(leaf_high.get_center()), FadeOut(check2), run_time=0.8)

        # Flash HIGH RISK
        self.play(
            leaf_high[0].animate.set_fill(FRAUD, opacity=0.7).set_stroke(ACCENT, width=5),
            Indicate(leaf_high, color=FRAUD, scale_factor=1.15),
            run_time=1.0
        )
        self.wait(0.5)

        # === INTERPRETABILITY ===
        interp_caption = Text(
            "The path is a human-readable rule — fully interpretable!",
            font_size=18, color=SOFT,
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, interp_caption), run_time=0.8)

        # Show rule path as text
        rule_box = VGroup(
            Text("Decision Path:", font_size=14, color=ACCENT),
            Text("deposit > $5,000 → YES", font_size=12, color=WHITE),
            Text("account age < 7 days → YES", font_size=12, color=WHITE),
            Text("→ HIGH RISK", font_size=14, color=FRAUD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(LEFT * 4.5 + DOWN * 0.8)
        rule_frame = SurroundingRectangle(rule_box, color=SOFT, buff=0.2, stroke_width=1.5)

        self.play(FadeIn(rule_box), Create(rule_frame), run_time=1.0)
        self.wait(0.5)

        # Final caption
        final = Text(
            "Why this user was flagged: clear, auditable reasoning",
            font_size=18, color=ACCENT,
        ).to_edge(DOWN, buff=0.4)

        self.play(Transform(caption, final), run_time=0.8)
        self.wait(2.0)
