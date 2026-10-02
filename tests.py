import pytest

from main import BooksCollector


@pytest.fixture
def collector():
    return BooksCollector()


class TestBooksCollector:

    # add_new_book
    def test_add_new_book_add_two_books(self, collector):
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        assert len(collector.get_books_genre()) == 2

    @pytest.mark.parametrize('name', ['А', 'А' * 40])
    def test_add_new_book_valid_name_length_book_added(self, collector, name):
        collector.add_new_book(name)

        assert name in collector.get_books_genre()

    @pytest.mark.parametrize('name', ['', 'А' * 41])
    def test_add_new_book_invalid_name_length_book_not_added(self, collector, name):
        collector.add_new_book(name)

        assert name not in collector.get_books_genre()

    def test_add_new_book_same_book_twice_added_once(self, collector):
        collector.add_new_book('Оно')
        collector.add_new_book('Оно')

        assert len(collector.get_books_genre()) == 1

    def test_add_new_book_new_book_has_no_genre(self, collector):
        collector.add_new_book('Оно')

        assert collector.get_book_genre('Оно') == ''

    # set_book_genre и get_book_genre
    @pytest.mark.parametrize('genre', ['Фантастика', 'Ужасы', 'Детективы', 'Мультфильмы', 'Комедии'])
    def test_set_book_genre_available_genre_genre_set(self, collector, genre):
        collector.add_new_book('Оно')
        collector.set_book_genre('Оно', genre)

        assert collector.get_book_genre('Оно') == genre

    def test_set_book_genre_unknown_genre_genre_not_set(self, collector):
        collector.add_new_book('Оно')
        collector.set_book_genre('Оно', 'Драма')

        assert collector.get_book_genre('Оно') == ''

    def test_set_book_genre_book_not_added_book_not_appears(self, collector):
        collector.set_book_genre('Оно', 'Ужасы')

        assert collector.get_book_genre('Оно') is None

    # get_books_with_specific_genre
    def test_get_books_with_specific_genre_returns_only_books_of_this_genre(self, collector):
        collector.add_new_book('Оно')
        collector.add_new_book('Шерлок Холмс')
        collector.add_new_book('Дюна')
        collector.set_book_genre('Оно', 'Ужасы')
        collector.set_book_genre('Шерлок Холмс', 'Детективы')
        collector.set_book_genre('Дюна', 'Фантастика')

        assert collector.get_books_with_specific_genre('Ужасы') == ['Оно']

    def test_get_books_with_specific_genre_unknown_genre_returns_empty_list(self, collector):
        collector.add_new_book('Оно')
        collector.set_book_genre('Оно', 'Ужасы')

        assert collector.get_books_with_specific_genre('Драма') == []

    # get_books_genre
    def test_get_books_genre_returns_current_dictionary(self, collector):
        collector.add_new_book('Оно')
        collector.set_book_genre('Оно', 'Ужасы')

        assert collector.get_books_genre() == {'Оно': 'Ужасы'}

    # get_books_for_children
    def test_get_books_for_children_book_without_age_rating_in_list(self, collector):
        collector.add_new_book('Простоквашино')
        collector.set_book_genre('Простоквашино', 'Мультфильмы')

        assert collector.get_books_for_children() == ['Простоквашино']

    @pytest.mark.parametrize('genre', ['Ужасы', 'Детективы'])
    def test_get_books_for_children_book_with_age_rating_not_in_list(self, collector, genre):
        collector.add_new_book('Оно')
        collector.set_book_genre('Оно', genre)

        assert 'Оно' not in collector.get_books_for_children()

    # add_book_in_favorites
    def test_add_book_in_favorites_book_in_collection_book_added(self, collector):
        collector.add_new_book('Оно')
        collector.add_book_in_favorites('Оно')

        assert collector.get_list_of_favorites_books() == ['Оно']

    def test_add_book_in_favorites_book_not_in_collection_book_not_added(self, collector):
        collector.add_book_in_favorites('Оно')

        assert collector.get_list_of_favorites_books() == []

    def test_add_book_in_favorites_same_book_twice_added_once(self, collector):
        collector.add_new_book('Оно')
        collector.add_book_in_favorites('Оно')
        collector.add_book_in_favorites('Оно')

        assert collector.get_list_of_favorites_books() == ['Оно']

    # delete_book_from_favorites
    def test_delete_book_from_favorites_book_in_favorites_book_deleted(self, collector):
        collector.add_new_book('Оно')
        collector.add_book_in_favorites('Оно')
        collector.delete_book_from_favorites('Оно')

        assert collector.get_list_of_favorites_books() == []

    def test_delete_book_from_favorites_book_not_in_favorites_list_unchanged(self, collector):
        collector.add_new_book('Оно')
        collector.add_new_book('Дюна')
        collector.add_book_in_favorites('Оно')
        collector.delete_book_from_favorites('Дюна')

        assert collector.get_list_of_favorites_books() == ['Оно']

    # get_list_of_favorites_books
    def test_get_list_of_favorites_books_returns_all_added_books(self, collector):
        collector.add_new_book('Оно')
        collector.add_new_book('Дюна')
        collector.add_book_in_favorites('Оно')
        collector.add_book_in_favorites('Дюна')

        assert collector.get_list_of_favorites_books() == ['Оно', 'Дюна'] 
        