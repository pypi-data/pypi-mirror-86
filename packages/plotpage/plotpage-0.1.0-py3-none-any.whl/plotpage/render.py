
import os
import datetime

from typing import List, Tuple
import jinja2
import markdown2


def render_page(path: str, figures_base64: List[str],
                doc_items: List[Tuple[int, str]], **kwargs: object) -> None:
    content_items: List[Tuple[str, bool]] = []

    for figure_i, figure_base64 in enumerate(figures_base64):
        # Take doc items added before figure with index 'i'
        while len(doc_items) and doc_items[0][0] <= figure_i:
            doc_item = doc_items.pop(0)[1]
            content_items.append((doc_item, False))
        
        content_items.append((figure_base64, True))
    
    content_items.extend((doc_item, False) for _, doc_item in doc_items)

    content_html_elements = [
        (f"<p><img src='data:image/png;base64,{data}' /></p>"
         if is_figure else
         f'<div id="markdown_content">{markdown2.markdown(data)}</div>')
        for data, is_figure in content_items
    ]
    
    output_names = {"stdout": "Output", "stderr": "Output (stderr)"}

    now = datetime.datetime.now()
    
    hljs_css = open(os.path.join(os.path.split(__file__)[0], "highlight-github.css")).read()
    hljs_source = open(os.path.join(os.path.split(__file__)[0], "highlight.pack.js")).read()

    with open(path, "w") as f:
        template = jinja2.Template(_template_string, autoescape=True)
        f.write(template.render(content_items=content_html_elements,
                                output_names=output_names, now=now,
                                hljs_css=hljs_css, hljs_source=hljs_source,
                                **kwargs))

_template_string = """
<html>
<head>
<style>

code {
    border-color: #aaaaaa;
    border-style: solid;
    border-width: 1px;
    width: 750px;
    display: block;
}

#markdown_content {
    width: 750px;
}

body {
    background-color: #eeeeee;
    font-family: Sans-Serif;
}

#wrapper {
    width: 100%;
    text-align: center;
}

#center {
    display: inline-block;
    overflow: hidden;
    text-align: left;
    background-color: #ffffff;
    padding: 20px;
    box-shadow: 0px 0px 12px 1px rgba(87, 87, 87, 0.2);
}

h1, h2, h3, h4, #source_code_toggle:link, #source_code_toggle:visited {
    color: #444444;
}

#source_code_toggle {
    font-weight: normal;
}

h3, h4 {
    margin-top: 2.2em;
}

.timestamp {
    font-size: small;
    font-style: italic;
    color: #777777;
}

.hidden {
    display: none;
}

{{ hljs_css|safe }}
</style>

<script>
{{ hljs_source|safe }}

hljs.initHighlightingOnLoad();
</script>

</head>

<body>

<div id="wrapper">
<div id="center">

<h2>{{ title }}</h2>

<p class="timestamp">Generated at {{ now.strftime('%Y-%m-%d %H:%M:%S') }}</p>

{% for content_item in content_items %}
{{ content_item|safe }}
{% endfor %}

<div>

{% for key, text in captured_outputs.items() %}
    <h3>{{ output_names[key] }}</h3>
    <pre><code class="plaintext">{{ text }}</code></pre>
{% endfor %}

<h3>Source code ({{ caller_filename }}) <a id="source_code_toggle" href="#">show/hide</a></h3>
<pre id="source_code" class="hidden"><code>{{ caller_source_code }}</code></pre>

<script>
document.getElementById("source_code_toggle").onclick = function() {
    document.getElementById('source_code').classList.toggle('hidden');
    return false;
}
</script>

</div>

</body>
</html>
"""
