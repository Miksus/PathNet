

import networkx as nx

from bokeh.models import Plot, graphs, ColumnDataSource, Range1d, Circle, HoverTool, BoxZoomTool, ResetTool, WheelZoomTool
from bokeh.io import show as bokeh_show

import matplotlib.pyplot as plt

class BokehMixin:

    def plot(self, show=False):
        "Plot using Bokeh as backend"

        G = nx.from_edgelist(self.edgelist)
        G = nx.DiGraph(G)
        
        plot_data = {"index": list(G.nodes()), 
                  "name": self.labels, "format": self.file_formats,
                  "colors": self.colors}
        
        # Show with Bokeh
        plot = Plot(plot_width=self.fig_size[0]*75, plot_height=self.fig_size[1]*75,
                    x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1))
        plot.title.text = f"Path Network for {self.path}"

        tools = [HoverTool(tooltips=[("name", "@name"), ("format", "@format")]), WheelZoomTool(), ResetTool(), BoxZoomTool()]
        plot.add_tools(*tools)

        graph_renderer = graphs.from_networkx(G, nx.spring_layout, scale=1, center=(0, 0))
        graph_renderer.node_renderer.data_source.data = ColumnDataSource(data=plot_data).data

        graph_renderer.node_renderer.glyph = Circle(size=10, fill_color="colors")

        plot.renderers.append(graph_renderer)

        if show:
            bokeh_show(plot)
        self.graph = G

class NetworkXMixin:

    def plot(self, show=False):
        "Plot using NetworkX default backend"
        plt.figure(figsize=self.fig_size)
        G= nx.from_edgelist(self.edgelist)
        G = nx.DiGraph(G)
        pos = nx.get_node_attributes(G, 'pos')

        nx.draw(G, labels=self.label_map, node_color=self.colors, with_labels=False, arrows=True,
               alpha=0.9, node_shape=".")

        if show:
            plt.show()
        self.graph = G
