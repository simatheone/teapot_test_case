import time

from .constants import (TEAPOT_ALREADY_OFF, TEAPOT_ALREADY_ON, TEAPOT_STOPPED,
                        TEAPOT_TURN_OFF, TEAPOT_TURN_ON, WATER_IS_BOILED,
                        WATER_TEMPERATURE)


class Teapot:
    def __init__(self, volume: float) -> None:
        self.is_on = False
        self._is_boiling = False
        self._volume = volume
        self._max_temperature = 100.0


class ElectricTeapot(Teapot):
    def __init__(self, volume: float) -> None:
        super().__init__(volume)
        self.water_temperature = 20.0
        self._stop_flag = False
        self._boil_time = 10

    def turn_on(self):
        """Выполняет включение чайника."""
        if not self.is_on:
            self.is_on = True
            print(TEAPOT_TURN_ON)
            return self.boil_water()
        return TEAPOT_ALREADY_ON

    def turn_off(self) -> str:
        """Выполняет выключение чайника."""
        if self.is_on:
            self.is_on, self._is_boiling = False, False
            self._stop_flag = True
            return TEAPOT_TURN_OFF
        return TEAPOT_ALREADY_OFF

    def boil_water(self) -> str:
        """Выполняет кипячение воды."""
        self._is_boiling = True
        temperature_per_sec = self._calculate_increasing_temperature()

        while self.water_temperature != self._max_temperature:
            if self._stop_flag:
                break

            self.water_temperature += temperature_per_sec
            print(WATER_TEMPERATURE.format(
                water_temperature=self.water_temperature
                )
            )
            time.sleep(1)

        if not self._stop_flag:
            print(WATER_IS_BOILED)
            return self.turn_off()
        return TEAPOT_STOPPED

    def _calculate_increasing_temperature(self):
        """
        Высчитывается насколько должна повышаться температура
        каждую секунду во время кипячения воды.
        """
        temperature_per_second = (
            self._max_temperature - self.water_temperature
        ) / self._boil_time
        return temperature_per_second
