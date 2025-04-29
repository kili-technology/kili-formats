from kili_export_formats.types import ProjectDict


image_asset = {
    "content": "https://storage.googleapis.com/label-backend-staging/projects/clk8fq8edf38d13",
    "externalId": "42015077eed072c50d59232dcc0ad0b1.jpg",
    "id": "clk8fq9ow00022a69icovadtq",
    "jsonContent": "",
    "jsonMetadata": {},
    "latestLabel": {
        "author": {
            "email": "user@kili-technology.com",
            "firstname": "Firstname",
            "id": "123456",
            "lastname": "Lastname",
        },
        "createdAt": "2023-07-18T15:24:11.433Z",
        "isLatestLabelForUser": True,
        "jsonResponse": {
            "OBJECT_DETECTION_JOB": {
                "annotations": [
                    {
                        "boundingPoly": [
                            {
                                "normalizedVertices": [
                                    {"x": 0.7412807669633257, "y": 0.11831185681407619},
                                    {"x": 0.7412807669633257, "y": 0.07455291056382807},
                                ]
                            }
                        ],
                        "categories": [{"name": "A"}],
                        "children": {},
                        "mid": "20230718172351536-92877",
                        "type": "rectangle",
                    }
                ]
            },
            "OBJECT_DETECTION_JOB_0": {
                "annotations": [
                    {
                        "categories": [{"name": "B"}],
                        "children": {},
                        "mid": "20230718172353363-53863",
                        "point": {"x": 0.8727983223923027, "y": 0.2035857007889187},
                        "type": "marker",
                    }
                ]
            },
            "OBJECT_DETECTION_JOB_1": {
                "annotations": [
                    {
                        "boundingPoly": [
                            {
                                "normalizedVertices": [
                                    {"x": 0.7891053325738627, "y": 0.2955916903407224},
                                    {"x": 0.6456316357422514, "y": 0.3483268306935856},
                                ]
                            }
                        ],
                        "categories": [{"name": "C"}],
                        "children": {},
                        "mid": "20230718172356733-32196",
                        "type": "polygon",
                    }
                ]
            },
            "OBJECT_DETECTION_JOB_2": {
                "annotations": [
                    {
                        "categories": [{"name": "D"}],
                        "children": {},
                        "mid": "20230718172359896-17202",
                        "polyline": [
                            {"x": 0.6555950869111132, "y": 0.2574428654046088},
                            {"x": 0.5659240263913562, "y": 0.17890116700672754},
                        ],
                        "type": "polyline",
                    }
                ]
            },
            "OBJECT_DETECTION_JOB_3": {
                "annotations": [
                    {
                        "boundingPoly": [
                            {
                                "normalizedVertices": [
                                    {"x": 0.3686485611814346, "y": 0.410038},
                                    {"x": 0.3806035400843882, "y": 0.410038},
                                ]
                            }
                        ],
                        "categories": [{"name": "E"}],
                        "children": {},
                        "mid": "20230718172405691-91771",
                        "type": "semantic",
                    }
                ]
            },
            "POSE_ESTIMATION_JOB": {
                "annotations": [
                    {
                        "categories": [{"name": "HEAD"}],
                        "children": {},
                        "mid": "20230220175803297-40094",
                        "points": [
                            {
                                "children": {},
                                "code": "RIGHT_EARBASE",
                                "mid": "20230220170039711-76095",
                                "point": {"x": 0.350897302238901, "y": 0.18537832978498114},
                                "type": "marker",
                            },
                            {
                                "children": {},
                                "code": "RIGHT_EYE",
                                "mid": "20230220170039711-75233",
                                "point": {"x": 0.3581081932428414, "y": 0.2305347416594279},
                                "type": "marker",
                            },
                            {
                                "children": {},
                                "code": "NOSE",
                                "mid": "20230220170039711-59132",
                                "point": {"x": 0.38815357242592613, "y": 0.32807259130823285},
                                "type": "marker",
                            },
                            {
                                "children": {},
                                "code": "LEFT_EYE",
                                "mid": "20230220170039711-27852",
                                "point": {"x": 0.4386476019456967, "y": 0.23889914422760516},
                                "type": "marker",
                            },
                            {
                                "children": {},
                                "code": "LEFT_EARBASE",
                                "mid": "20230220170039711-40802",
                                "point": {"x": 0.46187314422288966, "y": 0.1875659030559057},
                                "type": "marker",
                            },
                        ],
                        "type": "pose",
                    }
                ]
            },
        },
        "labelType": "DEFAULT",
        "modelName": None,
    },
    "pageResolutions": None,
    "resolution": {"height": 842, "width": 474},
}

image_asset_rotated = {
    "content": "https://storage.googleapis.com/label-backend-staging/projects/clk8fq8edf38d13",
    "externalId": "42015077eed072c50d59232dcc0ad0b1.jpg",
    "id": "clk8fq9ow00022a69icovadtq",
    "jsonContent": "",
    "jsonMetadata": {},
    "latestLabel": {
        "author": {
            "email": "user@kili-technology.com",
            "firstname": "Firstname",
            "id": "123456",
            "lastname": "Lastname",
        },
        "createdAt": "2023-07-18T15:24:11.433Z",
        "isLatestLabelForUser": True,
        "jsonResponse": {
            "ROTATION_JOB": {"rotation": 90},
            "OBJECT_DETECTION_JOB": {
                "annotations": [
                    {
                        "boundingPoly": [
                            {
                                "normalizedVertices": [
                                    {"x": 0.23872063368943108, "y": 0.2164674634794157},
                                    {"x": 0.23872063368943108, "y": 0.09960159362549803},
                                    {"x": 0.3895920741811515, "y": 0.09960159362549803},
                                    {"x": 0.3895920741811515, "y": 0.2164674634794157},
                                ]
                            }
                        ],
                        "categories": [{"name": "A"}],
                        "children": {},
                        "mid": "20230718172351536-92877",
                        "type": "rectangle",
                    }
                ]
            },
            "OBJECT_DETECTION_JOB_0": {
                "annotations": [
                    {
                        "categories": [{"name": "B"}],
                        "children": {},
                        "mid": "20230718172353363-53863",
                        "point": {"x": 0.8727983223923027, "y": 0.2035857007889187},
                        "type": "marker",
                    }
                ]
            },
            "OBJECT_DETECTION_JOB_1": {
                "annotations": [
                    {
                        "boundingPoly": [
                            {
                                "normalizedVertices": [
                                    {"x": 0.6225834126620363, "y": 0.3067729083665338},
                                    {"x": 0.6225834126620363, "y": 0.22045152722443562},
                                    {"x": 0.7581767325976331, "y": 0.22045152722443562},
                                    {"x": 0.7581767325976331, "y": 0.3067729083665338},
                                ]
                            }
                        ],
                        "categories": [{"name": "C"}],
                        "children": {},
                        "mid": "20230718172356733-32196",
                        "type": "polygon",
                    }
                ]
            },
            "OBJECT_DETECTION_JOB_2": {
                "annotations": [
                    {
                        "categories": [{"name": "D"}],
                        "children": {},
                        "mid": "20230718172359896-17202",
                        "polyline": [
                            {"x": 0.6555950869111132, "y": 0.2574428654046088},
                            {"x": 0.5659240263913562, "y": 0.17890116700672754},
                        ],
                        "type": "polyline",
                    }
                ]
            },
            "OBJECT_DETECTION_JOB_3": {
                "annotations": [
                    {
                        "boundingPoly": [
                            {
                                "normalizedVertices": [
                                    {"x": 0.15660073570026678, "y": 0.4183266932270916},
                                    {"x": 0.15660073570026678, "y": 0.3373173970783533},
                                    {"x": 0.24635969396749288, "y": 0.3373173970783533},
                                    {"x": 0.24635969396749288, "y": 0.4183266932270916},
                                ]
                            }
                        ],
                        "categories": [{"name": "E"}],
                        "children": {},
                        "mid": "20230718172405691-91771",
                        "type": "semantic",
                    }
                ]
            },
            "POSE_ESTIMATION_JOB": {
                "annotations": [
                    {
                        "categories": [{"name": "HEAD"}],
                        "children": {},
                        "mid": "20230220175803297-40094",
                        "points": [
                            {
                                "children": {},
                                "code": "RIGHT_EARBASE",
                                "mid": "20230220170039711-76095",
                                "point": {"x": 0.350897302238901, "y": 0.18537832978498114},
                                "type": "marker",
                            },
                            {
                                "children": {},
                                "code": "RIGHT_EYE",
                                "mid": "20230220170039711-75233",
                                "point": {"x": 0.3581081932428414, "y": 0.2305347416594279},
                                "type": "marker",
                            },
                            {
                                "children": {},
                                "code": "NOSE",
                                "mid": "20230220170039711-59132",
                                "point": {"x": 0.38815357242592613, "y": 0.32807259130823285},
                                "type": "marker",
                            },
                            {
                                "children": {},
                                "code": "LEFT_EYE",
                                "mid": "20230220170039711-27852",
                                "point": {"x": 0.4386476019456967, "y": 0.23889914422760516},
                                "type": "marker",
                            },
                            {
                                "children": {},
                                "code": "LEFT_EARBASE",
                                "mid": "20230220170039711-40802",
                                "point": {"x": 0.46187314422288966, "y": 0.1875659030559057},
                                "type": "marker",
                            },
                        ],
                        "type": "pose",
                    }
                ]
            },
        },
        "labelType": "DEFAULT",
        "modelName": None,
    },
    "pageResolutions": None,
    "resolution": {"height": 842, "width": 474},
}

image_project: ProjectDict = {
    "description": "description",
    "id": "fake_proj_id",
    "title": "title",
    "inputType": "IMAGE",
    "jsonInterface": {
        "jobs": {
            "OBJECT_DETECTION_JOB": {
                "content": {
                    "categories": {"A": {"children": [], "color": "#472CED", "name": "A"}},
                    "input": "radio",
                },
                "instruction": "BBOX",
                "mlTask": "OBJECT_DETECTION",
                "required": 1,
                "tools": ["rectangle"],
                "isChild": False,
            },
            "OBJECT_DETECTION_JOB_0": {
                "content": {
                    "categories": {"B": {"children": [], "color": "#5CE7B7", "name": "B"}},
                    "input": "radio",
                },
                "instruction": "POINT",
                "mlTask": "OBJECT_DETECTION",
                "required": 1,
                "tools": ["marker"],
                "isChild": False,
            },
            "OBJECT_DETECTION_JOB_1": {
                "content": {
                    "categories": {"C": {"children": [], "color": "#D33BCE", "name": "C"}},
                    "input": "radio",
                },
                "instruction": "POLYGON",
                "mlTask": "OBJECT_DETECTION",
                "required": 1,
                "tools": ["polygon"],
                "isChild": False,
            },
            "OBJECT_DETECTION_JOB_2": {
                "content": {
                    "categories": {"D": {"children": [], "color": "#FB753C", "name": "D"}},
                    "input": "radio",
                },
                "instruction": "LINE",
                "mlTask": "OBJECT_DETECTION",
                "required": 1,
                "tools": ["polyline"],
                "isChild": False,
            },
            "OBJECT_DETECTION_JOB_3": {
                "content": {
                    "categories": {"E": {"children": [], "color": "#3BCADB", "name": "E"}},
                    "input": "radio",
                },
                "instruction": "SEMANTIC",
                "mlTask": "OBJECT_DETECTION",
                "required": 1,
                "tools": ["semantic"],
                "isChild": False,
            },
            "POSE_ESTIMATION_JOB": {
                "content": {
                    "categories": {
                        "HEAD": {
                            "children": [],
                            "name": "Head",
                            "color": "#733AFB",
                            "points": [
                                {
                                    "code": "RIGHT_EARBASE",
                                    "name": "Right earbase",
                                    "id": "point53",
                                },
                                {"code": "RIGHT_EYE", "name": "Right eye", "id": "point54"},
                                {"code": "NOSE", "name": "Nose", "id": "point55"},
                                {"code": "LEFT_EYE", "name": "Left eye", "id": "point56"},
                                {
                                    "code": "LEFT_EARBASE",
                                    "name": "Left earbase",
                                    "id": "point57",
                                },
                            ],
                            "id": "category58",
                        }
                    },
                    "input": "radio",
                },
                "instruction": "Body parts from the animal point of view",
                "isChild": False,
                "tools": ["pose"],
                "mlTask": "OBJECT_DETECTION",
                "models": {},
                "isVisible": True,
                "required": 1,
                "isNew": False,
            },
        }
    },
    "organizationId": "fake_org_id",
}

image_project_asset_normalized = {
    "content": "https://storage.googleapis.com/label-backend-staging/projects/clk8fq8edf38d13",
    "externalId": "42015077eed072c50d59232dcc0ad0b1.jpg",
    "id": "clk8fq9ow00022a69icovadtq",
    "jsonContent": "",
    "jsonMetadata": {},
    "latestLabel": {
        "author": {
            "email": "user@kili-technology.com",
            "firstname": "Firstname",
            "id": "123456",
            "lastname": "Lastname",
        },
        "createdAt": "2023-07-18T15:24:11.433Z",
        "isLatestLabelForUser": True,
        "jsonResponse": {
            "OBJECT_DETECTION_JOB": {
                "annotations": [
                    {
                        "boundingPoly": [
                            {
                                "normalizedVertices": [
                                    {"x": 0.7412807669633257, "y": 0.11831185681407619},
                                    {"x": 0.7412807669633257, "y": 0.07455291056382807},
                                ],
                            }
                        ],
                        "categories": [{"name": "A"}],
                        "children": {},
                        "mid": "20230718172351536-92877",
                        "type": "rectangle",
                    }
                ]
            },
            "OBJECT_DETECTION_JOB_0": {
                "annotations": [
                    {
                        "categories": [{"name": "B"}],
                        "children": {},
                        "mid": "20230718172353363-53863",
                        "point": {"x": 0.8727983223923027, "y": 0.2035857007889187},
                        "pointPixels": {
                            "x": 0.8727983223923027 * 474,
                            "y": 0.2035857007889187 * 842,
                        },
                        "type": "marker",
                    }
                ]
            },
            "OBJECT_DETECTION_JOB_1": {
                "annotations": [
                    {
                        "boundingPoly": [
                            {
                                "normalizedVertices": [
                                    {"x": 0.7891053325738627, "y": 0.2955916903407224},
                                    {"x": 0.6456316357422514, "y": 0.3483268306935856},
                                ],
                            }
                        ],
                        "categories": [{"name": "C"}],
                        "children": {},
                        "mid": "20230718172356733-32196",
                        "type": "polygon",
                    }
                ]
            },
            "OBJECT_DETECTION_JOB_2": {
                "annotations": [
                    {
                        "categories": [{"name": "D"}],
                        "children": {},
                        "mid": "20230718172359896-17202",
                        "polyline": [
                            {"x": 0.6555950869111132, "y": 0.2574428654046088},
                            {"x": 0.5659240263913562, "y": 0.17890116700672754},
                        ],
                        "polylinePixels": [
                            {"x": 0.6555950869111132 * 474, "y": 0.2574428654046088 * 842},
                            {"x": 0.5659240263913562 * 474, "y": 0.17890116700672754 * 842},
                        ],
                        "type": "polyline",
                    }
                ]
            },
            "OBJECT_DETECTION_JOB_3": {
                "annotations": [
                    {
                        "boundingPoly": [
                            {
                                "normalizedVertices": [
                                    {"x": 0.3686485611814346, "y": 0.410038},
                                    {"x": 0.3806035400843882, "y": 0.410038},
                                ],
                            }
                        ],
                        "categories": [{"name": "E"}],
                        "children": {},
                        "mid": "20230718172405691-91771",
                        "type": "semantic",
                    }
                ]
            },
            "POSE_ESTIMATION_JOB": {
                "annotations": [
                    {
                        "categories": [{"name": "HEAD"}],
                        "children": {},
                        "mid": "20230220175803297-40094",
                        "points": [
                            {
                                "children": {},
                                "code": "RIGHT_EARBASE",
                                "mid": "20230220170039711-76095",
                                "point": {"x": 0.350897302238901, "y": 0.18537832978498114},
                                "pointPixels": {
                                    "x": 0.350897302238901 * 474,
                                    "y": 0.18537832978498114 * 842,
                                },
                                "type": "marker",
                            },
                            {
                                "children": {},
                                "code": "RIGHT_EYE",
                                "mid": "20230220170039711-75233",
                                "point": {"x": 0.3581081932428414, "y": 0.2305347416594279},
                                "pointPixels": {
                                    "x": 0.3581081932428414 * 474,
                                    "y": 0.2305347416594279 * 842,
                                },
                                "type": "marker",
                            },
                            {
                                "children": {},
                                "code": "NOSE",
                                "mid": "20230220170039711-59132",
                                "point": {"x": 0.38815357242592613, "y": 0.32807259130823285},
                                "pointPixels": {
                                    "x": 0.38815357242592613 * 474,
                                    "y": 0.32807259130823285 * 842,
                                },
                                "type": "marker",
                            },
                            {
                                "children": {},
                                "code": "LEFT_EYE",
                                "mid": "20230220170039711-27852",
                                "point": {"x": 0.4386476019456967, "y": 0.23889914422760516},
                                "pointPixels": {
                                    "x": 0.4386476019456967 * 474,
                                    "y": 0.23889914422760516 * 842,
                                },
                                "type": "marker",
                            },
                            {
                                "children": {},
                                "code": "LEFT_EARBASE",
                                "mid": "20230220170039711-40802",
                                "point": {"x": 0.46187314422288966, "y": 0.1875659030559057},
                                "pointPixels": {
                                    "x": 0.46187314422288966 * 474,
                                    "y": 0.1875659030559057 * 842,
                                },
                                "type": "marker",
                            },
                        ],
                        "type": "pose",
                    }
                ]
            },
        },
        "labelType": "DEFAULT",
        "modelName": None,
    },
    "pageResolutions": None,
    "resolution": {"height": 842, "width": 474},
}

image_project_asset_unnormalized = {
    "content": "https://storage.googleapis.com/label-backend-staging/projects/clk8fq8edf38d13",
    "externalId": "42015077eed072c50d59232dcc0ad0b1.jpg",
    "id": "clk8fq9ow00022a69icovadtq",
    "jsonContent": "",
    "jsonMetadata": {},
    "latestLabel": {
        "author": {
            "email": "user@kili-technology.com",
            "firstname": "Firstname",
            "id": "123456",
            "lastname": "Lastname",
        },
        "createdAt": "2023-07-18T15:24:11.433Z",
        "isLatestLabelForUser": True,
        "jsonResponse": {
            "OBJECT_DETECTION_JOB": {
                "annotations": [
                    {
                        "boundingPoly": [
                            {
                                "normalizedVertices": [
                                    {"x": 0.7412807669633257, "y": 0.11831185681407619},
                                    {"x": 0.7412807669633257, "y": 0.07455291056382807},
                                ],
                                "vertices": [
                                    {
                                        "x": 0.7412807669633257 * 474,
                                        "y": 0.11831185681407619 * 842,
                                    },
                                    {
                                        "x": 0.7412807669633257 * 474,
                                        "y": 0.07455291056382807 * 842,
                                    },
                                ],
                            }
                        ],
                        "categories": [{"name": "A"}],
                        "children": {},
                        "mid": "20230718172351536-92877",
                        "type": "rectangle",
                    }
                ]
            },
            "OBJECT_DETECTION_JOB_0": {
                "annotations": [
                    {
                        "categories": [{"name": "B"}],
                        "children": {},
                        "mid": "20230718172353363-53863",
                        "point": {"x": 0.8727983223923027, "y": 0.2035857007889187},
                        "pointPixels": {
                            "x": 0.8727983223923027 * 474,
                            "y": 0.2035857007889187 * 842,
                        },
                        "type": "marker",
                    }
                ]
            },
            "OBJECT_DETECTION_JOB_1": {
                "annotations": [
                    {
                        "boundingPoly": [
                            {
                                "normalizedVertices": [
                                    {"x": 0.7891053325738627, "y": 0.2955916903407224},
                                    {"x": 0.6456316357422514, "y": 0.3483268306935856},
                                ],
                                "vertices": [
                                    {
                                        "x": 0.7891053325738627 * 474,
                                        "y": 0.2955916903407224 * 842,
                                    },
                                    {
                                        "x": 0.6456316357422514 * 474,
                                        "y": 0.3483268306935856 * 842,
                                    },
                                ],
                            }
                        ],
                        "categories": [{"name": "C"}],
                        "children": {},
                        "mid": "20230718172356733-32196",
                        "type": "polygon",
                    }
                ]
            },
            "OBJECT_DETECTION_JOB_2": {
                "annotations": [
                    {
                        "categories": [{"name": "D"}],
                        "children": {},
                        "mid": "20230718172359896-17202",
                        "polyline": [
                            {"x": 0.6555950869111132, "y": 0.2574428654046088},
                            {"x": 0.5659240263913562, "y": 0.17890116700672754},
                        ],
                        "polylinePixels": [
                            {"x": 0.6555950869111132 * 474, "y": 0.2574428654046088 * 842},
                            {"x": 0.5659240263913562 * 474, "y": 0.17890116700672754 * 842},
                        ],
                        "type": "polyline",
                    }
                ]
            },
            "OBJECT_DETECTION_JOB_3": {
                "annotations": [
                    {
                        "boundingPoly": [
                            {
                                "normalizedVertices": [
                                    {"x": 0.3686485611814346, "y": 0.410038},
                                    {"x": 0.3806035400843882, "y": 0.410038},
                                ],
                                "vertices": [
                                    {"x": 0.3686485611814346 * 474, "y": 0.410038 * 842},
                                    {"x": 0.3806035400843882 * 474, "y": 0.410038 * 842},
                                ],
                            }
                        ],
                        "categories": [{"name": "E"}],
                        "children": {},
                        "mid": "20230718172405691-91771",
                        "type": "semantic",
                    }
                ]
            },
            "POSE_ESTIMATION_JOB": {
                "annotations": [
                    {
                        "categories": [{"name": "HEAD"}],
                        "children": {},
                        "mid": "20230220175803297-40094",
                        "points": [
                            {
                                "children": {},
                                "code": "RIGHT_EARBASE",
                                "mid": "20230220170039711-76095",
                                "point": {"x": 0.350897302238901, "y": 0.18537832978498114},
                                "pointPixels": {
                                    "x": 0.350897302238901 * 474,
                                    "y": 0.18537832978498114 * 842,
                                },
                                "type": "marker",
                            },
                            {
                                "children": {},
                                "code": "RIGHT_EYE",
                                "mid": "20230220170039711-75233",
                                "point": {"x": 0.3581081932428414, "y": 0.2305347416594279},
                                "pointPixels": {
                                    "x": 0.3581081932428414 * 474,
                                    "y": 0.2305347416594279 * 842,
                                },
                                "type": "marker",
                            },
                            {
                                "children": {},
                                "code": "NOSE",
                                "mid": "20230220170039711-59132",
                                "point": {"x": 0.38815357242592613, "y": 0.32807259130823285},
                                "pointPixels": {
                                    "x": 0.38815357242592613 * 474,
                                    "y": 0.32807259130823285 * 842,
                                },
                                "type": "marker",
                            },
                            {
                                "children": {},
                                "code": "LEFT_EYE",
                                "mid": "20230220170039711-27852",
                                "point": {"x": 0.4386476019456967, "y": 0.23889914422760516},
                                "pointPixels": {
                                    "x": 0.4386476019456967 * 474,
                                    "y": 0.23889914422760516 * 842,
                                },
                                "type": "marker",
                            },
                            {
                                "children": {},
                                "code": "LEFT_EARBASE",
                                "mid": "20230220170039711-40802",
                                "point": {"x": 0.46187314422288966, "y": 0.1875659030559057},
                                "pointPixels": {
                                    "x": 0.46187314422288966 * 474,
                                    "y": 0.1875659030559057 * 842,
                                },
                                "type": "marker",
                            },
                        ],
                        "type": "pose",
                    }
                ]
            },
        },
        "labelType": "DEFAULT",
        "modelName": None,
    },
    "pageResolutions": None,
    "resolution": {"height": 842, "width": 474},
}

image_rotated_project_asset_unnormalized = {
    "content": "https://storage.googleapis.com/label-backend-staging/projects/clk8fq8edf38d13",
    "externalId": "42015077eed072c50d59232dcc0ad0b1.jpg",
    "id": "clk8fq9ow00022a69icovadtq",
    "jsonContent": "",
    "jsonMetadata": {},
    "latestLabel": {
        "author": {
            "email": "user@kili-technology.com",
            "firstname": "Firstname",
            "id": "123456",
            "lastname": "Lastname",
        },
        "createdAt": "2023-07-18T15:24:11.433Z",
        "isLatestLabelForUser": True,
        "jsonResponse": {
            "OBJECT_DETECTION_JOB": {
                "annotations": [
                    {
                        "boundingPoly": [
                            {
                                "normalizedVertices": [
                                    {
                                        "x": 0.2164674634794157,
                                        "y": 0.7612793663105689,
                                    },
                                    {
                                        "x": 0.09960159362549803,
                                        "y": 0.7612793663105689,
                                    },
                                    {
                                        "x": 0.09960159362549803,
                                        "y": 0.6104079258188485,
                                    },
                                    {
                                        "x": 0.2164674634794157,
                                        "y": 0.6104079258188485,
                                    },
                                ],
                                "vertices": [
                                    {
                                        "x": 102.60557768924305,
                                        "y": 640.997226433499,
                                    },
                                    {
                                        "x": 47.21115537848607,
                                        "y": 640.997226433499,
                                    },
                                    {
                                        "x": 47.21115537848607,
                                        "y": 513.9634735394704,
                                    },
                                    {
                                        "x": 102.60557768924305,
                                        "y": 513.9634735394704,
                                    },
                                ],
                            },
                        ],
                        "categories": [{"name": "A"}],
                        "children": {},
                        "mid": "20230718172351536-92877",
                        "type": "rectangle",
                    }
                ]
            },
            "OBJECT_DETECTION_JOB_0": {
                "annotations": [
                    {
                        "categories": [{"name": "B"}],
                        "children": {},
                        "mid": "20230718172353363-53863",
                        "point": {"x": 0.8727983223923027, "y": 0.2035857007889187},
                        "pointPixels": {
                            "x": 0.8727983223923027 * 474,
                            "y": 0.2035857007889187 * 842,
                        },
                        "type": "marker",
                    }
                ]
            },
            "OBJECT_DETECTION_JOB_1": {
                "annotations": [
                    {
                        "boundingPoly": [
                            {
                                "normalizedVertices": [
                                    {
                                        "x": 0.3067729083665338,
                                        "y": 0.3774165873379637,
                                    },
                                    {
                                        "x": 0.22045152722443562,
                                        "y": 0.3774165873379637,
                                    },
                                    {
                                        "x": 0.22045152722443562,
                                        "y": 0.24182326740236693,
                                    },
                                    {
                                        "x": 0.3067729083665338,
                                        "y": 0.24182326740236693,
                                    },
                                ],
                                "vertices": [
                                    {
                                        "x": 145.41035856573703,
                                        "y": 317.7847665385654,
                                    },
                                    {
                                        "x": 104.49402390438249,
                                        "y": 317.7847665385654,
                                    },
                                    {
                                        "x": 104.49402390438249,
                                        "y": 203.61519115279296,
                                    },
                                    {
                                        "x": 145.41035856573703,
                                        "y": 203.61519115279296,
                                    },
                                ],
                            },
                        ],
                        "categories": [{"name": "C"}],
                        "children": {},
                        "mid": "20230718172356733-32196",
                        "type": "polygon",
                    }
                ]
            },
            "OBJECT_DETECTION_JOB_2": {
                "annotations": [
                    {
                        "categories": [{"name": "D"}],
                        "children": {},
                        "mid": "20230718172359896-17202",
                        "polyline": [
                            {"x": 0.6555950869111132, "y": 0.2574428654046088},
                            {"x": 0.5659240263913562, "y": 0.17890116700672754},
                        ],
                        "polylinePixels": [
                            {"x": 0.6555950869111132 * 474, "y": 0.2574428654046088 * 842},
                            {"x": 0.5659240263913562 * 474, "y": 0.17890116700672754 * 842},
                        ],
                        "type": "polyline",
                    }
                ]
            },
            "OBJECT_DETECTION_JOB_3": {
                "annotations": [
                    {
                        "boundingPoly": [
                            {
                                "normalizedVertices": [
                                    {
                                        "x": 0.4183266932270916,
                                        "y": 0.8433992642997332,
                                    },
                                    {
                                        "x": 0.3373173970783533,
                                        "y": 0.8433992642997332,
                                    },
                                    {
                                        "x": 0.3373173970783533,
                                        "y": 0.7536403060325071,
                                    },
                                    {
                                        "x": 0.4183266932270916,
                                        "y": 0.7536403060325071,
                                    },
                                ],
                                "vertices": [
                                    {
                                        "x": 198.28685258964143,
                                        "y": 710.1421805403754,
                                    },
                                    {
                                        "x": 159.88844621513945,
                                        "y": 710.1421805403754,
                                    },
                                    {
                                        "x": 159.88844621513945,
                                        "y": 634.565137679371,
                                    },
                                    {
                                        "x": 198.28685258964143,
                                        "y": 634.565137679371,
                                    },
                                ],
                            },
                        ],
                        "categories": [{"name": "E"}],
                        "children": {},
                        "mid": "20230718172405691-91771",
                        "type": "semantic",
                    }
                ]
            },
            "POSE_ESTIMATION_JOB": {
                "annotations": [
                    {
                        "categories": [{"name": "HEAD"}],
                        "children": {},
                        "mid": "20230220175803297-40094",
                        "points": [
                            {
                                "children": {},
                                "code": "RIGHT_EARBASE",
                                "mid": "20230220170039711-76095",
                                "point": {"x": 0.350897302238901, "y": 0.18537832978498114},
                                "pointPixels": {
                                    "x": 0.350897302238901 * 474,
                                    "y": 0.18537832978498114 * 842,
                                },
                                "type": "marker",
                            },
                            {
                                "children": {},
                                "code": "RIGHT_EYE",
                                "mid": "20230220170039711-75233",
                                "point": {"x": 0.3581081932428414, "y": 0.2305347416594279},
                                "pointPixels": {
                                    "x": 0.3581081932428414 * 474,
                                    "y": 0.2305347416594279 * 842,
                                },
                                "type": "marker",
                            },
                            {
                                "children": {},
                                "code": "NOSE",
                                "mid": "20230220170039711-59132",
                                "point": {"x": 0.38815357242592613, "y": 0.32807259130823285},
                                "pointPixels": {
                                    "x": 0.38815357242592613 * 474,
                                    "y": 0.32807259130823285 * 842,
                                },
                                "type": "marker",
                            },
                            {
                                "children": {},
                                "code": "LEFT_EYE",
                                "mid": "20230220170039711-27852",
                                "point": {"x": 0.4386476019456967, "y": 0.23889914422760516},
                                "pointPixels": {
                                    "x": 0.4386476019456967 * 474,
                                    "y": 0.23889914422760516 * 842,
                                },
                                "type": "marker",
                            },
                            {
                                "children": {},
                                "code": "LEFT_EARBASE",
                                "mid": "20230220170039711-40802",
                                "point": {"x": 0.46187314422288966, "y": 0.1875659030559057},
                                "pointPixels": {
                                    "x": 0.46187314422288966 * 474,
                                    "y": 0.1875659030559057 * 842,
                                },
                                "type": "marker",
                            },
                        ],
                        "type": "pose",
                    }
                ]
            },
            "ROTATION_JOB": {
                "rotation": 90,
            },
        },
        "labelType": "DEFAULT",
        "modelName": None,
    },
    "pageResolutions": None,
    "resolution": {"height": 842, "width": 474},
}
