from Repositories.UserRepository import UserRepository
from Test.DatabaseCleaner import DatabaseCleaner
from Test.Builders.UserBuilder import UserBuilder
from config import test_db_filename

def test_correct_register_user():
    DatabaseCleaner(test_db_filename).clean()
    user_repo = UserRepository(test_db_filename, False)
    builder = UserBuilder().with_name("Vladimir Larin").with_login("larin").with_password("12345678")
    expect = {'user_name': 'Vladimir Larin', 'image_id': None, 'image_url': None, 'login': 'larin'}
    response, error = user_repo.register_user(*builder.build_register_data())
    assert error == False
    assert response == expect

def test_correct_login_user():
    DatabaseCleaner(test_db_filename).clean()
    user_repo = UserRepository(test_db_filename, False)
    builder = UserBuilder().with_name("Vladimir Larin").with_login("larin").with_password("12345678")

    user_repo.register_user(*builder.build_register_data())

    expect = {'user_name': 'Vladimir Larin', 'image_id': None, 'image_url': None, 'login': 'larin'}
    response = user_repo.get_user_info(*builder.build_login_data())
    assert response == expect

def test_correct_change_username():
    DatabaseCleaner(test_db_filename).clean()
    user_repo = UserRepository(test_db_filename, False)
    username = "larin"
    new_name = "Not Vladimir Larin"
    status = user_repo.user_change_name(username, new_name)
    assert status == "OK"

def test_incorrect_login():
    DatabaseCleaner(test_db_filename).clean()
    user_repo = UserRepository(test_db_filename, False)
    username = "andreev"
    password = "12345678"
    response = user_repo.get_user_info(username, password)
    assert response is None

def test_assert_renew_register():
    DatabaseCleaner(test_db_filename).clean()
    user_repo = UserRepository(test_db_filename, False)
    builder = UserBuilder().with_name("Vladimir Larin").with_login("larin").with_password("12345678")
    user_repo.register_user(*builder.build_register_data())
    response, error = user_repo.register_user(*builder.build_register_data())
    assert error == True



