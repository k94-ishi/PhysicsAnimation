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
# "CMU Serif" (Computer Modern Unicode) looks like the obvious choice,
# since it's the same family LaTeX already renders every MathTex/Tex
# formula in - but it only gets TeX's own spacing corrections inside an
# actual LaTeX run. Text() never goes through LaTeX; it's shaped directly
# by Pango, and cm-unicode's OpenType conversion has incomplete/uneven
# kerning data for that path - confirmed by rendering the same sentence in
# CMU Serif vs. Georgia: CMU Serif comes out with visibly inconsistent
# word and letter spacing, Georgia doesn't. Georgia is a serif face with
# complete, well-behaved Pango kerning, so it pairs reasonably with the
# Computer Modern math without inheriting cm-unicode's rendering defects.
Text.set_default(font="Georgia")
