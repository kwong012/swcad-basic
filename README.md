<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Platform-Windows-lightgrey?style=for-the-badge&logo=windows" alt="Platform">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/SolidWorks-COM-orange?style=for-the-badge" alt="SolidWorks">
</p>

<h1 align="center">swcad</h1>
<p align="center"><em>SolidWorks COM 自动化核心库 — 通过 Python 控制 SolidWorks 进行参数化 3D 建模</em></p>

---

## 简介

**swcad** 是一个 Python 库，通过 `pywin32` 直接调用 SolidWorks COM API，实现参数化 3D 建模的自动化。所有 API 调用均经过 VBA 宏录制验证，确保参数准确无误。

## 快速开始

```bash
pip install pywin32 pyyaml
```

```python
from swcad import create_part, Sketch, Feature

part, app = create_part()

sketch = Sketch(part)
sketch.begin("front")
sketch.circle(0, 0, 20)   # φ40 圆
sketch.end()

feature = Feature(part)
feature.extrude(50)        # 拉伸 50mm
```

## 模块

| 模块 | 功能 |
|------|------|
| `SwApp` | SolidWorks 进程连接管理 |
| `PartDoc` | 文档生命周期管理 |
| `Sketch` | 草图绘制（圆、线、矩形、样条曲线等 11 种） |
| `Feature` | 特征操作（拉伸、旋转、阵列、镜像等 12 种） |
| `RefGeometry` | 参考几何（偏移平面、参考轴） |
| `Params` | 参数/方程管理 |
| `SpecEngine` | YAML 驱动自动化建模 |
| `Utils` | 单位转换（mm/inch/deg → API 单位） |

## 环境要求

- Windows + SolidWorks（已安装并运行）
- Python 3.8+
- `pywin32`、`pyyaml`

## License

[MIT](LICENSE)

Copyright © 2025 [kwong012](https://github.com/kwong012)
