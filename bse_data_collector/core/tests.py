import redis
from django.test import TestCase

from core.utils import connect_db
from core.models import RedisModel


# Student model for testing purpose
class Student(RedisModel):
    class Meta:
        name = 'student'
        fields = ['id', 'name']
        key_field = 'name'


class RedisModelTestCase(TestCase):

    def setUp(self):
        r = connect_db()
        r.flushall()
        Student(id=2, name='Jon').create()
        Student(id=3, name='Jen').create()

    def test_create_object(self):
        student = Student(id=1, name='Max')
        student.create()
        r = connect_db()
        self.assertFalse(r.hgetall('student:max') == {})

    def test_find(self):
        res = Student.find('Jon')
        self.assertEqual(res['name'], 'Jon')

    def test_find_all(self):
        res = Student.find_all('J')
        self.assertEqual(len(res), 2)
        res = Student.paginate()
        
        
