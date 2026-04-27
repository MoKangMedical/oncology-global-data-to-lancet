#!/usr/bin/env python3
"""
Cancer Epidemiology Research To Lancet - 启动脚本
"""

import uvicorn
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

PORT = int(os.environ.get("PORT", 8002))

if __name__ == "__main__":
    print("=" * 60)
    print("  Cancer Epidemiology Research To Lancet")
    print("  肿瘤学全球数据到柳叶刀")
    print("=" * 60)
    print()
    print(f"  Frontend: http://localhost:{PORT}")
    print(f"  API Docs: http://localhost:{PORT}/api/docs")
    print()
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=PORT,
        reload=False
    )
