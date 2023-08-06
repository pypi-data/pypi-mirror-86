
# relpath

下の方に日本語の説明があります<br>
底下有中文解释。

## Summary (Explanation in English)
Features of this package
1. you can use the relative path intuitively
    - The standard relative path in python is not intuitive.
2. you can import various modules relatively
    - It can handle complex projects where the folders are nested.

## Usage #1: A basic example

Example of getting the directory (location) of the python file itself

```python
from relpath import rel2abs
print(rel2abs("./")) # -> "(The directory this python file belongs to)"
```

## Usage #2: A Practical Example

A practical use case for this tool

```
.
`-- project_folder
    |-- parts
    |   |-- data.txt
    |   `-- script_B.py
    `-- script_A.py
```

As shown above, consider a project with multiple python files.
In `script_A.py`, we will use `script_B.py` as shown below.

```python
# script_A.py

# load script_B.py
from parts.script_B import get_data

print(get_data())
```

In this case, if you try to refer to `"./data.txt"` relatively from `script_B.py`, as shown in the following code example, it will fail. (Note 1)

```
(Note 1)
Strictly speaking, you can load it by specifying a relative path from `script_A.py`,
but if the caller is changed to another location, it won't work properly and is not easy to maintain.
To avoid this, we recommend using the `relpath` package.
```

```python
# script_B.py

def get_data():
    with open("./data.txt", "r") as f:  # -> FileNotFoundError: [Errno 2] No such file or directory: './data.txt'
        return f.read()
```

On the other hand, you can use the `relpath` package and write the following to refer to `"./data.txt"` relatively. (Note 2)

```python
# script_B.py

from relpath import rel2abs

def get_data():
    with open(rel2abs("./data.txt"), "r") as f:  # -> NO ERROR!!
        return f.read()
```

```
(Note 2)
The python specification of relative paths is not necessarily wrong.
Under the python specification, a relative path is always interpreted with the first executed python file as the reference position.
So users have to be aware of the position of the first executed python file
when writing a relative path.
On the other hand, the python specification has an advantage:
if the file containing the path is moved, you don't have to change the path.
The `relpath` package is just another way to give the programmer another option besides the python specification,
so we recommend that you consider whether to use it or not depending on the situation.
```

## Usage #3: Relative import example

The `relpath` package provides an intuitive relative import of a module, as shown in the following example.

```python
from relpath import add_import_path
add_import_path("../")

from my_module import some_function

some_function()
```

Why do I need to write like the above example? Can't I just write `sys.path.append("../")`?
As a matter of fact, `sys.path.append("../")` does not work well if your project folder has a complex hierarchical structure where one module is used from different locations.
Therefore, it is recommended to use the `add_import_path` of the `relpath` package whenever you want to implement relative import.

`add_import_path("../")` is internally equivalent to `sys.path.append(rel2abs("../"))`.

---

## 概要 (日本語)
このパッケージでできること:
1. 直感的な相対パス参照ができる
	- pythonのパス参照の仕様は直感に反する
2. モジュールの相対importに使える
	- フォルダが多重で複雑なプロジェクトにも対応できる

## 使い方1: 基本的な例

下記は、pythonファイル自身の場所(ディレクトリ)を取得する例です。

```python
from relpath import rel2abs
print(rel2abs("./"))	# -> "(このpythonファイルが存在するディレクトリ)"
```

## 使い方2: 実用的な例

このツールは、下記のような場合に真価を発揮します。

```
.
`-- project_folder
    |-- parts
    |   |-- data.txt
    |   `-- script_B.py
    `-- script_A.py
```

上記のように、複数のpythonファイルからなるプロジェクトを考えます。
`script_A.py`の中では下記のように、`script_B.py`を利用します。

```python
# script_A.py

# load script_B.py
from parts.script_B import get_data

print(get_data())
```

この場合に、下記のコード例のように、
`script_B.py`から"./data.txt"を相対的に読み込もうとすると失敗します。(注1)

```
(注1)
厳密には、`script_A.py`からの相対パス指定をすれば読み込めますが、
呼び出し元が別の場所に変更された場合、正常に動作しなくなるので、メンテナンス性が悪くなります。
これを回避するため、`relpath`パッケージの利用を推奨します。
```

```python
# script_B.py

def get_data():
    with open("./data.txt", "r") as f:  # -> FileNotFoundError: [Errno 2] No such file or directory: './data.txt'
        return f.read()
```

そこで、`relpath`パッケージを使って下記のように書くと、
`"./data.txt"`を相対的に読み込めるようになります。(注2)

```python
# script_B.py

from relpath import rel2abs

def get_data():
    with open(rel2abs("./data.txt"), "r") as f:  # -> NO ERROR!!
        return f.read()
```

```
(注2)
相対パスに関するpythonの仕様は、必ずしも間違いというわけではありません。
pythonの仕様(相対パスの指定が、記述するファイルの場所に関わらず、常に最初の呼び出し元を基準として解釈される仕様)には、
プログラムを開発する中でもしファイル読み込み等の命令を記述する場所(ファイル)が変更になった場合でも、
パス指定方法の変更が不要になるという利点があります。
`relpath`パッケージは、pythonの仕様の他に、プログラマーにもう一つの選択肢を与える手段に過ぎないので、
状況に応じて利用の要否を検討することを推奨します。
```

## 使い方3: 相対importとしての利用

`relpath`パッケージを利用すると、下記の例のように、
モジュールの直感的な相対importを実現できます。

```python
from relpath import add_import_path
add_import_path("../")

from my_module import some_function

some_function()
```

上記の例を見ると、単に`sys.path.append("../")`としても動作するように思われます。
しかし、プロジェクトフォルダの階層構造が複雑で、1つのモジュールが別々の場所から使われるような場合には、`sys.path.append("../")`では対応できないことがあります。
そのため、相対importを実現したいときは、常に`relpath`パッケージの`add_import_path`を利用することを推奨します。

なお、`add_import_path("../")`
は、内部的には`sys.path.append(rel2abs("../"))`と等価です。

---

## 摘要 (中文解释)

本套餐的特点

1. 你可以直观地使用相对路径。
    - python中标准的相对路径并不直观。
2. 可以相对导入各种模块
    - 它可以处理文件夹嵌套的复杂项目。

## 用法 #1: 一个基本的例子

获取python文件本身的目录（位置）的例子

```python
from relpath import rel2abs
print(rel2abs("./")) # -> "(这个python文件所属的目录)"
```

## 用法 ＃2: 一个实际例子

该工具的实际使用案例

```
.
`-- project_folder
    |-- parts
    |   |-- data.txt
    |   `-- script_B.py
    `-- script_A.py
```

如上图所示，考虑一个有多个python文件的项目。
在`script_A.py`中，我们将使用`script_B.py`，如下所示。

```python
# script_A.py

# load script_B.py
from parts.script_B import get_data

print(get_data())
```

在这种情况下，如果你试图从`script_B.py`中相对引用`"./data.txt"`，如下面的代码示例所示，它将失败。 (注1)

```
(注1)
严格来说，你可以通过指定`script_A.py`的相对路径来加载，
但如果调用者换到其他位置，就不能正常工作，而且不容易维护。
为了避免这种情况，我们建议使用`relpath`包。
```

```python
# script_B.py

def get_data():
    with open("./data.txt", "r") as f:  # -> FileNotFoundError: [Errno 2] No such file or directory: './data.txt'
        return f.read()
```

另一方面，你可以使用`relpath`包，并写下以下内容来相对引用`"./data.txt"`。 (注2)

```python
# script_B.py

from relpath import rel2abs

def get_data():
    with open(rel2abs("./data.txt"), "r") as f:  # -> NO ERROR!!
        return f.read()
```

```
(注2)
相对路径的python规范不一定是错的。
在python规范下，相对路径总是被理解为相对于第一个执行的Python文件作为参考位置。
所以用户在写相对路径的时候，要注意第一个执行的python文件的位置。
另一方面，python规范至少有一个优点。
其优点是，当移动包含路径的文件时，不需要改变路径。
`relpath`包只是给程序员在python规范之外的另一种选择，所以建议大家根据实际情况考虑是否使用。
```

## 用法 #3: 相对导入示例

`relpath`包提供了一个直观的模块相对导入，如下例所示。

```python
from relpath import add_import_path
add_import_path("../")

from my_module import some_function

some_function()
```

为什么要写成上面的例子？ 我不能直接写`sys.path.append("../")`吗？
事实上，如果你的项目文件夹具有复杂的层次结构，一个模块从不同的位置使用，`sys.path.append("../")`就不能很好地发挥作用。
因此，当你想实现相对导入时，建议使用`relpath`包中的`add_import_path`。

`add_import_path("../")`内部等同于`sys.path.append(rel2abs("../"))`。
