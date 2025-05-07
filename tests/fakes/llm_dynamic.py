from kili_formats.format.llm import JobLevel


jobs = {
    "CLASSIFICATION_JOB_AT_COMPLETION_LEVEL": {
        "content": {
            "categories": {
                "TOO_SHORT": {"children": [], "name": "Too short", "id": "category1"},
                "JUST_RIGHT": {"children": [], "name": "Just right", "id": "category2"},
                "TOO_VERBOSE": {"children": [], "name": "Too verbose", "id": "category3"},
            },
            "input": "radio",
        },
        "instruction": "Verbosity",
        "level": "completion",
        "mlTask": "CLASSIFICATION",
        "required": 0,
        "isChild": False,
        "isNew": False,
    },
    "CLASSIFICATION_JOB_AT_COMPLETION_LEVEL_1": {
        "content": {
            "categories": {
                "NO_ISSUES": {"children": [], "name": "No issues", "id": "category4"},
                "MINOR_ISSUES": {"children": [], "name": "Minor issue(s)", "id": "category5"},
                "MAJOR_ISSUES": {"children": [], "name": "Major issue(s)", "id": "category6"},
            },
            "input": "radio",
        },
        "instruction": "Instructions Following",
        "level": "completion",
        "mlTask": "CLASSIFICATION",
        "required": 0,
        "isChild": False,
        "isNew": False,
    },
    "CLASSIFICATION_JOB_AT_COMPLETION_LEVEL_2": {
        "content": {
            "categories": {
                "NO_ISSUES": {"children": [], "name": "No issues", "id": "category7"},
                "MINOR_INACCURACY": {
                    "children": [],
                    "name": "Minor inaccuracy",
                    "id": "category8",
                },
                "MAJOR_INACCURACY": {
                    "children": [],
                    "name": "Major inaccuracy",
                    "id": "category9",
                },
            },
            "input": "radio",
        },
        "instruction": "Truthfulness",
        "level": "completion",
        "mlTask": "CLASSIFICATION",
        "required": 0,
        "isChild": False,
        "isNew": False,
    },
    "CLASSIFICATION_JOB_AT_COMPLETION_LEVEL_3": {
        "content": {
            "categories": {
                "NO_ISSUES": {"children": [], "name": "No issues", "id": "category10"},
                "MINOR_SAFETY_CONCERN": {
                    "children": [],
                    "name": "Minor safety concern",
                    "id": "category11",
                },
                "MAJOR_SAFETY_CONCERN": {
                    "children": [],
                    "name": "Major safety concern",
                    "id": "category12",
                },
            },
            "input": "radio",
        },
        "instruction": "Harmlessness/Safety",
        "level": "completion",
        "mlTask": "CLASSIFICATION",
        "required": 0,
        "isChild": False,
        "isNew": False,
    },
    "COMPARISON_JOB": {
        "content": {
            "options": {
                "IS_MUCH_BETTER": {"children": [], "name": "Is much better", "id": "option13"},
                "IS_BETTER": {"children": [], "name": "Is better", "id": "option14"},
                "IS_SLIGHTLY_BETTER": {
                    "children": [],
                    "name": "Is slightly better",
                    "id": "option15",
                },
                "TIE": {"children": [], "name": "Tie", "mutual": True, "id": "option16"},
            },
            "input": "radio",
        },
        "instruction": "Pick the best answer",
        "mlTask": "COMPARISON",
        "required": 1,
        "isChild": False,
        "isNew": False,
    },
    "CLASSIFICATION_JOB_AT_ROUND_LEVEL": {
        "content": {
            "categories": {
                "BOTH_ARE_GOOD": {"children": [], "name": "Both are good", "id": "category17"},
                "BOTH_ARE_BAD": {"children": [], "name": "Both are bad", "id": "category18"},
            },
            "input": "radio",
        },
        "instruction": "Overall quality",
        "level": "round",
        "mlTask": "CLASSIFICATION",
        "required": 0,
        "isChild": False,
        "isNew": False,
    },
    "CLASSIFICATION_JOB_AT_CONVERSATION_LEVEL": {
        "content": {
            "categories": {
                "GLOBAL_GOOD": {"children": [], "name": "Globally good", "id": "category19"},
                "BOTH_ARE_BAD": {"children": [], "name": "Globally bad", "id": "category20"},
            },
            "input": "radio",
        },
        "instruction": "Global",
        "level": "conversation",
        "mlTask": "CLASSIFICATION",
        "required": 0,
        "isChild": False,
        "isNew": False,
    },
    "TRANSCRIPTION_JOB_AT_CONVERSATION_LEVEL": {
        "content": {"input": "textField"},
        "instruction": "Additional comments...",
        "level": "conversation",
        "mlTask": "TRANSCRIPTION",
        "required": 0,
        "isChild": False,
        "isNew": False,
    },
}


llm_dynamic_annotations = [
    {
        "id": "20250114170129511-1",
        "__typename": "ClassificationAnnotation",
        "job": "CLASSIFICATION_JOB_AT_COMPLETION_LEVEL",
        "path": [],
        "labelId": "cm5wnub7w01evp30w0ig9h8bh",
        "annotationValue": {"categories": ["JUST_RIGHT"]},
        "chatItemId": "cm5wnudcb01f1p30wcay0hht8",
    },
    {
        "id": "20250114170130144-2",
        "__typename": "ClassificationAnnotation",
        "job": "CLASSIFICATION_JOB_AT_COMPLETION_LEVEL_1",
        "path": [],
        "labelId": "cm5wnub7w01evp30w0ig9h8bh",
        "annotationValue": {"categories": ["MAJOR_ISSUES"]},
        "chatItemId": "cm5wnudcb01f1p30wcay0hht8",
    },
    {
        "id": "20250114170130780-3",
        "__typename": "ClassificationAnnotation",
        "job": "CLASSIFICATION_JOB_AT_COMPLETION_LEVEL_2",
        "path": [],
        "labelId": "cm5wnub7w01evp30w0ig9h8bh",
        "annotationValue": {"categories": ["MINOR_INACCURACY"]},
        "chatItemId": "cm5wnudfv01f2p30whovhbwzp",
    },
    {
        "id": "20250114170132013-4",
        "__typename": "ClassificationAnnotation",
        "job": "CLASSIFICATION_JOB_AT_COMPLETION_LEVEL_3",
        "path": [],
        "labelId": "cm5wnub7w01evp30w0ig9h8bh",
        "annotationValue": {"categories": ["MAJOR_SAFETY_CONCERN"]},
        "chatItemId": "cm5wnudfv01f2p30whovhbwzp",
    },
    {
        "id": "20250114170133181-5",
        "__typename": "ComparisonAnnotation",
        "job": "COMPARISON_JOB",
        "path": [],
        "labelId": "cm5wnub7w01evp30w0ig9h8bh",
        "annotationValue": {
            "choice": {
                "code": "Is better",
                "firstId": "cm5wnudcb01f1p30wcay0hht8",
                "secondId": "cm5wnudfv01f2p30whovhbwzp",
            }
        },
        "chatItemId": "cm5wnucrc01ezp30w3029eyv3",
    },
]

llm_dynamic_chat_items = [
    {
        "id": "cm5wnucrc01ezp30w3029eyv3",
        "content": "test",
        "createdAt": "2025-01-14T16:01:26.808Z",
        "externalId": None,
        "modelName": None,
        "modelId": None,
        "parentId": None,
        "role": "USER",
    },
    {
        "id": "cm5wnudcb01f1p30wcay0hht8",
        "content": " It looks like everything is working correctly. How can I assist you today?",
        "createdAt": "2025-01-14T16:01:27.563Z",
        "externalId": None,
        "modelName": None,
        "modelId": "cm5wnub7p01etp30w1e5wgwww",
        "parentId": "cm5wnucrc01ezp30w3029eyv3",
        "role": "ASSISTANT",
    },
    {
        "id": "cm5wnudfv01f2p30whovhbwzp",
        "content": " It looks like everything is working correctly. How can I assist you today?",
        "createdAt": "2025-01-14T16:01:27.692Z",
        "externalId": None,
        "modelName": None,
        "modelId": "cm5wnub7q01eup30w0g273df8",
        "parentId": "cm5wnucrc01ezp30w3029eyv3",
        "role": "ASSISTANT",
    },
]

llm_dynamic_expected_label = {
    JobLevel.COMPLETION: {
        "CLASSIFICATION_JOB_AT_COMPLETION_LEVEL": {
            "cm5wnudcb01f1p30wcay0hht8": {
                "categories": [
                    "JUST_RIGHT",
                ],
            },
        },
        "CLASSIFICATION_JOB_AT_COMPLETION_LEVEL_1": {
            "cm5wnudcb01f1p30wcay0hht8": {
                "categories": [
                    "MAJOR_ISSUES",
                ],
            },
        },
        "CLASSIFICATION_JOB_AT_COMPLETION_LEVEL_2": {
            "cm5wnudfv01f2p30whovhbwzp": {
                "categories": [
                    "MINOR_INACCURACY",
                ],
            },
        },
        "CLASSIFICATION_JOB_AT_COMPLETION_LEVEL_3": {
            "cm5wnudfv01f2p30whovhbwzp": {
                "categories": [
                    "MAJOR_SAFETY_CONCERN",
                ],
            },
        },
    },
    JobLevel.CONVERSATION: {},
    JobLevel.ROUND: {
        "COMPARISON_JOB": {
            0: {
                "code": "Is better",
                "firstId": "cm5wnudcb01f1p30wcay0hht8",
                "secondId": "cm5wnudfv01f2p30whovhbwzp",
            },
        },
    },
}
