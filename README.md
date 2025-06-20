<p align="center">
  <img src="doc/img/classmap.png" alt="ClassMap 继承关系图" width="600"/>
</p>

# ClassMap

ClassMap 是一个 Python 工具，用于分析 Python 项目中的类继承关系和代码引用。它可以：

1. 显示指定类的继承层级（父类和子类）
2. 生成类继承关系的可视化图
3. 查找类或函数在项目中的所有引用位置

## 安装

1. 克隆仓库：
```bash
git clone [repository-url]
cd ClassMap
```

2. 安装包：
```bash
pip install .
```

## 使用方法

### 查找类或函数

```bash
# 在当前目录下查找
classmap find MyClass

# 在指定目录下查找
classmap find MyClass -d /path/to/project
```

这个命令会：
1. 显示类的定义位置（如果存在）
2. 显示类的继承关系（如果是类）
3. 生成继承关系图（如果是类）
4. 显示所有引用位置

## 示例输出

```text
ClassMap
    │
    └── ./classmap/core.py  ── [LINE:9] 

Bases:
Children:
    └── TestMap


References:
    ├── ./classmap/__init__.py
    ├── ./classmap/cli.py
    └── ./classmap/test_map.py


Chained attribute access Call:
    
    TestMap (self.class_map)
        │
        └── ClassMap
    
    TestMap (self.test)
        │
        └── ClassMap
    
    TestMap (self.init())
        │
        └── ClassMap
```

注意：使用此工具需要安装 Graphviz。在 macOS 上可以使用 Homebrew 安装：
```bash
brew install graphviz
```
