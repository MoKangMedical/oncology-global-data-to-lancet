#!/usr/bin/env python3
"""
肿瘤学全球数据到柳叶刀 - 启动脚本
"""

import uvicorn
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("=" * 60)
    print("  Cancer Epidemiology Research To Lancet")
    print("  肿瘤学全球数据到柳叶刀")
    print("=" * 60)
    print()
    print("  启动中...")
    print("  API 文档: http://localhost:8000/api/docs")
    print("  前端界面: http://localhost:8000")
    print()
    print("=" * 60)
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8002,
        reload=True
    )
