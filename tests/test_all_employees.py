import os
import glob
import yaml
import re

REQUIRED_FIELDS = [
    "name",
    "email",
    "role",
    "team",
    "manager",
    "start_date",
    "end_date",
    "status",
    "action",
]

def get_employee_files():
    # grabs every .yml file inside employees/
    return glob.glob(os.path.join("employees", "*.yml"))

def load_employee(path):
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    assert "employee" in data, f"{path}: top-level 'employee' key missing"
    return data["employee"]

def test_all_employee_files_have_required_fields():
    for path in get_employee_files():
        emp = load_employee(path)
        for field in REQUIRED_FIELDS:
            assert field in emp, f"{path}: missing field '{field}'"

def test_required_fields_not_empty():
    non_empty_fields = ["name", "email", "role", "team", "manager", "start_date"]
    for path in get_employee_files():
        emp = load_employee(path)
        for field in non_empty_fields:
            assert emp[field] not in (None, ""), f"{path}: '{field}' is empty"

def test_all_employee_emails_are_valid():
    for path in get_employee_files():
        emp = load_employee(path)
        email = emp["email"]
        assert re.match(r"[^@]+@[^@]+\.[^@]+", email), f"{path}: invalid email '{email}'" 