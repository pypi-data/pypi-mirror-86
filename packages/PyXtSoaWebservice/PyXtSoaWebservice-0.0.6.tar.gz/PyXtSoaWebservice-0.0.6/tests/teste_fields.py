# from pyxtsoawebservice.fields import Fields
# 
# campo1 = Fields('a',1)
# campo1.save()
# 
# campo2 = Fields('b',1)
# campo2.save()
# 
# campo3 = Fields('c',1)
# campo3.save()
# 
# print(Fields.all())

class Fields(object):

    @classmethod
    def add(cls, **kwargs):
        obj = cls()
        for (field, value) in kwargs.items():
            setattr(cls, field, value)
        return obj

    @classmethod
    def get(cls, name, default=None):
        obj = cls()
        if hasattr(obj,name):
            return getattr(cls, name)
        else:
            return default

model = Fields()

model.add(foo=1, bar=2)
print(model.foo, model.bar)  # prints '1, 2'
model.add(cax=3)
print(model.foo, model.bar, model.cax)  # prints '1, 2'
print(model.get('fuo'))
