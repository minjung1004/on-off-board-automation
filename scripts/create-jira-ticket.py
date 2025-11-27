#!/usr/bin/env python3
import requests
import base64
import json
import sys
import os

# Get from env var passed by jenkins
JIRA_URL = os.getenv('JIRA_URL', 'https://on-off-board-automation.atlassian.net')
JIRA_EMAIL = os.getenv('JIRA_EMAIL', 'minjung10402@gmail.com')
JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')
PROJECT_KEY = os.getenv('JIRA_PROJECT', 'HR')

def create_ticket(employee_name, employee_email, action):
	# Create Jira ticket for onboarding/offboarding
	auth_string = f"{JIRA_EMAIL}:{JIRA_API_TOKEN}"
	auth_bytes = auth_string.encode('ascii')
	auth_base64 = base64.b64encode(auth_bytes).decode('ascii')

	headers = {
		"Authorized": f"Basic {auth_base64}",
		"Content-Type": "application/json"
	}
	
	# Create  ticket
	ticket_data = {
		"fields": {
			"project": {"key": PROJECT_KEY},
			"summary": f"{action.capitalize()}: {employee_name}",
			"description": {
				"type": "doc",
				"version": 1,
				"content": [
					{
						"type": "paragraph",
						"content": [
							{
								"type": "text",
								"text": f"Automation ticket for {action}ing {employee_name} ({employee_email})"
							}
						]
					}
				]
			},
			"issuetype": {"name": "Task"}
		}
	}
	
	response = requests.post(
		f"{JIRA_URL}/rest/api/3/issue",
		headers=headers,
		data=json.dumps(ticket_data)
	)

	if response.status_code == 201:
		ticket = response.json()
		ticket_key = ticket['key']
		print(f"JIRA_TICKET={ticket_key}")
		return ticket_key
	else:
		print(f"[ERROR]: {response.status_code}", file=sys.stderr)
		print(response.text, file=sys.stderr)
		sys.exit(1)

if __name__ == "__main__"
	if len(sys.argv) != 4:
		print("Usage: create-jira-ticket.py <employee_name> <employee_email> <action>")
		sys.exit(1)

	employee_name = sys.argv[1]
	employee_email = sys.argv[2]
	action = sys.argv[3]

	create_ticket(employee_name, employee_email, action)
