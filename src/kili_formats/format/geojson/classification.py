from typing import Dict


def kili_classification_annotation_to_geojson_non_localised_feature(
    classification_annotation: Dict, job_name: str
):
    return {
        "type": "Feature",
        "geometry": None,
        "properties": {
            "kili": {
                "categories": classification_annotation["categories"],
                "job": job_name,
            },
        },
    }
