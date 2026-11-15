from typing import Any

import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.mark.parametrize(
    "state, expected_ids",
    [
        ("EXECUTED", [41428829, 939719570]),
        ("CANCELED", [594226727, 615064591]),
        ("PENDING", []),
    ],
)
def test_filter_by_state(
    sample_transactions: list[dict[str, Any]],
    state: str,
    expected_ids: list[int],
) -> None:
    """Тестирование фильтрации операций по различным статусам."""
    result = filter_by_state(sample_transactions, state)
    assert [item["id"] for item in result] == expected_ids


def test_filter_by_state_default(sample_transactions: list[dict[str, Any]]) -> None:
    """Проверка фильтрации по статусу по умолчанию (EXECUTED)."""
    result = filter_by_state(sample_transactions)
    assert [item["id"] for item in result] == [41428829, 939719570]


def test_filter_by_state_empty_list() -> None:
    """Проверка работы функции при передаче пустого списка."""
    assert filter_by_state([], "EXECUTED") == []


def test_sort_by_date_descending(sample_transactions: list[dict[str, Any]]) -> None:
    """Тестирование сортировки по дате по убыванию (по умолчанию)."""
    result = sort_by_date(sample_transactions)
    assert [item["id"] for item in result] == [41428829, 615064591, 594226727, 939719570]


def test_sort_by_date_ascending(sample_transactions: list[dict[str, Any]]) -> None:
    """Тестирование сортировки по дате по возрастанию."""
    result = sort_by_date(sample_transactions, reverse=False)
    assert [item["id"] for item in result] == [939719570, 594226727, 615064591, 41428829]


def test_sort_by_date_same_dates(same_date_transactions: list[dict[str, Any]]) -> None:
    """Проверка сохранения относительного порядка при одинаковых датах."""
    result = sort_by_date(same_date_transactions, reverse=False)
    assert [item["id"] for item in result] == [1, 2, 3]


def test_sort_by_date_non_standard_format(invalid_date_transactions: list[dict[str, Any]]) -> None:
    """Проверка поведения сортировки при нестандартных строковых форматах дат."""
    result = sort_by_date(invalid_date_transactions, reverse=True)
    assert len(result) == 2


def test_sort_by_date_missing_key() -> None:
    """Проверка выброса KeyError при отсутствии ключа date в словаре."""
    with pytest.raises(KeyError):
        sort_by_date([{"id": 1, "state": "EXECUTED"}])
