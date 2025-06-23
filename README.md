<p align="center">
  <img src="doc/img/classmap.png" alt="ClassMap 继承关系图" width="600"/>
</p>

[中文说明 🇨🇳](./README_zh.md)
#
ClassMap is a Python tool based on *astroid*, used to analyze class inheritance and code references within Python projects. It can:

- Display the inheritance hierarchy (both parents and subclasses) of a specified class

- Generate a visualization of class inheritance relationships

- Find all reference locations of classes or functions within the project



## Install

1. clone：
```bash
git clone git@github.com:Ind1x1/ClassMap.git
cd ClassMap
```

2. install：
```bash
pip install .
```

## Start to use

### Find class/function

```bash
# Search in the current directory
classmap find MyClass

# Search in the specified directory
classmap find MyClass -d /path/to/project
```

What this command does:

- Displays the location of the class definition (if it exists)

- Displays the class's inheritance hierarchy (if applicable)

- Generates an inheritance diagram (if applicable)

- Lists all places where the class is referenced

## Output Example

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

Note: Using this tool requires Graphviz to be installed. On macOS, you can install it using Homebrew:
```bash
brew install graphviz
```

## Under development

**Matching based on class name**

May have trouble dealing with the following cases：

```text
    class A:
        def __init__(a):
            self.a = a
```

```text
    class A:
        def __init__(a):
            if a:
                self.a = a
            efif b:
                self.a = b
```

**Supports recursive search of classes**
