# ClassMap (a) 2025 Leyi Ye
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

class MapBase:
    def __init__(self, file_path: str, classname: str, bases: set[str] = None, children: set[str] = None):
        self.file_path: str = file_path
        self.classname = classname
        self.bases: set[str] = set(bases) if bases is not None else set()
        self.children: set[str] = set(children) if children is not None else set()

    def _Add_bases(self, base: str) -> bool:
        if base not in self.bases:
            self.bases.add(base)
            return True
        return False

    def _Add_children(self, child: str) -> bool:
        if child not in self.children:
            self.children.add(child)
            return True
        return False

class ChainBase:
    def __init__(self, class_name: str, parent = None, child = None):
        self.class_name:str = class_name       # 类名
        
        self.parent_list: list[ChainBase] = []
        self.child_list: list[ChainBase] = []

        self.parent_access_list: list[dict] = []
        self.child_access_list: list[dict] = []

        self.parent:ChainBase | None  = parent # 父层次
        self.child:ChainBase | None = child    # 子层次

        self.parent_access: dict | None = None   # 父类访问
        self.child_access: dict | None = None    # 子类访问

    def add_parent(self, parent: str, assess: str):
        chainparent = ChainBase(class_name=parent)
        _add_parent(self, chainparent, parent, assess)
        _add_child(chainparent, self, self.class_name, assess)

    def add_child(self, child: str, assess: str):
        childchain = ChainBase(class_name=child)
        _add_parent(self, childchain, self.class_name, assess)
        _add_child(childchain, self, child, assess)


def _add_child(chain: ChainBase, childchain:ChainBase, child: str, assess:str):
    chain.child = childchain
    if chain.child_access is None:
        chain.child_access = {}
    chain.child_access[child] = assess
    chain.child_list.append(childchain)
    chain.child_access_list.append({child: assess})


def _add_parent(chain: ChainBase, chainparent: ChainBase, parent: str, assess: str):
    chain.parent = chainparent
    if chain.parent_access is None:
        chain.parent_access = {}
    chain.parent_access[parent] = assess
    chain.parent_list.append(chainparent)
    chain.parent_access_list.append({parent: assess})

    
