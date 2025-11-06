json_interface_nested = {
    "jobs": {
        "OBJECT_DETECTION_JOB": {
            "content": {
                "categories": {
                    "OBJECT": {
                        "children": ["CLASSIFICATION_JOB"],
                        "color": "#472CED",
                        "name": "Object",
                        "id": "category1",
                    }
                },
                "input": "radio",
            },
            "instruction": "",
            "mlTask": "OBJECT_DETECTION",
            "required": 0,
            "tools": ["rectangle"],
            "isChild": False,
            "isNew": False,
        },
        "CLASSIFICATION_JOB": {
            "content": {
                "categories": {
                    "PLANE": {
                        "children": ["CLASSIFICATION_JOB_0"],
                        "name": "Plane",
                        "id": "category2",
                    },
                    "OTHER": {"children": [], "name": "Other", "id": "category3"},
                },
                "input": "radio",
            },
            "instruction": "",
            "mlTask": "CLASSIFICATION",
            "required": 0,
            "isChild": True,
            "isNew": False,
        },
        "CLASSIFICATION_JOB_0": {
            "content": {
                "categories": {
                    "CIVIL": {
                        "children": ["CLASSIFICATION_JOB_1"],
                        "name": "Civil",
                        "id": "category4",
                    },
                    "OTHER": {"children": [], "name": "Other", "id": "category5"},
                },
                "input": "checkbox",
            },
            "instruction": "",
            "mlTask": "CLASSIFICATION",
            "required": 0,
            "isChild": True,
            "isNew": False,
        },
        "CLASSIFICATION_JOB_1": {
            "content": {
                "categories": {
                    "AIRBUS": {
                        "children": ["CLASSIFICATION_JOB_2"],
                        "name": "Airbus",
                        "id": "category6",
                    },
                    "OTHER": {"children": [], "name": "Other", "id": "category7"},
                },
                "input": "radio",
            },
            "instruction": "",
            "mlTask": "CLASSIFICATION",
            "required": 0,
            "isChild": True,
            "isNew": False,
        },
        "CLASSIFICATION_JOB_2": {
            "content": {
                "categories": {
                    "A_2_XX": {
                        "children": ["CLASSIFICATION_JOB_3"],
                        "name": "A2XX",
                        "id": "category8",
                    },
                    "A_3_XX": {"children": [], "name": "A3XX", "id": "category9"},
                },
                "input": "radio",
            },
            "instruction": "",
            "mlTask": "CLASSIFICATION",
            "required": 0,
            "isChild": True,
            "isNew": False,
        },
        "CLASSIFICATION_JOB_3": {
            "content": {
                "categories": {
                    "A_220_100": {
                        "children": ["CLASSIFICATION_JOB_4"],
                        "name": "A220-100",
                        "id": "category10",
                    },
                    "A_220_300": {"children": [], "name": "A220-300", "id": "category11"},
                    "OTHER": {"children": [], "name": "Other", "id": "category12"},
                },
                "input": "radio",
            },
            "instruction": "",
            "mlTask": "CLASSIFICATION",
            "required": 0,
            "isChild": True,
            "isNew": False,
        },
        "CLASSIFICATION_JOB_4": {
            "content": {
                "categories": {
                    "AT_REST": {"children": [], "name": "At rest", "id": "category13"},
                    "OTHER": {"children": [], "name": "Other", "id": "category14"},
                },
                "input": "radio",
            },
            "instruction": "",
            "mlTask": "CLASSIFICATION",
            "required": 0,
            "isChild": True,
            "isNew": False,
        },
    }
}


latest_label_annotations_nested = {
    "annotations": [
        {
            "id": "20251106102550483-8",
            "job": "OBJECT_DETECTION_JOB",
            "path": [],
            "labelId": "cmhn82il9004a017a2ahshrtx",
            "category": "OBJECT",
            "mid": "20251106102548611-7",
            "name": "Object",
            "annotationValue": {
                "id": "20251106102550483-8",
                "isPrediction": False,
                "vertices": [
                    [
                        [
                            {"x": 124.37872679714252, "y": 13.664482835205533},
                            {"x": 124.37872679714252, "y": 13.664584823516138},
                            {"x": 124.37883527838291, "y": 13.664584823516138},
                            {"x": 124.37883527838291, "y": 13.664482835205533},
                        ]
                    ]
                ],
                "confidence": None,
                "__typename": "ObjectDetectionAnnotationValue",
            },
            "__typename": "ObjectDetectionAnnotation",
        },
        {
            "id": "20251106102551841-10",
            "job": "CLASSIFICATION_JOB",
            "path": [["20251106102550483-8", "OBJECT"]],
            "labelId": "cmhn82il9004a017a2ahshrtx",
            "chatItemId": None,
            "annotationValue": {
                "categories": ["PLANE"],
                "id": "20251106102551841-10",
                "isPrediction": False,
                "__typename": "ClassificationAnnotationValue",
            },
            "__typename": "ClassificationAnnotation",
        },
        {
            "id": "20251106102554680-11",
            "job": "CLASSIFICATION_JOB_0",
            "path": [["20251106102550483-8", "OBJECT"], ["20251106102551841-10", "PLANE"]],
            "labelId": "cmhn82il9004a017a2ahshrtx",
            "chatItemId": None,
            "annotationValue": {
                "categories": ["CIVIL"],
                "id": "20251106102554680-11",
                "isPrediction": False,
                "__typename": "ClassificationAnnotationValue",
            },
            "__typename": "ClassificationAnnotation",
        },
        {
            "id": "20251106102555712-12",
            "job": "CLASSIFICATION_JOB_1",
            "path": [
                ["20251106102550483-8", "OBJECT"],
                ["20251106102551841-10", "PLANE"],
                ["20251106102554680-11", "CIVIL"],
            ],
            "labelId": "cmhn82il9004a017a2ahshrtx",
            "chatItemId": None,
            "annotationValue": {
                "categories": ["AIRBUS"],
                "id": "20251106102555712-12",
                "isPrediction": False,
                "__typename": "ClassificationAnnotationValue",
            },
            "__typename": "ClassificationAnnotation",
        },
        {
            "id": "20251106102558678-13",
            "job": "CLASSIFICATION_JOB_2",
            "path": [
                ["20251106102550483-8", "OBJECT"],
                ["20251106102551841-10", "PLANE"],
                ["20251106102554680-11", "CIVIL"],
                ["20251106102555712-12", "AIRBUS"],
            ],
            "labelId": "cmhn82il9004a017a2ahshrtx",
            "chatItemId": None,
            "annotationValue": {
                "categories": ["A_2_XX"],
                "id": "20251106102558678-13",
                "isPrediction": False,
                "__typename": "ClassificationAnnotationValue",
            },
            "__typename": "ClassificationAnnotation",
        },
        {
            "id": "20251106102559783-14",
            "job": "CLASSIFICATION_JOB_3",
            "path": [
                ["20251106102550483-8", "OBJECT"],
                ["20251106102551841-10", "PLANE"],
                ["20251106102554680-11", "CIVIL"],
                ["20251106102555712-12", "AIRBUS"],
                ["20251106102558678-13", "A_2_XX"],
            ],
            "labelId": "cmhn82il9004a017a2ahshrtx",
            "chatItemId": None,
            "annotationValue": {
                "categories": ["A_220_100"],
                "id": "20251106102559783-14",
                "isPrediction": False,
                "__typename": "ClassificationAnnotationValue",
            },
            "__typename": "ClassificationAnnotation",
        },
        {
            "id": "20251106102600945-15",
            "job": "CLASSIFICATION_JOB_4",
            "path": [
                ["20251106102550483-8", "OBJECT"],
                ["20251106102551841-10", "PLANE"],
                ["20251106102554680-11", "CIVIL"],
                ["20251106102555712-12", "AIRBUS"],
                ["20251106102558678-13", "A_2_XX"],
                ["20251106102559783-14", "A_220_100"],
            ],
            "labelId": "cmhn82il9004a017a2ahshrtx",
            "chatItemId": None,
            "annotationValue": {
                "categories": ["AT_REST"],
                "id": "20251106102600945-15",
                "isPrediction": False,
                "__typename": "ClassificationAnnotationValue",
            },
            "__typename": "ClassificationAnnotation",
        },
        {
            "id": "20251106102604954-16",
            "job": "OBJECT_DETECTION_JOB",
            "path": [],
            "labelId": "cmhn82il9004a017a2ahshrtx",
            "category": "OBJECT",
            "mid": "20251106102550491-9",
            "name": "Object",
            "annotationValue": {
                "id": "20251106102604954-16",
                "isPrediction": False,
                "vertices": [
                    [
                        [
                            {"x": 124.37845827235364, "y": 13.66455986120682},
                            {"x": 124.37845827235364, "y": 13.664672100845443},
                            {"x": 124.37858248088462, "y": 13.664672100845443},
                            {"x": 124.37858248088462, "y": 13.66455986120682},
                        ]
                    ]
                ],
                "confidence": None,
                "__typename": "ObjectDetectionAnnotationValue",
            },
            "__typename": "ObjectDetectionAnnotation",
        },
        {
            "id": "20251106102607046-18",
            "job": "CLASSIFICATION_JOB",
            "path": [["20251106102604954-16", "OBJECT"]],
            "labelId": "cmhn82il9004a017a2ahshrtx",
            "chatItemId": None,
            "annotationValue": {
                "categories": ["OTHER"],
                "id": "20251106102607046-18",
                "isPrediction": False,
                "__typename": "ClassificationAnnotationValue",
            },
            "__typename": "ClassificationAnnotation",
        },
        {
            "id": "20251106102610274-19",
            "job": "OBJECT_DETECTION_JOB",
            "path": [],
            "labelId": "cmhn82il9004a017a2ahshrtx",
            "category": "OBJECT",
            "mid": "20251106102604988-17",
            "name": "Object",
            "annotationValue": {
                "id": "20251106102610274-19",
                "isPrediction": False,
                "vertices": [
                    [
                        [
                            {"x": 124.37863902718082, "y": 13.664615746221848},
                            {"x": 124.37863902718082, "y": 13.664734560537491},
                            {"x": 124.3787588859967, "y": 13.664734560537491},
                            {"x": 124.3787588859967, "y": 13.664615746221848},
                        ]
                    ]
                ],
                "confidence": None,
                "__typename": "ObjectDetectionAnnotationValue",
            },
            "__typename": "ObjectDetectionAnnotation",
        },
        {
            "id": "20251106102612500-21",
            "job": "CLASSIFICATION_JOB",
            "path": [["20251106102610274-19", "OBJECT"]],
            "labelId": "cmhn82il9004a017a2ahshrtx",
            "chatItemId": None,
            "annotationValue": {
                "categories": ["PLANE"],
                "id": "20251106102612500-21",
                "isPrediction": False,
                "__typename": "ClassificationAnnotationValue",
            },
            "__typename": "ClassificationAnnotation",
        },
        {
            "id": "20251106102616411-22",
            "job": "CLASSIFICATION_JOB_0",
            "path": [["20251106102610274-19", "OBJECT"], ["20251106102612500-21", "PLANE"]],
            "labelId": "cmhn82il9004a017a2ahshrtx",
            "chatItemId": None,
            "annotationValue": {
                "categories": ["CIVIL"],
                "id": "20251106102616411-22",
                "isPrediction": False,
                "__typename": "ClassificationAnnotationValue",
            },
            "__typename": "ClassificationAnnotation",
        },
        {
            "id": "20251106102619942-23",
            "job": "CLASSIFICATION_JOB_1",
            "path": [
                ["20251106102610274-19", "OBJECT"],
                ["20251106102612500-21", "PLANE"],
                ["20251106102616411-22", "CIVIL"],
            ],
            "labelId": "cmhn82il9004a017a2ahshrtx",
            "chatItemId": None,
            "annotationValue": {
                "categories": ["AIRBUS"],
                "id": "20251106102619942-23",
                "isPrediction": False,
                "__typename": "ClassificationAnnotationValue",
            },
            "__typename": "ClassificationAnnotation",
        },
        {
            "id": "20251106102623805-24",
            "job": "CLASSIFICATION_JOB_2",
            "path": [
                ["20251106102610274-19", "OBJECT"],
                ["20251106102612500-21", "PLANE"],
                ["20251106102616411-22", "CIVIL"],
                ["20251106102619942-23", "AIRBUS"],
            ],
            "labelId": "cmhn82il9004a017a2ahshrtx",
            "chatItemId": None,
            "annotationValue": {
                "categories": ["A_3_XX"],
                "id": "20251106102623805-24",
                "isPrediction": False,
                "__typename": "ClassificationAnnotationValue",
            },
            "__typename": "ClassificationAnnotation",
        },
    ],
    "author": {
        "email": "test+admin@kili-technology.com",
        "firstname": "Test",
        "id": "user-1",
        "lastname": "Admin",
    },
    "createdAt": "2025-06-02T13:24:37.078Z",
    "isLatestLabelForUser": True,
    "isSentBackToQueue": False,
    "jsonResponse": {},
    "labelType": "REVIEW",
    "modelName": None,
}

expected_latest_label_result_nested = {
    "author": {
        "email": "test+admin@kili-technology.com",
        "firstname": "Test",
        "id": "user-1",
        "lastname": "Admin",
    },
    "createdAt": "2025-06-02T13:24:37.078Z",
    "isLatestLabelForUser": True,
    "isSentBackToQueue": False,
    "jsonResponse": {
        "OBJECT_DETECTION_JOB": {
            "annotations": [
                {
                    "boundingPoly": [
                        {
                            "normalizedVertices": [
                                {
                                    "x": 124.37872679714252,
                                    "y": 13.664482835205533,
                                },
                                {
                                    "x": 124.37872679714252,
                                    "y": 13.664584823516138,
                                },
                                {
                                    "x": 124.37883527838291,
                                    "y": 13.664584823516138,
                                },
                                {
                                    "x": 124.37883527838291,
                                    "y": 13.664482835205533,
                                },
                            ],
                        },
                    ],
                    "categories": [
                        {
                            "name": "OBJECT",
                        },
                    ],
                    "children": {
                        "CLASSIFICATION_JOB": {
                            "categories": [
                                {
                                    "children": {
                                        "CLASSIFICATION_JOB_0": {
                                            "categories": [
                                                {
                                                    "children": {
                                                        "CLASSIFICATION_JOB_1": {
                                                            "categories": [
                                                                {
                                                                    "children": {
                                                                        "CLASSIFICATION_JOB_2": {
                                                                            "categories": [
                                                                                {
                                                                                    "children": {
                                                                                        "CLASSIFICATION_JOB_3": {
                                                                                            "categories": [
                                                                                                {
                                                                                                    "children": {
                                                                                                        "CLASSIFICATION_JOB_4": {
                                                                                                            "categories": [
                                                                                                                {
                                                                                                                    "name": "AT_REST",
                                                                                                                },
                                                                                                            ],
                                                                                                        },
                                                                                                    },
                                                                                                    "name": "A_220_100",
                                                                                                },
                                                                                            ],
                                                                                        },
                                                                                    },
                                                                                    "name": "A_2_XX",
                                                                                },
                                                                            ],
                                                                        },
                                                                    },
                                                                    "name": "AIRBUS",
                                                                },
                                                            ],
                                                        },
                                                    },
                                                    "name": "CIVIL",
                                                },
                                            ],
                                        },
                                    },
                                    "name": "PLANE",
                                },
                            ],
                        },
                    },
                    "mid": "20251106102548611-7",
                    "type": "rectangle",
                },
                {
                    "boundingPoly": [
                        {
                            "normalizedVertices": [
                                {
                                    "x": 124.37845827235364,
                                    "y": 13.66455986120682,
                                },
                                {
                                    "x": 124.37845827235364,
                                    "y": 13.664672100845443,
                                },
                                {
                                    "x": 124.37858248088462,
                                    "y": 13.664672100845443,
                                },
                                {
                                    "x": 124.37858248088462,
                                    "y": 13.66455986120682,
                                },
                            ],
                        },
                    ],
                    "categories": [
                        {
                            "name": "OBJECT",
                        },
                    ],
                    "children": {
                        "CLASSIFICATION_JOB": {
                            "categories": [
                                {
                                    "name": "OTHER",
                                },
                            ],
                        },
                    },
                    "mid": "20251106102550491-9",
                    "type": "rectangle",
                },
                {
                    "boundingPoly": [
                        {
                            "normalizedVertices": [
                                {
                                    "x": 124.37863902718082,
                                    "y": 13.664615746221848,
                                },
                                {
                                    "x": 124.37863902718082,
                                    "y": 13.664734560537491,
                                },
                                {
                                    "x": 124.3787588859967,
                                    "y": 13.664734560537491,
                                },
                                {
                                    "x": 124.3787588859967,
                                    "y": 13.664615746221848,
                                },
                            ],
                        },
                    ],
                    "categories": [
                        {
                            "name": "OBJECT",
                        },
                    ],
                    "children": {
                        "CLASSIFICATION_JOB": {
                            "categories": [
                                {
                                    "children": {
                                        "CLASSIFICATION_JOB_0": {
                                            "categories": [
                                                {
                                                    "children": {
                                                        "CLASSIFICATION_JOB_1": {
                                                            "categories": [
                                                                {
                                                                    "children": {
                                                                        "CLASSIFICATION_JOB_2": {
                                                                            "categories": [
                                                                                {
                                                                                    "name": "A_3_XX",
                                                                                },
                                                                            ],
                                                                        },
                                                                    },
                                                                    "name": "AIRBUS",
                                                                },
                                                            ],
                                                        },
                                                    },
                                                    "name": "CIVIL",
                                                },
                                            ],
                                        },
                                    },
                                    "name": "PLANE",
                                },
                            ],
                        },
                    },
                    "mid": "20251106102604988-17",
                    "type": "rectangle",
                },
            ],
        },
    },
    "labelType": "REVIEW",
    "modelName": None,
}

test_cases_full = [
    (
        json_interface_nested,
        latest_label_annotations_nested,
        expected_latest_label_result_nested,
    ),
]
