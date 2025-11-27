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

		# Check workspace container and update status
		if docker_container_exists(container_name):
			employee["status"] = "ONBOARDED"
			employee["action"] = "NONE"
		else:
			employee["status"] = "NONE"

		# If start_date is withinn 1 week , update action to onboard
		if within_one_week(start_date):
			employee["action"] = "ONBOARD"
		else:
			employee["action"] = "NONE"

		# If end_date is today, update action to offboard
		if is_today(end_date):
			employee["action"] = "OFFBOARD"

		# Save updates
		data["employee"] = employee
		save_yaml(path, data)

		print(f"[UPDATED] {filename}: status={employee.get('status')}, action={employee.get('action')}")

if __name__ == "__main__":
	main()
