from typing import Any, Union


def make_json_response_example(*,
                               example: dict[str, Any] = {},
                               description: str = '') -> dict[str, Any]:
    return {'description': description,
            'content': {'application/json': {'example': example}}}


def make_http_error_json(*,
                         detail: Union[str, dict[str, Any]]) -> dict[str, Any]:
    return {'detail': detail}
