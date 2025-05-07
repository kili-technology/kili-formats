import os
import tempfile

from kili_formats.format.llm import convert_from_kili_to_llm_rlhf_format, convert_from_kili_to_llm_static_or_dynamic_format
from .fakes.llm_dynamic import llm_dynamic_annotations, llm_dynamic_chat_items, llm_dynamic_expected_label, jobs
from .fakes.llm_static import llm_static_annotations, llm_static_chat_items, llm_static_expected_result
from .fakes.llm_rlhf import llm_rlhf_expected_result, llm_rlhf_assets, llm_rlhf_json_interface, mock_raw_asset_content


def test_convert_from_kili_to_llm_dynamic_format():
    """Test the conversion from Kili format to LLM dynamic format."""

    formatted_label = convert_from_kili_to_llm_static_or_dynamic_format(
        llm_dynamic_annotations, llm_dynamic_chat_items, jobs
    )

    assert formatted_label == llm_dynamic_expected_label

def test_convert_from_kili_to_llm_static_format():
    """Test the conversion from Kili format to LLM static format."""

    formatted_label = convert_from_kili_to_llm_static_or_dynamic_format(
        llm_static_annotations, llm_static_chat_items, jobs
    )

    assert formatted_label == llm_static_expected_result

def test_convert_from_kili_to_llm_rlhf_format():
    """Test the conversion from Kili format to LLM static format."""
    
    fd, path = tempfile.mkstemp()
    try:
        with os.fdopen(fd, "w") as tmp:
            tmp.write(mock_raw_asset_content)
        for mocked_asset in llm_rlhf_assets:
            mocked_asset["content"] = path
        print("mocked_asset", mocked_asset["content"])
        formatted_label = convert_from_kili_to_llm_rlhf_format(llm_rlhf_assets, llm_rlhf_json_interface, logging=None)
        assert formatted_label == llm_rlhf_expected_result
    finally:
        os.remove(path)