---
name: swcad
description: "通过 Python COM 接口控制 SolidWorks 进行参数化 3D 建模，支持草图绘制、特征操作、参考几何、参数管理及 YAML 驱动的自动化建模流程。适用于各类机械零件、钣金件、焊件等的自动建模与设计任务。"
metadata: { "os": ["win32"], "requires": { "anyBins": ["python", "py"] } }
---

# swcad — SolidWorks COM 自动化核心库

通过 Python `pywin32` 直接调用 SolidWorks COM API，实现参数化 3D 建模的自动化。所有 API 调用均经过 VBA 宏录制验证。

## 环境要求

- Windows 操作系统
- SolidWorks（已安装并运行，或通过 COM 自动启动）
- Python 3.8+
- `pywin32`（`pip install pywin32`）
- `pyyaml`（`pip install pyyaml`，仅 `SpecEngine` 需要）
- 界面语言自适应（中文/英文基准面名称自动映射）

## 架构概览

```
swcad/
├── app.py         # SolidWorks 进程连接管理
├── doc.py         # 文档生命周期管理
├── sketch.py      # 草图绘制操作
├── feature.py     # 特征操作
├── reference.py   # 参考几何
├── params.py      # 参数/方程管理
├── spec_engine.py # YAML 驱动自动化建模引擎
└── utils.py       # 单位转换工具
```

## 模块说明

### app.py — SwApp
管理 SolidWorks COM 连接。优先尝试绑定已有实例，失败时自动创建新实例。提供模板路径解析与应用生命周期控制。

### doc.py — PartDoc
封装文档操作：新建零件文档、实体选择（通过 `SelectByID2` 支持名称/坐标选择）、`VARIANT` 调用包装、保存与重建。

### sketch.py — Sketch
草图绘制模块。支持在任意基准面或已有面上开始/结束草图，提供多种草图图元绘制方法，坐标自动从毫米转为 API 单位。

### feature.py — Feature
特征操作模块。提供各类特征创建方法，包括拉伸基体/切除、旋转、圆角、倒角、抽壳、圆周/线性阵列、镜像等。内置经 VBA 验证的 COM 常量。

### reference.py — RefGeometry
参考几何创建模块。支持偏移基准面、参考轴、三点参考面等辅助几何元素。

### params.py — Params
参数与方程管理模块。支持全局参数设置和读取，可在设计表中定义关联关系，实现参数化驱动。

### spec_engine.py — SpecEngine
YAML 驱动的自动化建模引擎。解析结构化规格文件，按步骤序列执行建模操作，支持变量插值与表达式求值。

### utils.py
单位转换常量与函数。提供毫米、厘米、英寸、度与 API 单位（米、弧度）间的自动换算。

## 典型使用流程

1. 通过 `SwApp` 连接 SolidWorks
2. 通过 `PartDoc` 创建或打开零件文档
3. 使用 `Sketch` 在基准面上绘制草图轮廓
4. 使用 `Feature` 创建特征（拉伸、切除、旋转、阵列等）
5. 使用 `RefGeometry` 创建辅助参考几何
6. 使用 `Params` 管理设计参数
7. 保存并导出结果

各模块可灵活组合，支持从简单零件到复杂装配体的全流程参数化建模。
