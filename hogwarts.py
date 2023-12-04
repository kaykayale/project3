from pymongo import MongoClient

def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. Employee Lookup")
        print("2. Session Schedule Summary")
        print("3. Unit Report")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            employee_lookup()
        elif choice == '2':
            session_schedule_summary()
        elif choice == '3':
            unit_report()
        elif choice == '4':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

def employee_lookup():
    employee_name = input("Enter the name of the employee: ")
    # Assuming the employee's full name is stored in a field 'fullName'
    result = db.employees.find_one({"firstName": employee_name}, {"_id": 1, "firstName": 1, "wage": 1, "sessions": 1})

    if result:
        print(f"ID: {result['_id']}, Name: {result['firstName']}, Wage: {result['wage']}")
        for session in result['sessions']:
            # Retrieve session details
            session_details = db.sessions.find_one({"_id": session['sessionId']})
            print(f"Session Title: {session_details['title']}, Staff Name: {session['campName']}")
            # Add logic to print unit name if assigned
    else:
        print("Employee not found.")
    # Implement the logic to retrieve employee data
    # ...

def session_schedule_summary():
    session_id = input("Enter the ID of the session: ")
    activity_name = input("Enter the name of an activity: ")
    # Implement the logic to retrieve session schedule summary
    # ...

def unit_report():
    unit_name = input("Enter the name of the unit: ")
    session_name = input("Enter the name of the session: ")
    # Implement the logic to retrieve unit report
    # ...

def connect():
    CONNECTION_STRING = "mongodb://localhost:27017"
    client = MongoClient(CONNECTION_STRING)
    return client['project3']

if __name__ == "__main__":
    db = connect()
