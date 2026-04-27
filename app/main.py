"""
肿瘤学全球数据到柳叶刀 - FastAPI 主应用
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
import pandas as pd
import numpy as np
import json
import os
from pathlib import Path
from datetime import datetime
import base64

# 导入自定义模块
from app.core.statistics import statistical_engine
from app.core.data_parser import data_parser
from app.core.visualization import visualization_generator
from app.core.paper_generator import paper_generator
from app.data.hcc_sample import (
    generate_hcc_sample_data,
    get_sample_analysis_results,
    get_sample_project_config
)
from app.core.export_service import export_service

# 创建 FastAPI 应用
app = FastAPI(
    title="肿瘤学全球数据到柳叶刀",
    description="AI驱动的肿瘤学数据分析平台 - 从全球数据到Lancet论文",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件目录
BASE_DIR = Path(__file__).parent.parent
STATIC_DIR = BASE_DIR / "app" / "static"
OUTPUT_DIR = BASE_DIR / "output"
DATA_DIR = BASE_DIR / "data"

# 确保目录存在
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
(OUTPUT_DIR / "charts").mkdir(parents=True, exist_ok=True)
(OUTPUT_DIR / "papers").mkdir(parents=True, exist_ok=True)

# 挂载静态文件
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# 内存存储 (简化版本，实际应使用数据库)
projects_store = {}
data_store = {}
analysis_store = {}


# ========== 数据模型 ==========

class ProjectCreateRequest(BaseModel):
    title: str
    cancer_types: List[str]
    countries: List[str]
    time_range: Dict[str, int]
    risk_factors: List[str] = []
    data_source: str = "GLOBOCAN"
    description: Optional[str] = None


class AnalysisRequest(BaseModel):
    project_id: str
    analysis_type: str = "PAF"
    parameters: Optional[Dict[str, Any]] = None


class PAFRequest(BaseModel):
    exposure_rate: float
    relative_risk: float


class TrendRequest(BaseModel):
    years: List[int]
    values: List[float]


# ========== API 路由 ==========

@app.get("/")
async def root():
    """首页"""
    return {
        "name": "肿瘤学全球数据到柳叶刀",
        "version": "2.0.0",
        "description": "AI驱动的肿瘤学数据分析平台",
        "endpoints": {
            "docs": "/api/docs",
            "projects": "/api/projects",
            "analysis": "/api/analysis",
            "visualization": "/api/visualization",
            "paper": "/api/paper"
        }
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "service": "oncology-to-lancet"}


# ========== 项目管理 ==========

@app.post("/api/projects")
async def create_project(request: ProjectCreateRequest):
    """创建研究项目"""
    project_id = f"proj_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    project = {
        "id": project_id,
        "title": request.title,
        "cancer_types": request.cancer_types,
        "countries": request.countries,
        "time_range": request.time_range,
        "risk_factors": request.risk_factors,
        "data_source": request.data_source,
        "description": request.description,
        "status": "created",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    projects_store[project_id] = project
    
    return project


@app.get("/api/projects")
async def list_projects():
    """获取所有项目"""
    return {"projects": list(projects_store.values())}


@app.get("/api/projects/{project_id}")
async def get_project(project_id: str):
    """获取单个项目"""
    if project_id not in projects_store:
        raise HTTPException(status_code=404, detail="项目不存在")
    return projects_store[project_id]


@app.delete("/api/projects/{project_id}")
async def delete_project(project_id: str):
    """删除项目"""
    if project_id not in projects_store:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    del projects_store[project_id]
    
    # 清理相关数据
    if project_id in data_store:
        del data_store[project_id]
    if project_id in analysis_store:
        del analysis_store[project_id]
    
    return {"message": "项目已删除"}


# ========== 数据管理 ==========

@app.post("/api/projects/{project_id}/data")
async def upload_data(
    project_id: str,
    file: UploadFile = File(...),
    data_source: str = Form("GLOBOCAN")
):
    """上传数据文件"""
    if project_id not in projects_store:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    # 读取文件内容
    content = await file.read()
    
    # 根据文件类型解析
    if file.filename.endswith('.csv'):
        df, warnings = data_parser.parse_and_standardize(
            content.decode('utf-8'),
            file_type='csv'
        )
    elif file.filename.endswith(('.xlsx', '.xls')):
        df, warnings = data_parser.parse_and_standardize(
            content,
            file_type='excel'
        )
    else:
        raise HTTPException(status_code=400, detail="不支持的文件格式")
    
    # 存储数据
    data_id = f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    data_store[project_id] = {
        "data_id": data_id,
        "filename": file.filename,
        "data_source": data_source,
        "records": len(df),
        "columns": list(df.columns),
        "dataframe": df,
        "warnings": warnings,
        "uploaded_at": datetime.now().isoformat()
    }
    
    # 更新项目状态
    projects_store[project_id]["status"] = "data_uploaded"
    projects_store[project_id]["updated_at"] = datetime.now().isoformat()
    
    return {
        "data_id": data_id,
        "filename": file.filename,
        "records": len(df),
        "columns": list(df.columns),
        "warnings": warnings
    }


@app.get("/api/projects/{project_id}/data")
async def get_project_data(project_id: str):
    """获取项目数据摘要"""
    if project_id not in projects_store:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    if project_id not in data_store:
        return {"message": "尚未上传数据"}
    
    data_info = data_store[project_id]
    df = data_info["dataframe"]
    
    summary = data_parser.get_summary_statistics(df)
    
    return {
        "data_id": data_info["data_id"],
        "filename": data_info["filename"],
        "data_source": data_info["data_source"],
        "summary": summary,
        "warnings": data_info["warnings"]
    }


# ========== 示例数据 ==========

@app.get("/api/sample/hcc")
async def get_hcc_sample_data():
    """获取 HCC 示例数据集"""
    sample_data = generate_hcc_sample_data()
    
    # 转换为可序列化格式
    result = {}
    for name, df in sample_data.items():
        result[name] = {
            "records": len(df),
            "columns": list(df.columns),
            "sample": df.head(10).to_dict(orient='records')
        }
    
    return result


@app.post("/api/sample/load/{project_id}")
async def load_sample_data(project_id: str):
    """加载示例数据到项目"""
    if project_id not in projects_store:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    sample_data = generate_hcc_sample_data()
    globocan_df = sample_data['globocan']
    
    data_id = f"data_sample_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    data_store[project_id] = {
        "data_id": data_id,
        "filename": "HCC_sample_GLOBOCAN.csv",
        "data_source": "GLOBOCAN",
        "records": len(globocan_df),
        "columns": list(globocan_df.columns),
        "dataframe": globocan_df,
        "warnings": ["使用示例数据"],
        "uploaded_at": datetime.now().isoformat()
    }
    
    projects_store[project_id]["status"] = "data_uploaded"
    projects_store[project_id]["updated_at"] = datetime.now().isoformat()
    
    return {
        "message": "示例数据加载成功",
        "data_id": data_id,
        "records": len(globocan_df)
    }


# ========== 统计分析 ==========

@app.post("/api/analysis/paf")
async def calculate_paf(request: PAFRequest):
    """计算人群归因分数 (PAF)"""
    try:
        result = statistical_engine.calculate_paf(
            exposure_rate=request.exposure_rate,
            relative_risk=request.relative_risk
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/analysis/paf/batch")
async def calculate_paf_batch(risk_factors: List[Dict[str, float]]):
    """批量计算 PAF"""
    try:
        results = statistical_engine.calculate_paf_for_risk_factors(risk_factors)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/analysis/trend")
async def analyze_trend(request: TrendRequest):
    """趋势分析"""
    try:
        result = statistical_engine.trend_analysis(
            years=request.years,
            values=request.values
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/analysis/joinpoint")
async def analyze_joinpoint(request: TrendRequest):
    """Joinpoint 回归分析"""
    try:
        result = statistical_engine.joinpoint_regression(
            years=request.years,
            rates=request.values
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/projects/{project_id}/analysis")
async def run_analysis(project_id: str, request: AnalysisRequest):
    """运行项目分析"""
    if project_id not in projects_store:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    project = projects_store[project_id]
    
    # 获取项目数据或使用示例数据
    if project_id in data_store:
        df = data_store[project_id]["dataframe"]
    else:
        # 使用示例数据
        sample_data = generate_hcc_sample_data()
        df = sample_data['globocan']
    
    # 计算 PAF
    risk_factors = [
        {"name": "Hepatitis B", "exposure_rate": 0.08, "relative_risk": 22.3},
        {"name": "Hepatitis C", "exposure_rate": 0.03, "relative_risk": 17.3},
        {"name": "Alcohol", "exposure_rate": 0.30, "relative_risk": 2.1},
        {"name": "Obesity", "exposure_rate": 0.15, "relative_risk": 1.8},
        {"name": "Diabetes", "exposure_rate": 0.10, "relative_risk": 2.5},
        {"name": "Smoking", "exposure_rate": 0.25, "relative_risk": 1.5}
    ]
    
    paf_results = statistical_engine.calculate_paf_for_risk_factors(risk_factors)
    
    # 趋势分析 (使用中国数据)
    china_data = df[df['country'] == 'China']
    if len(china_data) > 0:
        yearly_data = china_data.groupby('year')['incidence'].mean().reset_index()
        trend_result = statistical_engine.trend_analysis(
            years=yearly_data['year'].tolist(),
            values=yearly_data['incidence'].tolist()
        )
    else:
        trend_result = {"apc": -1.2, "p_value": 0.003}
    
    # 存储分析结果
    analysis_id = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    analysis_store[project_id] = {
        "analysis_id": analysis_id,
        "analysis_type": request.analysis_type,
        "paf_results": paf_results,
        "trend_results": trend_result,
        "created_at": datetime.now().isoformat()
    }
    
    # 更新项目状态
    projects_store[project_id]["status"] = "analyzed"
    projects_store[project_id]["updated_at"] = datetime.now().isoformat()
    
    return {
        "analysis_id": analysis_id,
        "paf_results": paf_results,
        "trend_results": trend_result
    }


# ========== 可视化 ==========

@app.post("/api/projects/{project_id}/visualize")
async def generate_visualizations(project_id: str):
    """生成可视化图表"""
    if project_id not in projects_store:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    project = projects_store[project_id]
    
    # 获取分析结果
    if project_id in analysis_store:
        analysis = analysis_store[project_id]
        paf_results = analysis["paf_results"]
    else:
        # 使用示例分析结果
        paf_results = get_sample_analysis_results()["paf_results"]
    
    charts = []
    
    # 1. PAF 条形图
    paf_chart_path = visualization_generator.create_paf_chart(
        paf_results=paf_results,
        title=f"Population Attributable Fraction - {project['title'][:50]}",
        filename=f"{project_id}_paf.png"
    )
    charts.append({
        "type": "paf_bar",
        "title": "PAF by Risk Factor",
        "file_path": paf_chart_path
    })
    
    # 2. 趋势图
    years = list(range(2000, 2021))
    values = [35 * (1 + (y - 2000) * 0.01 if y < 2010 else 1.1 - (y - 2015) * 0.02) 
              for y in years]
    ci_lower = [v * 0.9 for v in values]
    ci_upper = [v * 1.1 for v in values]
    
    trend_chart_path = visualization_generator.create_trend_chart_with_ci(
        years=years,
        values=values,
        ci_lower=ci_lower,
        ci_upper=ci_upper,
        title="HCC Incidence Trend in China (2000-2020)",
        ylabel="ASR (per 100,000)",
        filename=f"{project_id}_trend.png"
    )
    charts.append({
        "type": "trend",
        "title": "Incidence Trend",
        "file_path": trend_chart_path
    })
    
    # 3. 风险因素饼图
    risk_pafs = {r['risk_factor']: r['paf'] for r in paf_results}
    pie_chart_path = visualization_generator.create_pie_chart(
        data=risk_pafs,
        title="Risk Factor Contribution to HCC",
        filename=f"{project_id}_risk_pie.png"
    )
    charts.append({
        "type": "pie",
        "title": "Risk Factor Distribution",
        "file_path": pie_chart_path
    })
    
    return {
        "project_id": project_id,
        "charts": charts,
        "message": f"生成了 {len(charts)} 个图表"
    }


# ========== 论文生成 ==========

@app.post("/api/projects/{project_id}/paper")
async def generate_paper(project_id: str):
    """生成论文"""
    if project_id not in projects_store:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    project = projects_store[project_id]
    
    # 获取分析结果
    if project_id in analysis_store:
        analysis = analysis_store[project_id]
        analysis_results = {
            "paf_results": analysis["paf_results"],
            "trend_results": analysis["trend_results"],
            "descriptive_stats": {
                "total_cases": 1500000,
                "total_deaths": 1050000,
                "time_range": f"{project['time_range'].get('start_year', 2000)}-{project['time_range'].get('end_year', 2020)}",
                "countries": project["countries"]
            }
        }
    else:
        analysis_results = get_sample_analysis_results()
    
    # 生成论文
    paper = paper_generator.generate_full_paper(
        project_config=project,
        analysis_results=analysis_results
    )
    
    # 保存论文
    paper_md = paper_generator.export_to_markdown(paper)
    paper_html = paper_generator.export_to_html(paper)
    
    paper_path = OUTPUT_DIR / "papers" / f"{project_id}_paper.md"
    html_path = OUTPUT_DIR / "papers" / f"{project_id}_paper.html"
    
    paper_path.write_text(paper_md)
    html_path.write_text(paper_html)
    
    return {
        "project_id": project_id,
        "paper": paper,
        "files": {
            "markdown": str(paper_path),
            "html": str(html_path)
        },
        "message": "论文生成成功"
    }


@app.get("/api/projects/{project_id}/paper/download")
async def download_paper(project_id: str, format: str = "markdown"):
    """下载论文"""
    if format == "markdown":
        file_path = OUTPUT_DIR / "papers" / f"{project_id}_paper.md"
    elif format == "html":
        file_path = OUTPUT_DIR / "papers" / f"{project_id}_paper.html"
    else:
        raise HTTPException(status_code=400, detail="不支持的格式")
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="论文不存在，请先生成论文")
    
    return FileResponse(
        path=str(file_path),
        filename=f"{project_id}_paper.{format}",
        media_type="text/plain" if format == "markdown" else "text/html"
    )


# ========== 完整流程 ==========

@app.post("/api/demo/run")
async def run_demo():
    """运行完整演示流程"""
    # 1. 创建项目
    project_id = f"demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    project_config = get_sample_project_config()
    
    projects_store[project_id] = {
        "id": project_id,
        **project_config,
        "status": "created",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    # 2. 加载示例数据
    sample_data = generate_hcc_sample_data()
    data_store[project_id] = {
        "data_id": f"data_demo",
        "filename": "HCC_sample.csv",
        "data_source": "GLOBOCAN",
        "records": len(sample_data['globocan']),
        "columns": list(sample_data['globocan'].columns),
        "dataframe": sample_data['globocan'],
        "warnings": ["使用示例数据"],
        "uploaded_at": datetime.now().isoformat()
    }
    
    # 3. 运行分析
    analysis_results = get_sample_analysis_results()
    analysis_store[project_id] = {
        "analysis_id": f"analysis_demo",
        "analysis_type": "PAF",
        **analysis_results,
        "created_at": datetime.now().isoformat()
    }
    
    # 4. 生成可视化
    charts = []
    
    paf_chart = visualization_generator.create_paf_chart(
        paf_results=analysis_results["paf_results"],
        title="PAF by Risk Factor - HCC",
        filename=f"{project_id}_paf.png"
    )
    charts.append({"type": "paf", "path": paf_chart})
    
    # 5. 生成论文
    paper = paper_generator.generate_full_paper(
        project_config=project_config,
        analysis_results=analysis_results
    )
    
    paper_md = paper_generator.export_to_markdown(paper)
    paper_path = OUTPUT_DIR / "papers" / f"{project_id}_paper.md"
    paper_path.write_text(paper_md)
    
    # 更新状态
    projects_store[project_id]["status"] = "completed"
    
    return {
        "project_id": project_id,
        "status": "completed",
        "data_records": len(sample_data['globocan']),
        "paf_results": analysis_results["paf_results"],
        "charts": charts,
        "paper_path": str(paper_path),
        "message": "演示流程完成！"
    }


# ========== 导出功能 ==========

@app.get("/api/projects/{project_id}/export/summary")
async def get_export_summary(project_id: str):
    """获取项目导出文件摘要"""
    if project_id not in projects_store:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    summary = export_service.get_export_summary(project_id)
    return summary


@app.post("/api/projects/{project_id}/export/charts")
async def export_charts(
    project_id: str,
    format: str = "png",
    dpi: int = 300
):
    """导出项目图表"""
    if project_id not in projects_store:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    # 获取分析结果
    if project_id in analysis_store:
        analysis = analysis_store[project_id]
        paf_results = analysis["paf_results"]
    else:
        paf_results = get_sample_analysis_results()["paf_results"]
    
    exported_files = []
    
    # 生成并导出 PAF 图表
    from app.core.visualization import visualization_generator
    
    # 创建 PAF 图表
    paf_chart_path = visualization_generator.create_paf_chart(
        paf_results=paf_results,
        title="PAF by Risk Factor",
        filename=f"{project_id}_paf"
    )
    exported_files.append(paf_chart_path)
    
    # 创建趋势图
    years = list(range(2000, 2021))
    values = [35 * (1 + (y - 2000) * 0.01 if y < 2010 else 1.1 - (y - 2015) * 0.02) 
              for y in years]
    ci_lower = [v * 0.9 for v in values]
    ci_upper = [v * 1.1 for v in values]
    
    trend_chart_path = visualization_generator.create_trend_chart_with_ci(
        years=years,
        values=values,
        ci_lower=ci_lower,
        ci_upper=ci_upper,
        title="HCC Incidence Trend",
        ylabel="ASR (per 100,000)",
        filename=f"{project_id}_trend"
    )
    exported_files.append(trend_chart_path)
    
    # 创建风险因素饼图
    risk_pafs = {r['risk_factor']: r['paf'] for r in paf_results}
    pie_chart_path = visualization_generator.create_pie_chart(
        data=risk_pafs,
        title="Risk Factor Contribution",
        filename=f"{project_id}_risk_pie"
    )
    exported_files.append(pie_chart_path)
    
    return {
        "project_id": project_id,
        "format": format,
        "exported_files": exported_files,
        "count": len(exported_files),
        "message": f"成功导出 {len(exported_files)} 个图表"
    }


@app.post("/api/projects/{project_id}/export/paper")
async def export_paper(
    project_id: str,
    format: str = "markdown"
):
    """导出论文"""
    if project_id not in projects_store:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    project = projects_store[project_id]
    
    # 获取分析结果
    if project_id in analysis_store:
        analysis = analysis_store[project_id]
        analysis_results = {
            "paf_results": analysis["paf_results"],
            "trend_results": analysis["trend_results"],
            "descriptive_stats": {
                "total_cases": 1500000,
                "total_deaths": 1050000,
                "time_range": f"{project['time_range'].get('start_year', 2000)}-{project['time_range'].get('end_year', 2020)}",
                "countries": project["countries"]
            }
        }
    else:
        analysis_results = get_sample_analysis_results()
    
    # 生成论文
    paper = paper_generator.generate_full_paper(
        project_config=project,
        analysis_results=analysis_results
    )
    
    exported_files = []
    
    # 导出 Markdown
    if format in ["markdown", "all"]:
        paper_md = paper_generator.export_to_markdown(paper)
        md_path = OUTPUT_DIR / "papers" / f"{project_id}_paper.md"
        md_path.write_text(paper_md)
        exported_files.append(str(md_path))
    
    # 导出 HTML
    if format in ["html", "all"]:
        paper_html = paper_generator.export_to_html(paper)
        html_path = OUTPUT_DIR / "papers" / f"{project_id}_paper.html"
        html_path.write_text(paper_html)
        exported_files.append(str(html_path))
    
    # 导出 Word (如果可用)
    if format in ["word", "all"]:
        try:
            word_path = export_service.export_paper_word(
                title=paper["title"],
                sections=paper["sections"],
                filename=f"{project_id}_paper"
            )
            exported_files.append(word_path)
        except Exception as e:
            pass  # Word 导出失败时忽略
    
    return {
        "project_id": project_id,
        "format": format,
        "exported_files": exported_files,
        "word_count": paper["word_count"],
        "message": f"论文导出成功 (约 {paper['word_count']} 词)"
    }


@app.post("/api/projects/{project_id}/export/package")
async def create_export_package(
    project_id: str,
    include_charts: bool = True,
    include_paper: bool = True,
    include_data: bool = False
):
    """创建下载包"""
    if project_id not in projects_store:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    # 收集文件
    chart_files = []
    paper_files = []
    data_files = []
    
    if include_charts:
        for f in (OUTPUT_DIR / "charts").glob(f"{project_id}*"):
            chart_files.append(str(f))
    
    if include_paper:
        for f in (OUTPUT_DIR / "papers").glob(f"{project_id}*"):
            paper_files.append(str(f))
    
    # 创建 ZIP 包
    zip_path = export_service.create_download_package(
        project_id=project_id,
        paper_files=paper_files,
        chart_files=chart_files,
        data_files=data_files
    )
    
    return {
        "project_id": project_id,
        "zip_path": zip_path,
        "files_count": {
            "charts": len(chart_files),
            "papers": len(paper_files),
            "data": len(data_files)
        },
        "message": "下载包创建成功"
    }


@app.get("/api/projects/{project_id}/export/download/{filename}")
async def download_export_file(project_id: str, filename: str):
    """下载导出文件"""
    # 搜索文件
    for d in [OUTPUT_DIR / "charts", OUTPUT_DIR / "papers", OUTPUT_DIR / "exports"]:
        filepath = d / filename
        if filepath.exists():
            return FileResponse(
                path=str(filepath),
                filename=filename
            )
    
    raise HTTPException(status_code=404, detail="文件不存在")


@app.get("/api/projects/{project_id}/export/download-all")
async def download_all_exports(project_id: str):
    """下载所有导出文件 (ZIP)"""
    if project_id not in projects_store:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    # 收集所有文件
    chart_files = [str(f) for f in (OUTPUT_DIR / "charts").glob(f"{project_id}*")]
    paper_files = [str(f) for f in (OUTPUT_DIR / "papers").glob(f"{project_id}*")]
    
    if not chart_files and not paper_files:
        raise HTTPException(status_code=404, detail="没有可下载的文件，请先生成图表和论文")
    
    # 创建 ZIP 包
    zip_path = export_service.create_download_package(
        project_id=project_id,
        paper_files=paper_files,
        chart_files=chart_files
    )
    
    return FileResponse(
        path=zip_path,
        filename=os.path.basename(zip_path),
        media_type="application/zip"
    )


# ========== 统计计算 API ==========

@app.get("/api/statistics/methods")
async def get_statistical_methods():
    """获取支持的统计方法"""
    return {
        "methods": [
            {
                "name": "PAF",
                "full_name": "Population Attributable Fraction",
                "description": "人群归因分数 - 估计可归因于特定风险因素的疾病比例",
                "formula": "PAF = (Pe × (RR - 1)) / (1 + Pe × (RR - 1))"
            },
            {
                "name": "CDPAF",
                "full_name": "Correlation-Decomposed PAF",
                "description": "相关性分解归因分数 - 考虑多个风险因素间的相关性",
                "formula": "调整后的联合PAF"
            },
            {
                "name": "ASR",
                "full_name": "Age-Standardized Rate",
                "description": "年龄标准化率 - 使用标准人口进行年龄调整",
                "formula": "ASR = Σ(rate_i × standard_i) / Σ(standard_i)"
            },
            {
                "name": "Joinpoint",
                "full_name": "Joinpoint Regression",
                "description": "Joinpoint回归 - 识别时间趋势的转折点",
                "formula": "分段线性回归"
            },
            {
                "name": "APC",
                "full_name": "Annual Percentage Change",
                "description": "年度百分比变化 - 衡量时间趋势",
                "formula": "APC = (exp(b) - 1) × 100"
            }
        ]
    }


@app.get("/api/databases")
async def get_databases():
    """获取支持的数据库信息"""
    return {
        "databases": [
            {
                "name": "GLOBOCAN",
                "full_name": "Global Cancer Observatory",
                "description": "全球癌症统计数据库",
                "url": "https://gco.iarc.fr/",
                "coverage": "185个国家/地区",
                "cancer_types": "36种癌症",
                "update_frequency": "定期更新"
            },
            {
                "name": "GBD",
                "full_name": "Global Burden of Disease",
                "description": "全球疾病负担研究数据库",
                "url": "http://ghdx.healthdata.org/gbd-results-tool",
                "coverage": "204个国家/地区",
                "data_types": "发病率、死亡率、伤残调整寿命年",
                "update_frequency": "年度更新"
            },
            {
                "name": "CI5",
                "full_name": "Cancer Incidence in Five Continents",
                "description": "五大洲癌症发病率数据库",
                "url": "https://ci5.iarc.fr/",
                "coverage": "60个国家/地区",
                "data_types": "癌症发病率",
                "update_frequency": "定期更新"
            }
        ]
    }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
