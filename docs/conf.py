# SPDX-FileCopyrightText: © 2025 Tenstorrent Inc.
#
# SPDX-License-Identifier: Apache-2.0

import collections
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.abspath("."))

from docs_versions import get_published_versions

SphinxConfig = collections.namedtuple("SphinxConfig", ["fullname", "shortname"])

sphinx_config = SphinxConfig(fullname="TT-XLA", shortname="tt-xla")

project = sphinx_config.fullname
copyright = "2025, Tenstorrent"
author = "Tenstorrent"

extensions = [
    "sphinx.ext.mathjax",
    "sphinx_sitemap",
    "myst_parser",
]

sitemap_locales = [None]
sitemap_url_scheme = "{link}"

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

myst_enable_extensions = [
    "colon_fence",
    "deflist",
]

myst_heading_anchors = 3

exclude_patterns = [
    "CMakeLists.txt",
    "doxygen.cfg.in",
    "bisect_improvements.md",
    "Thumbs.db",
    ".DS_Store",
]

html_theme = "sphinx_rtd_theme"
html_logo = "shared/images/tt_logo.svg"
html_favicon = "shared/images/favicon.png"
html_static_path = ["shared/_static"]
html_extra_path = []
templates_path = ["shared/_templates"]
html_last_updated_fmt = "%b %d, %Y"

html_baseurl = os.environ.get(
    "DOCS_HTML_BASEURL",
    "https://docs.tenstorrent.com/tt-xla",
).rstrip("/")

_docs_version = os.environ.get("DOCS_VERSION", "latest").strip()
_docs_site_base = os.environ.get(
    "DOC_SITE_BASE_URL",
    "https://tenstorrent.github.io/tt-xla",
).rstrip("/")

html_context = {
    "logo_link_url": "https://docs.tenstorrent.com/",
    "versions": get_published_versions(Path(__file__)),
    "current_version": _docs_version,
    "docs_site_base": _docs_site_base,
}


def setup(app):
    app.add_css_file("tt_theme.css")

