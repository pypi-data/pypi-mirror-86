from vidispine.base import EntityBase
from vidispine.errors import InvalidInput
from vidispine.metadata import MetadataMixin
from vidispine.typing import BaseJson


class Item(MetadataMixin, EntityBase):
    """Items

    Manage items.

    :vidispine_docs:`Vidispine doc reference <item/item>`

    """
    entity = 'item'

    def get(
        self,
        item_id: str,
        params: dict = None,
        metadata=True
    ) -> BaseJson:
        """Returns information about a single item.

        :param item_id: The ID of the item.
        :param params: Optional query parameters.
        :param metadata: Whether to return metadata or not.

        :return: JSON response from the request.
        :rtype: vidispine.typing.BaseJson.

        """
        if params is None:
            params = {}

        if metadata:
            params.setdefault('content', 'metadata')

        endpoint = self._build_url(item_id)

        return self.client.get(endpoint, params=params)

    def delete(self, item_id: str) -> None:
        """Delete a single item.

        :param item_id: The ID of the item.

        """
        endpoint = self._build_url(item_id)
        self.client.delete(endpoint)

    def create_placeholder(
        self,
        metadata: dict,
        params: dict = None
    ) -> BaseJson:
        """Creates a placeholder item.

        :param params: Optional query parameters.
        :param metadata: The metadata of the item.

        :return: JSON response from the request.
        :rtype: vidispine.typing.BaseJson.

        """
        if params is None:
            params = {}

        params.setdefault('container', 1)
        endpoint = 'import/placeholder'

        return self.client.post(
            endpoint, json=metadata, params=params
        )

    def import_to_placeholder(
        self,
        item_id: str,
        component_type: str,
        params: dict
    ) -> None:
        """Import a file to a placeholder item.

        :param item_id: The ID of the item.
        :param component_type: The component type, can be: container,
            audio, video or binary.
        :param params: Optional query parameters.

        :return: JSON response from the request.
        :rtype: vidispine.typing.BaseJson.

        """
        if not params:
            raise InvalidInput('Please supply a URI or fileId.')

        endpoint = f'import/placeholder/{item_id}/{component_type}'

        return self.client.post(endpoint, params=params)


class ItemShape(EntityBase):
    """Shapes

    Manages shapes for an Item.

    :vidispine_docs:`Vidispine doc reference <item/shape>`

    """

    entity = 'item'

    def create(
        self,
        metadata: dict,
        item_id: str,
        params: dict = None
    ) -> BaseJson:
        """Creates a new shape using the supplied information.

        :param metadata: Metadata (shape document) to create the shape
            with.
        :param item_id: The ID of the item.
        :param params: Optional query parameters.

        :return: JSON response from the request.
        :rtype: vidispine.typing.BaseJson.

        """
        if not metadata:
            raise InvalidInput('Please supply metadata.')

        if params is None:
            params = {}

        endpoint = self._build_url(f'{item_id}/shape/create')

        return self.client.post(endpoint, json=metadata, params=params)

    def get(
        self,
        item_id: str,
        shape_id: str,
        params: dict = None
    ) -> BaseJson:
        """Returns a shape for a specified item.

        :param item_id: The ID of the item.
        :param shape_id: The ID of the shape.
        :param params: Optional query parameters.

        :return: JSON response from the request.
        :rtype: vidispine.typing.BaseJson.

        """
        if params is None:
            params = {}

        endpoint = self._build_url(f'{item_id}/shape/{shape_id}')

        return self.client.get(endpoint, params=params)

    def list(self, item_id: str, params: dict = None) -> BaseJson:
        """Returns all existing shapes for a specified item.

        :param item_id: The ID of the item.
        :param params: Optional query parameters.

        :return: JSON response from the request.
        :rtype: vidispine.typing.BaseJson.

        """
        if params is None:
            params = {}

        endpoint = self._build_url(f'{item_id}/shape')

        return self.client.get(endpoint, params=params)

    def delete(self, item_id: str, shape_id: str, params: dict = None) -> None:
        """Removes the specified shape.

        :param item_id: The ID of the item.
        :param shape_id: The ID of the shape.
        :param params: Optional query parameters.

        """
        if params is None:
            params = {}

        endpoint = self._build_url(f'{item_id}/shape/{shape_id}')

        self.client.delete(endpoint, params=params)

    def delete_all(self, item_id: str, params: dict = None) -> None:
        """Removes all shapes from an item.

        :param item_id: The ID of the item.
        :param params: Optional query parameters.

        """
        if params is None:
            params = {}

        endpoint = self._build_url(f'{item_id}/shape')

        self.client.delete(endpoint, params=params)

    def import_shape(self, item_id: str, params: dict) -> None:
        """Starts a new shape import job.

        :param item_id: The ID of the item.
        :param params: Optional query parameters.

        :return: JSON response from the request.
        :rtype: vidispine.typing.BaseJson.

        """
        if not params:
            raise InvalidInput('Please supply a URI or fileId.')

        endpoint = self._build_url(f'{item_id}/shape')

        return self.client.post(endpoint, params=params)
