"""Модуль с интерфейсом и реализацией класса игры."""

from abc import ABC, abstractmethod
from copy import copy
from typing import Any, TypeVar

from .tamagochi import AbstractTamagochi
from .clicker import AbstractClicker
from .models import Food, Medicine
from .exceptions import NotEnoughMoney, TamagochiIsGone

InventoryItem = TypeVar("InventoryItem", Food, Medicine)


class AbstractGame(ABC):
    """Интерфейс для логики игры."""

    @abstractmethod
    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine]
    ):
        """
        Абстрактный метод инициализации класса игры

        :param tamagochi: экземпляр тамагочи
        :param clicker: экземпляр кликера
        :param all_food: все доступные варианты еды
        :param all_medicine: все доступные варианты лекарств.
        """
        raise NotImplementedError

    @abstractmethod
    def work(self) -> int:
        """
        Абстрактный метод для логики действия "работа

        :return: количество заработанных монет.
        """
        raise NotImplementedError

    @abstractmethod
    def buy_food(self) -> None:
        """Абстрактный метод для покупки еды."""
        raise NotImplementedError

    @abstractmethod
    def buy_medicine(self) -> None:
        """Абстрактный метод для покупки лекарства."""
        raise NotImplementedError

    @abstractmethod
    def feed_tamagochi(self) -> None:
        """Абстрактный метод для кормления тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def heal_tamagochi(self) -> None:
        """Абстрактный метод для лечения тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def rest_tamagochi(self):
        """Абстрактный метод для отдыха тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def play_with_tamagochi(self):
        """Абстрактный метод для игры с тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> dict[str, Any]:
        """
        Абстрактный метод для получения статуса (всех характеристик) тамагочи

        :return: словарь со всеми характеристиками тамагочи.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def food(self) -> list[Food]:
        """
        Абстрактное свойство для доступа к сумке с едой

        :return: список с имеющимися (купленными) объектами еды.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def medicine(self) -> list[Medicine]:
        """
        Абстрактное свойство для доступа к сумке с лекарствами

        :return: список с имеющимися (купленными) объектами лекарств.
        """
        raise NotImplementedError


class Game(AbstractGame):
    """Управляет питомцем, кликами и запасами предметов."""

    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine],
    ) -> None:
        """Создаёт игру с питомцем, кликером и каталогом товаров."""
        self.tamagochi = tamagochi
        self.clicker = clicker
        self.all_food = list(all_food)
        self.all_medicine = list(all_medicine)
        self._food: list[Food] = []
        self._medicine: list[Medicine] = []
        self._coins = 0

    @property
    def food(self) -> list[Food]:
        """Возвращает купленную еду."""
        return self._food

    @property
    def medicine(self) -> list[Medicine]:
        """Возвращает купленные лекарства."""
        return self._medicine

    def work(self) -> int:
        """Начисляет доход за один клик и возвращает его размер."""
        self._ensure_alive()
        self.clicker.click()
        income = self.clicker.income_per_click
        self._coins += income
        self.tamagochi.update()
        return income

    def _ensure_alive(self) -> None:
        """Завершает действие исключением, если питомец умер."""
        if not self.tamagochi.is_alive():
            raise TamagochiIsGone("Питомец умер")

    def _purchase(
        self,
        options: list[InventoryItem],
        inventory: list[InventoryItem],
        noun: str,
    ) -> None:
        """Показывает каталог, списывает стоимость и добавляет товар."""
        if not options:
            print(f"Нет доступных вариантов: {noun}")
            return
        for index, item in enumerate(options, 1):
            print(f"{index}. {item}")
        try:
            selection = int(input("Выберите номер (0 — отмена): "))
        except (ValueError, EOFError):
            return
        if selection == 0:
            return
        if not 1 <= selection <= len(options):
            print("Неверный номер")
            return
        item = options[selection - 1]
        if self._coins < item.price:
            raise NotEnoughMoney("Недостаточно монет")
        self._coins -= item.price
        inventory.append(copy(item))

    def buy_food(self) -> None:
        """Покупает выбранную еду."""
        try:
            self._purchase(self.all_food, self._food, "еды")
        finally:
            self.tamagochi.update()

    def buy_medicine(self) -> None:
        """Покупает выбранное лекарство."""
        try:
            self._purchase(self.all_medicine, self._medicine, "лекарства")
        finally:
            self.tamagochi.update()

    @staticmethod
    def _take_item(
        inventory: list[InventoryItem], description: str
    ) -> InventoryItem | None:
        """Возвращает выбранный предмет инвентаря или None."""
        if not inventory:
            print(f"В сумке нет {description}")
            return None
        for index, item in enumerate(inventory, 1):
            print(f"{index}. {item}")
        try:
            selection = int(input("Выберите номер: "))
        except (ValueError, EOFError):
            return None
        if 1 <= selection <= len(inventory):
            return inventory[selection - 1]
        return None

    def feed_tamagochi(self) -> None:
        """Кормит питомца и удаляет использованную еду из сумки."""
        self._ensure_alive()
        try:
            item = self._take_item(self._food, "еды")
            if item is not None:
                self.tamagochi.feed(item)
                self._food.remove(item)
        finally:
            self.tamagochi.update()

    def heal_tamagochi(self) -> None:
        """Лечит питомца и удаляет израсходованное лекарство."""
        self._ensure_alive()
        try:
            item = self._take_item(self._medicine, "лекарств")
            if item is not None:
                self.tamagochi.heal(item)
                if item.is_empty():
                    self._medicine.remove(item)
        finally:
            self.tamagochi.update()

    def rest_tamagochi(self) -> None:
        """Даёт питомцу отдохнуть и обновляет его состояние."""
        self._ensure_alive()
        self.tamagochi.rest()
        self.tamagochi.update()

    def play_with_tamagochi(self) -> None:
        """Играет с питомцем и обновляет его состояние."""
        self._ensure_alive()
        self.tamagochi.play()
        self.tamagochi.update()

    def get_status(self) -> dict[str, Any]:
        """Возвращает показатели питомца и текущий баланс монет."""
        self._ensure_alive()
        return {**self.tamagochi.status, "coins": self._coins}
