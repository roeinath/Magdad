import mongomock
import unittest
from mongoengine import connect, disconnect
from APIs.TalpiotAPIs import *


class TestUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.connection = connect('mongoenginetest', host='mongomock://localhost')

    @classmethod
    def tearDownClass(cls) -> None:
        disconnect()

    def test_create_user(self):
        u = User(name="Test McTest", email="test@test.test")
        u.save()

        found = User.objects().first()
        self.assertEqual(found.name, "Test McTest")

    def test_get_first_name(self):
        u = User(name="Test McTest", email="test@test.test")
        u.save()

        found = User.objects().first()
        self.assertEqual(found.get_first_name(), "Test")

    def test_get_last_name(self):
        u = User(name="Test McTest", email="test@test.test")
        u.save()

        found = User.objects().first()
        self.assertEqual(found.get_last_name(), "McTest")

    def test_get_gender(self):
        u = User(name="Test McTest1", email="test@test.test", gender="male")
        u.save()

        found = User.objects(name="Test McTest1").first()
        self.assertEqual(found.get_gender(), Gender.male)

        u = User(name="Test McTest2", email="test@test.test", gender="female")
        u.save()

        found = User.objects(name="Test McTest2").first()
        self.assertEqual(found.get_gender(), Gender.female)

        u = User(name="Test McTest3", email="test@test.test", gender="other")
        u.save()

        found = User.objects(name="Test McTest3").first()
        self.assertEqual(found.get_gender(), Gender.other)
