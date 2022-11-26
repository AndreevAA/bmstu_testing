import pytest
import allure

@allure.epic('Allure Epic')
@allure.feature('Demo Feature')
@allure.story('Passed Example')
@allure.issue('https://example.org/issue/1')
@allure.testcase('https://example.org/tms/2')
def test_passed_scenario():
    """
    Passed Scenario
    """
    with allure.step("Given I'm on a site"):
        print('step1')
    with allure.step("When I enter something on the page"):
        print('step2')
    with allure.step("Then I verify is OK"):
        print('step3')

@allure.epic('Allure Epic')
@allure.feature('Demo Feature')
@allure.story('Failed Example')
@allure.issue('https://example.org/issue/3')
@allure.testcase('https://example.org/tms/4')
def test_failed_scenario():
    """
    Failed Scenario
    """
    with allure.step("Given I'm on a site"):
        print('step1')
    with allure.step("When I enter something on the page"):
        print('step2')
    with allure.step("Then I verify is FAILED"):
        print('step3')
        pytest.fail('FAILURE ON PURPOSE')

@allure.epic('Allure Epic')
@allure.feature('Demo Feature')
@allure.story('bROKEN Example')
@allure.issue('https://example.org/issue/5')
@allure.testcase('https://example.org/tms/6')
def test_broken_scenario():
    """
    Broken Scenario
    """
    with allure.step("Given I'm on a site"):
        print('step1')
    with allure.step("When I enter something on the page"):
        print('step2')
    with allure.step("Then I verify is BROKEN"):
        print('step3')
        raise NotImplementedError('NOT IMPLEMENTED')

@pytest.fixture(autouse=True)
def hooks():
    # set up
    f = open("./allure-results/environment.properties", "w+")
    f.write("myvar=myvalue\n")
    f.write("myvar2=myvalue2\n")
    f.close()

    yield
    # tear down
    f = open('./files/fescobar.png', "rb")
    image = f.read()
    allure.attach(
        image,
        name = 'image',
        attachment_type = allure.attachment_type.PNG
    )

    f = open('./files/google.mp4', "rb")
    image = f.read()
    allure.attach(
        image,
        name = 'image',
        attachment_type = allure.attachment_type.MP4
    )


#     python3 -m pytest Test/User/UserServiceTestCase.py
# python3 -m pytest Test/User/UserRepositoryTestCase.py
#
# python3 -m pytest Test/Item/ItemServiceTestCase.py
# python3 -m pytest Test/Item/ItemRepositoryTestCase.py
#
# python3 -m pytest Test/Look/LookServiceTestCase.py
# python3 -m pytest Test/Look/LookRepositoryTestCase.py
#
# python3 -m pytest Test/Wardrobe/WardrobeRepositoryTestCase.py
# python3 -m pytest Test/Wardrobe/WardrobeServiceTestCase.py
#
# python3 -m pytest Test/Invite/InviteServiceTestCase.py
# python3 -m pytest Test/Invite/InviteRepositoryTestCase.py

# @allure.epic('User service')
# def test_user_service_test_case():

from pymock import PyMock

from Services.user_service import UserService
from Test.MockImageRepository import MockImageRepository
from Test.User.UserMockRepository import UserMockRepository


def inject_mock_user_service_and_repo(f):
    def decorated_function(*args, **kwargs):
        repo = PyMock.create(UserMockRepository)
        service = UserService(repo, MockImageRepository())
        return f(repo, service, *args, **kwargs)

    return decorated_function


@inject_mock_user_service_and_repo
def test_register_valid(repo, service):
    args = ['larin', 'Vladimir Larin', '12345678', None]
    expect_return = {"login": "larin", "name": "Vladimir Larin", "password": "12345678", "imageid": None}, False
    PyMock.setup(repo.register_user(*args)).returns(expect_return)

    response, code = service.register('larin', 'Vladimir Larin', '12345678', None)
    assert response == '{"login": "larin", "name": "Vladimir Larin", "password": "12345678", "imageid": null}'
    assert code == 200
