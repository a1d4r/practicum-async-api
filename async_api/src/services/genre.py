from typing import Annotated, NewType

import asyncio

from dataclasses import dataclass
from uuid import UUID

from core.settings import settings
from db.elastic import get_elastic
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from models.genre import Genre

GenreID = NewType("GenreID", UUID)


@dataclass
class GenreService:
    elastic: Annotated[AsyncElasticsearch, Depends(get_elastic)]

    async def get_by_id(self, genre_id: GenreID) -> Genre | None:
        try:
            doc = await self.elastic.get(index=settings.es_genres_index, id=str(genre_id))
        except NotFoundError:
            return None
        return Genre.model_validate(doc["_source"])

    async def search(
        self,
        page: int = 1,
        size: int = settings.default_page_size,
    ) -> list[Genre]:
        result = await self.elastic.search(
            index=settings.es_genres_index,
            from_=(page - 1) * size,
            size=size,
            query={"match_all": {}},
        )
        return [Genre.model_validate(hit["_source"]) for hit in result["hits"]["hits"]]


async def main() -> None:
    elastic = get_elastic()
    service = GenreService(elastic)
    genre = await service.get_by_id(GenreID(UUID("3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff")))
    print(genre)  # noqa: T201
    genre = await service.get_by_id(GenreID(UUID("3e8d9bf5-0d90-4353-88ba-4ccc5d2c07ff")))
    print(genre)  # noqa: T201
    genres_1 = await service.search(page=1)
    genres_2 = await service.search(page=2)
    print(genres_1)  # noqa: T201
    print(genres_2)  # noqa: T201


if __name__ == "__main__":
    asyncio.run(main())
