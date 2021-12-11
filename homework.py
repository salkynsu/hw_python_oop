class InfoMessage:
    """Информационное сообщение о тренировке."""

    message: str = (
        'Тип тренировки: {}; '
        'Длительность: {:.3f} ч.; '
        'Дистанция: {:.3f} км; '
        'Ср. скорость: {:.3f} км/ч; '
        'Потрачено ккал: {:.3f}.'
    )

    def __init__(
        self,
        training_type: str,
        duration: float,
        distance: float,
        speed: float,
        calories: float,
    ) -> None:
        self.training_type = training_type
        self.duration_h = duration
        self.distance_km = distance
        self.speed_kmh = speed
        self.calories_kcal = calories

    def get_message(self) -> str:
        return self.message.format(
            self.training_type,
            self.duration_h,
            self.distance_km,
            self.speed_kmh,
            self.calories_kcal,
        )


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000
    MIN_IN_H: int = 60
    LEN_STEP: float = 0.65

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег."""

    coeff_calorie_1: int = 18
    coeff_calorie_2: int = 20

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float
    ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories = (
            (self.coeff_calorie_1
             * self.get_mean_speed()
             - self.coeff_calorie_2
             )
            * self.weight
            / self.M_IN_KM
            * self.duration
            * self.MIN_IN_H
        )
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    coeff_calorie_1: float = 0.035
    coeff_calorie_2: float = 0.029

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories = (
            (self.coeff_calorie_1
              * self.weight
              + (self.get_mean_speed() ** 2
                 // self.height
                )
              * self.coeff_calorie_2
              * self.weight
            )
            * self.duration
            * self.MIN_IN_H
        )
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    coeff_calorie_1: float = 1.1
    coeff_calorie_2: float = 2

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: float,
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = (
            self.length_pool
            * self.count_pool
            / self.M_IN_KM
            / self.duration
        )
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories = (
            (self.get_mean_speed()
             + self.coeff_calorie_1
             )
            * self.coeff_calorie_2
            * self.weight
        )
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные, полученные от датчиков."""

    workout = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in workout.keys():
        raise ValueError('Неизвестный тип тренировки')
    training = workout[workout_type](*data)
    return training


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
