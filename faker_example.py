from faker import Faker


faker_instance = Faker('UK')

print(faker_instance.first_name())
print(faker_instance.last_name())
print(faker_instance.email())
print(faker_instance.password())
print(faker_instance.profile())
