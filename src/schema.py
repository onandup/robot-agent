from pydantic import BaseModel
from typing import List, Optional
from typing import List

class ObjectDetection(BaseModel):
    name: str
    type: str
    location: List[int]
    confidence: Optional[float] = None


class Scene(BaseModel):
    objects: List[ObjectDetection]
    obstacles: List[List[int]]
    grid_size: List[int]


class Action(BaseModel):
    action: str
    target: Optional[str] = None
    location: Optional[List[int]] = None


class Plan(BaseModel):
    goal: str
    actions: List[Action]


class ExecutionResult(BaseModel):
    success: bool
    steps_executed: int
    failure_reason: Optional[str] = None

class ValidationResult(BaseModel):
    valid: bool
    errors: List[str]


class RunTrace(BaseModel):
    run_id: str
    goal: str
    model_name: str
    perception_latency_ms: float
    planning_latency_ms: float
    execution_latency_ms: float
    scene: dict
    plan: dict
    result: dict