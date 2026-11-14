from kili_formats.types import ProjectDict

pdf_asset = {
    "latestLabel": {
        "author": {
            "id": "test-user-1",
            "email": "test-user@kili-technology.com",
            "firstname": "Feat1",
            "lastname": "Test Admin",
            "name": "Feat1 Test Admin",
        },
        "jsonResponse": {
            "OBJECT_DETECTION_JOB": {
                "annotations": [
                    {
                        "children": {},
                        "annotations": [
                            {
                                "boundingPoly": [
                                    {
                                        "normalizedVertices": [
                                            {"x": 0.47, "y": 0.1},
                                            {"x": 0.47, "y": 0.23},
                                            {"x": 0.67, "y": 0.23},
                                            {"x": 0.67, "y": 0.1},
                                        ]
                                    }
                                ],
                                "pageNumberArray": [1],
                                "polys": [
                                    {
                                        "normalizedVertices": [
                                            {"x": 0.47, "y": 0.1},
                                            {"x": 0.47, "y": 0.23},
                                            {"x": 0.67, "y": 0.23},
                                            {"x": 0.67, "y": 0.1},
                                        ]
                                    }
                                ],
                            }
                        ],
                        "categories": [{"confidence": 100, "name": "A"}],
                        "content": "",
                        "mid": "20230703112327217-43948",
                        "type": "rectangle",
                    },
                ]
            }
        },
        "createdAt": "2023-07-03T12:18:08.825Z",
        "isLatestLabelForUser": True,
        "labelType": "DEFAULT",
        "modelName": None,
    },
    "pageResolutions": [
        {"pageNumber": 1, "height": 842, "width": 595, "rotation": 0},
        {"pageNumber": 2, "height": 842, "width": 595, "rotation": 0},
    ],
    "content": "https://",
    "jsonContent": "https://",
}

pdf_asset_rotated = {
    "latestLabel": {
        "author": {
            "id": "test-user-1",
            "email": "test-user@kili-technology.com",
            "firstname": "Feat1",
            "lastname": "Test Admin",
            "name": "Feat1 Test Admin",
        },
        "jsonResponse": {
            "ROTATION_JOB": {"rotation": 90},
            "OBJECT_DETECTION_JOB": {
                "annotations": [
                    {
                        "children": {},
                        "annotations": [
                            {
                                "boundingPoly": [
                                    {
                                        "normalizedVertices": [
                                            {"x": 0.47, "y": 0.1},
                                            {"x": 0.47, "y": 0.23},
                                            {"x": 0.67, "y": 0.23},
                                            {"x": 0.67, "y": 0.1},
                                        ]
                                    }
                                ],
                                "pageNumberArray": [1],
                                "polys": [
                                    {
                                        "normalizedVertices": [
                                            {"x": 0.47, "y": 0.1},
                                            {"x": 0.47, "y": 0.23},
                                            {"x": 0.67, "y": 0.23},
                                            {"x": 0.67, "y": 0.1},
                                        ]
                                    }
                                ],
                            }
                        ],
                        "categories": [{"confidence": 100, "name": "A"}],
                        "content": "",
                        "mid": "20230703112327217-43948",
                        "type": "rectangle",
                    },
                ]
            },
        },
        "createdAt": "2023-07-03T12:18:08.825Z",
        "isLatestLabelForUser": True,
        "labelType": "DEFAULT",
        "modelName": None,
    },
    "pageResolutions": [
        {"pageNumber": 1, "height": 842, "width": 595, "rotation": 0},
        {"pageNumber": 2, "height": 842, "width": 595, "rotation": 0},
    ],
    "content": "https://",
    "jsonContent": "https://",
}

pdf_project: ProjectDict = {
    "description": "description",
    "id": "project-id",
    "inputType": "PDF",
    "jsonInterface": {
        "jobs": {
            "OBJECT_DETECTION_JOB": {
                "content": {
                    "categories": {
                        "A": {"children": [], "color": "#472CED", "name": "A"},
                        "B": {"children": [], "name": "B", "color": "#5CE7B7"},
                    },
                    "input": "radio",
                },
                "instruction": "BB",
                "mlTask": "OBJECT_DETECTION",
                "required": 1,
                "tools": ["rectangle"],
                "isChild": False,
            }
        }
    },
    "organizationId": "organization-id",
    "title": "title",
}

pdf_project_asset_unnormalized = {
    "content": "https://",
    "jsonContent": "https://",
    "latestLabel": {
        "author": {
            "id": "test-user-1",
            "email": "test-user@kili-technology.com",
            "firstname": "Feat1",
            "lastname": "Test Admin",
            "name": "Feat1 Test Admin",
        },
        "jsonResponse": {
            "OBJECT_DETECTION_JOB": {
                "annotations": [
                    {
                        "children": {},
                        "annotations": [
                            {
                                "boundingPoly": [
                                    {
                                        "normalizedVertices": [
                                            {"x": 0.47, "y": 0.1},
                                            {"x": 0.47, "y": 0.23},
                                            {"x": 0.67, "y": 0.23},
                                            {"x": 0.67, "y": 0.1},
                                        ],
                                        "vertices": [
                                            {"x": 0.47 * 595, "y": 0.1 * 842},
                                            {"x": 0.47 * 595, "y": 0.23 * 842},
                                            {"x": 0.67 * 595, "y": 0.23 * 842},
                                            {"x": 0.67 * 595, "y": 0.1 * 842},
                                        ],
                                    }
                                ],
                                "pageNumberArray": [1],
                                "polys": [
                                    {
                                        "normalizedVertices": [
                                            {"x": 0.47, "y": 0.1},
                                            {"x": 0.47, "y": 0.23},
                                            {"x": 0.67, "y": 0.23},
                                            {"x": 0.67, "y": 0.1},
                                        ],
                                        "vertices": [
                                            {"x": 0.47 * 595, "y": 0.1 * 842},
                                            {"x": 0.47 * 595, "y": 0.23 * 842},
                                            {"x": 0.67 * 595, "y": 0.23 * 842},
                                            {"x": 0.67 * 595, "y": 0.1 * 842},
                                        ],
                                    }
                                ],
                            }
                        ],
                        "categories": [{"confidence": 100, "name": "A"}],
                        "content": "",
                        "mid": "20230703112327217-43948",
                        "type": "rectangle",
                    },
                ]
            }
        },
        "createdAt": "2023-07-03T12:18:08.825Z",
        "isLatestLabelForUser": True,
        "labelType": "DEFAULT",
        "modelName": None,
    },
    "pageResolutions": [
        {"pageNumber": 1, "height": 842, "width": 595, "rotation": 0},
        {"pageNumber": 2, "height": 842, "width": 595, "rotation": 0},
    ],
}


def rectangle(x_0: float, y_0: float, x_1: float, y_1: float):
    """The four vertices of a rectangle, as the backend writes them."""
    return [{"x": x_0, "y": y_1}, {"x": x_0, "y": y_0}, {"x": x_1, "y": y_0}, {"x": x_1, "y": y_1}]


def pdf_asset_with_fragments(fragments, page_resolutions):
    """A PDF asset labelled with one entity per page fragment of `fragments`."""
    return {
        "latestLabel": {
            "jsonResponse": {
                "OBJECT_DETECTION_JOB": {
                    "annotations": [
                        {
                            "annotations": [fragment],
                            "categories": [{"name": "A"}],
                            "children": {},
                            "content": "",
                            "mid": f"entity-{index}",
                            "type": "rectangle",
                        }
                        for index, fragment in enumerate(fragments)
                    ]
                }
            },
        },
        "pageResolutions": page_resolutions,
    }


def pdf_asset_with_entities(entities, page_resolutions):
    """A PDF asset labelled with one entity per item of `entities`, in the backend's shape.

    Each item is (polys rings, pageNumberArray, boundingPoly rings, boundingPolyPageNumberArray).
    """
    return pdf_asset_with_fragments(
        [
            {
                "boundingPoly": [{"normalizedVertices": bounding_rings}],
                "boundingPolyPageNumberArray": bounding_page_numbers,
                "pageNumberArray": page_numbers,
                "polys": [{"normalizedVertices": rings}],
            }
            for rings, page_numbers, bounding_rings, bounding_page_numbers in entities
        ],
        page_resolutions,
    )
