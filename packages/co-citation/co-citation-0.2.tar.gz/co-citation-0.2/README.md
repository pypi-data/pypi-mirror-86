<!--
SPDX-License-Identifier: GPL-3.0-only
SPDX-FileCopyrightText: 2020 Vincent Lequertier <vi.le@autistici.org>
-->

# Co-citation graph generator

[![REUSE status](https://api.reuse.software/badge/gitlab.com/vi.le/co-citation)](https://api.reuse.software/info/gitlab.com/vi.le/co-citation)
[![pipeline status](https://gitlab.com/vi.le/co-citation/badges/master/pipeline.svg)](https://gitlab.com/vi.le/co-citation/-/commits/master)
[![PyPI version](https://img.shields.io/pypi/v/co-citation.svg)](https://pypi.python.org/pypi/co-citation)

Generate a co-citation graph from an article list in two steps:

1. Get the references of each article and their corresponding journals
2. Generate the co-citation pairs and add them the graph. The weights are the
   number of times the journals are co-cited.

## Example


```python
from co_citation import CoCitation

cites = CoCitation(
    [
        "https://arxiv.org/abs/1602.05112",
    ],
    data_type="journal" # or "article"
)
cites.write_graph_edges("graph")
cites.plot_graph()
```

## Documentation

See [the documentation](http://vi.le.gitlab.io/co-citation/).
