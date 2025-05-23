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
