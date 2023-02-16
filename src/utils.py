import logging
import sys
import threading
from typing import Literal, Union

from .constants import POURED_WATER
from .teapot import ElectricTeapot

INPUT_AND_ERRORS_MSG = {
    'teapot': (
        'Введи объем чайника (л.): ',
        'Объем чайника должен быть больше 0.',
    ),
    'water': (
        'Укажите наливаемое количество воды (л.): ',
        'Количество наливаемой воды должно быть больше 0.',
    ),
    'invalid_char': 'Введите цифры вместо букв/спецсимволов.',
}
POURING_WATER_MESSAGE = (
    'Наливаемое количество воды превышает объем чайника. '
    'В чайник будет налито {teapot_volume} л. воды '
    '(равных объему чайника).'
)

INPUT_MESSAGE = 0
ENTITY_ERROR_MESSAGE = 1
INVALID_CHARACTER = 2

stop_event = threading.Event()


def get_volume(
    entity_type: Union[Literal['teapot'], Literal['water']]
) -> float:
    """
    Считывает информацию из input и проверяет, что пользователь задал
    цифры, а не буквы/символы.
    Выполняет проверку объема чайника/количество наливаемой воды.
    Задаваемый объем должен быть больше нуля.
    """
    try:
        volume_amount = float(
            input(INPUT_AND_ERRORS_MSG[entity_type][INPUT_MESSAGE])
        )
    except ValueError:
        print(INPUT_AND_ERRORS_MSG['invalid_char'][INVALID_CHARACTER])
        return get_volume(entity_type)

    if volume_amount == 0.0:
        print(INPUT_AND_ERRORS_MSG[entity_type][ENTITY_ERROR_MESSAGE])
        return get_volume(entity_type)
    return volume_amount


def correct_pouring_water_amount(
    pouring_water_input: float, teapot_volume: float
) -> float:
    """Корректирует значение наливаемой воды в чайник."""
    pouring_water_value = None
    if pouring_water_input > teapot_volume:
        print(POURING_WATER_MESSAGE.format(teapot_volume=teapot_volume))
        pouring_water_value = teapot_volume
    else:
        pouring_water_value = pouring_water_input

    print(POURED_WATER.format(amount_for_pouring=pouring_water_value))
    return pouring_water_value


def get_input(teapot: ElectricTeapot) -> None:
    """
    Функция вызываемая в первом потоке.

    Ожидает вызова команд:
        - включить чайник "on";
        - остановить/выключить чайник "off";
        - выйти из программы "exit".

    При получении команды "on":
        - записывает сообщение в логи;
        - вызывает метод запуска чайника;
        - после выполнения записывает информацию в лог о том,
          что чайник закипел.

    При получении команды "off":
        - вызывает метод остановки чайника;

    При получении команды "exit":
        - записывает сообщение в логи;
        - переключает флаг у События (Event) на True;
        - выполняет системный выход из программы.

    При получении неизестной команды печатает сообщение в терминал.
    """
    while not stop_event.is_set():
        action = input(
            'Доступные команды по управлению чайником: \n'
            '- включить чайник -> on \n'
            '- остановить/выключить чайник -> off \n'
            '- выйти из программы -> exit \n'
            'Введите команду -> '
        )

        if action == 'on':
            logging.info('Запуск чайника')
            print(teapot.turn_on())
            logging.info('Чайника закипел. Завершение работы чайника')

        elif action == 'off':
            print(teapot.turn_off())

        elif action == 'exit':
            logging.info('Пользователь завершил работу программы')
            stop_event.set()
            sys.exit(0)

        else:
            print('Неизвестная команда')


def turn_off_teapot(teapot: ElectricTeapot) -> None:
    """
    Функция вызываемая во втором потоке.
    Ожидает, что вызова команды "off".

    В случае получения команды:
        - записывает сообщение об остановке в логи;
        - вызывает метод остановки чайника;
        - переключает флаг у События (Event) на True;
        - перывает выполнение цикла.
    """
    while not stop_event.is_set():
        action = input('')
        if action == 'off':
            logging.info('Остановка работы чайника')
            print(teapot.turn_off())
            stop_event.set()
            break
