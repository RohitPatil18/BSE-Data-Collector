import redis

from django.core.exceptions import ValidationError, ObjectDoesNotExist

from core.utils import connect_db

'''
I could have used Django's caching framework to manage storage action. 
But I decided to keep DB and Caching layer seperated.
'''

class RedisIntegerField:
    ''''
    Idea is to implement fields so we can add validation layer and all. But as I'm already behind the timing,
    Not going ahead with it. We can add more functionalities like required and all sort of things.
    '''
    value = None

    def validate(self, val):
        if type(val) == int:
            return val
        raise ValidationError("Invalid value for Integer field", 'invalid_value')



class RedisModel:
    '''
    Custom Redis Model to manage DB related tasks related to Redis
    '''
    data = {}

    class Meta:
        fields = []
        name = None
        key_field = None
    
    def __init__(self, *args, **kwargs):
        self._check_meta_fields()
        _fields = set()
        if kwargs:
            for key, value in kwargs.items():
                if key in self.Meta.fields:
                    self.data[key] = value
                _fields.add(key)
        # Setting null values for the fields that were not found.
        other_fields = set(self.Meta.fields) - _fields
        for f in other_fields:
            self.data[f] = None

    def _check_meta_fields(self):
        if self.Meta.name == None:
            raise Exception(f"set name in {self.__class__.__name__}'s which can be used to save data in redis db")
        if self.Meta.fields == []:
            raise Exception(f"fields cannot be empty. set fields in {self.__class__.__name__}'s Meta class")
        if self.Meta.key_field == None:
            raise Exception(f"set non-null attr key_field in {self.__class__.__name__}'s Meta class")
        if self.Meta.fields and self.Meta.key_field and self.Meta.key_field not in self.Meta.fields:
            raise Exception(f"Make sure key_field exists in fields list in {self.__class__.__name__}'s Meta class")

    def validate(self):
        # For time being, I am only validating key_field which will be used as key
        if self.data[self.Meta.key_field] in [None, '']:
            raise ValidationError(f'Key field {self.Meta.key_field} cannot be null/empty')

    def create(self):
        self.validate()
        r = connect_db()
        _key_field = self.data[self.Meta.key_field]
        if type(_key_field) == str:
            _key_field = _key_field.lower()
        r.hset(f'{self.Meta.name}:{_key_field}', mapping=self.data)
        r.persist(f'{self.Meta.name}:{_key_field}')

    def update(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError

    @classmethod
    def all(self):
        r = connect_db()
        data = []
        for i in r.scan_iter(f'{self.Meta.name}:*'):
            data.append(r.hgetall(i))
        return data

    def _get_sliced_data(self, pattern, page, size):
        r = connect_db()
        data = []
        cursor = page-1
        keys = r.scan(cursor, pattern, count=size)
        for i in keys[1]:
            data.append(r.hgetall(i))
        return data 

    @classmethod
    def paginate(cls, page=1, size=50):
        pattern = f'{cls.Meta.name}:*'
        return cls._get_sliced_data(cls, pattern, page, size)


    @classmethod
    def find_all(cls, value):
        '''
        Returns list of objects which key_field value startswith provided value
        '''
        data = []
        value = value.lower()
        # if paginate:
        #     pattern = f'{cls.Meta.name}:{value}*'
        #     print(pattern)
        #     data = cls._get_sliced_data(cls, pattern, page, size)
        # else:
        r = connect_db()
        for i in r.scan_iter(f'{cls.Meta.name}:{value}*'):
            data.append(r.hgetall(i))
        return data   

    @classmethod
    def find(cls, value):
        '''
        Returns list of objects which key_field value startswith provided value
        '''
        r = connect_db()
        value = value.lower()
        data = r.hgetall(f'{cls.Meta.name}:{value}')
        if data == {}:
            raise ObjectDoesNotExist
        return data     