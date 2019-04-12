from pathlib import Path
from typing import Dict, List, Tuple, AnyStr

from .backend_mixins import BokehMixin, NetworkXMixin

class PathNet(BokehMixin, NetworkXMixin):
    
    color_files = {
        # source code
        ".py": "yellow",
        ".ipynb": "yellow",
        ".m": "yellow",
        ".r": "yellow",
        ".R": "yellow",
        ".c": "yellow",
        ".h": "yellow",
        ".vb": "yellow",
        ".java": "yellow",
        ".htm": "yellow",
        ".html": "yellow",

        # Programs
        ".exe": "orange",
        ".bin": "orange",
        ".pyc": "orange",
        
        # Data/table files
        ".xlsx": "green",
        ".xls": "green",
        ".xlsm": "green",
        ".xla": "green",
        ".sql": "green",
        ".log": "green",
        ".json": "green",
        ".csv": "green",
        ".dat": "green",

        # Documentation
        ".docx": "blue",
        ".doc": "blue",
        ".pdf": "blue",
        ".txt": "blue",
        ".md": "blue",
        ".dia": "blue",
        ".ppt": "blue",
        ".pptx": "blue",
        
        # Images
        ".png": "cyan",
        ".jpg": "cyan",
        ".jpeg": "cyan",
        ".fig": "cyan",
        ".gif": "cyan",

        # Zip and compressed
        ".zip": "grey",
        ".gzip": "grey",
        ".tgz": "grey",
        ".gz": "grey",

        # Other
        "dir": "white",
        "": "black",
    }
    
    fig_size = [10, 10]
    

    def __init__(self, path, max_files=200, max_depth=20, ignore_hidden=False):
        """Initialize path network
        
        Arguments:
            path {str} -- Path for plotted directory See pathlib
        
        Keyword Arguments:
            max_files {int} -- Maximum files in a directory to be plotted (default: {200})
            max_depth {int} -- Maximum depth of subdirectories plotted (default: {20})
            ignore_hidden {bool} -- Whether to ignore hidden files (starts with ".") (default: {False})
        """

        self.base_path = Path(path)
        self.max_files = max_files
        self.max_depth = max_depth
        self.ignore_hidden = ignore_hidden
        self.edge_paths = set()

    # Core
    def plot(self, backend=None, **kwargs):

        cls_backend = {
            None: NetworkXMixin,
            "bokeh": BokehMixin
        }[backend]

        cls_backend.plot(self, **kwargs)
        
    @property
    def edgelist(self) -> List[Tuple]:
        paths = self.paths
        return [(str(path.parents[0]), str(path)) for path in paths]
        
    @property
    def paths(self) -> List:
        if hasattr(self, "_paths"):
            return self._paths
        base = self.base_path
        base_len = len(base.parts)
 
        paths = []

        if self.ignore_hidden:
            self.edge_paths.update(list(base.rglob('.*')))

        for path in base.rglob('*'):

            is_banned_root = any(str(path).startswith(str(edge_path)) for edge_path in self.edge_paths)
            if is_banned_root:
                continue

            is_too_deep = len(path.parts) - base_len >= self.max_depth if self.max_depth is not None else False
            has_too_many_files = len(list(path.glob("*"))) >= self.max_files if self.max_files is not None else False

            if is_too_deep or has_too_many_files:
                self.edge_paths.update([path])

            paths.append(path)
        self._paths = paths
        return paths

    # Plotting properties
    @property
    def path_sizes(self) -> List:
        return [self.base_path.stat().st_size] + [path.stat().st_size for path in self.paths]

    @property
    def path_formats(self) -> List:
        return ["dir"] + ["dir" if path.is_dir() else path.suffix for path in self.paths]
        
    @property
    def path_labels(self) -> List:
        paths = self.paths
        return [str(self.base_path)] + [path.name if path not in self.edge_paths else f'{path.name}/...' for path in paths]
        
    @property
    def label_map(self) -> Dict[AnyStr, List]:
        paths = self.paths
        return {str(path): path.name if path not in self.edge_paths else f'{path.name}/...' for path in paths}
        
    @property
    def path_colors(self) -> List:
        return ["purple"] + [self.color_files.get("dir" if path.is_dir() else path.suffix, "black") for path in self.paths]