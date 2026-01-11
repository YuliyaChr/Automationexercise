import requests
from pprint import pprint
from faker import Faker

fake = Faker()

def test_1_get_all_products_list():
    url = "https://automationexercise.com/api/productsList"
    response = requests.get(
        url=url
    )
    print("Response:", response)
    pprint(response.json())
    assert response.status_code == 200
    # assert isinstance(response.json(), dict)
    assert "products" in response.json() #response has "products" key


def test_2_post_to_all_products_list():
    url = "https://automationexercise.com/api/productsList"
    response = requests.post (url=url)
    print("Response object:", response)
    print("Status code:", response.status_code)
    print("Response text:", response.text)
    pprint(response.json())

    json_response = response.json()

    assert (response.status_code == 405 or json_response.get("responseCode") == 405)
    assert "This request method is not supported." in response.text


def test_3_get_all_brands_list():
    url = "https://automationexercise.com/api/brandsList"
    response = requests.get(
        url=url)
    print("Response object:", response)
    print("Status code:", response.status_code)
    print("response.text: ", response.text)

    assert response.status_code == 200


def test_4_put_all_brands_list():
    url = "https://automationexercise.com/api/brandsList"
    response = requests.put(
        url=url)
    print("Response object:", response)
    print("Status code:", response.status_code)
    print("response.text: ", response.text)

    json_response = response.json()

    assert (response.status_code == 405 or json_response.get("responseCode") == 405)
    assert "This request method is not supported." in response.text


def test_5_search_products_with_search_parameter():
    search_product = {"search_product": "dress"}
    # search_product = {"search_product": "women"}
    url = "https://automationexercise.com/api/searchProduct"
    response = requests.post(
        url=url,
        data=search_product   #data
    )
    # print(response.json())
    pprint(response.json())
    print("response.text: ", response.text)

    body = response.json()
    products_list = body["products"]
    assert response.status_code == 200

    for product in products_list:
        assert "dress" in product["category"]["category"].lower()
        # assert "women" in product["category"]["usertype"]["usertype"].lower()
        # assert {"usertype": "women"} in product["category"]["usertype"]
        # print(product["category"]["usertype"])


def test_6_search_products_without_search_parameter():
    url = "https://automationexercise.com/api/searchProduct"
    response = requests.post(
        url=url,
    )
    print(response.json())
    pprint(response.json())

    assert response.status_code == 400, f"Wrong status code, expected 400, received {response.status_code}"
    # Expecting 400 normally, but actual API returns 200


def test_7_valid_user_login(registered_user):
    url = "https://automationexercise.com/api/verifyLogin"

    email = registered_user["email"]
    password = registered_user["password"]

    payload = {
        "email": email,
        "password": password
    }

    response = requests.post(
        url=url,
        data=payload
    )

    print("Status code:", response.status_code)
    pprint(response.json())

    assert response.status_code == 200, f"Wrong status code, expected 200, received {response.status_code}"

    #{'message': 'User exists!', 'responseCode': 200}????


def test_8_user_login_without_email(registered_user):
    url = "https://automationexercise.com/api/verifyLogin"

    password = registered_user["password"]

    payload = {
        "password": password
    }

    response = requests.post(
        url=url,
        data=payload
    )
    json_response = response.json()

    print("Status code:", response.status_code)
    print("response.json(): ",response.json())
    pprint(response.json())

    assert (response.status_code == 400 or json_response.get("responseCode") == 400)



def test_9_delete_account_to_verify_login(registered_user):
    url = "https://automationexercise.com/api/verifyLogin"

    email = registered_user["email"]
    password = registered_user["password"]

    payload = {
        "email": email,
        "password": password
    }

    response = requests.delete(
        url=url,
        data=payload
    )

    json_response = response.json()

    print("Status code:", response.status_code)
    pprint(response.json())

    assert (response.status_code == 405 or json_response.get("responseCode") == 405)
    assert "This request method is not supported." in response.text


def test_10_verify_login_invalid_password(registered_user):
    url = "https://automationexercise.com/api/verifyLogin"

    email = fake.email()
    password = registered_user["password"]

    payload = {
        "email": email,
        "password": password
    }

    response = requests.post(
        url=url,
        data=payload
    )
    json_response = response.json()

    print("Status code:", response.status_code)
    print("response.json(): ",response.json())
    pprint(response.json())
    print("response.text: ", response.text)

    assert (response.status_code == 404 or json_response.get("responseCode") == 404)
    assert "User not found!" in response.text


def test_11_create_user_account():
    url = "https://automationexercise.com/api/createAccount"

    fake_email = fake.email()
    fake_name = fake.first_name()
    password = "123qwe"

    payload = {
        "name": fake_name,
        "email": fake_email,
        "password": "123qwe",
        "title": "Mr",
        "birth_date": "2",
        "birth_month": "January",
        "birth_year": "2000",
        "newsletter": "true",
        "optin": "true",
        "firstname": fake_name,  #id = id="first_name"
        "lastname": fake.last_name(),  #id="last_name"
        "company": fake.company(),
        "address1": fake.address(),
        "country": "United States",
        "state": fake.state(),
        "city": fake.city(),
        "zipcode": fake.zipcode(),
        "mobile_number": fake.phone_number()
    }

    response = requests.post(
        url=url,
        data=payload
    )

    json_response = response.json()

    assert (response.status_code == 201 or json_response.get("responseCode") == 201)
    assert "User created!" in response.text


    print("Email used:", fake_email)
    print("Response:", response)
    print("Response text:", response.text)
    # pprint(response.json())
# status code: 200 and responseCode: 201



def test_12_delete_account(registered_user):
    url = "https://automationexercise.com/api/deleteAccount"

    email = registered_user["email"]
    password = registered_user["password"]

    payload = {
        "email": email,
        "password": password
    }

    response = requests.delete(
        url=url,
        data=payload
    )

    json_response = response.json()

    print("Status code:", response.status_code)
    pprint(response.json())

    assert (response.status_code == 200 or json_response.get("responseCode") == 200)
    assert "Account deleted!" in response.text


def test_13_update_user_account(registered_user):
    url = "https://automationexercise.com/api/updateAccount"

    email = registered_user["email"]
    password = registered_user["password"]

    payload = {
        "email": email,
        "password": password,
        "city": "Tampa"
    }

    response = requests.put(
        url=url,
        data=payload
    )
    json_response = response.json()

    print("Status code:", response.status_code)
    print("response.json(): ",response.json())
    pprint(response.json())
    print("response.text: ", response.text)

    assert (response.status_code == 200 or json_response.get("responseCode") == 200)
    assert "User updated!" in response.text



def test_14_get_user_account_detail_by_email(registered_user):
    url = "https://automationexercise.com/api/getUserDetailByEmail"

    email = registered_user["email"]

    payload = {
        "email": email
    }

    response = requests.get(
        url=url,
        params=payload
    )
    json_response = response.json()

    print("Status code:", response.status_code)
    print("response.json(): ",response.json())
    pprint(response.json())
    print("response.text: ", response.text)

    assert (response.status_code == 200 or json_response.get("responseCode") == 200)
