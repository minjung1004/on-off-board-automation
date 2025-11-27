# On-Off-Board Automation

## 📌 Overview

This project automates the **onboarding and offboarding** process for employees using an integrated DevOps workflow.  
Instead of manually provisioning environments, tracking tasks, or sending updates, the system allows HR or IT to simply **add or modify an employee YAML file** in the `employees/` folder.

A Jenkins pipeline automatically detects the file change and triggers:

- Creating or removing a **Docker workspace** for the employee  
- Updating the employee’s status  
- Creating or updating **Jira tickets** (To Do → In Progress → Done)  
- Sending notifications through a **Webex bot**  
- Running validation scripts and cleanup tasks  

This demonstrates real-world DevOps automation, CI/CD, and API integration.

---

## 🧩 Technologies Used

### **GitHub**
- Stores all employee YAML files  
- Hosts the automation scripts  
- Triggers Jenkins via webhook on each commit  

### **Jenkins**
- Orchestrates onboarding/offboarding  
- Detects changes in `employees/` directory  
- Runs Dockerized automation steps  
- Provides build logs and status outputs  

### **Docker**
- Runs Python scripts inside a consistent environment  
- Creates a **workspace container** per employee  
- Deletes the workspace during offboarding  
- Ensures reproducible execution  

### **Python Scripts**
Located in `scripts/`, they handle:
- Parsing & validating employee YAML  
- Creating / updating Jira tickets  
- Sending Webex notifications  
- Updating employee status fields  
- Running onboarding/offboarding logic  

### **Jira (Cloud API)**
- Creates onboarding/offboarding tickets  
- Automates workflow transitions  
- Provides tracking visibility for IT/HR  

### **Webex Bot**
- Sends messages for:
  - Onboarding started  
  - Workspace created  
  - Jira ticket created  
  - Offboarding complete  
  - Pipeline errors  
- Keeps teams updated in real time  

---

## 📁 Repository Structure
on-off-board-automation/
│
├── ansible/ # (Optional – for future enhancements)
│
├── docker/
│ └── Dockerfile # Build environment for scripts
│
├── employees/ # Employee YAML files (pipeline triggers)
│ ├── bob_dylan.yml
│ ├── jane_doe.yml
│ ├── jenny_kim.yml
│ ├── john_smith.yml
│ └── christopher_serrano.yml <-- Your file goes here
│
├── jenkins/
│ └── Jenkinsfile # Main pipeline automation
│
├── scripts/
│ ├── update_employees.py # Core onboarding/offboarding logic
│ ├── jira_integration.py # Jira API handling
│ └── webex_notify.py # Webex bot notifications
│
├── tests/
│ └── test_employee_data.py # YAML validation tests
│
└── .gitignore

