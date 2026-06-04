import uuid

from src.schema import RunTrace
from src.perception.qwen_scene_parser import QwenSceneParser
from src.planning.task_planner import create_plan
from src.execution.gridworld import execute_plan
from src.validation.scene_validator import validate_scene
from src.validation.plan_validator import validate_plan
import time

def main():
    image_path = "examples/kitchen_counter.png"
    goal = "Put the red mug on the tray"

    parser = QwenSceneParser()
    run_id = str(uuid.uuid4())

    start = time.time()
    scene = parser.parse(image_path, goal)
    perception_latency_ms = (time.time() - start) * 1000

    start = time.time()
    plan = create_plan(goal, scene)
    planning_latency_ms = (time.time() - start) * 1000
    
    
    start = time.time()
    result = execute_plan(scene, plan)
    execution_latency_ms = (time.time() - start) * 1000

    scene_validation = validate_scene(scene)
    if not scene_validation.valid:
        print(scene_validation.errors)

    plan_validation = validate_plan(
        scene,
        plan
    )

    if not plan_validation.valid:
        print(plan_validation.errors)

    trace = RunTrace(
        run_id=run_id,
        goal=goal,
        model_name="Qwen2.5-VL-3B",
        perception_latency_ms=perception_latency_ms,
        planning_latency_ms=planning_latency_ms,
        execution_latency_ms=execution_latency_ms,
        scene=scene.model_dump(),
        plan=plan.model_dump(),
        result=result.model_dump()
    )

    print(trace)


if __name__ == "__main__":
    main()