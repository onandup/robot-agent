from perception.qwen_scene_parser import QwenSceneParser
from planning.task_planner import create_plan
from execution.gridworld import execute_plan
from validation.scene_validator import validate_scene


def main():
    image_path = "examples/kitchen_counter.png"
    goal = "Put the red mug on the tray"

    parser = QwenSceneParser()
    scene = parser.parse(image_path, goal)

    plan = create_plan(goal, scene)
    result = execute_plan(scene, plan)
    
    scene_validation = validate_scene(scene)

    if not scene_validation.valid:
        print(scene_validation.errors)
    return

    plan_validation = validate_plan(
        scene,
        plan
    )

    if not plan_validation.valid:
        print(plan_validation.errors)
    return

    print(scene.model_dump_json(indent=2))
    print(plan.model_dump_json(indent=2))
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()