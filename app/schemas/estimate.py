from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class BridgeEstimateRequest(BaseModel):
    project_type: str = Field(default="bridge", description="Type of construction: bridge, building, road")
    bridge_type: str = Field(default="RCC", description="Structural type: RCC, PSC, Steel-Composite")
    length_m: float = Field(..., gt=0, description="Total bridge length in metres")
    width_m: float = Field(..., gt=0, description="Total deck width in metres")
    height_m: float = Field(..., gt=0, description="Bridge pier height from riverbed/ground to pier cap in metres")
    location: str = Field(default="Assam, India", description="Project location in India")
    currency: str = Field(default="INR", description="Currency symbol/code")
    span_length_m: Optional[float] = Field(default=None, description="Average span length in metres (optional)")
    concrete_grade: Optional[str] = Field(default="M35", description="Grade of concrete (e.g. M30, M35, M40)")
    steel_grade: Optional[str] = Field(default="Fe500D", description="Grade of reinforcement steel")
    foundation_type: Optional[str] = Field(default=None, description="Foundation type: pile, well, or open")
    custom_rates: Optional[Dict[str, float]] = Field(default=None, description="Optional custom rates overrides")

class MaterialItem(BaseModel):
    name: str
    category: str
    quantity: float
    unit: str
    rate: float
    amount: float
    formula_basis: str

class StructuralComponent(BaseModel):
    component_name: str
    concrete_volume_m3: float
    formwork_area_m2: float
    steel_weight_tonnes: float
    description: str

class SourceReference(BaseModel):
    title: str
    code_reference: str
    excerpt: str
    relevance_score: Optional[float] = None

class CostBreakdown(BaseModel):
    materials_cost: float
    labour_cost: float
    machinery_equipment_cost: float
    contractor_profit_and_overhead: float
    total_cost: float
    currency: str = "INR"

class EstimationSummary(BaseModel):
    status: str = "preliminary"
    total_estimated_cost: float
    currency: str = "INR"
    cost_per_linear_metre: float
    cost_per_sqm_deck: float

class ProjectDetails(BaseModel):
    type: str
    bridge_type: str
    location: str
    length_m: float
    width_m: float
    height_m: float
    spans_count: int
    span_length_m: float
    concrete_grade: str
    steel_grade: str
    foundation_type: str

class EstimateResponse(BaseModel):
    success: bool
    project: ProjectDetails
    estimation: EstimationSummary
    components: List[StructuralComponent]
    materials: List[MaterialItem]
    cost_breakdown: CostBreakdown
    civil_engineering_assumptions: List[str]
    source_references: List[SourceReference]
    missing_inputs: List[str]
    requires_engineer_review: bool = True
    ai_engineer_analysis: Optional[str] = None

class DocumentIngestRequest(BaseModel):
    content: str
    source: str
    category: str = "standards"
    metadata: Optional[Dict[str, Any]] = None
