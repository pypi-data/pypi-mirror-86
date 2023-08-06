# SPDX-License-Identifier: GPL-3.0-only
# SPDX-FileCopyrightText: 2020 Vincent Lequertier <vi.le@autistici.org>

from collections import Counter
import time
from typing import Dict, List, Union
from bs4 import BeautifulSoup
import networkx as nx
import requests
from matplotlib import cm
from matplotlib.colors import to_hex
import numpy as np
import plotly.colors
import plotly.graph_objects as go
from sklearn import preprocessing


class CoCitation:
    """
    Create a co-citation graph

    """

    def __init__(
        self,
        articles_list: List[str],
        sd_api_key: str = "",
        graph: str = "",
        wait=None,
        data_type="journal",
    ):
        """
        Instantiate the co-citation graph

        Args:
            articles_list (list): The list of articles URL. At the moment only arXiv,
            ScienceDirect and PubMed are supported
            sd_api_key (str): The key to query the ScienceDirect API
            graph (str): A saved netowrkx weighted graph file (optional)
            wait (int): Number of seconds to wait between API call to workaround
            API call thresholds( optional)
            data_type (str): Type of data (journal or article)
        """
        self.sd_api_key = sd_api_key
        self.abbreviations = self.load_abbreviations()
        self.wait = wait
        self.type = data_type

        if not sd_api_key and any(
            ["sciencedirect" in article_url for article_url in articles_list]
        ):
            raise ValueError(
                "Missing ScienceDirect API key and at least one article is from ScienceDirect"
            )

        if graph:
            self.co_citation_graph = nx.read_weighted_edgelist(
                graph, nodetype=str, delimiter="\t"
            )
        else:
            self.co_citation_graph = self.create_citation_graph(articles_list)

    @staticmethod
    def load_abbreviations() -> Dict[str, str]:
        """
        Get journal abbreviations

        Returns:
            dict: The abbreviations
        """
        abbreviations = {}
        with open("abbreviations.txt", "r") as fh:
            for line in fh.readlines():
                k, v = line.split("\t")
                abbreviations[k.lower()] = v.strip()

        return abbreviations

    def create_citation_graph(self, articles_list: List[str]) -> nx.Graph:
        """
        1. Get the references of each article and their corresponding journals
        2. Generate the co-citation pairs and add them the graph. The weights are the\
        number of times the journals are co-cited.

        Args:
            articles_list (list): The list of articles URL. At the moment only arXiv,
                ScienceDirect and PubMed are supported

        Returns:
            list: The pairs
        """
        graph = nx.Graph()
        for article in articles_list:
            if self.wait:
                time.sleep(self.wait)
            citations = self.get_citations(article)
            citations = list(filter(lambda c: c != "", citations))
            pairs = self.gen_perms(citations)
            for j1, j2, w in pairs:
                graph.add_edge(
                    j1,
                    j2,
                    weight=w
                    if not graph.has_edge(j1, j2)
                    else graph[j1][j2]["weight"] + w,
                )

        return graph

    @staticmethod
    def gen_perms(citations: List[str]) -> List[List[Union[str, int]]]:
        """
        Get all pair commutative permutations of a list

        Args:
            citations (list): The list of journal citations
        Returns:
            list: The pairs
        """
        pairs = []
        counts = Counter(citations)
        for i in range(len(citations)):
            for j in range(i + 1, len(citations)):
                pairs.append(
                    [
                        citations[i],
                        citations[j],
                        min(counts[citations[i]], counts[citations[j]]),
                    ]
                )

        return pairs

    def get_article_title_pubmed(self, article_url: str) -> str:
        """
        Get the title of a pubmed article

        Args:
            article_url (str): The URL of the article.
        Returns:
            str: The article's title
        """

        pmid = article_url.split("/")[-1]
        url = (
            "https://www.ncbi.nlm.nih.gov/entrez/eutils/efetch.cgi?db=pubmed&retmode=xml&id="
            + pmid
        )
        xml_parsed = BeautifulSoup(requests.get(url).text, features="lxml")
        authors = xml_parsed.find_all("author")
        year = xml_parsed.find("year").text
        if len(authors) > 2:
            return (
                authors[0].initials.text
                + ". "
                + authors[0].lastname.text
                + " et al. ("
                + year
                + ")"
            )
        else:
            return (
                " and ".join(
                    [
                        author.initials.text + ". " + author.lastname.text
                        for author in authors
                    ]
                )
                + " "
                + year.join(["(", ")"])
            )

    def get_article_title_sem_scholar(self, ref: dict) -> str:
        """
        Get the title of an article indexed in semanticscholar

        Args:
            ref (list[str]): An article reference
        Returns:
            str: The article's title
        """
        if len(ref["authors"]) > 2:
            return (
                ref["authors"][0]["name"]
                + " et al. "
                + str(ref["year"]).join(["(", ")"])
            )
        else:
            return (
                " and ".join([author["name"] for author in ref["authors"]])
                + " "
                + str(ref["year"]).join(["(", ")"])
            )

    def get_journal_pubmed(self, article_url: str) -> Union[str, "NotImplemented"]:
        """
        Get the journal of an article

        Args:
            article_url (str): The URL of the article. At the moment only arXiv,
                ScienceDirect and PubMed are supported
        Returns:
            str: The journal's name
        """
        pmid = article_url.split("/")[-1]
        url = (
            "https://www.ncbi.nlm.nih.gov/entrez/eutils/efetch.cgi?db=pubmed&retmode=xml&id="
            + pmid
        )
        return (
            BeautifulSoup(requests.get(url).text, features="lxml")
            .find("isoabbreviation")
            .text
        )

    def get_journal_sem_scholar(self, ref: dict) -> Union[str, "NotImplemented"]:
        """
        Get the journal of an article

        Args:
            ref (str): A semanticscholar referece
        Returns:
            str: The journal's name
        """
        return (
            self.abbreviations[ref["venue"].lower()]
            if ref["venue"].lower() in self.abbreviations
            else ref["venue"]
        )

    def get_citations(self, article_url: str) -> List[str]:
        """
        Get all citations data for an article

        This function does two things:

        1. Get the citations
        2. For each citation, get the data (journal or artilce)

        Args:
            article_url (str): The URL of the article. At the moment only arXiv,
                ScienceDirect and PubMed are supported
        Returns:
            list: The list of citations
        """
        if (
            "pubmed" not in article_url
            and "arxiv" not in article_url
            and "sciencedirect" not in article_url
        ):
            raise NotImplementedError("URL {} not implemented".format(article_url))
        if "pubmed" in article_url:
            pmid = article_url.split("/")[-1]
            url = (
                "https://www.ncbi.nlm.nih.gov/entrez/eutils/elink.cgi?db=pubmed&linkname=pubmed_pubmed&retmode=xml&id="
                + pmid
            )
            if self.type == "journal":
                return [
                    self.get_journal_pubmed(
                        "https://www.ncbi.nlm.nih.gov/pubmed/" + idx.text
                    )
                    for idx in BeautifulSoup(
                        requests.get(url).text, features="lxml"
                    ).linksetdb.find_all("id")
                    if self.wait is None
                    or (self.wait is not None and time.sleep(self.wait) is None)
                ]
            else:
                return [
                    self.get_article_title_pubmed(
                        "https://www.ncbi.nlm.nih.gov/pubmed/" + idx.text
                    )
                    for idx in BeautifulSoup(
                        requests.get(url).text, features="lxml"
                    ).linksetdb.find_all("id")
                    if self.wait is None
                    or (self.wait is not None and time.sleep(self.wait) is None)
                ]
        if "arxiv" in article_url:
            idx = article_url.split("/")[-1].rstrip()
            url = "https://api.semanticscholar.org/v1/paper/arxiv:" + idx
            refs = requests.get(url).json()["references"]
        if "sciencedirect" in article_url:
            pii = article_url.split("/")[-1].rstrip()
            doi = (
                BeautifulSoup(
                    requests.get(
                        "https://api.elsevier.com/content/article/pii/"
                        + pii
                        + "?httpAccept=text/xml&APIKey="
                        + self.sd_api_key
                    ).text,
                    features="lxml",
                )
                .find("prism:doi")
                .text
            )
            url = "https://api.semanticscholar.org/v1/paper/" + doi
            refs = requests.get(url).json()["references"]

        if self.type == "journal":
            return [self.get_journal_sem_scholar(ref) for ref in refs]
        else:
            return [self.get_article_title_sem_scholar(ref) for ref in refs]

    def get_edge_trace(self) -> List[go.Scatter]:
        """
        Generate the edges trace. The colors corresponds to the edge weights

        Returns:
            list: The list of edges trace
        """

        edges_trace = []
        greys = cm.get_cmap("Greys", 12)
        weights = [
            edge[2]["weight"] for edge in self.co_citation_graph.edges(data=True)
        ]
        weights = (
            preprocessing.normalize(np.array(weights).reshape(1, -1)) * 50
        ).flatten()
        colors = greys(weights)
        for idx, edge in enumerate(self.co_citation_graph.edges(data=True)):
            x0, y0 = self.co_citation_graph.nodes[edge[0]]["pos"]
            x1, y1 = self.co_citation_graph.nodes[edge[1]]["pos"]
            edges_trace.append(
                go.Scatter(
                    x=[x0, x1, None],
                    y=[y0, y1, None],
                    mode="lines",
                    line=dict(width=1.5, color=to_hex(colors[idx])),
                )
            )

        return edges_trace

    def get_node_trace(self) -> dict:
        """
        Generate the nodes trace. The colors corresponds to the sum edge weights
        connected to the noes

        Returns:
            dict: The nodes trace
        """
        node_x = []
        node_y = []
        for node in self.co_citation_graph.nodes():
            x, y = self.co_citation_graph.nodes[node]["pos"]
            node_x.append(x)
            node_y.append(y)

        node_sizes = []

        for n in self.co_citation_graph.nodes:
            node_sizes.append(
                sum(
                    self.co_citation_graph[n][neighbor]["weight"]
                    for neighbor in list(self.co_citation_graph.neighbors(n))
                )
            )
        return dict(
            x=node_x,
            type="scatter",
            y=node_y,
            text=list(self.co_citation_graph.nodes),
            textposition="top center",
            mode="markers+text",
            textfont={"family": "sans serif", "size": 21, "color": "#000000"},
            marker=dict(
                colorscale=plotly.colors.sequential.Greys[2:],
                reversescale=False,
                color=node_sizes,
                size=16,
                line_width=0,
                line=None,
            ),
        )

    def plot_graph(self, display=True) -> None:
        """
        Plot the co-citation graph

        Args:
            display (bool): If True, view the plot in a web browser, else write
                the plot to disk

        """

        pos = nx.spring_layout(self.co_citation_graph, k=20)
        nx.set_node_attributes(self.co_citation_graph, pos, "pos")

        edges_trace = self.get_edge_trace()
        node_trace = self.get_node_trace()

        fig = go.Figure(
            data=edges_trace + [node_trace],
            layout=go.Layout(
                title={
                    "text": "Co-citation graph",
                    "y": 0.9999,
                    "x": 0.5,
                    "font_size": 30,
                    "font": {"family": "sans serif", "color": "#000000"},
                    "xanchor": "center",
                    "yanchor": "top",
                },
                showlegend=False,
                plot_bgcolor="rgba(26,150,65,0.0)",
                hovermode="closest",
                margin=dict(b=40, l=5, r=5, t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            ),
        )

        if display:
            fig.show()
        else:
            fig.write_image("co-citation-graph.png", scale=2, width=1980, height=1200)

    def filter_low_co_citations(self, criteria: int) -> None:
        """
        Remove low weight edges and isolated nodes

        Args:
            criteria (int): The weight minimum in the resulting graph
        """
        self.co_citation_graph.remove_edges_from(
            [
                e[:2]
                for e in list(
                    filter(
                        lambda e: e[2]["weight"] < criteria,
                        self.co_citation_graph.edges(data=True),
                    )
                )
            ]
        )
        self.co_citation_graph.remove_nodes_from(
            list(nx.isolates(self.co_citation_graph))
        )

    def write_graph_edges(self, filename: str) -> None:
        """
        Write the edge list to a file

        Args:
            filename (str): The path to the file
        """
        nx.write_weighted_edgelist(
            self.co_citation_graph, filename, "utf-8", delimiter="\t"
        )
