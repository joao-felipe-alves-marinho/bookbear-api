from typing import Any

from django.db.models import QuerySet
from ninja import Field, Schema
from ninja.pagination import AsyncPaginationBase


class AsyncPageNumberPagination(AsyncPaginationBase):
    def paginate_queryset(self, queryset: QuerySet, pagination: Any, **params: Any) -> Any:
        pass

    class Input(Schema):
        page: int = Field(1, ge=1)
        page_size: int = Field(10, ge=1, le=50)

    class Output(Schema):
        nb_items: int = Field(ge=0)
        nb_pages: int = Field(ge=0)
        page_size: int = Field(ge=1)
        page: int = Field(ge=1)

    async def apaginate_queryset(self, queryset, pagination: Input, **params) -> Any:
        offset = (pagination.page - 1) * pagination.page_size
        nb_items = await self._aitems_count(queryset)

        return {
            "nb_items": nb_items,
            "nb_pages": (nb_items + pagination.page_size - 1) // pagination.page_size,
            "page_size": pagination.page_size,
            "page": pagination.page,
            "items": queryset[offset: offset + pagination.page_size],
        }
