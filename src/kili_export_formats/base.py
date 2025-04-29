from typing import Dict, List

def reverse_rotation_vertices(normalized_vertices, rotation_angle) -> List[Dict]:
    """Allows to retrieve vertices without rotation."""
    vertices_before_rotate = []
    for vertice in normalized_vertices:
        new_x = vertice["x"]
        new_y = vertice["y"]
        if rotation_angle == 90:
            new_x = vertice["y"]
            new_y = 1 - vertice["x"]
        elif rotation_angle == 180:
            new_x = 1 - vertice["x"]
            new_y = 1 - vertice["y"]
        elif rotation_angle == 270:
            new_x = 1 - vertice["y"]
            new_y = vertice["x"]
        vertices_before_rotate.append({"x": new_x, "y": new_y})
    return vertices_before_rotate