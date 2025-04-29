from kili_export_formats.types import ProjectDict


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