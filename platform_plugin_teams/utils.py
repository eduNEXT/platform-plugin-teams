"""Utils for the Teams plugin."""
from rest_framework import status
from rest_framework.response import Response


def api_field_errors(
    field_errors: dict, status_code: int = status.HTTP_400_BAD_REQUEST
) -> Response:
    """
    Build a response with field errors.

    Args:
        field_errors (dict): Errors to return.
        status_code (int, optional): Status code to return. Defaults to
            status.HTTP_400_BAD_REQUEST.

    Returns:
        Response: Response with field errors.
    """
    return Response(
        data={"field_errors": field_errors},
        status=status_code,
    )


def api_error(error: str, status_code: int = status.HTTP_400_BAD_REQUEST) -> Response:
    """
    Build a response with an error.

    Args:
        error (str): Error to return.
        status_code (int, optional): Status code to return. Defaults to
            status.HTTP_400_BAD_REQUEST.

    Returns:
        Response: Response with an error.
    """
    return Response(
        data={"error": [error]},
        status=status_code,
    )
