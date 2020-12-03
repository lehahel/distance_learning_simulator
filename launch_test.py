import unittest
from server import lib
import launch_server


class TestStudent(unittest.TestCase):
    def test_eating_class(self):
        student = lib.Student("Alice", 50)
        food = lib.Food()
        self.assertEqual(student.fat, 50)
        self.assertEqual(student.energy, 0)

        student.eat()
        self.assertEqual(student.fat, 53)
        self.assertEqual(student.energy, 1)
        self.assertEqual(student.get_mood(), 'good')

        for _ in range(3):
            student.eat(food)
        self.assertEqual(student.fat, 62)
        self.assertEqual(student.energy, 4)
        self.assertEqual(student.get_mood(), 'very good')

    def test_eating_server(self):
        self.assertEqual(launch_server.student.name, "Unknown")
        self.assertEqual(launch_server.student.fat, 0)
        self.assertEqual(launch_server.student.energy, 0)
        self.assertEqual(launch_server.student.get_mood(), 'neutral')

        launch_server.eat()
        self.assertEqual(launch_server.student.fat, 3)
        self.assertEqual(launch_server.student.energy, 1)
        self.assertEqual(launch_server.student.get_mood(), 'good')

        for _ in range(3):
            launch_server.eat()
        self.assertEqual(launch_server.student.fat, 12)
        self.assertEqual(launch_server.student.energy, 4)
        self.assertEqual(launch_server.student.get_mood(), 'very good')

    def test_play_student(self):
        student = lib.Student("Alice", 50)
        self.assertEqual(student.fat, 50)
        self.assertEqual(student.energy, 0)

        student.energy = 10
        student.play_games()
        self.assertNotEqual(student.energy, -1)
        self.assertNotEqual(student.energy, 11)

    def test_play_server(self):
        launch_server.student.energy = 10
        launch_server.play()
        self.assertNotEqual(launch_server.student.energy, -1)
        self.assertNotEqual(launch_server.student.energy, 11)

    def test_study_student(self):
        student = lib.Student("Alice", 50)
        student.energy = 10
        student.study()
        self.assertEqual(student.energy, 0)
        self.assertEqual(student.get_mood(), 'very bad')
        self.assertEqual(student.xp, 2)

        student.study()
        self.assertEqual(student.energy, 0)
        self.assertEqual(student.get_mood(), 'very bad')
        self.assertEqual(student.xp, 2)


if __name__ == '__launch_test__':
    unittest.main()
