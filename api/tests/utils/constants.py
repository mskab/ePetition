USER_TEST_DATA = {
    "firstname": "testfirstname", "lastname": "testlastname",
    "email": "testemail@email.com", "password": "testing"
}

ADMIN_TEST_DATA = {
    "firstname": "admin", "lastname": "admin",
    "email": "admin@admin.com", "password": "admin123"
}

DECISION_MAKER_TEST_DATA = {
    "naming": "decision_maker", "affiliation": "affiliation",
    "email": "decision_maker@dmaker.com"
}

COMPLAINT_TEST_DATA = {
    "abuse": "Misleading or spam",
    "description": "description",
}

PETITION_TEST_DATA = {
    "title": "title",
    "description": "description",
    "country": "Country",
    "due_date": "2001-01-01",
    "signed_goal": 1,
}

AUTH_ERRORS = {
    "password_not_mutch_email": "Password does not match the email provided",
    "email_not_exist": "Email does not exist",
    "account_inactive": "Account is inactive"
}

USER_MESSAGES = {
    "user_already_exist": "User already exists",
    "403": "Forbidden",
    "user_not_found_with_id": "User not found with the given ID",
    "user_deleted": "User deleted successfully"
}

DECISION_MAKER_MESSAGES = {
   "already_exist": "Decision maker already exists",
   "deleted": "Decision maker deleted successfully",
   "not_found": "Decision maker not found with the given ID"
}
