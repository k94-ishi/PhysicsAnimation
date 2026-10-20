from manim import Text

# Manim's Text leaves its font unset by default, so it falls back to
# whatever the system's font-matching resolves "serif"/generic to. On a
# Japanese-locale system that resolves to a CJK font (e.g. Hiragino
# Mincho), which has no real kerning tables for Latin glyphs and renders
# English text with visibly uneven letter spacing. Pin a real Latin font
# globally (every scene imports something from common.*, which runs this
# file first) so Text() looks right regardless of the rendering machine's
# locale.
Text.set_default(font="Helvetica")
