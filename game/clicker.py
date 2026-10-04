"""Модуль с интерфейсом и реализацией кликера"""

from abc import ABC, abstractmethod


class AbstractClicker(ABC):
    """Интерфейс для кликера"""

    @abstractmethod
    def __init__(self, income_per_click: int) -> None:
        """Абстрактный метод инициализации"""
        raise NotImplementedError

    @abstractmethod
    def click(self) -> None:
        """Абстрактный метод клика для накапливания монет"""
        raise NotImplementedError

    @property
    @abstractmethod
    def income_per_click(self) -> int:
        """Абстрактное свойство для доступа к количеству монет за клик"""
        raise NotImplementedError


class Clicker(AbstractClicker):
    """Кликер с фиксированным доходом за каждый клик."""

    def __init__(self, income_per_click: int = 1) -> None:
        if income_per_click < 0:
            raise ValueError("Доход за клик не может быть отрицательным")
        self._income_per_click = income_per_click

    @property
    def income_per_click(self) -> int:
        """Возвращает доход за один клик"""
        return self._income_per_click

    def click(self) -> None:
        """Интерфейс клика; начисление средств выполняет объект игры"""
