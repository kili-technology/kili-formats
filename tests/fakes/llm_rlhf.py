llm_rlhf_json_interface = {
    "jobs": {
        "CLASSIFICATION_JOB": {
            "content": {
                "categories": {
                    "A_BETTER_THAN_B": {
                        "children": [],
                        "name": "A better than B",
                        "id": "category1",
                    },
                    "B_BETTER_THAN_A": {
                        "children": [],
                        "name": "B better than A",
                        "id": "category2",
                    },
                    "TIE": {"children": [], "name": "Tie", "id": "category3"},
                },
                "input": "radio",
            },
            "instruction": "Compare",
            "mlTask": "CLASSIFICATION",
            "required": 0,
            "isChild": False,
            "isNew": False,
        },
        "TRANSCRIPTION_JOB": {
            "content": {"input": "markdown"},
            "instruction": "",
            "mlTask": "TRANSCRIPTION",
            "required": 0,
            "isChild": False,
            "isNew": False,
        },
    }
}

llm_rlhf_assets = [
    {
        "labels": [
            {
                "author": {
                    "id": "user-1",
                    "email": "test+admin@kili-technology.com",
                    "firstname": "Test",
                    "lastname": "Admin",
                },
                "jsonResponse": {
                    "CLASSIFICATION_JOB": {"categories": [{"name": "A_BETTER_THAN_B"}]}
                },
                "createdAt": "2024-08-05T13:03:00.051Z",
                "isLatestLabelForUser": True,
                "isSentBackToQueue": False,
                "labelType": "DEFAULT",
                "modelName": None,
            }
        ],
        "content": "https://storage.googleapis.com/label-public-staging/demo-projects/LLM/01.json",
        "externalId": "asset#0",
        "jsonMetadata": {},
        "status": "LABELED",
    },
    {
        "labels": [
            {
                "author": {
                    "id": "user-1",
                    "email": "test+admin@kili-technology.com",
                    "firstname": "Test",
                    "lastname": "Admin",
                },
                "jsonResponse": {
                    "CLASSIFICATION_JOB": {"categories": [{"name": "B_BETTER_THAN_A"}]}
                },
                "createdAt": "2024-08-05T13:03:03.061Z",
                "isLatestLabelForUser": True,
                "isSentBackToQueue": False,
                "labelType": "DEFAULT",
                "modelName": None,
            }
        ],
        "content": "https://storage.googleapis.com/label-public-staging/demo-projects/LLM/02.json",
        "externalId": "asset#1",
        "jsonMetadata": {},
        "status": "LABELED",
    },
    {
        "labels": [
            {
                "author": {
                    "id": "user-1",
                    "email": "test+admin@kili-technology.com",
                    "firstname": "Test",
                    "lastname": "Admin",
                },
                "jsonResponse": {
                    "CLASSIFICATION_JOB": {"categories": [{"name": "TIE"}]},
                    "TRANSCRIPTION_JOB": {"text": "There is only some formatting changes\n"},
                },
                "createdAt": "2024-08-05T13:03:16.028Z",
                "isLatestLabelForUser": True,
                "isSentBackToQueue": True,
                "labelType": "DEFAULT",
                "modelName": None,
            }
        ],
        "content": "https://storage.googleapis.com/label-public-staging/demo-projects/LLM/03.json",
        "externalId": "asset#2",
        "jsonMetadata": {},
        "status": "LABELED",
    },
]

mock_raw_asset_content = """{
    "prompts": [
        {
            "prompt": "BLABLABLA",
            "completions": [
                {
                    "content": "response A1"
                },
                {
                    "content": "response B1"
                }
            ]
        },
        {
            "prompt": "BLIBLIBLI",
            "completions": [
                {
                    "content": "response A2"
                },
                {
                    "content": "response B2"
                }
            ]
        }
    ],
    "type": "markdown",
    "version": "0.1"
}
"""

llm_rlhf_expected_result = [
    {
        "external_id": "asset#0",
        "labels": [
            {
                "author": "test+admin@kili-technology.com",
                "created_at": "2024-08-05T13:03:00.051Z",
                "label": {
                    "conversation": {
                        "CLASSIFICATION_JOB": [
                            "A_BETTER_THAN_B",
                        ],
                    },
                },
                "label_type": "DEFAULT",
            },
        ],
        "metadata": {},
        "raw_data": [
            {
                "chat_id": None,
                "content": "BLABLABLA",
                "id": None,
                "model": None,
                "role": "user",
            },
            {
                "chat_id": None,
                "content": "response A1",
                "id": None,
                "model": None,
                "role": "assistant",
            },
            {
                "chat_id": None,
                "content": "response B1",
                "id": None,
                "model": None,
                "role": "assistant",
            },
            {
                "chat_id": None,
                "content": "BLIBLIBLI",
                "id": None,
                "model": None,
                "role": "user",
            },
            {
                "chat_id": None,
                "content": "response A2",
                "id": None,
                "model": None,
                "role": "assistant",
            },
            {
                "chat_id": None,
                "content": "response B2",
                "id": None,
                "model": None,
                "role": "assistant",
            },
        ],
        "status": "LABELED",
    },
    {
        "external_id": "asset#1",
        "labels": [
            {
                "author": "test+admin@kili-technology.com",
                "created_at": "2024-08-05T13:03:03.061Z",
                "label": {
                    "conversation": {
                        "CLASSIFICATION_JOB": [
                            "B_BETTER_THAN_A",
                        ],
                    },
                },
                "label_type": "DEFAULT",
            },
        ],
        "metadata": {},
        "raw_data": [
            {
                "chat_id": None,
                "content": "BLABLABLA",
                "id": None,
                "model": None,
                "role": "user",
            },
            {
                "chat_id": None,
                "content": "response A1",
                "id": None,
                "model": None,
                "role": "assistant",
            },
            {
                "chat_id": None,
                "content": "response B1",
                "id": None,
                "model": None,
                "role": "assistant",
            },
            {
                "chat_id": None,
                "content": "BLIBLIBLI",
                "id": None,
                "model": None,
                "role": "user",
            },
            {
                "chat_id": None,
                "content": "response A2",
                "id": None,
                "model": None,
                "role": "assistant",
            },
            {
                "chat_id": None,
                "content": "response B2",
                "id": None,
                "model": None,
                "role": "assistant",
            },
        ],
        "status": "LABELED",
    },
    {
        "external_id": "asset#2",
        "labels": [
            {
                "author": "test+admin@kili-technology.com",
                "created_at": "2024-08-05T13:03:16.028Z",
                "label": {
                    "conversation": {
                        "CLASSIFICATION_JOB": [
                            "TIE",
                        ],
                        "TRANSCRIPTION_JOB": "There is only some formatting changes\n",
                    },
                },
                "label_type": "DEFAULT",
            },
        ],
        "metadata": {},
        "raw_data": [
            {
                "chat_id": None,
                "content": "BLABLABLA",
                "id": None,
                "model": None,
                "role": "user",
            },
            {
                "chat_id": None,
                "content": "response A1",
                "id": None,
                "model": None,
                "role": "assistant",
            },
            {
                "chat_id": None,
                "content": "response B1",
                "id": None,
                "model": None,
                "role": "assistant",
            },
            {
                "chat_id": None,
                "content": "BLIBLIBLI",
                "id": None,
                "model": None,
                "role": "user",
            },
            {
                "chat_id": None,
                "content": "response A2",
                "id": None,
                "model": None,
                "role": "assistant",
            },
            {
                "chat_id": None,
                "content": "response B2",
                "id": None,
                "model": None,
                "role": "assistant",
            },
        ],
        "status": "LABELED",
    },
]
