from typing import (
    Optional,
    Any,
)

from django.db.models import QuerySet

from rest_framework.request import Request as DRF_Request
from rest_framework.response import Response as DRF_Response
from rest_framework.serializers import Serializer
from rest_framework.pagination import BasePagination
from rest_framework import status


class DRFResponseHandler:
    """Handler for DRF response."""

    def get_drf_response(
        self,
        request: DRF_Request,
        data: QuerySet,
        serializer_class: Serializer,
        many: bool = False,
        paginator: Optional[BasePagination] = None,
        serializer_context: Optional[dict[str, Any]] = None
    ) -> DRF_Response:
        if not serializer_context:
            serializer_context = {"request": request}
        if paginator and many:
            objects: list = paginator.paginate_queryset(
                queryset=data,
                request=request
            )
            serializer: Serializer = serializer_class(
                objects,
                many=many,
                context=serializer_context
            )
            response: DRF_Response = \
                paginator.get_paginated_response(
                    serializer.data
                )
            return response

        serializer: Serializer = serializer_class(
            data,
            many=many,
            context=serializer_context
        )
        response: DRF_Response = DRF_Response(
            {
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )
        return response
