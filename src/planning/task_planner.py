from schema import Scene, Plan, Action


def create_plan(goal: str, scene: Scene) -> Plan:
    source = None
    destination = None

    for obj in scene.objects:
        if "mug" in obj.name:
            source = obj
        if "tray" in obj.name:
            destination = obj

    if not source or not destination:
        raise ValueError("Could not find required source or destination object")

    return Plan(
        goal=goal,
        actions=[
            Action(action="navigate", target=source.name, location=source.location),
            Action(action="pick", target=source.name),
            Action(action="navigate", target=destination.name, location=destination.location),
            Action(action="place", target=destination.name),
        ],
    )