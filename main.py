"""Точка входа в игру."""

from game.clicker import Clicker
from game.exceptions import NotEnoughMoney, TamagochiIsGone
from game.game import Game
from game.models import Food, Medicine
from game.tamagochi import Tamagochi


WELCOME = "Добро пожаловать в Тамагочи-кликер!"
SCREEN_LINES = (
    "{message}",
    "",
    "Сумка с едой: {food}",
    "Сумка с лекарствами: {medicine}",
    "",
    "Статус: голод {hunger}, здоровье {hp}, энергия {energy}, монет {coins}",
    "{sickness}",
    "1. Пойти на работу",
    "2. Купить еду",
    "3. Купить лекарство",
    "4. Покормить",
    "5. Вылечить",
    "6. Играть",
    "7. Отдых",
    "0. Выход",
)


def main() -> None:
    """Запускает игровой цикл."""
    all_food = [
        Food(name="Бургер", satiety=20, price=40),
        Food(name="Салат", satiety=10, price=20),
        Food(name="Яблоко", satiety=10, price=15),
    ]
    all_medicine = [
        Medicine(name="Ибупрофен", price=30, heal_hp=20, number_of_uses=2)
    ]
    tamagochi = Tamagochi()
    game = Game(
        tamagochi,
        Clicker(10),
        all_food=all_food,
        all_medicine=all_medicine,
    )
    output = WELCOME

    try:
        while True:
            sickness = ""
            if tamagochi.is_sick():
                sickness = (
                    "=======Тамагочи болеет=======\n"
                    "=======Отдых действует менее эффективно======="
                )
            screen_values = {
                "message": output,
                "food": game.food,
                "medicine": game.medicine,
                "sickness": sickness,
                **game.get_status(),
            }
            print("\n".join(line.format(**screen_values) for line in SCREEN_LINES))

            match input("Выберите действие: "):
                case "1":
                    income = game.work()
                    output = f"Вы заработали {income} монет"
                case "2":
                    try:
                        game.buy_food()
                    except NotEnoughMoney as error:
                        output = str(error)
                    else:
                        output = ""
                case "3":
                    try:
                        game.buy_medicine()
                    except NotEnoughMoney as error:
                        output = str(error)
                    else:
                        output = ""
                case "4":
                    game.feed_tamagochi()
                    output = ""
                case "5":
                    game.heal_tamagochi()
                    output = ""
                case "6":
                    game.play_with_tamagochi()
                    output = "Вы поиграли с питомцем"
                case "7":
                    game.rest_tamagochi()
                    output = "Питомец отдохнул"
                case "0":
                    break
                case _:
                    output = "Неверная команда"
    except TamagochiIsGone as error:
        output = str(error)
        print("\n".join([output]))


if __name__ == "__main__":
    main()
