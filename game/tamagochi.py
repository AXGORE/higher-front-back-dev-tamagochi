"""Интерфейс и реализация питомца."""

from abc import ABC, abstractmethod

from .exceptions import TamagochiIsGone
from .models import Food, Medicine


class AbstractTamagochi(ABC):
    """Интерфейс логики тамагочи"""

    @abstractmethod
    def feed(self, food: Food) -> None:
        """Накормить питомца"""
        raise NotImplementedError

    @abstractmethod
    def play(self) -> None:
        """Поиграть с питомцем"""
        raise NotImplementedError

    @abstractmethod
    def rest(self) -> None:
        """Дать питомцу отдохнуть"""
        raise NotImplementedError

    @abstractmethod
    def heal(self, medicine: Medicine) -> None:
        """Использовать лекарство для лечения питомца"""
        raise NotImplementedError

    @property
    @abstractmethod
    def status(self) -> dict[str, int]:
        """Вернуть показатели питомца"""
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        """Проверить, жив ли питомец"""
        raise NotImplementedError

    @abstractmethod
    def is_sick(self) -> bool:
        """Проверить, болен ли питомец"""
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        """Обновить показатели питомца"""
        raise NotImplementedError


class Tamagochi(AbstractTamagochi):
    """Питомец с ограниченными показателями состояния"""

    MAX_HUNGER = 100
    MAX_HP = 100
    MAX_ENERGY = 100

    def __init__(self) -> None:
        """Создаёт здорового и отдохнувшего питомца"""
        self._hunger = 0
        self._hp = self.MAX_HP
        self._energy = self.MAX_ENERGY
        self._sick = False

    @property
    def status(self) -> dict[str, int]:
        """Возвращает голод, здоровье и энергию"""
        return {"hunger": self._hunger, "hp": self._hp, "energy": self._energy}

    def _ensure_alive(self) -> None:
        if not self.is_alive():
            raise TamagochiIsGone("Питомец умер")

    def feed(self, food: Food) -> None:
        """Уменьшает голод и немного расходует энергию"""
        self._ensure_alive()
        self._hunger = max(0, self._hunger - food.satiety)
        self._energy = max(0, self._energy - 2)

    def play(self) -> None:
        """Игра повышает голод и расходует энергию"""
        self._ensure_alive()
        self._hunger = min(self.MAX_HUNGER, self._hunger + 5)
        self._energy = max(0, self._energy - 5)

    def rest(self) -> None:
        """Восстанавливает энергию и немного повышает голод"""
        self._ensure_alive()
        recovery = 10 if self._sick else 20
        self._energy = min(self.MAX_ENERGY, self._energy + recovery)
        self._hunger = min(self.MAX_HUNGER, self._hunger + 2)

    def heal(self, medicine: Medicine) -> None:
        """Применяет одну дозу лекарства, если она доступна"""
        self._ensure_alive()
        if not medicine.is_empty():
            medicine.uses += 1
            self._hp = min(self.MAX_HP, self._hp + medicine.heal_hp)
            self._sick = False

    def is_alive(self) -> bool:
        """Возвращает True, пока здоровье выше нуля"""
        return self._hp > 0

    def is_sick(self) -> bool:
        """Возвращает признак болезни питомца"""
        return self._sick

    def update(self) -> None:
        """Повышает голод, снижает энергию и при нужде здоровье"""
        self._ensure_alive()
        self._hunger = min(self.MAX_HUNGER, self._hunger + 1)
        self._energy = max(0, self._energy - 1)
        if self._hunger >= 80 or self._energy == 0:
            self._hp -= 1
        if not self.is_alive():
            raise TamagochiIsGone("Питомец умер")
