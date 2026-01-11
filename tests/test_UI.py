import time

from playwright.sync_api import expect
from faker import Faker

fake = Faker()


def test_1_register_new_user(page):

    # Generate fake data
    fake_email = fake.email()
    fake_name = fake.first_name()
    fake_password = fake.password()

    # Open the page
    page.goto("https://automationexercise.com/")
    expect(page.get_by_role("link", name="Home")).to_have_css("color", "rgb(255, 165, 0)")


    # Click Sign Up/Login
    page.get_by_role("link", name=" Signup / Login").click()

    # Verify we navigated to the login page
    expect(page.get_by_text("New User Signup!", exact=True)).to_be_visible()

    # Fill in the signup form
    page.get_by_placeholder("Name").fill(fake_name)
    page.locator("input[data-qa='signup-email']").fill(fake_email)

    # Click Sign Up
    page.get_by_role("button", name="Signup").click()

    # Verify we navigated to the next page
    expect(page).to_have_url("https://automationexercise.com/signup")
    expect(page.get_by_text("Enter Account Information", exact=True)).to_be_visible()
    # expect(page.locator("h2:has-text('Enter Account Information')")).to_be_visible()

    # selecting radio button
    page.get_by_role("radio", name="Mr.").check()
    expect(page.locator("#id_gender1")).to_be_checked()
    expect(page.locator("#id_gender2")).not_to_be_checked()

    # Fill in the password
    page.get_by_label("Password").fill(fake_password)

    # Date of Birth, select day, month, year
    page.select_option("#days", "2")
    page.select_option("#months", "January")
    page.select_option("#years", "2000")

    # click Sign up for our newsletter!
    page.get_by_role("checkbox", name="Sign up for our newsletter!").check()
    expect(page.locator("#newsletter")).to_be_checked()

    # click Receive special offers from our partners!
    page.get_by_role("checkbox", name="Receive special offers from our partners!").check()
    expect(page.locator("#optin")).to_be_checked()

    #Address Information
    page.get_by_label("First name ").fill(fake_name)
    # page.locator("#first_name").fill(fake_name)
    page.locator("#last_name").fill(fake.last_name())
    page.locator("#company").fill(fake.company())
    page.fill("input#address1", fake.street_address())
    page.select_option("#country", "United States")
    page.fill("input#state", fake.state())
    page.fill("input#city", fake.city())
    page.fill("input#zipcode", fake.zipcode())
    page.fill("input#mobile_number", fake.phone_number())

    page.get_by_role("button", name="Create Account").click()

    # Verify we navigated to the next page
    expect(page).to_have_url("https://automationexercise.com/account_created")
    expect(page.locator("h2:has-text('Account Created!')")).to_be_visible()

    page.get_by_text("Continue").click()
    expect(page.get_by_text(f"Logged in as {fake_name}")).to_be_visible()

    page.get_by_role("link", name=" Delete Account").click()
    expect(page.get_by_text("Account Deleted!")).to_be_visible()
    print(f"✅ Test passed for user: {fake_name} ({fake_email})")


def test_2_registered_user_login_with_correct_email_passw(page, registered_user):
    email = registered_user["email"]
    password = registered_user["password"]
    first_name = registered_user["first_name"]
    last_name = registered_user["last_name"]

    # Open the page
    page.goto("https://automationexercise.com/")
    expect(page.get_by_role("link", name="Home")).to_have_css("color", "rgb(255, 165, 0)")

    # Click Sign Up/Login
    page.get_by_role("link", name=" Signup / Login").click()

    # Verify we navigated to the login page
    expect(page.get_by_text("Login to your account", exact=True)).to_be_visible()


    page.locator("input[data-qa='login-email']").fill(email)
    page.locator("input[data-qa='login-password']").fill(password)
    page.get_by_role("button", name="Login").click()
    expect(page.get_by_text(f"Logged in as {first_name}")).to_be_visible()

    page.get_by_role("link", name=" Delete Account").click()
    expect(page.get_by_text("Account Deleted!")).to_be_visible()
    print(f"✅ Test passed for user: {first_name} ({email})")



def test_3_registered_user_login_with_incorrect_email_passw(page):

    # Generate fake data
    fake_email = fake.email()
    fake_password = fake.password()

    # Open the page
    page.goto("https://automationexercise.com/")
    expect(page.get_by_role("link", name="Home")).to_have_css("color", "rgb(255, 165, 0)")

    # Click Sign Up/Login
    page.get_by_role("link", name=" Signup / Login").click()

    # Verify we navigated to the login page
    expect(page.get_by_text("Login to your account", exact=True)).to_be_visible()

    page.locator("input[data-qa='login-email']").fill(fake_email)
    page.locator("input[data-qa='login-password']").fill(fake_password)
    page.get_by_role("button", name="Login").click()
    expect(page.get_by_text("Your email or password is incorrect!")).to_be_visible()
    expect(page.get_by_text("Your email or password is incorrect!")).to_have_css("color", "rgb(255, 0, 0)")



def test_4_user_logout(page, registered_user):

    email = registered_user["email"]
    password = registered_user["password"]
    first_name = registered_user["first_name"]
    last_name = registered_user["last_name"]

    # Open the page
    page.goto("https://automationexercise.com/")
    expect(page.get_by_role("link", name="Home")).to_have_css("color", "rgb(255, 165, 0)")

    # Click Sign Up/Login
    page.get_by_role("link", name=" Signup / Login").click()

    # Verify we navigated to the login page
    expect(page.get_by_text("Login to your account", exact=True)).to_be_visible()

    page.locator("input[data-qa='login-email']").fill(email)
    page.locator("input[data-qa='login-password']").fill(password)
    page.get_by_role("button", name="Login").click()
    expect(page.get_by_text(f"Logged in as {first_name}")).to_be_visible()



    page.get_by_role("link", name="  Logout").click()
    expect(page.get_by_text("Login to your account", exact=True)).to_be_visible()
    expect(page.get_by_text("New User Signup!", exact=True)).to_be_visible()


def test_5_register_user_with_existing_email(page, registered_user):

    email = registered_user["email"]
    fake_name = fake.name()


    # Open the page
    page.goto("https://automationexercise.com/")
    expect(page.get_by_role("link", name="Home")).to_have_css("color", "rgb(255, 165, 0)")

    # Click Sign Up/Login
    page.get_by_role("link", name=" Signup / Login").click()

    # Verify we navigated to the login page
    expect(page.get_by_text("New User Signup!", exact=True)).to_be_visible()

    # Fill in the signup form
    page.get_by_placeholder("Name").fill(fake_name)
    page.locator("input[data-qa='signup-email']").fill(email)
    page.get_by_role("button", name="Signup").click()
    expect(page.get_by_text("Email Address already exist!")).to_be_visible()
    expect(page.get_by_text("Email Address already exist!")).to_have_css("color", "rgb(255, 0, 0)")


def test_6_contact_us_form(page):

    # Generate fake data
    fake_name = fake.name()
    fake_email = fake.email()
    fake_text = fake.text()

    # Open the page
    page.goto("https://automationexercise.com/")
    expect(page.get_by_role("link", name="Home")).to_have_css("color", "rgb(255, 165, 0)")

    page.get_by_role("link", name=" Contact us").click()
    expect(page.get_by_text("Get In Touch")).to_be_visible()

    page.get_by_placeholder("Name").fill(fake_name)
    time.sleep(0.5)
    page.locator("input[data-qa='email']").fill(fake_email)
    time.sleep(0.5)
    page.get_by_placeholder("Subject").fill(fake_text)
    time.sleep(0.5)
    page.get_by_placeholder("Your Message Here").fill(fake_text)
    time.sleep(0.5)

    # Upload file (example: stored inside 'tests/files/sample.txt')
    page.set_input_files("input[name='upload_file']", "/Users/yuliyacherniienko/PycharmProjects/RedRover 2025/Automationexercise/tests/upload_sample.txt")

    # Handle popup alert
    page.once("dialog", lambda dialog: dialog.accept())

    page.locator("input[data-qa='submit-button']").click(force=True)

    expect(page.get_by_text("Success! Your details have been submitted successfully.").first).to_be_visible(timeout=10000)

    # expect(page.locator("div.status.alert.alert-success")).to_have_text("Success! Your details have been submitted successfully.")


def test_7_verify_test_cases_page(page):

    page.goto("https://automationexercise.com/")
    expect(page.get_by_role("link", name="Home")).to_have_css("color", "rgb(255, 165, 0)")
    page.get_by_role("link", name="Test Cases").first.click()
    expect(page).to_have_url("https://automationexercise.com/test_cases")
    # Verify the main header text (in <b> tag)
    expect(page.locator("b", has_text="Test Cases")).to_be_visible()



def test_8_verify_products_and_product_detail_page(page):

    page.goto("https://automationexercise.com/")
    expect(page.get_by_role("link", name="Home")).to_have_css("color", "rgb(255, 165, 0)")

    page.get_by_role("link", name=" Products").first.click()
    expect(page).to_have_url("https://automationexercise.com/products")
    expect(page.get_by_text("All Products")).to_be_visible()
    products_count = page.locator(".features_items .single-products").count()
    assert products_count >= 1

    page.get_by_role("link", name=" View Product").first.click()
    expect(page).to_have_url("https://automationexercise.com/product_details/1")
    product_information_code = page.locator(".product-details .product-information")
    expect(product_information_code.locator("> h2")).to_be_visible()
    product_name = product_information_code.locator("> h2").inner_text()
    assert product_name.strip() !=""
    assert len(product_name.strip()) > 0
    product_info = product_information_code.locator("> p")
    product_category = product_info.first
    print(product_category)

    expect(product_category).to_be_visible()
    expect(product_category).to_contain_text("Category:")
    product_availability = product_info.nth(1)
    expect(product_availability).to_be_visible()
    expect(product_availability).to_contain_text("Availability:")

    product_condition = product_info.nth(2)
    expect(product_condition).to_be_visible()
    expect(product_condition).to_contain_text("Condition:")

    product_brand = product_info.last
    expect(product_brand).to_be_visible()
    expect(product_brand).to_contain_text("Brand:")


    expect(product_information_code.locator("> span > span")).to_be_visible()
    expect(product_information_code.locator("> span > span")).to_contain_text("Rs.")

    # expect(page.get_by_text("Availability:")).to_be_visible()
    # expect(page.get_by_text("Condition:")).to_be_visible()
    # expect(page.get_by_text("Brand:")).to_be_visible()

# правильно ли это прописывать видимость цены в таком формате - "Rs. 500", она может поменять


def test_9_search_product(page):

    page.goto("https://automationexercise.com/")
    expect(page.get_by_role("link", name="Home")).to_have_css("color", "rgb(255, 165, 0)")

    page.get_by_role("link", name=" Products").first.click()
    expect(page).to_have_url("https://automationexercise.com/products")
    expect(page.get_by_text("All Products")).to_be_visible()

    page.get_by_placeholder("Search Product").fill("Blue Top")
    page.locator("#submit_search").click()
    expect(page.get_by_text("Searched Products")).to_be_visible()
    # expect(page.locator(".product-image-wrapper").first).to_be_visible()
    expect(page.locator(".productinfo p", has_text="Blue Top")).to_be_visible()


def test_10_verify_subscription_in_home_page(page):

    page.goto("https://automationexercise.com/")
    expect(page.get_by_role("link", name="Home")).to_have_css("color", "rgb(255, 165, 0)")








