from pathlib import Path
from typing import Dict, List, Tuple, AnyStr

from .backend_mixins import BokehMixin, NetworkXMixin

class PathNet(BokehMixin, NetworkXMixin):
    
    color_files = {
        ".py": "yellow",
        ".xlsx": "green",
        ".docx": "blue",
        ".txt": "blue",
        ".pdf": "blue",
        
        ".png": "pink",
        ".jpg": "pink",
        "": "white"
    }
    
    fig_size = [10, 10]
    

    def __init__(self, path, max_files=200, max_depth=20):
        self.path = path
        self.max_files = max_files
        self.max_depth = max_depth
        
        self.edge_paths = set()

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
    def file_formats(self) -> List:
        return [""] +[path.suffix for path in self.paths]
        
    @property
    def labels(self) -> List:
        paths = self.paths
        return [self.path] + [path.name if path not in self.edge_paths else f'{path.name}/...' for path in paths]
        
    @property
    def label_map(self) -> Dict[AnyStr, List]:
        paths = self.paths
        return {str(path): path.name if path not in self.edge_paths else f'{path.name}/...' for path in paths}
        
    @property
    def colors(self) -> List:
        return ["purple"] + [self.color_files.get(path.suffix, "black") for path in self.paths]
        
    @property
    def paths(self) -> List:
        if hasattr(self, "_paths"):
            return self._paths
        base = Path(self.path)
        base_len = len(base.parts)
 
        paths = []
        
        for path in base.rglob('*'):

            is_cut_off = any(str(edge_path) in str(path) for edge_path in self.edge_paths)
            if is_cut_off:
                continue

            is_too_deep = len(path.parts) - base_len >= self.max_depth if self.max_depth is not None else False
            has_too_many_files = len(list(path.glob("*"))) >= self.max_files if self.max_files is not None else False

            if is_too_deep or has_too_many_files:
                self.edge_paths.update([path])

            paths.append(path)
        self._paths = paths
        return paths

