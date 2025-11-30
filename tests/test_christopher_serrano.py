import yaml
import re

def test_employee_yaml_format():
    with open("employees/christopher_serrano.yml", "r") as f:
        data = yaml.safe_load(f)

    assert "employee" in data

    emp = data["employee"]

    required = [
        "name",
        "email",
        "role",
        "team",
        "manager",
        "start_date",
        "end_date",
        "status",
        "action"
    ]

    for key in required:
        assert key in emp, f"Missing field: {key}"

    # These fields must NOT be empty
    assert emp["name"] != ""
    assert emp["email"] != ""
    assert emp["role"] != ""
    assert emp["team"] != ""
    assert emp["manager"] != ""
    assert emp["start_date"] != ""

def test_email_format():
    with open("employees/christopher_serrano.yml", "r") as f:
        data = yaml.safe_load(f)

    email = data["employee"]["email"]
    assert re.match(r"[^@]+@[^@]+\.[^@]+", email) 