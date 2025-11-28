#!/usr/bin/env python3

import os
import yaml
import subprocess
from datetime import datetime, timedelta

EMPLOYEE_DIR = "employees"

# YAML Helper
def load_yaml(path):
	with open(path, 'r') as f:
		return yaml.safe_load(f)

def save_yaml(path,data):
	with open(path, 'w') as f:
		yaml.dump(data, f, sort_keys=False)

# Docker Helpers
def docker_container_exists(name):
	result = subprocess.run(
		["docker", "ps", "-a", "-q", "--filter", f"name=^{name}$"],
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE,
		text=True
	)

	return result.stdout.strip() != ""

# Date Helpers
def within_one_week(date_str):
	# Return True if date is within +/- 7 days from today
	if not date_str:
		return False
	try:
		date = datetime.strptime(date_str, "%Y-%m-%d")
	except ValueError:
		return False

	return abs((datetime.today() - date).days) <= 7

def is_today(date_str):
	# Return True if date matches today's date
	if not date_str:
		return False
	try:
		date = datetime.strptime(date_str, "%Y-%m-%d")
	except ValueError:
		return False

	return date.date() == datetime.today().date()

def is_past(date_str):
    if not date_str:
        return False
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return False
    return date.date() < datetime.today().date()

# Change name to container format
def format_container_name(employee_name):
	return f"workspace-{employee_name.lower().replace(' ', '-')}"

# Main Logic
def main():
	for filename in os.listdir(EMPLOYEE_DIR):
		if not filename.endswith(".yml"):
			continue

		path = os.path.join(EMPLOYEE_DIR, filename)
		data = load_yaml(path)
		employee = data.get("employee", {})

		name = employee.get("name", "")
		start_date = employee.get("start_date")
		end_date = employee.get("end_date")

		# Build container name
		container_name = format_container_name(name)
		container_exists = docker_container_exists(container_name)

		# Default
		status = "NONE"
		action = "NONE"

		# Past end date -> OFFBOARDED
		if is_past(end_date):
				status = "OFFBOARDED"
				action = "NONE"

		# End date is today -> OFFBOARD
		elif is_today(end_date):
				status = "ONBOARDED" if container_exists else "NONE"
				action = "OFFBOARD"

		# start date within a week -> ONBAORD
		elif within_one_week(start_date) and not container_exists:
				status = "NONE"
				action = "ONBOARD"

		# Container exists -> ONBOARDED
		elif container_exists:
			status = "ONBOARDED"
			action = "NONE"
			
		# Update YAML
		employee["status"] = status
		employee["action"] = action
		save_yaml(path, data)

		print(f"[UPDATED] {filename}: status={employee.get('status')}, action={employee.get('action')}")

if __name__ == "__main__":
	main()
