job_0 = {
    "JOB_0": {
        "annotations": [
            {
                "categories": [{"confidence": 100, "name": "OBJECT_A"}],
                "jobName": "JOB_0",
                "mid": "2022040515434712-7532",
                "mlTask": "OBJECT_DETECTION",
                "boundingPoly": [
                    {
                        "normalizedVertices": [
                            {"x": 0.16504140348233334, "y": 0.7986938935103378},
                            {"x": 0.16504140348233334, "y": 0.2605618833516984},
                            {"x": 0.8377886490672706, "y": 0.2605618833516984},
                            {"x": 0.8377886490672706, "y": 0.7986938935103378},
                        ]
                    }
                ],
                "type": "rectangle",
                "children": {},
            }
        ]
    }
}
job_object_detection_with_0_rotation = {
    "JOB_0": {
        "annotations": [
            {
                "categories": [{"confidence": 100, "name": "OBJECT_A"}],
                "jobName": "JOB_0",
                "mid": "2022040515434712-7532",
                "mlTask": "OBJECT_DETECTION",
                "boundingPoly": [
                    {
                        "normalizedVertices": [
                            {"x": 0.07787903893951942, "y": 0.4746554191458914},
                            {"x": 0.07787903893951942, "y": 0.09429841078556889},
                            {"x": 0.3388566694283348, "y": 0.09429841078556889},
                            {"x": 0.3388566694283348, "y": 0.4746554191458914},
                        ]
                    }
                ],
                "type": "rectangle",
                "children": {},
            }
        ]
    }
}
job_object_detection_with_90_rotation = {
    "JOB_0": {
        "annotations": [
            {
                "categories": [{"confidence": 100, "name": "OBJECT_A"}],
                "jobName": "JOB_0",
                "mid": "2022040515434712-7532",
                "mlTask": "OBJECT_DETECTION",
                "boundingPoly": [
                    {
                        "normalizedVertices": [
                            {"x": 0.5253445808541086, "y": 0.07787903893951942},
                            {"x": 0.9057015892144311, "y": 0.07787903893951942},
                            {"x": 0.9057015892144311, "y": 0.3388566694283348},
                            {"x": 0.5253445808541086, "y": 0.3388566694283348},
                        ]
                    }
                ],
                "type": "rectangle",
                "children": {},
            }
        ]
    },
    "ROTATION_JOB": {"rotation": 90},
}
job_object_detection_with_180_rotation = {
    "JOB_0": {
        "annotations": [
            {
                "categories": [{"confidence": 100, "name": "OBJECT_A"}],
                "jobName": "JOB_0",
                "mid": "2022040515434712-7532",
                "mlTask": "OBJECT_DETECTION",
                "boundingPoly": [
                    {
                        "normalizedVertices": [
                            {"x": 0.9221209610604806, "y": 0.5253445808541086},
                            {"x": 0.9221209610604806, "y": 0.9057015892144311},
                            {"x": 0.6611433305716652, "y": 0.9057015892144311},
                            {"x": 0.6611433305716652, "y": 0.5253445808541086},
                        ]
                    }
                ],
                "type": "rectangle",
                "children": {},
            }
        ]
    },
    "ROTATION_JOB": {"rotation": 180},
}
job_object_detection_with_270_rotation = {
    "JOB_0": {
        "annotations": [
            {
                "categories": [{"confidence": 100, "name": "OBJECT_A"}],
                "jobName": "JOB_0",
                "mid": "2022040515434712-7532",
                "mlTask": "OBJECT_DETECTION",
                "boundingPoly": [
                    {
                        "normalizedVertices": [
                            {"x": 0.4746554191458914, "y": 0.9221209610604806},
                            {"x": 0.09429841078556889, "y": 0.9221209610604806},
                            {"x": 0.09429841078556889, "y": 0.6611433305716652},
                            {"x": 0.4746554191458914, "y": 0.6611433305716652},
                        ]
                    }
                ],
                "type": "rectangle",
                "children": {},
            }
        ]
    },
    "ROTATION_JOB": {"rotation": 270},
}
asset = {
    "latestLabel": {"jsonResponse": job_0},
    "externalId": "car_1",
    "content": "https://storage.googleapis.com/label-public-staging/car/car_1.jpg",
    "jsonContent": "",
    "isProcessingAuthorized": False,
    "resolution": {"height": 1080, "width": 1920},
}
asset_with_0_rotation = {
    "latestLabel": {"jsonResponse": job_object_detection_with_0_rotation},
    "externalId": "car_1",
    "content": "https://storage.googleapis.com/label-public-staging/car/car_1.jpg",
    "jsonContent": "",
    "isProcessingAuthorized": False,
    "resolution": {"height": 1080, "width": 1920},
}
asset_with_90_rotation = {
    "latestLabel": {"jsonResponse": job_object_detection_with_90_rotation},
    "externalId": "car_1",
    "content": "https://storage.googleapis.com/label-public-staging/car/car_1.jpg",
    "jsonContent": "",
    "isProcessingAuthorized": False,
    "resolution": {"height": 1080, "width": 1920},
}
asset_with_180_rotation = {
    "latestLabel": {"jsonResponse": job_object_detection_with_180_rotation},
    "externalId": "car_1",
    "content": "https://storage.googleapis.com/label-public-staging/car/car_1.jpg",
    "jsonContent": "",
    "isProcessingAuthorized": False,
    "resolution": {"height": 1080, "width": 1920},
}
asset_with_270_rotation = {
    "latestLabel": {"jsonResponse": job_object_detection_with_270_rotation},
    "externalId": "car_1",
    "content": "https://storage.googleapis.com/label-public-staging/car/car_1.jpg",
    "jsonContent": "",
    "isProcessingAuthorized": False,
    "resolution": {"height": 1080, "width": 1920},
}


def yolo_annotation(tool, *rings, mid=None):
    """A job-0 annotation of OBJECT_A with the tool and rings given, as (x, y) pairs."""
    return {
        "categories": [{"name": "OBJECT_A"}],
        "mid": mid or f"mid-{tool}",
        "type": tool,
        "boundingPoly": [
            {"normalizedVertices": [{"x": x, "y": y} for x, y in ring]} for ring in rings
        ],
    }


def yolo_label(*annotations):
    """A label holding the annotations in job 0."""
    return {"jsonResponse": {"JOB_0": {"annotations": list(annotations)}}}


yolo_box = yolo_annotation("rectangle", [(0.1, 0.1), (0.3, 0.1), (0.3, 0.3), (0.1, 0.3)])
yolo_triangle = yolo_annotation("polygon", [(0.5, 0.1), (0.7, 0.4), (0.3, 0.4)])
# A mask part whose second ring is a hole.
yolo_mask_with_hole = yolo_annotation(
    "semantic",
    [(0.1, 0.5), (0.5, 0.5), (0.5, 0.9), (0.1, 0.9)],
    [(0.2, 0.6), (0.4, 0.6), (0.4, 0.8), (0.2, 0.8)],
)
# A mask part with two holes, the second one's leftmost vertex nearer the first hole than the outline.
yolo_mask_with_two_holes = yolo_annotation(
    "semantic",
    [(0.1, 0.1), (0.9, 0.1), (0.9, 0.9), (0.1, 0.9)],
    [(0.2, 0.2), (0.4, 0.2), (0.4, 0.4), (0.2, 0.4)],
    [(0.45, 0.45), (0.8, 0.45), (0.8, 0.8), (0.45, 0.8)],
)
# A mask in two parts: the backend stores one annotation per part, sharing the mid.
yolo_mask_part_1 = yolo_annotation(
    "semantic", [(0.6, 0.6), (0.8, 0.6), (0.8, 0.8)], mid="mid-two-parts"
)
yolo_mask_part_2 = yolo_annotation(
    "semantic", [(0.6, 0.1), (0.9, 0.1), (0.9, 0.3)], mid="mid-two-parts"
)
yolo_segment = yolo_annotation("polygon", [(0.1, 0.1), (0.2, 0.2)])
