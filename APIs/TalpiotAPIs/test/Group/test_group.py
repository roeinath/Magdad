import mongomock
import unittest
from mongoengine import connect, disconnect
from APIs.TalpiotAPIs import *


class TestGroup(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.connection = connect('mongoenginetest', host='mongomock://localhost')
        u1 = User(name="Test McTest 1", email="test1@test.test")
        u1.save()
        u2 = User(name="Test McTest 2", email="test2@test.test")
        u2.save()
        u3 = User(name="Test McTest 3", email="test3@test.test")
        u3.save()
        u4 = User(name="Test McTest 4", email="test4@test.test")
        u4.save()

        cls.u1 = u1
        cls.u2 = u2
        cls.u3 = u3
        cls.u4 = u4

    @classmethod
    def tearDownClass(cls) -> None:
        disconnect()

    def test_create_group(self):
        g = Group(name="test group", description="the test group", participants=[self.u1, self.u2], admins=[self.u1])
        g.save()

        found = Group.objects(name="test group").first()
        self.assertEqual(found.name, "test group")
        self.assertEqual(found.description, "the test group")
        self.assertEqual(found.participants, [self.u1, self.u2])
        self.assertEqual(found.admins, [self.u1])

    def test_create_new_group(self):
        create_new_group("test group 2", "the test group", [self.u1, self.u2], [self.u1])

        found = Group.objects(name="test group 2").first()
        self.assertEqual(found.name, "test group 2")
        self.assertEqual(found.description, "the test group")
        self.assertEqual(found.participants, [self.u1, self.u2])
        self.assertEqual(found.admins, [self.u1])

    def test_repr(self):
        g = Group(name="test group 3", description="the test group", participants=[self.u1, self.u2], admins=[self.u1])
        self.assertEqual(g.__repr__(), "test group 3")

    def test_get_user_groups(self):
        g1 = Group(name="test group 4", description="the test group", participants=[self.u3, self.u4], admins=[self.u3])
        g1.save()
        g2 = Group(name="test group 5", description="the test group", participants=[self.u3], admins=[self.u4])
        g2.save()

        found = get_user_groups(self.u3)
        self.assertEqual(found, [g1, g2])

        found = get_user_groups(self.u4)
        self.assertEqual(found, [g1])

    def test_is_user_in_group(self):
        g = Group(name="test group 6", description="the test group", participants=[self.u1], admins=[self.u1])
        g.save()

        self.assertTrue(is_user_in_group_name(self.u1, "test group 6"))
        self.assertFalse(is_user_in_group_name(self.u2, "test group 6"))

        self.assertTrue(is_user_in_group(self.u1, g))
        self.assertFalse(is_user_in_group(self.u2, g))
