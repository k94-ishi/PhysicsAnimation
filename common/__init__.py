from manim import Text

# Manim's Text leaves its font unset by default, so it falls back to
# whatever the system's font-matching resolves "serif"/generic to. On a
# Japanese-locale system that resolves to a CJK font (e.g. Hiragino
# Mincho), which has no real kerning tables for Latin glyphs and renders
# English text with visibly uneven letter spacing. Pin a real Latin font
# globally (every scene imports something from common.*, which runs this
# file first) so Text() looks right regardless of the rendering machine's
# locale.
#
# "CMU Serif" (Computer Modern Unicode) is the standard choice in the
# Manim community for Text: it's metrically the same family LaTeX uses for
# every MathTex/Tex formula in this project (Computer Modern is LaTeX's
# default math font), so prose captions and equations share one typeface
# instead of clashing (e.g. a sans-serif caption next to serif formulas).
# Requires the cm-unicode font family to be installed and visible to
# fontconfig (ships with most LaTeX distributions, e.g. TeX Live's
# cm-unicode package, but isn't always registered as a system font - see
# README.md > Development).
Text.set_default(font="CMU Serif")
