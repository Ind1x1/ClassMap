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



    
