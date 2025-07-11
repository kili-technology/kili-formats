from kili_formats.types import ProjectDict

video_asset = {
    "content": "https://storage.googleapis.com/label-public-staging/demo-projects/video/tuto_video.mp4",
    "externalId": "Click here to start",
    "id": "clk9h07o602jv0j5bg5uw1bw7",
    "jsonContent": "",
    "jsonMetadata": {
        "processingParameters": {
            "codec": "h264",
            "delayDueToMinPts": 0,
            "framesPlayedPerSecond": 20,
            "numberOfFrames": 86,
            "shouldKeepNativeFrameRate": True,
            "shouldUseNativeVideo": True,
            "startTime": 0,
        }
    },
    "latestLabel": {
        "author": {
            "email": "test+admin+1@kili-technology.com",
            "firstname": "Feat1",
            "id": "user-feat1-1",
            "lastname": "Test Admin",
        },
        "createdAt": "2023-07-19T08:38:46.356Z",
        "isLatestLabelForUser": True,
        "jsonResponse": {
            "0": {},
            "1": {},
            "2": {},
            "3": {},
            "4": {},
            "5": {},
            "6": {},
            "7": {},
            "8": {},
            "9": {},
            "10": {},
            "11": {
                "OBJECT_DETECTION_JOB": {
                    "annotations": [
                        {
                            "boundingPoly": [
                                {
                                    "normalizedVertices": [
                                        {"x": 0.311841531097634, "y": 0.6538423037514713},
                                        {"x": 0.311841531097634, "y": 0.5449016956222676},
                                        {"x": 0.40148639384560253, "y": 0.5449016956222676},
                                        {"x": 0.40148639384560253, "y": 0.6538423037514713},
                                    ]
                                }
                            ],
                            "categories": [{"name": "A"}],
                            "children": {},
                            "isKeyFrame": True,
                            "mid": "20230719103804051-62814",
                            "type": "rectangle",
                        }
                    ]
                }
            },
            "12": {
                "OBJECT_DETECTION_JOB": {
                    "annotations": [
                        {
                            "boundingPoly": [
                                {
                                    "normalizedVertices": [
                                        {"x": 0.3198865828827081, "y": 0.5560227160354572},
                                        {"x": 0.3198865828827081, "y": 0.6672329201673526},
                                        {"x": 0.40787135557978826, "y": 0.6672329201673526},
                                        {"x": 0.40787135557978826, "y": 0.5560227160354572},
                                    ]
                                }
                            ],
                            "categories": [{"name": "A"}],
                            "children": {},
                            "isKeyFrame": False,
                            "mid": "20230719103804051-62814",
                            "type": "rectangle",
                        }
                    ]
                }
            },
        },
        "labelType": "DEFAULT",
        "modelName": None,
    },
    "pageResolutions": None,
    "resolution": {"height": 1080, "width": 1920},
}
video_project: ProjectDict = {
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
                "models": {"tracking": {}},
            }
        }
    },
    "inputType": "VIDEO",
    "title": "Object tracking on video",
    "description": "Use bounding-box to track objects across video frames.",
    "id": "fake_proj_id",
    "organizationId": "fake_org_id",
}
video_project_asset_unnormalized = {
    "content": (
        "https://storage.googleapis.com/label-public-staging/demo-projects/video/tuto_video.mp4"
    ),
    "externalId": "Click here to start",
    "id": "clk9h07o602jv0j5bg5uw1bw7",
    "jsonContent": "",
    "jsonMetadata": {
        "processingParameters": {
            "codec": "h264",
            "delayDueToMinPts": 0,
            "framesPlayedPerSecond": 20,
            "numberOfFrames": 86,
            "shouldKeepNativeFrameRate": True,
            "shouldUseNativeVideo": True,
            "startTime": 0,
        }
    },
    "latestLabel": {
        "author": {
            "email": "test+admin+1@kili-technology.com",
            "firstname": "Feat1",
            "id": "user-feat1-1",
            "lastname": "Test Admin",
        },
        "createdAt": "2023-07-19T08:38:46.356Z",
        "isLatestLabelForUser": True,
        "jsonResponse": {
            "0": {},
            "1": {},
            "2": {},
            "3": {},
            "4": {},
            "5": {},
            "6": {},
            "7": {},
            "8": {},
            "9": {},
            "10": {},
            "11": {
                "OBJECT_DETECTION_JOB": {
                    "annotations": [
                        {
                            "boundingPoly": [
                                {
                                    "normalizedVertices": [
                                        {
                                            "x": 0.311841531097634,
                                            "y": 0.6538423037514713,
                                        },
                                        {
                                            "x": 0.311841531097634,
                                            "y": 0.5449016956222676,
                                        },
                                        {
                                            "x": 0.40148639384560253,
                                            "y": 0.5449016956222676,
                                        },
                                        {
                                            "x": 0.40148639384560253,
                                            "y": 0.6538423037514713,
                                        },
                                    ],
                                    "vertices": [
                                        {
                                            "x": 1920 * 0.311841531097634,
                                            "y": 1080 * 0.6538423037514713,
                                        },
                                        {
                                            "x": 1920 * 0.311841531097634,
                                            "y": 1080 * 0.5449016956222676,
                                        },
                                        {
                                            "x": 1920 * 0.40148639384560253,
                                            "y": 1080 * 0.5449016956222676,
                                        },
                                        {
                                            "x": 1920 * 0.40148639384560253,
                                            "y": 1080 * 0.6538423037514713,
                                        },
                                    ],
                                }
                            ],
                            "categories": [{"name": "A"}],
                            "children": {},
                            "isKeyFrame": True,
                            "mid": "20230719103804051-62814",
                            "type": "rectangle",
                        }
                    ]
                }
            },
            "12": {
                "OBJECT_DETECTION_JOB": {
                    "annotations": [
                        {
                            "boundingPoly": [
                                {
                                    "normalizedVertices": [
                                        {
                                            "x": 0.3198865828827081,
                                            "y": 0.5560227160354572,
                                        },
                                        {
                                            "x": 0.3198865828827081,
                                            "y": 0.6672329201673526,
                                        },
                                        {
                                            "x": 0.40787135557978826,
                                            "y": 0.6672329201673526,
                                        },
                                        {
                                            "x": 0.40787135557978826,
                                            "y": 0.5560227160354572,
                                        },
                                    ],
                                    "vertices": [
                                        {
                                            "x": 1920 * 0.3198865828827081,
                                            "y": 1080 * 0.5560227160354572,
                                        },
                                        {
                                            "x": 1920 * 0.3198865828827081,
                                            "y": 1080 * 0.6672329201673526,
                                        },
                                        {
                                            "x": 1920 * 0.40787135557978826,
                                            "y": 1080 * 0.6672329201673526,
                                        },
                                        {
                                            "x": 1920 * 0.40787135557978826,
                                            "y": 1080 * 0.5560227160354572,
                                        },
                                    ],
                                }
                            ],
                            "categories": [{"name": "A"}],
                            "children": {},
                            "isKeyFrame": False,
                            "mid": "20230719103804051-62814",
                            "type": "rectangle",
                        }
                    ]
                }
            },
        },
        "labelType": "DEFAULT",
        "modelName": None,
    },
    "pageResolutions": None,
    "resolution": {"height": 1080, "width": 1920},
}

latest_label_annotations_rectangle_rotated = {
    "annotations": [
        {
            "__typename": "VideoObjectDetectionAnnotation",
            "id": "20250611172432110-2",
            "job": "JOB_0",
            "path": [],
            "labelId": "cmbs3q9ie001n8m9kf78bg0xy",
            "frames": [{"end": 10, "start": 0}],
            "keyAnnotations": [
                {
                    "frame": 0,
                    "id": "20250611172432110-2-0",
                    "annotationValue": {
                        "vertices": [
                            [
                                [
                                    {"x": 0.38151816589866916, "y": 0.7515395920400955},
                                    {"x": 0.36739440026464604, "y": 0.591311803253454},
                                    {"x": 0.4939204305925588, "y": 0.5560627471411912},
                                    {"x": 0.5080441962265819, "y": 0.7162905359278327},
                                ]
                            ]
                        ]
                    },
                },
                {
                    "frame": 6,
                    "id": "20250611172432110-2-6",
                    "annotationValue": {
                        "vertices": [
                            [
                                [
                                    {"x": 0.4473684210526316, "y": 0.6816778376334383},
                                    {"x": 0.43664287285794606, "y": 0.5441606027764878},
                                    {"x": 0.33269774529216684, "y": 0.5697470957157564},
                                    {"x": 0.34334115959042594, "y": 0.7059936085567078},
                                ]
                            ]
                        ]
                    },
                },
                {
                    "frame": 14,
                    "id": "20250611172432110-2-14",
                    "annotationValue": {
                        "vertices": [
                            [
                                [
                                    {"x": 0.29844705572561797, "y": 0.6693395360404346},
                                    {"x": 0.28771929824561404, "y": 0.5475906182543382},
                                    {"x": 0.37723354629347966, "y": 0.5232757552197771},
                                    {"x": 0.387719298245614, "y": 0.644258148504387},
                                ]
                            ]
                        ]
                    },
                },
            ],
            "category": "OBJECT_B",
            "mid": "20250611172428468-1",
            "name": "Car 1",
        }
    ],
    "author": {
        "email": "test+admin@kili-technology.com",
        "firstname": "Test",
        "id": "user-1",
        "lastname": "Admin",
    },
    "createdAt": "2025-06-11T15:25:32.966Z",
    "isLatestLabelForUser": True,
    "isSentBackToQueue": False,
    "jsonResponse": {
        "0": {
            "ANNOTATION_JOB_COUNTER": {"JOB_0": {"OBJECT_B": 1}},
            "ANNOTATION_NAMES_JOB": {"20250611172428468-1": "Car 1"},
        }
    },
    "labelType": "DEFAULT",
    "modelName": None,
}
latest_label_annotations_rectangle = {
    "annotations": [
        {
            "__typename": "VideoObjectDetectionAnnotation",
            "id": "20250602131124989-8",
            "job": "JOB_0",
            "path": [],
            "labelId": "cmbezotki049em39k2v08gz5l",
            "frames": [{"end": 0, "start": 0}],
            "keyAnnotations": [
                {
                    "frame": 0,
                    "id": "20250602131124989-8-0",
                    "annotationValue": {
                        "vertices": [
                            [
                                [
                                    {"x": 0.37250948766603414, "y": 0.7419354838709677},
                                    {"x": 0.37250948766603414, "y": 0.5711574952561669},
                                    {"x": 0.5005929791271347, "y": 0.5711574952561669},
                                    {"x": 0.5005929791271347, "y": 0.7419354838709677},
                                ]
                            ]
                        ]
                    },
                }
            ],
            "category": "OBJECT_B",
            "mid": "20250602131121389-7",
            "name": "Car 1",
        }
    ],
    "author": {
        "email": "test+admin@kili-technology.com",
        "firstname": "Test",
        "id": "user-1",
        "lastname": "Admin",
    },
    "createdAt": "2025-06-02T11:11:26.898Z",
    "isLatestLabelForUser": True,
    "isSentBackToQueue": False,
    "jsonResponse": {
        "0": {
            "ANNOTATION_JOB_COUNTER": {"JOB_0": {"OBJECT_B": 1}},
            "ANNOTATION_NAMES_JOB": {"20250602131121389-7": "Car 1"},
        }
    },
    "labelType": "DEFAULT",
    "modelName": None,
}
latest_label_annotations_polygon = {
    "annotations": [
        {
            "__typename": "VideoObjectDetectionAnnotation",
            "id": "20250602134212280-11",
            "job": "OBJECT_DETECTION_JOB",
            "path": [],
            "labelId": "cmbf0sewn04lem39kgtbh5ggw",
            "frames": [{"end": 0, "start": 0}],
            "keyAnnotations": [
                {
                    "frame": 0,
                    "id": "20250602134212280-11-0",
                    "annotationValue": {
                        "vertices": [
                            [
                                [
                                    {"x": 0.36717267552182165, "y": 0.5957106226563309},
                                    {"x": 0.3959914611005693, "y": 0.5653559412470912},
                                    {"x": 0.48991935483870974, "y": 0.5577672708947812},
                                    {"x": 0.5134013282732448, "y": 0.7342038565859876},
                                    {"x": 0.4002609108159393, "y": 0.751278364878685},
                                ]
                            ]
                        ]
                    },
                }
            ],
            "category": "TEST",
            "mid": "20250602134206930-10",
            "name": "Test 1",
        }
    ],
    "author": {
        "email": "test+admin@kili-technology.com",
        "firstname": "Test",
        "id": "user-1",
        "lastname": "Admin",
    },
    "createdAt": "2025-06-02T11:42:14.135Z",
    "isLatestLabelForUser": True,
    "isSentBackToQueue": False,
    "jsonResponse": {
        "0": {
            "ANNOTATION_JOB_COUNTER": {"OBJECT_DETECTION_JOB": {"TEST": 1}},
            "ANNOTATION_NAMES_JOB": {"20250602134206930-10": "Test 1"},
        }
    },
    "labelType": "REVIEW",
    "modelName": None,
}
latest_label_annotations_semantic = {
    "annotations": [
        {
            "__typename": "VideoObjectDetectionAnnotation",
            "id": "20250602144338196-2",
            "job": "OBJECT_DETECTION_JOB",
            "path": [],
            "labelId": "cmbf2ziox05sim39k4we534kc",
            "frames": [{"end": 0, "start": 0}],
            "keyAnnotations": [
                {
                    "frame": 0,
                    "id": "20250602144338196-2-0",
                    "annotationValue": {
                        "vertices": [
                            [
                                [
                                    {"x": 0.38416210624999997, "y": 0.5150611305555556},
                                    {"x": 0.3841575109375, "y": 0.5150611305555556},
                                    {"x": 0.3841483197916667, "y": 0.5150611305555556},
                                    {"x": 0.38414372395833335, "y": 0.5150611305555556},
                                    {"x": 0.384139128125, "y": 0.5150692990740742},
                                    {"x": 0.38413453281250004, "y": 0.5150774675925927},
                                    {"x": 0.3841299369791667, "y": 0.5150856361111111},
                                    {"x": 0.3841253416666667, "y": 0.5150856361111111},
                                    {"x": 0.3841253416666667, "y": 0.5150938046296296},
                                    {"x": 0.3841253416666667, "y": 0.5151019731481481},
                                    {"x": 0.3841253416666667, "y": 0.5151101416666666},
                                    {"x": 0.3841299369791667, "y": 0.5151101416666666},
                                    {"x": 0.38413453281250004, "y": 0.5151101416666666},
                                    {"x": 0.38413453281250004, "y": 0.5151183101851852},
                                    {"x": 0.384139128125, "y": 0.5151183101851852},
                                    {"x": 0.38414372395833335, "y": 0.5151264787037038},
                                    {"x": 0.3841483197916667, "y": 0.5151264787037038},
                                    {"x": 0.38415291510416666, "y": 0.5151264787037038},
                                    {"x": 0.3841575109375, "y": 0.5151264787037038},
                                    {"x": 0.38416210624999997, "y": 0.5151264787037038},
                                    {"x": 0.3841667020833333, "y": 0.5151264787037038},
                                    {"x": 0.38417129791666665, "y": 0.5151264787037038},
                                    {"x": 0.3841758932291667, "y": 0.5151264787037038},
                                    {"x": 0.38418048906249996, "y": 0.5151264787037038},
                                    {"x": 0.384185084375, "y": 0.5151264787037038},
                                    {"x": 0.384185084375, "y": 0.5151183101851852},
                                    {"x": 0.38418968020833333, "y": 0.5151101416666666},
                                    {"x": 0.38418968020833333, "y": 0.5151019731481481},
                                ]
                            ]
                        ]
                    },
                }
            ],
            "category": "TEST",
            "mid": "20250602144334575-1",
            "name": "Test 3",
        }
    ],
    "author": {
        "email": "test+admin@kili-technology.com",
        "firstname": "Test",
        "id": "user-1",
        "lastname": "Admin",
    },
    "createdAt": "2025-06-02T12:43:44.865Z",
    "isLatestLabelForUser": True,
    "isSentBackToQueue": False,
    "jsonResponse": {
        "0": {
            "ANNOTATION_JOB_COUNTER": {"OBJECT_DETECTION_JOB": {"TEST": 1}},
            "ANNOTATION_NAMES_JOB": {"20250602144334575-1": "Test 3"},
        }
    },
    "labelType": "REVIEW",
    "modelName": None,
}
latest_label_annotations_semantic_with_hole = {
    "annotations": [
        {
            "__typename": "VideoObjectDetectionAnnotation",
            "id": "20250602144338196-2",
            "job": "OBJECT_DETECTION_JOB",
            "path": [],
            "labelId": "cmbf3l6mj0659m39ka2dy85id",
            "frames": [{"end": 0, "start": 0}],
            "keyAnnotations": [
                {
                    "frame": 0,
                    "id": "20250602144338196-2-0",
                    "annotationValue": {
                        "vertices": [
                            [
                                [
                                    {"x": 0.3841253416666667, "y": 0.5151101416666666},
                                    {"x": 0.38413453281250004, "y": 0.5151101416666666},
                                    {"x": 0.38413453281250004, "y": 0.5151183101851852},
                                    {"x": 0.384139128125, "y": 0.5151183101851852},
                                    {"x": 0.38414372395833335, "y": 0.5151264787037038},
                                    {"x": 0.384185084375, "y": 0.5151264787037038},
                                    {"x": 0.384185084375, "y": 0.5151183101851852},
                                    {"x": 0.38418968020833333, "y": 0.5151101416666666},
                                    {"x": 0.38418968020833333, "y": 0.5151019731481481},
                                    {"x": 0.38416210624999997, "y": 0.5150611305555556},
                                    {"x": 0.38414372395833335, "y": 0.5150611305555556},
                                    {"x": 0.384139128125, "y": 0.5150692990740742},
                                    {"x": 0.38413453281250004, "y": 0.5150774675925927},
                                    {"x": 0.3841299369791667, "y": 0.5150856361111111},
                                    {"x": 0.3841253416666667, "y": 0.5150856361111111},
                                ],
                                [
                                    {"x": 0.38414881458333333, "y": 0.5150947064814815},
                                    {"x": 0.38414881458333333, "y": 0.5150921648148148},
                                    {"x": 0.3841489578125, "y": 0.5150916564814815},
                                    {"x": 0.38414910052083334, "y": 0.5150911490740742},
                                    {"x": 0.38414910052083334, "y": 0.5150906407407407},
                                    {"x": 0.38414924375, "y": 0.5150901324074073},
                                    {"x": 0.38414938645833335, "y": 0.5150893694444445},
                                    {"x": 0.3841495296875, "y": 0.5150891157407407},
                                    {"x": 0.3841495296875, "y": 0.5150886074074075},
                                    {"x": 0.384149815625, "y": 0.515088099074074},
                                    {"x": 0.38415010156249996, "y": 0.5150878453703704},
                                    {"x": 0.3841513880208333, "y": 0.5150875907407406},
                                    {"x": 0.38415496250000003, "y": 0.5150875907407406},
                                    {"x": 0.38415596354166665, "y": 0.5150888611111111},
                                    {"x": 0.38415610625, "y": 0.5150888611111111},
                                    {"x": 0.38415639218750003, "y": 0.5150893694444445},
                                    {"x": 0.384156678125, "y": 0.5150893694444445},
                                    {"x": 0.3841568213541667, "y": 0.5150896240740741},
                                    {"x": 0.3841569640625, "y": 0.5150896240740741},
                                    {"x": 0.38415710729166663, "y": 0.5150901324074073},
                                    {"x": 0.38415710729166663, "y": 0.5150906407407407},
                                    {"x": 0.38415725, "y": 0.5150908944444446},
                                    {"x": 0.38415725, "y": 0.5150926731481481},
                                    {"x": 0.38415710729166663, "y": 0.5150929277777777},
                                    {"x": 0.38415710729166663, "y": 0.5150934361111111},
                                    {"x": 0.3841569640625, "y": 0.5150936898148148},
                                    {"x": 0.3841569640625, "y": 0.5150949601851852},
                                    {"x": 0.3841568213541667, "y": 0.5150949601851852},
                                    {"x": 0.3841568213541667, "y": 0.5150952148148148},
                                    {"x": 0.384156678125, "y": 0.5150952148148148},
                                    {"x": 0.38415639218750003, "y": 0.5150954685185185},
                                    {"x": 0.3841562494791667, "y": 0.5150957231481481},
                                    {"x": 0.38415596354166665, "y": 0.5150957231481481},
                                    {"x": 0.384155534375, "y": 0.5150959768518519},
                                    {"x": 0.3841552484375, "y": 0.5150962314814815},
                                    {"x": 0.38415496250000003, "y": 0.5150962314814815},
                                    {"x": 0.3841546765625, "y": 0.5150964851851851},
                                    {"x": 0.384150959375, "y": 0.5150964851851851},
                                    {"x": 0.38415053020833334, "y": 0.5150962314814815},
                                    {"x": 0.38415010156249996, "y": 0.5150962314814815},
                                    {"x": 0.3841499583333333, "y": 0.5150959768518519},
                                    {"x": 0.3841496723958333, "y": 0.5150957231481481},
                                    {"x": 0.3841495296875, "y": 0.5150957231481481},
                                    {"x": 0.38414938645833335, "y": 0.5150954685185185},
                                    {"x": 0.38414924375, "y": 0.5150954685185185},
                                    {"x": 0.38414910052083334, "y": 0.5150952148148148},
                                    {"x": 0.3841489578125, "y": 0.5150949601851852},
                                ],
                            ]
                        ]
                    },
                }
            ],
            "category": "TEST",
            "mid": "20250602144334575-1",
            "name": "Test 3",
        }
    ],
    "author": {
        "email": "test+admin@kili-technology.com",
        "firstname": "Test",
        "id": "user-1",
        "lastname": "Admin",
    },
    "createdAt": "2025-06-02T13:00:35.659Z",
    "isLatestLabelForUser": True,
    "isSentBackToQueue": False,
    "jsonResponse": {
        "0": {
            "ANNOTATION_JOB_COUNTER": {"OBJECT_DETECTION_JOB": {"TEST": 1}},
            "ANNOTATION_NAMES_JOB": {"20250602144334575-1": "Test 3"},
        }
    },
    "labelType": "REVIEW",
    "modelName": None,
}
latest_label_annotations_semantic_multipart = {
    "annotations": [
        {
            "__typename": "VideoObjectDetectionAnnotation",
            "id": "20250602144338196-2",
            "job": "OBJECT_DETECTION_JOB",
            "path": [],
            "labelId": "cmbf4g2ty06njm39k3bqm0xtt",
            "frames": [{"end": 0, "start": 0}],
            "keyAnnotations": [
                {
                    "frame": 0,
                    "id": "20250602144338196-2-0",
                    "annotationValue": {
                        "vertices": [
                            [
                                [
                                    {"x": 0.3841253416666667, "y": 0.5151101416666666},
                                    {"x": 0.38413453281250004, "y": 0.5151101416666666},
                                    {"x": 0.38413453281250004, "y": 0.5151183101851852},
                                    {"x": 0.384139128125, "y": 0.5151183101851852},
                                    {"x": 0.38414372395833335, "y": 0.5151264787037038},
                                    {"x": 0.384185084375, "y": 0.5151264787037038},
                                    {"x": 0.384185084375, "y": 0.5151183101851852},
                                    {"x": 0.38418968020833333, "y": 0.5151101416666666},
                                    {"x": 0.38418968020833333, "y": 0.5151019731481481},
                                    {"x": 0.38416210624999997, "y": 0.5150611305555556},
                                    {"x": 0.38414372395833335, "y": 0.5150611305555556},
                                    {"x": 0.384139128125, "y": 0.5150692990740742},
                                    {"x": 0.38413453281250004, "y": 0.5150774675925927},
                                    {"x": 0.3841299369791667, "y": 0.5150856361111111},
                                    {"x": 0.3841253416666667, "y": 0.5150856361111111},
                                ]
                            ],
                            [
                                [
                                    {"x": 0.384200771875, "y": 0.5150941185185185},
                                    {"x": 0.38420065052083335, "y": 0.5150941185185185},
                                    {"x": 0.3842004067708333, "y": 0.5150943351851851},
                                    {"x": 0.38420016354166664, "y": 0.5150945509259259},
                                    {"x": 0.38419979895833334, "y": 0.5150949833333334},
                                    {"x": 0.38419943385416666, "y": 0.5150956324074074},
                                    {"x": 0.3841993119791667, "y": 0.515095848148148},
                                    {"x": 0.38419906875, "y": 0.5150962805555556},
                                    {"x": 0.38419882552083334, "y": 0.5150967129629629},
                                    {"x": 0.3841987041666667, "y": 0.5150971453703704},
                                    {"x": 0.3841987041666667, "y": 0.515097362037037},
                                    {"x": 0.3841987041666667, "y": 0.5150977944444444},
                                    {"x": 0.3841987041666667, "y": 0.5150980111111111},
                                    {"x": 0.3841987041666667, "y": 0.5150984435185185},
                                    {"x": 0.38419882552083334, "y": 0.5150986592592592},
                                    {"x": 0.3841989473958333, "y": 0.5150988759259258},
                                    {"x": 0.38419906875, "y": 0.5150990916666667},
                                    {"x": 0.384199190625, "y": 0.5150993083333333},
                                    {"x": 0.384199190625, "y": 0.5150995240740741},
                                    {"x": 0.3841993119791667, "y": 0.5150997407407407},
                                    {"x": 0.3841995552083333, "y": 0.5150999564814815},
                                    {"x": 0.3841996770833333, "y": 0.5150999564814815},
                                    {"x": 0.38419979895833334, "y": 0.5151001731481482},
                                    {"x": 0.3842000421875, "y": 0.5151003888888889},
                                    {"x": 0.38420016354166664, "y": 0.5151003888888889},
                                    {"x": 0.3842005286458334, "y": 0.5151003888888889},
                                    {"x": 0.384200771875, "y": 0.5151003888888889},
                                    {"x": 0.38420101510416665, "y": 0.5151003888888889},
                                    {"x": 0.38420138020833333, "y": 0.5151003888888889},
                                    {"x": 0.38420186666666667, "y": 0.5151001731481482},
                                    {"x": 0.3842022317708333, "y": 0.5150999564814815},
                                    {"x": 0.384202596875, "y": 0.5150995240740741},
                                    {"x": 0.3842029614583333, "y": 0.5150993083333333},
                                    {"x": 0.38420320520833334, "y": 0.5150990916666667},
                                    {"x": 0.3842033265625, "y": 0.5150988759259258},
                                    {"x": 0.3842034484375, "y": 0.5150986592592592},
                                    {"x": 0.38420356979166664, "y": 0.5150984435185185},
                                    {"x": 0.38420356979166664, "y": 0.5150982268518519},
                                    {"x": 0.38420356979166664, "y": 0.5150980111111111},
                                    {"x": 0.3842036916666667, "y": 0.5150977944444444},
                                    {"x": 0.3842036916666667, "y": 0.5150975787037038},
                                    {"x": 0.3842036916666667, "y": 0.5150971453703704},
                                    {"x": 0.3842036916666667, "y": 0.5150967129629629},
                                    {"x": 0.3842036916666667, "y": 0.5150962805555556},
                                    {"x": 0.3842036916666667, "y": 0.5150960648148148},
                                    {"x": 0.3842036916666667, "y": 0.5150956324074074},
                                    {"x": 0.38420356979166664, "y": 0.5150954157407408},
                                    {"x": 0.3842034484375, "y": 0.5150949833333334},
                                    {"x": 0.3842033265625, "y": 0.5150947675925927},
                                    {"x": 0.38420320520833334, "y": 0.5150945509259259},
                                    {"x": 0.38420308333333336, "y": 0.5150943351851851},
                                    {"x": 0.38420284010416667, "y": 0.5150941185185185},
                                    {"x": 0.3842027182291667, "y": 0.5150939027777778},
                                    {"x": 0.38420247500000004, "y": 0.5150939027777778},
                                    {"x": 0.3842022317708333, "y": 0.5150939027777778},
                                ]
                            ],
                        ]
                    },
                }
            ],
            "category": "TEST",
            "mid": "20250602144334575-1",
            "name": "Test 3",
        }
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
    "jsonResponse": {
        "0": {
            "ANNOTATION_JOB_COUNTER": {"OBJECT_DETECTION_JOB": {"TEST": 1}},
            "ANNOTATION_NAMES_JOB": {"20250602144334575-1": "Test 3"},
        }
    },
    "labelType": "REVIEW",
    "modelName": None,
}
latest_label_annotations_asset_level = {
    "annotations": [
        {
            "__typename": "ClassificationAnnotation",
            "id": "20250630101255345-3",
            "job": "classification_at_asset_level",
            "path": [],
            "labelId": "cmcixnyx302ts9g9k95z2c6st",
            "annotationValue": {"categories": ["OUI"]},
            "chatItemId": None,
        },
        {
            "__typename": "TranscriptionAnnotation",
            "id": "20250630120051158-1",
            "job": "transcription_at_asset_level",
            "path": [],
            "labelId": "cmcixnyx302ts9g9k95z2c6st",
            "annotationValue": {"text": "this is a transcription at asset level"},
            "chatItemId": None,
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
    "jsonResponse": {"0": {"ANNOTATION_JOB_COUNTER": {}, "ANNOTATION_NAMES_JOB": {}}},
    "labelType": "REVIEW",
    "modelName": None,
}

expected_latest_label_result_rectangle = {
    "author": {
        "email": "test+admin@kili-technology.com",
        "firstname": "Test",
        "id": "user-1",
        "lastname": "Admin",
    },
    "createdAt": "2025-06-02T11:11:26.898Z",
    "isLatestLabelForUser": True,
    "isSentBackToQueue": False,
    "jsonResponse": {
        "0": {
            "JOB_0": {
                "annotations": [
                    {
                        "children": {},
                        "isKeyFrame": True,
                        "categories": [{"name": "OBJECT_B"}],
                        "mid": "20250602131121389-7",
                        "type": "rectangle",
                        "boundingPoly": [
                            {
                                "normalizedVertices": [
                                    {"x": 0.37250948766603414, "y": 0.7419354838709677},
                                    {"x": 0.37250948766603414, "y": 0.5711574952561669},
                                    {"x": 0.5005929791271347, "y": 0.5711574952561669},
                                    {"x": 0.5005929791271347, "y": 0.7419354838709677},
                                ]
                            }
                        ],
                    }
                ]
            },
            "ANNOTATION_JOB_COUNTER": {"JOB_0": {"OBJECT_B": 1}},
            "ANNOTATION_NAMES_JOB": {"20250602131121389-7": "Car 1"},
        }
    },
    "labelType": "DEFAULT",
    "modelName": None,
}
expected_latest_label_result_rectangle_rotated = {
    "author": {
        "email": "test+admin@kili-technology.com",
        "firstname": "Test",
        "id": "user-1",
        "lastname": "Admin",
    },
    "createdAt": "2025-06-11T15:25:32.966Z",
    "isLatestLabelForUser": True,
    "isSentBackToQueue": False,
    "jsonResponse": {
        "0": {
            "ANNOTATION_JOB_COUNTER": {
                "JOB_0": {
                    "OBJECT_B": 1,
                }
            },
            "ANNOTATION_NAMES_JOB": {
                "20250611172428468-1": "Car 1",
            },
            "JOB_0": {
                "annotations": [
                    {
                        "boundingPoly": [
                            {
                                "normalizedVertices": [
                                    {
                                        "x": 0.38151816589866916,
                                        "y": 0.7515395920400955,
                                    },
                                    {
                                        "x": 0.36739440026464604,
                                        "y": 0.591311803253454,
                                    },
                                    {
                                        "x": 0.4939204305925588,
                                        "y": 0.5560627471411912,
                                    },
                                    {
                                        "x": 0.5080441962265819,
                                        "y": 0.7162905359278327,
                                    },
                                ],
                            },
                        ],
                        "categories": [
                            {
                                "name": "OBJECT_B",
                            },
                        ],
                        "children": {},
                        "isKeyFrame": True,
                        "mid": "20250611172428468-1",
                        "type": "rectangle",
                    },
                ],
            },
        },
        "1": {
            "JOB_0": {
                "annotations": [
                    {
                        "boundingPoly": [
                            {
                                "normalizedVertices": [
                                    {
                                        "x": 0.5519165866947012,
                                        "y": 0.7025939844520813,
                                    },
                                    {
                                        "x": 0.430471751501098,
                                        "y": 0.5618829162905962,
                                    },
                                    {
                                        "x": 0.307612915789384,
                                        "y": 0.5954336667545235,
                                    },
                                    {
                                        "x": 0.4290577509829872,
                                        "y": 0.7361447349160086,
                                    },
                                ],
                            },
                        ],
                        "categories": [
                            {
                                "name": "OBJECT_B",
                            },
                        ],
                        "children": {},
                        "isKeyFrame": False,
                        "mid": "20250611172428468-1",
                        "type": "rectangle",
                    },
                ],
            },
        },
        "2": {
            "JOB_0": {
                "annotations": [
                    {
                        "boundingPoly": [
                            {
                                "normalizedVertices": [
                                    {
                                        "x": 0.539589038930231,
                                        "y": 0.6970962577496009,
                                    },
                                    {
                                        "x": 0.42318349062154,
                                        "y": 0.5594694300718758,
                                    },
                                    {
                                        "x": 0.30403136954671167,
                                        "y": 0.5913567054823222,
                                    },
                                    {
                                        "x": 0.4204369178554027,
                                        "y": 0.7289835331600473,
                                    },
                                ],
                            },
                        ],
                        "categories": [
                            {
                                "name": "OBJECT_B",
                            },
                        ],
                        "children": {},
                        "isKeyFrame": False,
                        "mid": "20250611172428468-1",
                        "type": "rectangle",
                    },
                ],
            },
        },
        "3": {
            "JOB_0": {
                "annotations": [
                    {
                        "boundingPoly": [
                            {
                                "normalizedVertices": [
                                    {
                                        "x": 0.5272892633106142,
                                        "y": 0.6915631160060605,
                                    },
                                    {
                                        "x": 0.4158286875862567,
                                        "y": 0.5570562843319565,
                                    },
                                    {
                                        "x": 0.30042205115918563,
                                        "y": 0.5873151592511807,
                                    },
                                    {
                                        "x": 0.4118826268835432,
                                        "y": 0.7218219909252847,
                                    },
                                ],
                            },
                        ],
                        "categories": [
                            {
                                "name": "OBJECT_B",
                            },
                        ],
                        "children": {},
                        "isKeyFrame": False,
                        "mid": "20250611172428468-1",
                        "type": "rectangle",
                    },
                ],
            },
        },
        "4": {
            "JOB_0": {
                "annotations": [
                    {
                        "boundingPoly": [
                            {
                                "normalizedVertices": [
                                    {
                                        "x": 0.5150179801892442,
                                        "y": 0.6859947625709126,
                                    },
                                    {
                                        "x": 0.4084073764200846,
                                        "y": 0.5546430362481952,
                                    },
                                    {
                                        "x": 0.2967842402734132,
                                        "y": 0.5833088247116466,
                                    },
                                    {
                                        "x": 0.4033948440425727,
                                        "y": 0.714660551034364,
                                    },
                                ],
                            },
                        ],
                        "categories": [
                            {
                                "name": "OBJECT_B",
                            },
                        ],
                        "children": {},
                        "isKeyFrame": False,
                        "mid": "20250611172428468-1",
                        "type": "rectangle",
                    },
                ],
            },
        },
        "5": {
            "JOB_0": {
                "annotations": [
                    {
                        "boundingPoly": [
                            {
                                "normalizedVertices": [
                                    {
                                        "x": 0.5027759059289272,
                                        "y": 0.6803914049788155,
                                    },
                                    {
                                        "x": 0.40091959942739885,
                                        "y": 0.5522292433304743,
                                    },
                                    {
                                        "x": 0.29311722052658734,
                                        "y": 0.579337494329062,
                                    },
                                    {
                                        "x": 0.3949735270281157,
                                        "y": 0.7074996559774032,
                                    },
                                ],
                            },
                        ],
                        "categories": [
                            {
                                "name": "OBJECT_B",
                            },
                        ],
                        "children": {},
                        "isKeyFrame": False,
                        "mid": "20250611172428468-1",
                        "type": "rectangle",
                    },
                ],
            },
        },
        "6": {
            "JOB_0": {
                "annotations": [
                    {
                        "boundingPoly": [
                            {
                                "normalizedVertices": [
                                    {
                                        "x": 0.4473684210526316,
                                        "y": 0.6816778376334383,
                                    },
                                    {
                                        "x": 0.43664287285794606,
                                        "y": 0.5441606027764878,
                                    },
                                    {
                                        "x": 0.33269774529216684,
                                        "y": 0.5697470957157564,
                                    },
                                    {
                                        "x": 0.34334115959042594,
                                        "y": 0.7059936085567078,
                                    },
                                ],
                            },
                        ],
                        "categories": [
                            {
                                "name": "OBJECT_B",
                            },
                        ],
                        "children": {},
                        "isKeyFrame": True,
                        "mid": "20250611172428468-1",
                        "type": "rectangle",
                    },
                ],
            },
        },
        "7": {
            "JOB_0": {
                "annotations": [
                    {
                        "boundingPoly": [
                            {
                                "normalizedVertices": [
                                    {
                                        "x": 0.28359980844570865,
                                        "y": 0.5727403060372047,
                                    },
                                    {
                                        "x": 0.3812628911654557,
                                        "y": 0.6966964942357857,
                                    },
                                    {
                                        "x": 0.4833879116673934,
                                        "y": 0.6712376064881812,
                                    },
                                    {
                                        "x": 0.38572482894764637,
                                        "y": 0.5472814182896002,
                                    },
                                ],
                            },
                        ],
                        "categories": [
                            {
                                "name": "OBJECT_B",
                            },
                        ],
                        "children": {},
                        "isKeyFrame": False,
                        "mid": "20250611172428468-1",
                        "type": "rectangle",
                    },
                ],
            },
        },
        "8": {
            "JOB_0": {
                "annotations": [
                    {
                        "boundingPoly": [
                            {
                                "normalizedVertices": [
                                    {
                                        "x": 0.27820592361298063,
                                        "y": 0.5700196741972453,
                                    },
                                    {
                                        "x": 0.37539401352941115,
                                        "y": 0.6918335012755875,
                                    },
                                    {
                                        "x": 0.4757033502684251,
                                        "y": 0.666511217504332,
                                    },
                                    {
                                        "x": 0.3785152603519946,
                                        "y": 0.5446973904259896,
                                    },
                                ],
                            },
                        ],
                        "categories": [
                            {
                                "name": "OBJECT_B",
                            },
                        ],
                        "children": {},
                        "isKeyFrame": False,
                        "mid": "20250611172428468-1",
                        "type": "rectangle",
                    },
                ],
            },
        },
        "9": {
            "JOB_0": {
                "annotations": [
                    {
                        "boundingPoly": [
                            {
                                "normalizedVertices": [
                                    {
                                        "x": 0.27282648312092234,
                                        "y": 0.5672919317750155,
                                    },
                                    {
                                        "x": 0.36950615857353797,
                                        "y": 0.686968640667589,
                                    },
                                    {
                                        "x": 0.46800434452878714,
                                        "y": 0.6617919391027532,
                                    },
                                    {
                                        "x": 0.3713246690761715,
                                        "y": 0.5421152302101796,
                                    },
                                ],
                            },
                        ],
                        "categories": [
                            {
                                "name": "OBJECT_B",
                            },
                        ],
                        "children": {},
                        "isKeyFrame": False,
                        "mid": "20250611172428468-1",
                        "type": "rectangle",
                    },
                ],
            },
        },
        "10": {
            "JOB_0": {
                "annotations": [
                    {
                        "boundingPoly": [
                            {
                                "normalizedVertices": [
                                    {
                                        "x": 0.2674613937218017,
                                        "y": 0.5645570248326202,
                                    },
                                    {
                                        "x": 0.3635993101129763,
                                        "y": 0.6821019872841423,
                                    },
                                    {
                                        "x": 0.46029098769621146,
                                        "y": 0.6570798252213398,
                                    },
                                    {
                                        "x": 0.3641530713050369,
                                        "y": 0.5395348627698177,
                                    },
                                ],
                            },
                        ],
                        "categories": [
                            {
                                "name": "OBJECT_B",
                            },
                        ],
                        "children": {},
                        "isKeyFrame": False,
                        "mid": "20250611172428468-1",
                        "type": "rectangle",
                    },
                ],
            },
        },
    },
    "labelType": "DEFAULT",
    "modelName": None,
}
expected_latest_label_result_semantic = {
    "author": {
        "email": "test+admin@kili-technology.com",
        "firstname": "Test",
        "id": "user-1",
        "lastname": "Admin",
    },
    "createdAt": "2025-06-02T12:43:44.865Z",
    "isLatestLabelForUser": True,
    "isSentBackToQueue": False,
    "jsonResponse": {
        "0": {
            "OBJECT_DETECTION_JOB": {
                "annotations": [
                    {
                        "children": {},
                        "isKeyFrame": True,
                        "categories": [{"name": "TEST"}],
                        "mid": "20250602144334575-1",
                        "type": "semantic",
                        "boundingPoly": [
                            {
                                "normalizedVertices": [
                                    {"x": 0.38416210624999997, "y": 0.5150611305555556},
                                    {"x": 0.3841575109375, "y": 0.5150611305555556},
                                    {"x": 0.3841483197916667, "y": 0.5150611305555556},
                                    {"x": 0.38414372395833335, "y": 0.5150611305555556},
                                    {"x": 0.384139128125, "y": 0.5150692990740742},
                                    {"x": 0.38413453281250004, "y": 0.5150774675925927},
                                    {"x": 0.3841299369791667, "y": 0.5150856361111111},
                                    {"x": 0.3841253416666667, "y": 0.5150856361111111},
                                    {"x": 0.3841253416666667, "y": 0.5150938046296296},
                                    {"x": 0.3841253416666667, "y": 0.5151019731481481},
                                    {"x": 0.3841253416666667, "y": 0.5151101416666666},
                                    {"x": 0.3841299369791667, "y": 0.5151101416666666},
                                    {"x": 0.38413453281250004, "y": 0.5151101416666666},
                                    {"x": 0.38413453281250004, "y": 0.5151183101851852},
                                    {"x": 0.384139128125, "y": 0.5151183101851852},
                                    {"x": 0.38414372395833335, "y": 0.5151264787037038},
                                    {"x": 0.3841483197916667, "y": 0.5151264787037038},
                                    {"x": 0.38415291510416666, "y": 0.5151264787037038},
                                    {"x": 0.3841575109375, "y": 0.5151264787037038},
                                    {"x": 0.38416210624999997, "y": 0.5151264787037038},
                                    {"x": 0.3841667020833333, "y": 0.5151264787037038},
                                    {"x": 0.38417129791666665, "y": 0.5151264787037038},
                                    {"x": 0.3841758932291667, "y": 0.5151264787037038},
                                    {"x": 0.38418048906249996, "y": 0.5151264787037038},
                                    {"x": 0.384185084375, "y": 0.5151264787037038},
                                    {"x": 0.384185084375, "y": 0.5151183101851852},
                                    {"x": 0.38418968020833333, "y": 0.5151101416666666},
                                    {"x": 0.38418968020833333, "y": 0.5151019731481481},
                                ]
                            }
                        ],
                    }
                ]
            },
            "ANNOTATION_JOB_COUNTER": {"OBJECT_DETECTION_JOB": {"TEST": 1}},
            "ANNOTATION_NAMES_JOB": {"20250602144334575-1": "Test 3"},
        }
    },
    "labelType": "REVIEW",
    "modelName": None,
}
expected_latest_label_result_with_hole = {
    "author": {
        "email": "test+admin@kili-technology.com",
        "firstname": "Test",
        "id": "user-1",
        "lastname": "Admin",
    },
    "createdAt": "2025-06-02T13:00:35.659Z",
    "isLatestLabelForUser": True,
    "isSentBackToQueue": False,
    "jsonResponse": {
        "0": {
            "OBJECT_DETECTION_JOB": {
                "annotations": [
                    {
                        "children": {},
                        "isKeyFrame": True,
                        "categories": [{"name": "TEST"}],
                        "mid": "20250602144334575-1",
                        "type": "semantic",
                        "boundingPoly": [
                            {
                                "normalizedVertices": [
                                    {"x": 0.3841253416666667, "y": 0.5151101416666666},
                                    {"x": 0.38413453281250004, "y": 0.5151101416666666},
                                    {"x": 0.38413453281250004, "y": 0.5151183101851852},
                                    {"x": 0.384139128125, "y": 0.5151183101851852},
                                    {"x": 0.38414372395833335, "y": 0.5151264787037038},
                                    {"x": 0.384185084375, "y": 0.5151264787037038},
                                    {"x": 0.384185084375, "y": 0.5151183101851852},
                                    {"x": 0.38418968020833333, "y": 0.5151101416666666},
                                    {"x": 0.38418968020833333, "y": 0.5151019731481481},
                                    {"x": 0.38416210624999997, "y": 0.5150611305555556},
                                    {"x": 0.38414372395833335, "y": 0.5150611305555556},
                                    {"x": 0.384139128125, "y": 0.5150692990740742},
                                    {"x": 0.38413453281250004, "y": 0.5150774675925927},
                                    {"x": 0.3841299369791667, "y": 0.5150856361111111},
                                    {"x": 0.3841253416666667, "y": 0.5150856361111111},
                                ]
                            },
                            {
                                "normalizedVertices": [
                                    {"x": 0.38414881458333333, "y": 0.5150947064814815},
                                    {"x": 0.38414881458333333, "y": 0.5150921648148148},
                                    {"x": 0.3841489578125, "y": 0.5150916564814815},
                                    {"x": 0.38414910052083334, "y": 0.5150911490740742},
                                    {"x": 0.38414910052083334, "y": 0.5150906407407407},
                                    {"x": 0.38414924375, "y": 0.5150901324074073},
                                    {"x": 0.38414938645833335, "y": 0.5150893694444445},
                                    {"x": 0.3841495296875, "y": 0.5150891157407407},
                                    {"x": 0.3841495296875, "y": 0.5150886074074075},
                                    {"x": 0.384149815625, "y": 0.515088099074074},
                                    {"x": 0.38415010156249996, "y": 0.5150878453703704},
                                    {"x": 0.3841513880208333, "y": 0.5150875907407406},
                                    {"x": 0.38415496250000003, "y": 0.5150875907407406},
                                    {"x": 0.38415596354166665, "y": 0.5150888611111111},
                                    {"x": 0.38415610625, "y": 0.5150888611111111},
                                    {"x": 0.38415639218750003, "y": 0.5150893694444445},
                                    {"x": 0.384156678125, "y": 0.5150893694444445},
                                    {"x": 0.3841568213541667, "y": 0.5150896240740741},
                                    {"x": 0.3841569640625, "y": 0.5150896240740741},
                                    {"x": 0.38415710729166663, "y": 0.5150901324074073},
                                    {"x": 0.38415710729166663, "y": 0.5150906407407407},
                                    {"x": 0.38415725, "y": 0.5150908944444446},
                                    {"x": 0.38415725, "y": 0.5150926731481481},
                                    {"x": 0.38415710729166663, "y": 0.5150929277777777},
                                    {"x": 0.38415710729166663, "y": 0.5150934361111111},
                                    {"x": 0.3841569640625, "y": 0.5150936898148148},
                                    {"x": 0.3841569640625, "y": 0.5150949601851852},
                                    {"x": 0.3841568213541667, "y": 0.5150949601851852},
                                    {"x": 0.3841568213541667, "y": 0.5150952148148148},
                                    {"x": 0.384156678125, "y": 0.5150952148148148},
                                    {"x": 0.38415639218750003, "y": 0.5150954685185185},
                                    {"x": 0.3841562494791667, "y": 0.5150957231481481},
                                    {"x": 0.38415596354166665, "y": 0.5150957231481481},
                                    {"x": 0.384155534375, "y": 0.5150959768518519},
                                    {"x": 0.3841552484375, "y": 0.5150962314814815},
                                    {"x": 0.38415496250000003, "y": 0.5150962314814815},
                                    {"x": 0.3841546765625, "y": 0.5150964851851851},
                                    {"x": 0.384150959375, "y": 0.5150964851851851},
                                    {"x": 0.38415053020833334, "y": 0.5150962314814815},
                                    {"x": 0.38415010156249996, "y": 0.5150962314814815},
                                    {"x": 0.3841499583333333, "y": 0.5150959768518519},
                                    {"x": 0.3841496723958333, "y": 0.5150957231481481},
                                    {"x": 0.3841495296875, "y": 0.5150957231481481},
                                    {"x": 0.38414938645833335, "y": 0.5150954685185185},
                                    {"x": 0.38414924375, "y": 0.5150954685185185},
                                    {"x": 0.38414910052083334, "y": 0.5150952148148148},
                                    {"x": 0.3841489578125, "y": 0.5150949601851852},
                                ]
                            },
                        ],
                    }
                ]
            },
            "ANNOTATION_JOB_COUNTER": {"OBJECT_DETECTION_JOB": {"TEST": 1}},
            "ANNOTATION_NAMES_JOB": {"20250602144334575-1": "Test 3"},
        }
    },
    "labelType": "REVIEW",
    "modelName": None,
}
expected_latest_label_result_semantic_multipart = {
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
        "0": {
            "OBJECT_DETECTION_JOB": {
                "annotations": [
                    {
                        "children": {},
                        "isKeyFrame": True,
                        "categories": [{"name": "TEST"}],
                        "mid": "20250602144334575-1",
                        "type": "semantic",
                        "boundingPoly": [
                            {
                                "normalizedVertices": [
                                    {"x": 0.3841253416666667, "y": 0.5151101416666666},
                                    {"x": 0.38413453281250004, "y": 0.5151101416666666},
                                    {"x": 0.38413453281250004, "y": 0.5151183101851852},
                                    {"x": 0.384139128125, "y": 0.5151183101851852},
                                    {"x": 0.38414372395833335, "y": 0.5151264787037038},
                                    {"x": 0.384185084375, "y": 0.5151264787037038},
                                    {"x": 0.384185084375, "y": 0.5151183101851852},
                                    {"x": 0.38418968020833333, "y": 0.5151101416666666},
                                    {"x": 0.38418968020833333, "y": 0.5151019731481481},
                                    {"x": 0.38416210624999997, "y": 0.5150611305555556},
                                    {"x": 0.38414372395833335, "y": 0.5150611305555556},
                                    {"x": 0.384139128125, "y": 0.5150692990740742},
                                    {"x": 0.38413453281250004, "y": 0.5150774675925927},
                                    {"x": 0.3841299369791667, "y": 0.5150856361111111},
                                    {"x": 0.3841253416666667, "y": 0.5150856361111111},
                                ]
                            }
                        ],
                    },
                    {
                        "children": {},
                        "isKeyFrame": True,
                        "categories": [{"name": "TEST"}],
                        "mid": "20250602144334575-1",
                        "type": "semantic",
                        "boundingPoly": [
                            {
                                "normalizedVertices": [
                                    {"x": 0.384200771875, "y": 0.5150941185185185},
                                    {"x": 0.38420065052083335, "y": 0.5150941185185185},
                                    {"x": 0.3842004067708333, "y": 0.5150943351851851},
                                    {"x": 0.38420016354166664, "y": 0.5150945509259259},
                                    {"x": 0.38419979895833334, "y": 0.5150949833333334},
                                    {"x": 0.38419943385416666, "y": 0.5150956324074074},
                                    {"x": 0.3841993119791667, "y": 0.515095848148148},
                                    {"x": 0.38419906875, "y": 0.5150962805555556},
                                    {"x": 0.38419882552083334, "y": 0.5150967129629629},
                                    {"x": 0.3841987041666667, "y": 0.5150971453703704},
                                    {"x": 0.3841987041666667, "y": 0.515097362037037},
                                    {"x": 0.3841987041666667, "y": 0.5150977944444444},
                                    {"x": 0.3841987041666667, "y": 0.5150980111111111},
                                    {"x": 0.3841987041666667, "y": 0.5150984435185185},
                                    {"x": 0.38419882552083334, "y": 0.5150986592592592},
                                    {"x": 0.3841989473958333, "y": 0.5150988759259258},
                                    {"x": 0.38419906875, "y": 0.5150990916666667},
                                    {"x": 0.384199190625, "y": 0.5150993083333333},
                                    {"x": 0.384199190625, "y": 0.5150995240740741},
                                    {"x": 0.3841993119791667, "y": 0.5150997407407407},
                                    {"x": 0.3841995552083333, "y": 0.5150999564814815},
                                    {"x": 0.3841996770833333, "y": 0.5150999564814815},
                                    {"x": 0.38419979895833334, "y": 0.5151001731481482},
                                    {"x": 0.3842000421875, "y": 0.5151003888888889},
                                    {"x": 0.38420016354166664, "y": 0.5151003888888889},
                                    {"x": 0.3842005286458334, "y": 0.5151003888888889},
                                    {"x": 0.384200771875, "y": 0.5151003888888889},
                                    {"x": 0.38420101510416665, "y": 0.5151003888888889},
                                    {"x": 0.38420138020833333, "y": 0.5151003888888889},
                                    {"x": 0.38420186666666667, "y": 0.5151001731481482},
                                    {"x": 0.3842022317708333, "y": 0.5150999564814815},
                                    {"x": 0.384202596875, "y": 0.5150995240740741},
                                    {"x": 0.3842029614583333, "y": 0.5150993083333333},
                                    {"x": 0.38420320520833334, "y": 0.5150990916666667},
                                    {"x": 0.3842033265625, "y": 0.5150988759259258},
                                    {"x": 0.3842034484375, "y": 0.5150986592592592},
                                    {"x": 0.38420356979166664, "y": 0.5150984435185185},
                                    {"x": 0.38420356979166664, "y": 0.5150982268518519},
                                    {"x": 0.38420356979166664, "y": 0.5150980111111111},
                                    {"x": 0.3842036916666667, "y": 0.5150977944444444},
                                    {"x": 0.3842036916666667, "y": 0.5150975787037038},
                                    {"x": 0.3842036916666667, "y": 0.5150971453703704},
                                    {"x": 0.3842036916666667, "y": 0.5150967129629629},
                                    {"x": 0.3842036916666667, "y": 0.5150962805555556},
                                    {"x": 0.3842036916666667, "y": 0.5150960648148148},
                                    {"x": 0.3842036916666667, "y": 0.5150956324074074},
                                    {"x": 0.38420356979166664, "y": 0.5150954157407408},
                                    {"x": 0.3842034484375, "y": 0.5150949833333334},
                                    {"x": 0.3842033265625, "y": 0.5150947675925927},
                                    {"x": 0.38420320520833334, "y": 0.5150945509259259},
                                    {"x": 0.38420308333333336, "y": 0.5150943351851851},
                                    {"x": 0.38420284010416667, "y": 0.5150941185185185},
                                    {"x": 0.3842027182291667, "y": 0.5150939027777778},
                                    {"x": 0.38420247500000004, "y": 0.5150939027777778},
                                    {"x": 0.3842022317708333, "y": 0.5150939027777778},
                                ]
                            }
                        ],
                    },
                ]
            },
            "ANNOTATION_JOB_COUNTER": {"OBJECT_DETECTION_JOB": {"TEST": 1}},
            "ANNOTATION_NAMES_JOB": {"20250602144334575-1": "Test 3"},
        }
    },
    "labelType": "REVIEW",
    "modelName": None,
}
expected_latest_label_result_polygon = {
    "author": {
        "email": "test+admin@kili-technology.com",
        "firstname": "Test",
        "id": "user-1",
        "lastname": "Admin",
    },
    "createdAt": "2025-06-02T11:42:14.135Z",
    "isLatestLabelForUser": True,
    "isSentBackToQueue": False,
    "jsonResponse": {
        "0": {
            "OBJECT_DETECTION_JOB": {
                "annotations": [
                    {
                        "children": {},
                        "isKeyFrame": True,
                        "categories": [{"name": "TEST"}],
                        "mid": "20250602134206930-10",
                        "type": "polygon",
                        "boundingPoly": [
                            {
                                "normalizedVertices": [
                                    {"x": 0.36717267552182165, "y": 0.5957106226563309},
                                    {"x": 0.3959914611005693, "y": 0.5653559412470912},
                                    {"x": 0.48991935483870974, "y": 0.5577672708947812},
                                    {"x": 0.5134013282732448, "y": 0.7342038565859876},
                                    {"x": 0.4002609108159393, "y": 0.751278364878685},
                                ]
                            }
                        ],
                    }
                ]
            },
            "ANNOTATION_JOB_COUNTER": {"OBJECT_DETECTION_JOB": {"TEST": 1}},
            "ANNOTATION_NAMES_JOB": {"20250602134206930-10": "Test 1"},
        }
    },
    "labelType": "REVIEW",
    "modelName": None,
}
expected_latest_label_result_asset_level = {
    "author": {
        "email": "test+admin@kili-technology.com",
        "firstname": "Test",
        "id": "user-1",
        "lastname": "Admin",
    },
    "jsonResponse": {
        "transcription_at_asset_level": {"text": "this is a transcription at asset level"},
        "classification_at_asset_level": {"category": [{"name": "OUI"}]},
    },
    "createdAt": "2025-06-02T11:42:14.135Z",
    "isLatestLabelForUser": True,
    "isSentBackToQueue": False,
    "labelType": "REVIEW",
    "modelName": None,
}

json_interface_asset_level = {
    "jobs": {
        "transcription_at_asset_level": {
            "content": {"input": "textField"},
            "instruction": "Transcription at Asset Level",
            "mlTask": "TRANSCRIPTION",
            "required": 0,
            "isChild": False,
            "level": "asset",
            "isNew": False,
        },
        "classification_at_asset_level": {
            "content": {
                "categories": {
                    "OUI": {"children": [], "name": "Oui", "id": "category1"},
                    "NON": {"children": [], "name": "Non", "id": "category2"},
                },
                "input": "radio",
            },
            "instruction": "Classification at Asset Level",
            "mlTask": "CLASSIFICATION",
            "required": 1,
            "isChild": False,
            "level": "asset",
            "isNew": False,
        },
    }
}
json_interface_rectangle = {
    "jobs": {
        "JOB_0": {
            "content": {
                "categories": {
                    "OBJECT_B": {
                        "children": [],
                        "name": "Car",
                        "color": "#3CD876",
                        "id": "category10",
                    }
                },
                "input": "radio",
            },
            "instruction": "Track objects A and B",
            "isChild": False,
            "tools": ["rectangle"],
            "mlTask": "OBJECT_DETECTION",
            "models": {"tracking": {}},
            "isVisible": True,
            "required": 0,
            "isNew": False,
        }
    }
}
json_interface_polygon = {
    "jobs": {
        "OBJECT_DETECTION_JOB": {
            "content": {
                "categories": {
                    "TEST": {"children": [], "color": "#472CED", "name": "Test", "id": "category17"}
                },
                "input": "radio",
            },
            "instruction": "Object",
            "mlTask": "OBJECT_DETECTION",
            "required": 0,
            "tools": ["polygon"],
            "isChild": False,
            "isNew": False,
        }
    }
}
json_interface_semantic = {
    "jobs": {
        "OBJECT_DETECTION_JOB": {
            "content": {
                "categories": {
                    "TEST": {"children": [], "color": "#472CED", "name": "Test", "id": "category21"}
                },
                "input": "radio",
            },
            "instruction": "Object",
            "mlTask": "OBJECT_DETECTION",
            "required": 0,
            "tools": ["semantic"],
            "isChild": False,
            "isNew": False,
        }
    }
}

test_cases = [
    (
        json_interface_asset_level,
        latest_label_annotations_asset_level,
        expected_latest_label_result_asset_level,
    ),
    (
        json_interface_rectangle,
        latest_label_annotations_rectangle,
        expected_latest_label_result_rectangle,
    ),
    (
        json_interface_rectangle,
        latest_label_annotations_rectangle_rotated,
        expected_latest_label_result_rectangle_rotated,
    ),
    (
        json_interface_polygon,
        latest_label_annotations_polygon,
        expected_latest_label_result_polygon,
    ),
    (
        json_interface_semantic,
        latest_label_annotations_semantic,
        expected_latest_label_result_semantic,
    ),
    (
        json_interface_semantic,
        latest_label_annotations_semantic_with_hole,
        expected_latest_label_result_with_hole,
    ),
    (
        json_interface_semantic,
        latest_label_annotations_semantic_multipart,
        expected_latest_label_result_semantic_multipart,
    ),
]
