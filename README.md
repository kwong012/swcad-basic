<p align="center">
  <img src="assets/banner.png" alt="swcad banner" width="110%">
</p>

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python" alt="Python"></a>
  <a href="https://www.microsoft.com/windows/"><img src="https://img.shields.io/badge/Platform-Windows-lightgrey?style=for-the-badge&logo=windows" alt="Platform"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License"></a>
  <a href="https://www.solidworks.com/"><img src="https://img.shields.io/badge/SolidWorks-COM-orange?style=for-the-badge" alt="SolidWorks"></a>
</p>



<h1 align="center">swcad-basic：通过Python控制SolidWorks进行参数化建模 </h1>


---

## 

**swcad** 是一个包含Python)库的agent skill,.通过pywin:32直接调用SolidWorks COM API,实现参数化3D建模的自动化。下载后在任意LLM Agent下加载/swcad使用。目前API调用大部分通过VBA宏录制验证，不同设备和环境下可能出现报错或建模错误。

拿ds盲人在CLI里训练的，目前还存在导入工程图后草图位置出错、有概率不能连续建模、各种剖视图识别不出的问题（悲


## 快速开始

```bash
pip install pywin32 pyyaml
git clone https://github.com/kwong012/swcad-basic.git 
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

- Windows（只在win11上验证，win10不知道行不行）
- SolidWorks (sw2024 sp0.1)，不同版本的sw api调用可能不同，建议先录制一段vba作为对比
- Python 3.8+
- `pywin32`、`pyyaml`

## License

[MIT](LICENSE)

Copyright © 2025 [kwong012](https://github.com/kwong012)


