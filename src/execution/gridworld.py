from src.schema import Scene, Plan, ExecutionResult


def execute_plan(scene: Scene, plan: Plan) -> ExecutionResult:
    robot_location = [0, 0]
    holding = None
    steps = 0

    obstacle_set = {tuple(o) for o in scene.obstacles}

    for action in plan.actions:
        steps += 1

        if action.action == "navigate":
            if tuple(action.location) in obstacle_set:
                return ExecutionResult(
                    success=False,
                    steps_executed=steps,
                    failure_reason=f"Target location {action.location} is blocked",
                )
            robot_location = action.location

        elif action.action == "pick":
            holding = action.target

        elif action.action == "place":
            if not holding:
                return ExecutionResult(
                    success=False,
                    steps_executed=steps,
                    failure_reason="Tried to place object while holding nothing",
                )
            holding = None

    return ExecutionResult(success=True, steps_executed=steps)