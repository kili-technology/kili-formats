from pathlib import Path
import json
from typing import Dict, List, Optional, Union, cast

from ..types import ChatItemRole, ConversationLabel, ExportLLMItem, JobLevel


DEFAULT_JOB_LEVEL = JobLevel.ROUND
SEPARATOR = "___"

def convert_from_kili_to_llm_static_or_dynamic_format(annotations: List[Dict], chat_items: List[Dict], jobs: Dict) -> ConversationLabel:
    formatted_label = {JobLevel.COMPLETION: {}, JobLevel.CONVERSATION: {}, JobLevel.ROUND: {}}

    for job_name, job in jobs.items():
        job_level = job.get("level", DEFAULT_JOB_LEVEL)

        if job_level == JobLevel.COMPLETION:
            job_label = format_completion_job(job_name, annotations, chat_items)
        elif job_level == JobLevel.CONVERSATION:
            job_label = format_conversation_job(job_name, annotations)
        elif job_level == JobLevel.ROUND:
            job_label = format_round_job(job_name, annotations, chat_items)
        else:
            raise ValueError(f"Unknown job level: {job_level}")

        if job_label:
            formatted_label[job_level][job_name] = job_label

    return cast(ConversationLabel, formatted_label)

def format_completion_job(
    job_name: str, annotations: List[Dict], chat_items: List[Dict]
) -> Dict:
    id_to_external_id = {
        item["id"]: item.get("externalId") or item["id"] for item in chat_items
    }
    job_annotations = [
        annotation for annotation in annotations if annotation.get("job") == job_name
    ]
    return {
        id_to_external_id.get(annotation["chatItemId"]): annotation["annotationValue"]
        for annotation in job_annotations
    }

def format_round_job(
    job_name: str, annotations: List[Dict], chat_items: List[Dict]
) -> Dict:
    id_to_external_id = {
        item["id"]: item.get("externalId") or item["id"] for item in chat_items
    }
    job_annotations = [
        annotation for annotation in annotations if annotation.get("job") == job_name
    ]
    user_chat_item_ids = [
        chat_item.get("external_id") or chat_item["id"]
        for chat_item in chat_items
        if chat_item["role"] == ChatItemRole.USER
    ]

    return {
        user_chat_item_ids.index(annotation["chatItemId"]): format_annotation_value(
            annotation["annotationValue"], id_to_external_id
        )
        for annotation in job_annotations
    }

def format_conversation_job(job_name: str, annotations: List[Dict]) -> Dict:
    annotation = next(
        (annotation for annotation in annotations if annotation["job"] == job_name), None
    )
    if annotation:
        return annotation["annotationValue"]
    return {}

def format_annotation_value(annotation_value: Dict, id_to_external_id: Dict[str, str]) -> Dict:
    if annotation_value.get("choice"):
        return {
            "code": annotation_value["choice"]["code"],
            "firstId": id_to_external_id.get(annotation_value["choice"]["firstId"]),
            "secondId": id_to_external_id.get(annotation_value["choice"]["secondId"]),
        }
    return annotation_value

def convert_from_kili_to_llm_rlhf_format(
    assets: List[Dict], json_interface: Dict[str, Dict], logging
) -> List[Dict[str, Union[List[str], str]]]:
    result = []
    for asset in assets:
        result.append(
            {
                "raw_data": _format_raw_data(asset),
                "status": asset["status"],
                "external_id": asset["externalId"],
                "metadata": asset["jsonMetadata"],
                "labels": list(
                    map(
                        lambda label: {
                            "author": label["author"]["email"],
                            "created_at": label["createdAt"],
                            "label_type": label["labelType"],
                            "label": _format_json_response(
                                json_interface["jobs"], label["jsonResponse"], logging
                            ),
                        },
                        asset["labels"],
                    )
                ),
            }
        )
    return result

def _format_json_response(
    jobs_config: Dict, json_response: Dict, logging
) -> Dict[str, Dict[str, Union[str, List[str]]]]:
    result = {}
    for job_name, job_value in json_response.items():
        job_config = jobs_config[job_name]
        if job_config is None:
            continue
        if job_config["mlTask"] == "CLASSIFICATION":
            result[job_name] = []
            for category in job_value["categories"]:
                result[job_name].append(category["name"])
                if "children" in category:
                    for child_name, child_value in _format_json_response(
                        jobs_config, category["children"], logging
                    ).items():
                        result[f"{job_name}.{category['name']}.{child_name}"] = child_value
        elif job_config["mlTask"] == "TRANSCRIPTION":
            result[job_name] = job_value["text"]
        else:
            logging.warning(f"Job {job_name} with mlTask {job_config['mlTask']} not supported")
    if len(result) != 0:
        return {"conversation": result}
    return result


def _format_raw_data(
    asset, step_number: Optional[int] = None, all_model_keys: Optional[bool] = False
) -> List[ExportLLMItem]:
    raw_data = []

    chat_id = asset["jsonMetadata"].get("chat_id", None)

    if (
        "chat_item_ids" in asset["jsonMetadata"]
        and isinstance(asset["jsonMetadata"]["chat_item_ids"], str)
        and len(asset["jsonMetadata"]["chat_item_ids"]) > 0
    ):
        chat_items_ids = str.split(asset["jsonMetadata"]["chat_item_ids"], SEPARATOR)
        if step_number is not None:
            chat_items_ids = chat_items_ids[step_number * 3 :]
    else:
        chat_items_ids = []

    if (
        "models" in asset["jsonMetadata"]
        and isinstance(asset["jsonMetadata"]["models"], str)
        and len(asset["jsonMetadata"]["models"]) > 0
    ):
        models = str.split(asset["jsonMetadata"]["models"], SEPARATOR)
    else:
        models = []
    with Path(asset["content"]).open(encoding="utf8") as file:
        data = json.load(file)
    version = data.get("version", None)
    if version == "0.1":
        prompts = data["prompts"]
        if step_number is not None:
            prompts = [prompts[step_number]]
        for index, prompt in enumerate(prompts):
            raw_data.append(
                ExportLLMItem(
                    {
                        "role": prompt.get("title", "user"),
                        "content": prompt["prompt"],
                        "id": _safe_pop(chat_items_ids),
                        "chat_id": chat_id,
                        "model": None,
                    }
                )
            )
            raw_data.extend(
                ExportLLMItem(
                    {
                        "role": completion.get("title", "assistant"),
                        "content": completion["content"],
                        "id": _safe_pop(chat_items_ids),
                        "chat_id": chat_id,
                        "model": models[index_completion]
                        if (
                            (index == len(prompts) - 1 or all_model_keys)
                            and len(models) > index_completion
                        )
                        else None,
                    }
                )
                for index_completion, completion in enumerate(prompt["completions"])
            )
    else:
        raise ValueError(f"Version {version} not supported")
    return raw_data

def _safe_pop(lst, index=0):
    try:
        return lst.pop(index)
    except IndexError:
        return None