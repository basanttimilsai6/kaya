# core/swagger.py

from drf_spectacular.utils import extend_schema, OpenApiParameter

def schema_decorator(
    request_serializer=None,
    query_params=None,
    summary=None,
    description=None,
    responses=None
):
    """
    A reusable decorator for drf-spectacular schema generation.

    :param request_serializer: DRF serializer class or None
    :param query_params: List of dicts with keys: name, type, required, description
    :param summary: Short summary of the endpoint
    :param description: Detailed description
    :param responses: Optional response schema (default: inferred)
    :return: extend_schema decorator
    """
    parameters = []
    if query_params:
        for param in query_params:
            parameters.append(OpenApiParameter(
                name=param.get("name"),
                type=param.get("type", str),
                location=param.get("location", OpenApiParameter.QUERY),
                required=param.get("required", False),
                description=param.get("description", "")
            ))

    return extend_schema(
        request=request_serializer,
        parameters=parameters,
        summary=summary,
        description=description,
        responses=responses
    )


delete_schema_decorator = schema_decorator(request_serializer=None,query_params=[{"name": "unique_id","type": str,"required": True,"description": "Unique ID of data"}],summary="Delete",description="Delete a data by unique_id passed as a query parameter.")