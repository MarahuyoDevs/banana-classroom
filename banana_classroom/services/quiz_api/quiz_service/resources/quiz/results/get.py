from pypox.processing.base import processor
from pypox._types import QueryStr


@processor()
async def endpoint(class_id: QueryStr, quiz_id: QueryStr):
    pass
