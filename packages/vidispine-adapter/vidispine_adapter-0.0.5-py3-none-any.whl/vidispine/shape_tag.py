from vidispine.base import EntityBase
from vidispine.errors import InvalidInput
from vidispine.typing import BaseJson


class ShapeTag(EntityBase):
    """Shape tags

    Manage shape tags.

    :vidispine_docs:`Vidispine doc reference <shape-tag>`

    """
    entity = 'shape-tag'

    def create(self, shape_tag_name: str, metadata: dict) -> None:
        """Creates a new shape tag with the given tag name.

        :param shape_tag_name: The name of the shape tag to create.
        :param metadata: The metadata (transcode preset document) to
            create the shape tag with.

        """
        self._update(shape_tag_name, metadata)

    def update(self, shape_tag_name: str, metadata: dict) -> None:
        """Updates a shape tag with the given tag name.

        :param shape_tag_name: The name of the shape tag to update.
        :param metadata: The metadata (transcode preset document) to
            update the shape tag with.

        """
        self._update(shape_tag_name, metadata)

    def _update(self, shape_tag_name: str, metadata: dict) -> None:
        if not metadata:
            raise InvalidInput('Please supply metadata.')

        endpoint = self._build_url(shape_tag_name)
        self.client.put(endpoint, json=metadata)

    def list(self, params: dict = None) -> BaseJson:
        """Retrieves all shape tags known by the system.

        :param params: Optional query params.
        :return: JSON response from the request.
        :rtype: vidispine.typing.BaseJson.

        """
        return self.client.get(self.entity)

    def get(self, shape_tag_name: str) -> BaseJson:
        """Retrieves the metadata (transcode preset) of a shape tag with
            the given tag name.

        :param shape_tag_name: The name of the shape tag.

        :return: JSON response from the request.
        :rtype: vidispine.typing.BaseJson.

        """
        endpoint = self._build_url(shape_tag_name)
        return self.client.get(endpoint)

    def delete(self, shape_tag_name: str) -> None:
        """Deletes a shape tag with the given tag name.

        :param shape_tag_name: The name of the shape tag to delete.

        """
        endpoint = self._build_url(shape_tag_name)
        self.client.delete(endpoint)
