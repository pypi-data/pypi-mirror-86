import logging
import pathlib
import textwrap
from typing import Optional, Tuple

import mkdocs.utils
from jinja2 import BaseLoader, Environment

__all__ = ["TemplateRewritingLoader"]


log = logging.getLogger(f"mkdocs.plugins.{__name__}")
log.addFilter(mkdocs.utils.warning_filter)


class TemplateRewritingLoader(BaseLoader):
    def __init__(self, loader: BaseLoader):
        self.loader = loader
        self.found_supported_theme = False

    def get_source(self, environment: Environment, template: str) -> Tuple[str, str, bool]:
        src, filename, uptodate = self.loader.get_source(environment, template)
        old_src = src
        path = pathlib.Path(filename).as_posix()

        if path.endswith("/material/partials/nav-item.html"):
            src = _transform_material_nav_item_template(src)
        elif path.endswith("/themes/readthedocs/base.html"):
            src = _transform_readthedocs_base_template(src)
        else:
            return src, filename, uptodate
        self.found_supported_theme = True

        if old_src == src:
            log.warning(
                f"Failed to adapt the theme file '{filename}'. "
                f"This is likely a bug in mkdocs-section-index, and things won't work as expected."
            )
        return src, filename, uptodate


def _transform_material_nav_item_template(src: str) -> str:
    repl = """\
        {% if nav_item.url %}
          <a href="{{ nav_item.url | url }}"{% if nav_item == page %} class="md-nav__link--active"{% endif %}>
        {% endif %}
          [...]
        {% if nav_item.url %}</a>{% endif %}
    """
    lines = src.split("\n")
    for i, line in enumerate(lines):
        if line.endswith("{{ nav_item.title }}") and "href=" not in lines[i - 1]:
            lines[i] = _replace_line(lines[i], repl)
    return "\n".join(lines)


def _transform_readthedocs_base_template(src: str) -> str:
    repl = """\
        {% if nav_item.url %}
            <ul><li{% if nav_item == page %} class="current"{% endif %}>
                <a href="{{ nav_item.url|url }}" style="padding: 0; font-size: inherit; line-height: inherit">
        {% endif %}
                [...]
        {% if nav_item.url %}
                </a>
            </li></ul>
        {% endif %}
    """
    lines = src.split("\n")
    for i, line in enumerate(lines):
        if "{{ nav_item.title }}" in line:
            lines[i] = _replace_line(lines[i], repl)
    return "\n".join(lines)


def _replace_line(line: str, wrapper: str, new_line: Optional[str] = None) -> str:
    leading_space = line[: -len(line.lstrip())]
    if new_line is None:
        new_line = line.lstrip()
    new_text = textwrap.dedent(wrapper.rstrip()).replace("[...]", new_line)
    return textwrap.indent(new_text, leading_space)
