from Faker import Faker
# this Populator is only a function thats return a django_faker.populator.Populator instance
# correctly initialized with a faker.generator.Generator instance, configured as above
populator = Faker.getPopulator()

from aska.models import User, Queston, Answer, Tag, Like
populator.addEntity(User,5)
populator.addEntity(Question,10)

insertedPks = populator.execute()