from time import sleep
from random import randint

interrupted_sleep_reasons = [
    "You've been woken up by your aggressive cat"
]

well_slept_reasons = [
    "You've slept enough and now feeling like cucumber"
]

min_stat_limits = {
    "energy": 0,
    "mood_level": -5
}

max_stat_limits = {
    "energy": 15,
    "mood_level": 5
}


class Food:
    def __init__(self, name, fat, time_to_eat, energy):
        self.fat = fat
        self.time_to_eat = time_to_eat
        self.energy = energy
        self.name = name


class Student:
    def __init__(self, name, fat):
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

    def eat(self, food=Food('borgar', 3, 2, 1)):
        if not isinstance(food, Food):
            raise TypeError("food should gave Food type!")
        # sleep(food.time_to_eat)
        self.fat += food.fat
        self.energy += food.energy
        self.mood_level += 1
        self.regulate_stats()
        return "You've eaten {} and now feeling happier".format(food.name)

    def sleep(self):
        time = randint(1, 12)
        # sleep(time)
        wake_up_reasons = interrupted_sleep_reasons if time <= 5 else well_slept_reasons
        result = wake_up_reasons[randint(0, len(wake_up_reasons) - 1)] \
            + ("\nTime: {} hours".format(time) if time > 1 else "1 hour")
        self.energy += time // 2
        self.mood_level += 1 if time > 5 else -1
        self.regulate_stats()
        return result

    def play_games(self):
        if self.energy == 0:
            return "No energy to play;("
        # sleep(self.energy)
        wins = randint(0, self.energy)
        self.mood_level += 2 * wins - self.energy
        self.energy = wins
        self.regulate_stats()
        return "You won {} games".format(wins)

    def study(self):
        if self.energy < 5:
            return "Not enough energy (5 at least needed)"
        # sleep(self.energy)
        self.xp += self.energy // 5
        self.fat -= 10
        self.energy = min_stat_limits["energy"]
        self.mood_level = min_stat_limits["mood_level"]
        return "You've run out of energy and your mood's bad, but you've become smarter"

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

