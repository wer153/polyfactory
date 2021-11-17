from typing import Optional, Tuple, Union

from exrex import getone  # pylint: disable=import-error
from pydantic import ConstrainedBytes, ConstrainedStr

from pydantic_factories.utils import create_random_bytes, create_random_string


def parse_constrained_string_or_bytes(
    field: Union[ConstrainedStr, ConstrainedBytes]
) -> Tuple[Optional[int], Optional[int], bool]:
    """Parses and validates the given field"""
    lower_case = field.to_lower
    min_length = field.min_length
    max_length = field.max_length
    assert min_length >= 0 if min_length is not None else True, "min_length must be greater or equal to 0"
    assert max_length >= 0 if max_length is not None else True, "max_length must be greater or equal to 0"
    if max_length is not None and min_length is not None:
        assert max_length >= min_length, "max_length must be greater than min_length"
    return min_length, max_length, lower_case


def handle_constrained_bytes(field: ConstrainedBytes) -> bytes:
    """Handles ConstrainedStr and Fields with string constraints"""
    min_length, max_length, lower_case = parse_constrained_string_or_bytes(field)
    if max_length == 0:
        return b""
    return create_random_bytes(min_length=min_length, max_length=max_length, lower_case=lower_case)


def handle_constrained_string(field: ConstrainedStr) -> str:
    """Handles ConstrainedStr and Fields with string constraints"""
    min_length, max_length, lower_case = parse_constrained_string_or_bytes(field)
    if max_length == 0:
        return ""
    if not field.regex:
        return create_random_string(min_length, max_length, lower_case=lower_case)
    result = getone(str(field.regex))
    if min_length:
        while len(result) < min_length:
            result += getone(str(field.regex))
    if max_length and len(result) > max_length:
        result = result[:max_length]
    return result.lower() if lower_case else result
