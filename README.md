# 深圳杯 2024 数学建模

本仓库包含我在 2024 年深圳杯数学建模竞赛中使用的代码文件和 PDF 论文。内容包括所有用于数据分析、仿真和最终算法的脚本，问题 1 至 4 的求解过程和可视化过程，以及最终的 LaTeX 论文文件和 PDF。

## 目录结构

```
ShenzhenCup2024-MathModeling/
│
├── code/
│ ├── problem1/
│ │ ├── 1-1_ 设备数量确定 .py
│ │ ├── 1-1_ 设备数量确定 _ 遗传算法 .py
│ │ ├── 1-1_ 问题一预处理 .py
│ │ └── 1-2_ 问题一求解 .py
│ ├── problem2/
│ │ ├── 2-1_ 问题二设备数量确定 .py
│ │ └── 2-2_ 设备数量确定（模拟环境，作验证用）.py
│ ├── problem3/
│ │ ├── 3-1 问题三位置求解 .py
│ │ ├── 3-2 问题三求解可视化 .py
│ │ └── 3-3 问题三时间求解 .py
│ ├── problem4/
│ │ ├── 
│ │ └── 4-1 问题四求解 .py
│
├── paper/
│ ├── main/
| | ├── figures/
| | ├── cumcmthesis.cls
| | ├── main.tex
│ │ └── ShenzhenCup2024-Paper.pdf
│ └── example/
│
└── README.md
```

## 内容简介

### 代码

`code` 目录下包含了每个问题的求解和可视化脚本：

- `problem1/`：问题 1 的求解和可视化。
- `problem2/`：问题 2 的求解和可视化。
- `problem3/`：问题 3 的求解和可视化。
- `problem4/`：问题 4 的求解和可视化。

### 论文

`paper` 目录下包含了最终论文的 LaTeX 文件和生成的 PDF 文件：

- `main/main.tex`：论文的主文件。
- `figures/`：存放论文中使用的图表。
- `ShenzhenCup2024-Paper.pdf`：最终生成的论文 PDF 文件。
- `cumcmthesis.cls`：LaTex 模板文件。

## 使用说明

### 克隆仓库

首先，克隆此仓库到本地：

```bash
git clone https://github.com/tanzhijir-04/ShenzhenCup2024-MathModeling.git
cd ShenzhenCup2024-MathModeling
```

### 设置 Python 环境
确保你已经安装了 Python 3.x，并且已安装了必要的依赖库。

### 运行代码
进入各个问题的目录，并运行相应的脚本。例如：

```
cd code/problem1
python 1-1_ 设备数量确定 .py
python 1-1_ 设备数量确定 _ 遗传算法 .py
```

### 编译论文
如果你需要重新编译论文，可以进入 paper 目录并使用以下命令：

```
cd paper
xelatex main.tex
```
## 联系方式
如果你有任何问题或建议，请提交 issue。