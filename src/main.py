from perception.mock_scene_parser import parse_scene_mock
from planning.task_planner import create_plan
from execution.gridworld import execute_plan


def main():
    image_path = "examples/kitchen_counter.png"
    goal = "Put the red mug on the tray"

    scene = parse_scene_mock(image_path)
    plan = create_plan(goal, scene)
    result = execute_plan(scene, plan)

    print("SCENE:")
    print(scene.model_dump_json(indent=2))

    print("\nPLAN:")
    print(plan.model_dump_json(indent=2))

    print("\nRESULT:")
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()