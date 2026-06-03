from schema import Scene, ObjectDetection


def parse_scene_mock(image_path: str) -> Scene:
    return Scene(
        grid_size=[6, 6],
        objects=[
            ObjectDetection(name="red mug", type="cup", location=[2, 3], confidence=0.95),
            ObjectDetection(name="tray", type="container", location=[5, 1], confidence=0.92),
        ],
        obstacles=[[3, 3], [3, 4]],
    )