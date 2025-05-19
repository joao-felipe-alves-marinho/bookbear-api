from typing import List

from django.shortcuts import aget_object_or_404
from ninja_extra import (
    api_controller,
    ControllerBase,
    route, permissions
)

from BookBearApi.models import Publisher
from BookBearApi.schemas import PublisherSchema


@api_controller('/publisher', tags=['publisher'], permissions=[permissions.AllowAny], auth=None)
class PublisherController(ControllerBase):
    @route.get('/', response=List[PublisherSchema])
    async def get_publishers(self):
        """
        Get a list of publishers.
        :return: List[PublisherSchema]
        """
        return [publisher async for publisher in Publisher.objects.all()]

    @route.get('/{publisher_id}', response=PublisherSchema)
    async def get_publisher(self, publisher_id: int):
        """
        Get a publisher by id.
        :param publisher_id: int
        :return: PublisherSchema
        """
        return await aget_object_or_404(Publisher, id=publisher_id)
