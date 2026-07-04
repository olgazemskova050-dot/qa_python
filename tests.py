import pytest
from main import BooksCollector


class TestBooksCollector:

    # ==================== ТЕСТЫ ДЛЯ МЕТОДА add_new_book ====================
    def test_add_new_book_success(self):
        collector = BooksCollector()
        collector.add_new_book('Гарри Поттер')
        assert 'Гарри Поттер' in collector.get_books_genre()
        assert collector.get_book_genre('Гарри Поттер') == ''

    def test_add_new_book_duplicate_not_added(self):
        collector = BooksCollector()
        collector.add_new_book('Гарри Поттер')
        collector.add_new_book('Гарри Поттер')
        assert len(collector.get_books_genre()) == 1

    @pytest.mark.parametrize('name', [
        '',
        'A' * 41
    ])
    def test_add_new_book_invalid_name_not_added(self, name):
        collector = BooksCollector()
        collector.add_new_book(name)
        assert name not in collector.get_books_genre()

    # ==================== ТЕСТЫ ДЛЯ МЕТОДА set_book_genre ====================
    def test_set_book_genre_success(self):
        collector = BooksCollector()
        collector.add_new_book('Гарри Поттер')
        collector.set_book_genre('Гарри Поттер', 'Фантастика')
        assert collector.get_book_genre('Гарри Поттер') == 'Фантастика'

    def test_set_book_genre_invalid_genre_not_set(self):
        collector = BooksCollector()
        collector.add_new_book('Гарри Поттер')
        collector.set_book_genre('Гарри Поттер', 'Роман')
        assert collector.get_book_genre('Гарри Поттер') == ''

    def test_set_book_genre_for_nonexistent_book_not_set(self):
        collector = BooksCollector()
        collector.set_book_genre('Гарри Поттер', 'Фантастика')
        assert 'Гарри Поттер' not in collector.get_books_genre()

    # ==================== ТЕСТЫ ДЛЯ МЕТОДА get_book_genre ====================
    def test_get_book_genre_exists(self):
        collector = BooksCollector()
        collector.add_new_book('Гарри Поттер')
        collector.set_book_genre('Гарри Поттер', 'Фантастика')
        assert collector.get_book_genre('Гарри Поттер') == 'Фантастика'

    def test_get_book_genre_not_exists(self):
        collector = BooksCollector()
        assert collector.get_book_genre('Гарри Поттер') is None

    # ==================== ТЕСТЫ ДЛЯ МЕТОДА get_books_with_specific_genre ====================
    @pytest.mark.parametrize('genre, expected_books', [
        ('Фантастика', ['Гарри Поттер']),
        ('Ужасы', ['Оно']),
        ('Комедии', [])
    ])
    def test_get_books_with_specific_genre(self, genre, expected_books):
        collector = BooksCollector()
        collector.add_new_book('Гарри Поттер')
        collector.set_book_genre('Гарри Поттер', 'Фантастика')
        collector.add_new_book('Оно')
        collector.set_book_genre('Оно', 'Ужасы')
        assert collector.get_books_with_specific_genre(genre) == expected_books

    def test_get_books_with_specific_genre_empty_books(self):
        collector = BooksCollector()
        assert collector.get_books_with_specific_genre('Фантастика') == []

    # ==================== ТЕСТЫ ДЛЯ МЕТОДА get_books_for_children ====================
    def test_get_books_for_children_excludes_age_rating(self):
        collector = BooksCollector()
        collector.add_new_book('Гарри Поттер')
        collector.set_book_genre('Гарри Поттер', 'Фантастика')
        collector.add_new_book('Оно')
        collector.set_book_genre('Оно', 'Ужасы')
        collector.add_new_book('Шрек')
        collector.set_book_genre('Шрек', 'Мультфильмы')
        children_books = collector.get_books_for_children()
        assert 'Гарри Поттер' in children_books
        assert 'Шрек' in children_books
        assert 'Оно' not in children_books

    def test_get_books_for_children_empty(self):
        collector = BooksCollector()
        assert collector.get_books_for_children() == []

    def test_get_books_for_children_without_genre_not_included(self):
        collector = BooksCollector()
        collector.add_new_book('Гарри Поттер')
        children_books = collector.get_books_for_children()
        assert 'Гарри Поттер' not in children_books

    # ==================== ТЕСТЫ ДЛЯ МЕТОДА add_book_in_favorites ====================
    def test_add_book_in_favorites_success(self):
        collector = BooksCollector()
        collector.add_new_book('Гарри Поттер')
        collector.add_book_in_favorites('Гарри Поттер')
        assert 'Гарри Поттер' in collector.get_list_of_favorites_books()

    def test_add_book_in_favorites_duplicate_not_added(self):
        collector = BooksCollector()
        collector.add_new_book('Гарри Поттер')
        collector.add_book_in_favorites('Гарри Поттер')
        collector.add_book_in_favorites('Гарри Поттер')
        assert collector.get_list_of_favorites_books().count('Гарри Поттер') == 1

    def test_add_book_in_favorites_not_in_books_not_added(self):
        collector = BooksCollector()
        collector.add_book_in_favorites('Гарри Поттер')
        assert 'Гарри Поттер' not in collector.get_list_of_favorites_books()

    # ==================== ТЕСТЫ ДЛЯ МЕТОДА delete_book_from_favorites ====================
    def test_delete_book_from_favorites_success(self):
        collector = BooksCollector()
        collector.add_new_book('Гарри Поттер')
        collector.add_book_in_favorites('Гарри Поттер')
        collector.delete_book_from_favorites('Гарри Поттер')
        assert 'Гарри Поттер' not in collector.get_list_of_favorites_books()

    def test_delete_book_from_favorites_not_in_list(self):
        collector = BooksCollector()
        collector.add_new_book('Гарри Поттер')
        collector.delete_book_from_favorites('Гарри Поттер')
        assert collector.get_list_of_favorites_books() == []

    def test_delete_book_from_favorites_nonexistent_book(self):
        collector = BooksCollector()
        collector.delete_book_from_favorites('Гарри Поттер')
        assert collector.get_list_of_favorites_books() == []

    # ==================== ТЕСТЫ ДЛЯ МЕТОДА get_list_of_favorites_books ====================
    def test_get_list_of_favorites_books_empty(self):
        collector = BooksCollector()
        assert collector.get_list_of_favorites_books() == []

    def test_get_list_of_favorites_books_with_books(self):
        collector = BooksCollector()
        collector.add_new_book('Гарри Поттер')
        collector.add_new_book('Оно')
        collector.add_book_in_favorites('Гарри Поттер')
        collector.add_book_in_favorites('Оно')
        favorites = collector.get_list_of_favorites_books()
        assert len(favorites) == 2
        assert 'Гарри Поттер' in favorites
        assert 'Оно' in favorites

    # ==================== ТЕСТЫ ДЛЯ МЕТОДА get_books_genre ====================
    def test_get_books_genre_empty(self):
        collector = BooksCollector()
        assert collector.get_books_genre() == {}

    def test_get_books_genre_with_books(self):
        collector = BooksCollector()
        collector.add_new_book('Гарри Поттер')
        collector.set_book_genre('Гарри Поттер', 'Фантастика')
        expected = {'Гарри Поттер': 'Фантастика'}
        assert collector.get_books_genre() == expected