import os
import astroid
import warnings
from graphviz import Digraph

from .mapbase import MapBase
from .contents import INFO_LEVEL
    
class ClassMap:
    """
        最快找到class定义位置
    """
    def __init__(self, class_dir: str = '.'):
        self.class_dir = class_dir
        self.references_file = set[str]()
        self.class_file = None
        self.class_line = None
        self.class_name = None

    def __call__(self, class_name: str, level: INFO_LEVEL):
        match level:
            case INFO_LEVEL.BASE_INFO:
                pass
            case INFO_LEVEL.INVOKE_INFO:
                pass
            case INFO_LEVEL.ALL_INFO:
                self.class_name = class_name
                self._find_class_in_dir(self.class_dir, class_name)
                self._find_references(self.class_dir, class_name)
                self.parse_directory()
                self.show_class_info()

    def _find_class_in_dir(self, dir_path: str, class_name: str) -> tuple[str, int] | None:
        import re
        class_pattern = re.compile(rf'^\s*class\s+{re.escape(class_name)}(\s*\(|\s*:)', re.ASCII)

        ignore_dirs = {'.git', '.svn', '__pycache__', 'venv', 'env', 'node_modules', 'build', 'dist', '.vscode'
                       'tests', 'docker'}

        try:
            with os.scandir(dir_path) as entries:
                for entry in entries:
                    if entry.name.startswith('.') or (entry.is_dir() and entry.name in ignore_dirs):
                        continue
                    if entry.is_dir():
                        result = self._find_class_in_dir(entry.path, class_name)
                        if result:
                            return result
                    elif entry.name.endswith('.py'):
                        try:
                            with open(entry.path, 'r', encoding='utf-8', errors='ignore') as f:
                                for lineno, line in enumerate(f, 1):
                                    if class_pattern.match(line):
                                        self.class_file = entry.path
                                        self.class_line = lineno
                                        return self.class_file, self.class_line
                        except Exception as e:
                            print(f"Error reading file {entry.path}: {e}")
            return None
        except Exception as e:
            print(f"Error accessing directory {dir_path}: {e}")
            return None
    
    def _find_references(self, class_dir: str, class_name: str) -> set[str]:
        import re
        import_pattern = re.compile(rf'(^|\s)import\s+.*\b{re.escape(class_name)}\b|(^|\s)from\s+.*\bimport\s+.*\b{re.escape(class_name)}\b')
        self.references_file.clear()
        ignore_dirs = {'.git', '.svn', '__pycache__', 'venv', 'env', 'node_modules', 'build', 'dist', '.vscode',
                       'tests', 'docker'}
        def scan_dir(dir_path):
            try:
                with os.scandir(dir_path) as entries:
                    for entry in entries:
                        if entry.name.startswith('.') or (entry.is_dir() and entry.name in ignore_dirs):
                            continue
                        if entry.is_dir():
                            scan_dir(entry.path)
                        elif entry.name.endswith('.py'):
                            try:
                                with open(entry.path, 'r', encoding='utf-8', errors='ignore') as f:
                                    for line in f:
                                        if import_pattern.search(line):
                                            self.references_file.add(entry.path)
                                            break
                            except Exception as e:
                                print(f"Error reading file {entry.path}: {e}")
            except Exception as e:
                print(f"Error accessing directory {dir_path}: {e}")
        scan_dir(class_dir)
        return self.references_file
    
    def print_references(self,index: set[str]):
        if not index:
            print("No references found")
            return
        print("\n")
        print("References:")
        for i, path in enumerate(sorted(index)):
            prefix = "    └── " if i == len(index)-1 else "    ├── "
            print(f"{prefix}{path}")

    def print_references_tree(self, index: set[str]):

        def _build_tree(paths):
            tree = {}
            for path in paths:
                parts = os.path.relpath(path, self.class_dir).split(os.sep)
                node = tree
                for part in parts:
                    node = node.setdefault(part, {})
            return tree

        def print_tree(node, prefix=""):
            items = list(node.items())
            for i, (name, child) in enumerate(items):
                connector = "└── " if i == len(items) - 1 else "├── "
                print(prefix + connector + name)
                if child:
                    extension = "    " if i == len(items) - 1 else "│   "
                    print_tree(child, prefix + extension)

        if not index:
            print("No references found")
            return
        
        print("References:")
        tree = _build_tree(index)
        print_tree(tree)

    def print_bases_and_children(self, class_map: MapBase):
        print(f"Bases:")
        for i, base in enumerate(sorted(class_map.bases)):
            prefix = "    └── " if i == len(class_map.bases)-1 else "    ├── "
            print(f"{prefix}{base}")
        print(f"Children:")
        for i, child in enumerate(sorted(class_map.children)):
            prefix = "    └── " if i == len(class_map.children)-1 else "    ├── "
            print(f"{prefix}{child}")

    def print_class(self, class_name: str, class_file: str, class_line: int):
        print("\n")
        print(f"{class_name}")
        print(f"    │")
        print(f"    └── {class_file}  ── [LINE:{class_line}] \n")
    
    def show_class_info(self):
        self.print_class(self.class_name, self.class_file, self.class_line)
        self.print_bases_and_children(self.class_map)
        # self.print_references_tree(self.references_file)
        self.print_references(self.references_file)
        print("\n")

    def parse_file(self, file_path: str) -> None:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            with warnings.catch_warnings():
                    warnings.simplefilter("ignore", SyntaxWarning)
                    module = astroid.parse(content, path=file_path)
                
            self._process_module(module, file_path)
        except SyntaxError as e:
            print(f"Grammatical error - file {file_path}: {e}")
        except Exception as e:
            print(f"An Error occurred when parsing the {file_path} : {e}")

    def _process_module(self, module, file_path):
        for node in module.body:
            if isinstance(node, astroid.ClassDef):
                print(f"node: {node.name}")
                print(f"node.bases: {node.bases}")
                self._process_class(node, file_path)

    def _process_class(self, node, file_path):
        self.__children_info(node)
        print(f"类 {node.name} 的实例变量（self.xxx）及赋值：")
        for init in node.body:
            if isinstance(init, astroid.FunctionDef) and init.name == "__init__":
                print(init)
                for assign in init.body:
                    if isinstance(assign, astroid.Assign):
                        print(assign)

    def __children_info(self, node):
        for base in node.bases:
            if base.as_string() == self.class_name:
                self.class_map._Add_children(node.name)

    def ___bases_info(self, module, file_path):
        for node in module.body:
            if isinstance(node, astroid.ClassDef) and node.name == self.class_name:
                for base in node.bases:
                    self.class_map._Add_bases(base.as_string())

    def __bases_info(self, file_path: str):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            with warnings.catch_warnings():
                    warnings.simplefilter("ignore", SyntaxWarning)
                    module = astroid.parse(content, path=file_path)
                
            self.___bases_info(module, file_path)

        except SyntaxError as e:
            print(f"Grammatical error - file {file_path}: {e}")
        except Exception as e:
            print(f"An Error occurred when parsing the {file_path} : {e}")

    def parse_directory(self) -> None:
        self.class_map = MapBase(
            file_path = self.class_file,
            classname = self.class_name,
            bases = [],
            children = []
        )
        self.__bases_info(self.class_file)
        for i, path in enumerate(sorted(self.references_file)):
            self.parse_file(path)