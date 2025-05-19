from typing import Dict


def kili_transcription_annotation_to_geojson_non_localised_feature(
    transcription_annotation: Dict, job_name: str
):
    return {
        "type": "Feature",
        "geometry": None,
        "properties": {
            "kili": {
                "text": transcription_annotation["text"],
                "job": job_name,
            },
        },
    }
