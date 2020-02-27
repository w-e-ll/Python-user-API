from pytest_mongodb import plugin


def test_client(mongodb):
    collection_names = mongodb.list_collection_names()
    assert 'users' in collection_names
    assert len(plugin._cache.keys()) == 1
    test_check_users(mongodb.users)


def test_check_users(users):
    assert users.count_documents({}) == 4
    check_keys_in_docs(
        users, ["firstname", "lastname", "company", "email"]
    )
    manuel = users.find_one({"firstname": "Manuel"})
    assert manuel["lastname"] == "Neuer"
    assert manuel["company"] == "Yandex"
    test_insert(users)


def check_keys_in_docs(collection, keys):
    for doc in collection.find():
        for key in keys:
            assert key in doc


def test_insert(users):
    users.insert_one({
        'firstname': 'Bastian',
        'lastname': 'Schweinsteiger',
        'company': 'Smegg',
        'email': 'bastian.schweinsteiger@smashdocs.net',
        'status': 'confirmed',
        'links': 'http://google_453.net'
    })
    assert users.count_documents({}) == 5
    assert users.find_one({'name': 'Bastian'})


def test_mongo_engine(pytestconfig):
    pymongo = plugin.mongo_engine()
    assert pymongo == 'pymongo'
