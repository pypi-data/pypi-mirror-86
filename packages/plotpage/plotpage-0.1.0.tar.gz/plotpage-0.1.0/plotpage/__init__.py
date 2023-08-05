
import inspect
import os
import webbrowser
from typing import Optional, List, Tuple

from .plot import render_mpl_figures, get_figure_count
from .render import render_page
from .output import capture_output, get_captured_outputs
from .cache import cached, cache_function

__all__ = ["show", "cached", "cache_function", "capture_output"]


_doc_items: List[Tuple[int, str]] = []

def add_markdown(markdown_content: str):
    active_figure_count = get_figure_count()
    _doc_items.append((active_figure_count, markdown_content))


def show(title: Optional[str] = None,
         output_path: str = "plotpage-output.html") -> None:
    captured_outputs = get_captured_outputs()

    figures_base64 = render_mpl_figures()

    caller_path = inspect.stack()[1].filename
    caller_source_code = open(caller_path).read()
    caller_filename = os.path.split(caller_path)[1]

    if title is None:
        title = caller_filename

    render_page(
        output_path,
        title=title,
        captured_outputs=captured_outputs,
        figures_base64=figures_base64,
        caller_filename=caller_filename,
        caller_source_code=caller_source_code,
        doc_items=_doc_items
    )

    webbrowser.open("file://" + os.path.abspath(output_path))
