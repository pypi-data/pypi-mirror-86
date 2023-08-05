
import base64
import io
from typing import List

import matplotlib.pyplot
import matplotlib.figure


def get_figure_count() -> int:
    return len(matplotlib.pyplot.get_fignums())

def render_mpl_figures() -> List[str]:
    figures = [matplotlib.pyplot.figure(i) for i in matplotlib.pyplot.get_fignums()]
    figures_base64 = [_render_figure_to_base64(fig) for fig in figures]
    return figures_base64

def _render_figure_to_base64(fig: matplotlib.figure.Figure, dpi: float = None) -> str:
    tmpfile = io.BytesIO()
    fig.savefig(tmpfile, format='png', dpi=dpi)
    return base64.b64encode(tmpfile.getvalue()).decode("ascii")
