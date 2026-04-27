# 肿瘤学全球数据到柳叶刀

AI驱动的肿瘤学数据分析 — 全球数据到顶级期刊的桥梁

## 项目目标

将全球肿瘤学公开数据（SEER/GLOBOCAN/TCGA）转化为柳叶刀级别发表的临床研究论文。

## 核心能力

- 全球癌症数据自动获取与清洗
- 统计分析自动化（生存分析/亚组分析/敏感性分析）
- 论文初稿自动生成
- 图表标准化（符合顶级期刊要求）

## 快速开始

    git clone https://github.com/MoKangMedical/oncology-global-data-to-lancet.git
    cd oncology-global-data-to-lancet
    pip install -r requirements.txt
    python src/main.py --cancer "lung" --dataset "SEER"

MIT License
