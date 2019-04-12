

import networkx as nx

from bokeh.models import Plot, graphs, ColumnDataSource, Range1d, Circle, HoverTool, BoxZoomTool, ResetTool, WheelZoomTool
from bokeh.io import show as bokeh_show

import matplotlib.pyplot as plt

class BokehMixin:
    
    def plot(self, show=False, kwds_network=None, sizes=False):
        "Plot using Bokeh as backend"
        if kwds_network is None or not "layout_function" in kwds_network:
            kwds_network = dict(layout_function=nx.spring_layout, k=0.05,iterations=100)
        size_marker = "size_marker" if sizes else 10

        G = nx.from_edgelist(self.edgelist)
        G = nx.DiGraph(G)
        
        plot_data = {"index": list(G.nodes()), 
                  "name": self.path_labels, "format": self.path_formats, "size": self.path_sizes,
                  "size_marker": [size / sum(self.path_sizes)*100+5 for size in self.path_sizes],
                  "colors": self.path_colors}
        
        # Show with Bokeh
        plot = Plot(plot_width=self.fig_size[0]*75, plot_height=self.fig_size[1]*75,
                    x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1))
        plot.title.text = f"Path Network for {self.base_path}"

        tools = [HoverTool(tooltips=[("Name", "@name"), ("Format", "@format"), ("Size", "@size")]), WheelZoomTool(), ResetTool(), BoxZoomTool()]
        plot.add_tools(*tools)

        graph_renderer = graphs.from_networkx(G, **kwds_network)
        graph_renderer.node_renderer.data_source.data = ColumnDataSource(data=plot_data).data

        graph_renderer.node_renderer.glyph = Circle(size=size_marker, fill_color="colors")

        plot.renderers.append(graph_renderer)

        self.graph = G
        self.plot_ = plot
        if show:
            bokeh_show(plot)


class NetworkXMixin:

    def plot(self, show=False):
        "Plot using NetworkX default backend"
        plt.figure(figsize=self.fig_size)
        G= nx.from_edgelist(self.edgelist)
        G = nx.DiGraph(G)
        pos = nx.get_node_attributes(G, 'pos')

        nx.draw(G, labels=self.label_map, node_color=self.path_colors, with_labels=False, arrows=True,
               alpha=0.9, node_shape=".")

        if show:
            plt.show()
            
        self.graph = G
