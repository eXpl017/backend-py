from faker import Faker

fake = Faker()

books = [
    {
        'isbn10': fake.isbn10(separator=''),
        'title': ' '.join(x.capitalize() for x in fake.words(nb=5)),
        'author': fake.name(),
        'publisher': fake.company(),
        'published_date': fake.date(),
        'page_count': fake.random_int(50,2000),
        'language': fake.language_name()
    } for _ in range(10)
]

# print(json.dumps(books))
