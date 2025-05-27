from kili_formats.types import ProjectDict

text_asset = {
    "latestLabel": {
        "author": {
            "id": "cldbnzmmq00go0jwc20fq1jkl",
            "email": "john.doe@kili-technology.com",
        },
        "createdAt": "2023-05-11T16:01:48.093Z",
        "id": "clhjbhrul015m0k7hct21drz4",
        "jsonResponse": {"JOB_0": {"text": "some text abc"}},
    },
    "content": "https://storage.googleapis.com/label-backend-staging/",
    "externalId": "4bad2303e43bfefa0169d890c68f5c9d--cherry-blossom-tree-blossom-trees.jpg",
    "id": "asset_id",
    "isHoneypot": False,
    "jsonMetadata": {},
    "skipped": False,
    "status": "LABELED",
}

text_project: ProjectDict = {
    "description": "Project description",
    "id": "project_id",
    "inputType": "TEXT",
    "jsonInterface": {
        "jobs": {"JOB_0": {"mlTask": "TRANSCRIPTION", "required": 1, "isChild": False}}
    },
    "title": "Project text",
    "organizationId": "fake_org_id",
}

text_project_asset_unnormalized = {
    "content": "https://storage.googleapis.com/label-backend-staging/",
    "externalId": "4bad2303e43bfefa0169d890c68f5c9d--cherry-blossom-tree-blossom-trees.jpg",
    "id": "asset_id",
    "isHoneypot": False,
    "jsonMetadata": {},
    "latestLabel": {
        "author": {
            "id": "cldbnzmmq00go0jwc20fq1jkl",
            "email": "john.doe@kili-technology.com",
        },
        "createdAt": "2023-05-11T16:01:48.093Z",
        "id": "clhjbhrul015m0k7hct21drz4",
        "jsonResponse": {"JOB_0": {"text": "some text abc"}},
    },
    "skipped": False,
    "status": "LABELED",
}
