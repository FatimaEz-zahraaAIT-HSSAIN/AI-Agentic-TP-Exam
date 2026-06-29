import json
from langchain_core.tools import tool

MOCK_EMPLOYEE_DB = {
    "emp_001": {"name": "Aicha", "department": "Engineering", "leave_balance": 14},
    "emp_002": {"name": "Ahmad", "department": "HR", "leave_balance": 2},
    "emp_003": {"name": "Sara", "department": "Engineering", "leave_balance": 0}
}

@tool
def get_leave_balance(identifier: str) -> str:
    """Fetches the leave balance data for an employee. Returns raw data including ID, name, and balance."""
    # Check by ID
    if identifier in MOCK_EMPLOYEE_DB:
        emp = MOCK_EMPLOYEE_DB[identifier].copy()
        emp["employee_id"] = identifier
        return json.dumps(emp)
    
    # Check by Name
    for emp_id, emp_data in MOCK_EMPLOYEE_DB.items():
        if identifier.lower() in emp_data["name"].lower():
            emp = emp_data.copy()
            emp["employee_id"] = emp_id
            return json.dumps(emp)
            
    return json.dumps({"error": f"No employee found matching '{identifier}'."})

@tool
def get_employee_details(identifier: str) -> str:
    """Fetches the profile data for an employee. Returns raw data including ID, name, and department."""
    # Check by ID
    if identifier in MOCK_EMPLOYEE_DB:
        emp = MOCK_EMPLOYEE_DB[identifier].copy()
        emp["employee_id"] = identifier
        return json.dumps(emp)
    
    # Check by Name
    for emp_id, emp_data in MOCK_EMPLOYEE_DB.items():
        if identifier.lower() in emp_data["name"].lower():
            emp = emp_data.copy()
            emp["employee_id"] = emp_id
            return json.dumps(emp)
            
    return json.dumps({"error": f"No employee found matching '{identifier}'."})