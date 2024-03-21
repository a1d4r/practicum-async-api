from uuid import UUID


async def test_get_by_id(genre_service):
    # Arrange
    action_genre_id = UUID("3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff")

    # Act
    genre = await genre_service.get_by_id(action_genre_id)

    # Assert
    assert genre is not None
    assert genre.id == action_genre_id
    assert genre.name == "Action"


async def test_search_genres(genre_service):
    # Arrange
    page = 2
    size = 5

    # Act
    genres = await genre_service.search(page, size)

    # Assert
    assert len(genres) == size
