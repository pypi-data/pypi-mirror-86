from typing import (
    Any,
    Callable,
    Generic,
    Optional,
    TypeVar,
)

import marshmallow as m

from requests import Response

T = TypeVar('T')


__all__ = [
    "PaddockResponse"
]


class PaddockResponse(Generic[T]):
    """
    Wrapper to the HTTP response for the Paddock client.

    Provides an easy way to access the parsed and converted HTTP response body,
    in addition to the raw response, status code, etc.

    Note that body deserialization occurs lazily, only when the ``body()``
    method is called. This means that users can inspect the status code,
    headers, etc. before deciding to read the body, as errors may have
    occurred.
    """

    def __init__(self, *, response: Response, converter: Callable[[], T]):
        """
        :param response: the response to wrap
        :param converter: the converter function that parses the response
        """
        self.raw = response
        self.status_code = response.status_code
        self.__converter = converter
        self.__cached_body: Optional[T] = None

    @classmethod
    def not_implemented(cls, response: Response):
        def converter():
            raise NotImplementedError(
                "Conversion has not been implemented for this resource."
            )

        return PaddockResponse(
            response=response,
            converter=converter
        )

    @classmethod
    def bodiless(cls, response: Response, /) -> 'PaddockResponse[None]':
        """
        Construct an instant of PaddockCloudResponse with None for body.

        :param response: the response
        :return: a bodiless PaddockCloudResponse
        """
        return PaddockResponse(response=response, converter=lambda: None)

    @classmethod
    def json(
            cls, *,
            response: Response,
            schema: m.Schema
    ) -> 'PaddockResponse[Any]':
        """
        Create a response whose body is deserialized lazily as JSON with the
        body() function according to the given schema.

        :param response: the response to wrap
        :param schema: the schema to use to deserialize the body
        :return: the wrapped response
        """
        text = response.text
        return PaddockResponse(
            response=response,
            converter=lambda: schema.loads(text)
        )

    def body(self) -> T:
        """
        Get the parsed response body.

        Parsing is lazy, and the response is parsed for the first time when
        this method is called, then the result is cached for later calls.

        :return: the parsed response body
        """
        if self.__cached_body is None:
            self.__cached_body = self.__converter()
        return self.__cached_body
