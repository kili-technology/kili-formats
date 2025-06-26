# kili-formats

This package expose all the methods needed for [Kili](https://github.com/kili-technology/kili-python-sdk) to format the export in `coco, kili, llm, voc, GeoJSON` and `yolo`

Here the methods that are exposed :

```python
clean_json_response,
convert_from_kili_to_coco_format,
convert_from_kili_to_geojson_format,
convert_from_kili_to_llm_rlhf_format,
convert_from_kili_to_llm_static_or_dynamic_format,
convert_from_kili_to_voc_format,
convert_from_kili_to_yolo_format,
convert_to_pixel_coords,
format_json_response
```

## Installation

```bash
pip install kili-formats
```

## Usage

```python
from kili_formats import clean_json_response

clean_json_response(asset)
```

## Development

If you want to contribute, here are the [installation steps](CONTRIBUTING.md)
