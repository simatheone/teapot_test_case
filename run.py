import logging
import sys
import threading

from src.configs import configure_logging
from src.teapot import ElectricTeapot
from src.utils import (correct_pouring_water_amount, get_input, get_volume,
                       turn_off_teapot)


def main() -> None:
    """Главная функция по управлению чайником."""
    configure_logging()
    logging.info('Программа запущена')

    teapot_volume = get_volume('teapot')
    logging.info(f'Новый чайник. Объем чайника: {teapot_volume}')

    water_volume = get_volume('water')
    poured_water = correct_pouring_water_amount(water_volume, teapot_volume)
    logging.info(f'Добавлено воды: {poured_water}')

    teapot = ElectricTeapot(teapot_volume)

    activate_input_thread = threading.Thread(target=get_input, args=(teapot,))
    turn_off_thread = threading.Thread(target=turn_off_teapot, args=(teapot,))
    threads = (activate_input_thread, turn_off_thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Программа остановлена')
        logging.info('Программа завершила работу')
        sys.exit(0)
