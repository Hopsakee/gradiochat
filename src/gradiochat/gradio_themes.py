"""Prebuild themes for the gradio user Interface"""

# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/98_gradio_themes.ipynb.

# %% auto 0
__all__ = ['themeWDODelta']

# %% ../../nbs/98_gradio_themes.ipynb 3
import gradio as gr

# %% ../../nbs/98_gradio_themes.ipynb 5
themeWDODelta = gr.themes.Base(
    primary_hue=gr.themes.Color(c100="#ffedd5", c200="#ffddb3", c300="#fdba74", c400="#f29100", c50="#fff7ed", c500="#f97316", c600="#ea580c", c700="#c2410c", c800="#9a3412", c900="#7c2d12", c950="#6c2e12"),
    neutral_hue="slate",
    radius_size="sm",
    font=['VivalaSansRound', 'ui-sans-serif', 'system-ui', 'sans-serif'],
).set(
    embed_radius='*radius_xs',
    border_color_accent='*primary_400',
    border_color_accent_dark='*secondary_700',
    border_color_primary='*secondary_700',
    border_color_primary_dark='*secondary_700',
    color_accent='*primary_400',
    shadow_drop='*shadow_drop_lg',
    button_primary_background_fill='*primary_400',
    button_primary_background_fill_dark='*primary_400',
    button_primary_background_fill_hover='*secondary_700',
    button_primary_background_fill_hover_dark='*secondary_700',
    button_primary_border_color='*secondary_700',
    button_primary_border_color_dark='*secondary_700'
)
