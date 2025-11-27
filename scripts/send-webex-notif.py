#!/usr/bin/env python3
import requests
import sys
import os

WEBEX_TOKEN = os.getenv('WEBEX_BOT_TOKEN')
ROOM_ID = os.getenv('WEBEX_ROOM_ID')

def send_msg(employee_name, action, jira_ticket, manager_email):
	# Send Webex Notification
	headers = {
		"Authorization": f"Bearer {WEBEX_TOKEN}",
		"Content-Type": "application/json"
	}

	# Create msg
	if action == "onboard":
		emoji = "🎉"
		status = " Successfully onboarded!"
	else:
		emoji = "👋"
		status = "Successfully offboarded!"

	msg = f"""
		{emoji} **Employee {action.capitalize()}**
		**Name:** {employee_name}
		**Action:** {action}
		**Jira Ticket:** {jira_ticket}
		**Manager:** {manager_email}
		✅ Automation completed successfully!
	"""

	data = {
		"roomId": ROOM_ID,
		"markdown": msg
	}

	response = requests.post(
		"https://webexapis.com/v1/messages",
		headers=headers,
		json=data
	)

	if response.status_code == 200:
		print(f"✅ Webex notification sent successfully!")
	else:
		print(f"❌ Error sending Webex notification: {response.status_code}", file=sys.stderr")
		print(response.text, file=sys.stderr)
		sys.exit(1)

if __name__ == "__main__":
	if len(sys.argv) != 5:
		print("Usage: send-webex-notif.py <employee_name> <action> <jira_ticket> <manager_email>")
		sys.exit(1)

	employee_name = sys.argv[1]
	action = sys.argv[2]
	jira_ticket = sys.argv[3]
	manager_email = sys.argv[4]

	send_msg(employee_name, action, jira_ticket, manager_email)
