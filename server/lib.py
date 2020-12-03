from random import randint
from const import const

interrupted_sleep_reasons = const.interrupted_sleep_reasons
well_slept_reasons = const.well_slept_reasons
min_stat_limits = const.min_stat_limits
max_stat_limits = const.max_stat_limits


class Food:
    def __init__(self, name='borgar', fat=3, time_to_eat=0, energy=1):
        if not isinstance(name, str) or not isinstance(fat, int) \
                or not isinstance(time_to_eat, int) or not isinstance(energy, int):
            raise AttributeError(const.errors['wrong_args_food'])

        self.fat = fat
        self.time_to_eat = time_to_eat
        self.energy = energy
        self.name = name


class Student:
    def __init__(self, name, fat):
        if not isinstance(name, str) or not isinstance(fat, int):
            raise AttributeError(const.errors['wrong_args_student'])
        self.name = name
        self.xp = 0
        self.energy = 0
        self.fat = fat
        self.mood_level = 0

    def regulate_stats(self):
        if self.energy < min_stat_limits["energy"]:
            self.energy = min_stat_limits["energy"]
        elif self.energy > max_stat_limits["energy"]:
            self.energy = max_stat_limits["energy"]
        if self.mood_level < min_stat_limits["mood_level"]:
            self.mood_level = min_stat_limits["mood_level"]
        elif self.mood_level > max_stat_limits["mood_level"]:
            self.mood_level = max_stat_limits["mood_level"]

    def eat(self, food=Food()):
        if not isinstance(food, Food):
            raise TypeError(const.errors['wrong_food'])

        self.fat += food.fat
        self.energy += food.energy
        self.mood_level += 1
        self.regulate_stats()
        return const.end_text['eat'].format(food.name)

    def sleep(self):
        time = randint(1, 12)
        wake_up_reasons = interrupted_sleep_reasons if time <= 5 else well_slept_reasons
        result = wake_up_reasons[randint(0, len(wake_up_reasons) - 1)] \
                 + "\nTime: " + ("{} hours".format(time) if time > 1 else "1 hour")

        self.energy += time // 2
        self.mood_level += 1 if time > 5 else -1
        self.regulate_stats()
        return result

    def play_games(self):
        if self.energy == 0:
            return const.end_text['no_en_play']
        wins = randint(0, self.energy)

        self.mood_level += 2 * wins - self.energy
        self.energy = wins
        self.regulate_stats()
        return const.end_text['play'].format(wins)

    def study(self):
        if self.energy < 5:
            return const.end_text['no_en_study']

        self.xp += self.energy // 5
        self.fat -= 10
        self.energy = min_stat_limits["energy"]
        self.mood_level = min_stat_limits["mood_level"]
        return const.end_text['study']

    def get_mood(self):
        if self.mood_level < -3:
            return "very bad"
        elif self.mood_level < 0:
            return "bad"
        elif self.mood_level == 0:
            return "neutral"
        elif self.mood_level < 4:
            return "good"
        else:
            return "very good"
