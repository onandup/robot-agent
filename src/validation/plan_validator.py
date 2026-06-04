from src.schema import (
    Scene,
    Plan,
    ValidationResult
)

def validate_plan(scene: Scene, plan: Plan) -> ValidationResult:
    object_names = {
        obj.name
        for obj in scene.objects
    }

    errors = []
    picked = False
    width, height = scene.grid_size
    for action in plan.actions:
        ## Check if action type is valid
        if action.target:
            if action.target not in object_names:
                errors.append(
                    f"Unknown target {action.target}"
                )
        ## Check if navigation locations are within grid bounds
        if action.location:
            x, y = action.location

            if x < 0 or x >= width:
                errors.append(
                    f"Navigation x outside grid"
                )

            if y < 0 or y >= height:
                errors.append(
                    f"Navigation y outside grid"
                )

        ## Check for place before pick
        if action.action == "pick":
            picked = True

        if action.action == "place":
            if not picked:
                errors.append(
                    "Place before pick"
                )

    return ValidationResult(
        valid=len(errors) == 0,
        errors=errors
    )