from schema import Scene, ValidationResult

def validate_scene(scene: Scene) -> ValidationResult:
    errors = []

    width, height = scene.grid_size
    locations = set()
    obstacles = {
        tuple(o)
        for o in scene.obstacles
    }

    for obj in scene.objects:

        x, y = obj.location
        ## Check if object location is within grid bounds   
        if x < 0 or x >= width:
            errors.append(
                f"{obj.name} x coordinate outside grid"
            )
        if y < 0 or y >= height:
            errors.append(
                f"{obj.name} y coordinate outside grid"
            )

        ## Check for multiple objects in the same location
        loc = tuple(obj.location)
        if loc in locations:
            errors.append(
                f"Multiple objects at {loc}"
            )

        locations.add(loc)

        if tuple(obj.location) in obstacles:
            errors.append(
                f"{obj.name} overlaps obstacle"
            )

    return ValidationResult(
        valid=len(errors) == 0,
        errors=errors
    )