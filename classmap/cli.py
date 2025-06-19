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
import sys
import argparse
from .core import ClassMap
from .contents import INFO_LEVEL

def main():
    parser = argparse.ArgumentParser(description='分析Python代码中的类关系和引用')
    parser.add_argument('command', choices=['find'], help='要执行的命令')
    parser.add_argument('name', help='要查找的类名或函数名')
    parser.add_argument('-d', '--directory', default='.', help='要分析的目录路径（默认为当前目录）')
    
    args = parser.parse_args()
    
    # class_map = ClassMap(directory=args.directory)
    
    if args.command == 'find':
        finder = ClassMap(args.directory)
        finder(args.name, INFO_LEVEL.ALL_INFO)
        
if __name__ == '__main__':
    main()