from kili_formats.format.voc import convert_from_kili_to_voc_format

xml_str = '<?xml version="1.0" ?>\n<annotation>\n   <folder/>\n   <filename>filename.xml</filename>\n   <path/>\n   <source>\n      <database>Kili Technology</database>\n   </source>\n   <size>\n      <width>1920</width>\n      <height>1080</height>\n      <depth>3</depth>\n   </size>\n   <segmented/>\n   <object>\n      <name>OBJECT_A</name>\n      <job_name>JOB_0</job_name>\n      <pose>Unspecified</pose>\n      <truncated>0</truncated>\n      <difficult>0</difficult>\n      <occluded>0</occluded>\n      <bndbox>\n         <xmin>317</xmin>\n         <xmax>1609</xmax>\n         <ymin>281</ymin>\n         <ymax>863</ymax>\n      </bndbox>\n   </object>\n</annotation>\n'
def test_voc_convert_from_kili_to_voc_format():
    """Test the conversion from Kili format to VOC format."""

    response = {
        "JOB_0": {
        "annotations": [
            {
                "categories": [{"confidence": 100, "name": "OBJECT_A"}],
                "jobName": "JOB_0",
                "mid": "2022040515434712-7532",
                "mlTask": "OBJECT_DETECTION",
                "boundingPoly": [
                    {
                        "normalizedVertices": [
                            {"x": 0.16504140348233334, "y": 0.7986938935103378},
                            {"x": 0.16504140348233334, "y": 0.2605618833516984},
                            {"x": 0.8377886490672706, "y": 0.2605618833516984},
                            {"x": 0.8377886490672706, "y": 0.7986938935103378},
                        ]
                    }
                ],
                "type": "rectangle",
                "children": {},
            }
        ]
    }
    }

    width = 1920
    height = 1080
    parameters = {
        "filename": "filename.xml",
    }

    xmlstr = convert_from_kili_to_voc_format(response, width, height, parameters, ["JOB_0"])
    assert xmlstr == xml_str