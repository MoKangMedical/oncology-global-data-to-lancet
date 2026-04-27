"""
肿瘤学全球数据到柳叶刀 - 数据模型
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class DataSource(str, Enum):
    """数据源类型"""
    GLOBOCAN = "GLOBOCAN"
    GBD = "GBD"
    CI5 = "CI5"
    SEER = "SEER"
    CUSTOM = "CUSTOM"


class CancerType(str, Enum):
    """癌症类型"""
    LIVER = "liver"  # 肝癌
    LUNG = "lung"  # 肺癌
    BREAST = "breast"  # 乳腺癌
    COLORECTAL = "colorectal"  # 结直肠癌
    STOMACH = "stomach"  # 胃癌
    PROSTATE = "prostate"  # 前列腺癌
    THYROID = "thyroid"  # 甲状腺癌
    ESOPHAGUS = "esophagus"  # 食管癌
    PANCREAS = "pancreas"  # 胰腺癌
    BLADDER = "bladder"  # 膀胱癌
    ALL = "all"  # 所有癌症


class RiskFactor(str, Enum):
    """风险因素"""
    SMOKING = "smoking"  # 吸烟
    ALCOHOL = "alcohol"  # 饮酒
    OBESITY = "obesity"  # 肥胖
    HEPATITIS_B = "hepatitis_b"  # 乙肝
    HEPATITIS_C = "hepatitis_c"  # 丙肝
    DIABETES = "diabetes"  # 糖尿病
    HPV = "hpv"  # 人乳头瘤病毒
    H_PYLORI = "h_pylori"  # 幽门螺杆菌
    AIR_POLLUTION = "air_pollution"  # 空气污染
    PHYSICAL_INACTIVITY = "physical_inactivity"  # 缺乏运动


class AnalysisType(str, Enum):
    """分析类型"""
    PAF = "PAF"  # 人群归因分数
    CDPAF = "CDPAF"  # 相关性分解归因分数
    TREND = "TREND"  # 趋势分析
    ASR = "ASR"  # 年龄标准化率
    SURVIVAL = "SURVIVAL"  # 生存分析


# ========== 请求模型 ==========

class ProjectCreate(BaseModel):
    """创建项目请求"""
    title: str = Field(..., description="项目标题")
    cancer_types: List[CancerType] = Field(..., description="癌症类型")
    countries: List[str] = Field(..., description="目标国家/地区")
    time_range: Dict[str, int] = Field(..., description="时间范围 (start_year, end_year)")
    risk_factors: List[RiskFactor] = Field(default=[], description="风险因素")
    data_source: DataSource = Field(default=DataSource.GLOBOCAN, description="数据源")
    description: Optional[str] = Field(default=None, description="项目描述")


class DataUploadRequest(BaseModel):
    """数据上传请求"""
    project_id: str
    data_source: DataSource
    file_name: str
    file_content: str  # Base64 编码的文件内容


class AnalysisRequest(BaseModel):
    """分析请求"""
    project_id: str
    analysis_type: AnalysisType
    parameters: Optional[Dict[str, Any]] = None


# ========== 响应模型 ==========

class ProjectResponse(BaseModel):
    """项目响应"""
    id: str
    title: str
    cancer_types: List[CancerType]
    countries: List[str]
    time_range: Dict[str, int]
    risk_factors: List[RiskFactor]
    data_source: DataSource
    description: Optional[str]
    status: str = "created"
    created_at: datetime
    updated_at: datetime


class CancerDataRecord(BaseModel):
    """癌症数据记录"""
    country: str
    year: int
    cancer_type: str
    sex: str  # male/female/both
    incidence: Optional[float] = None  # 发病率
    mortality: Optional[float] = None  # 死亡率
    prevalence: Optional[float] = None  # 患病率
    asr_incidence: Optional[float] = None  # 年龄标准化发病率
    asr_mortality: Optional[float] = None  # 年龄标准化死亡率
    population: Optional[int] = None  # 人口数
    cases: Optional[int] = None  # 病例数
    deaths: Optional[int] = None  # 死亡数


class PAFResult(BaseModel):
    """PAF 分析结果"""
    risk_factor: str
    exposure_rate: float  # 暴露率
    relative_risk: float  # 相对风险
    paf: float  # 人群归因分数
    paf_ci_lower: Optional[float] = None  # 置信区间下限
    paf_ci_upper: Optional[float] = None  # 置信区间上限


class TrendResult(BaseModel):
    """趋势分析结果"""
    period: str  # 时间段
    apc: float  # 年度百分比变化
    apc_ci_lower: Optional[float] = None
    apc_ci_upper: Optional[float] = None
    p_value: Optional[float] = None
    joinpoint_year: Optional[int] = None  # 转折点年份


class AnalysisResponse(BaseModel):
    """分析结果响应"""
    project_id: str
    analysis_type: AnalysisType
    results: Dict[str, Any]
    summary: str
    created_at: datetime


class VisualizationResponse(BaseModel):
    """可视化响应"""
    project_id: str
    chart_type: str
    title: str
    file_path: str
    file_url: Optional[str] = None
    created_at: datetime


class PaperSection(BaseModel):
    """论文章节"""
    section_type: str  # summary, introduction, methods, results, discussion
    title: str
    content: str


class PaperResponse(BaseModel):
    """论文响应"""
    project_id: str
    title: str
    sections: List[PaperSection]
    word_count: int
    status: str  # draft, review, final
    created_at: datetime


# ========== 统计数据模型 ==========

class GlobalCancerStats(BaseModel):
    """全球癌症统计数据"""
    year: int
    total_cases: int
    total_deaths: int
    asr_incidence: float
    asr_mortality: float
    top_cancers: List[Dict[str, Any]]
    top_countries: List[Dict[str, Any]]
