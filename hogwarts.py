from pymongo import MongoClient
from pprint import pprint
from bson import ObjectId

def connect():
    CONNECTION_STRING = "mongodb://localhost:27017"
    client = MongoClient(CONNECTION_STRING)
    return client['Project3']

if __name__ == "__main__":
    db = connect()

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
    emp_FN = input("Employee FIRST name: ")
    employee_search = [      
        {
            "$match": {
                "firstName": emp_FN
            }
        },
        {
            "$project":{
                "name" : {"$concat" : ["$firstName", " ", "$lastName"]},
                "wage" :1,
                "sessions":1
            }
        }
        
    ]
    # Run the pipeline.
    results = db['employees'].aggregate(employee_search)


    for employee in results:
        print(f"\nName: {employee['name']}   ID:{employee['_id']}\nWage: {employee['wage']}\nSessions Worked: ")
        for session in employee['sessions']:
            print(f"title: {session.get('sessionTitle','None')}")
            print(f"camp name: {session.get('campName','None')}")
            unit_name = session.get('unitName')
            if unit_name is not None:
                print(f"unit name: {session.get('unitName')}")

    



def session_schedule_summary():
    session_id = input("Enter the ID of the session: ")
    activity_name = input("Enter the name of an activity: \n")

    rotation_search=[
        {
            "$match":{
                "sessionId":ObjectId(session_id)
            }
        },
        {
            "$unwind":{
                "path":"$schedule"
            }
        },
        {
            "$match":{
                "schedule.activityName":activity_name
            }
        },
        {
            "$project":{
                "title":1,
                "staffCampName": "$schedule.staffCampName",
                "unitName": "$schedule.unitName"
            }
        }
    ]
    results = db['rotations'].aggregate(rotation_search)


    for rotation in results:
        print(f"Rotation Title: {rotation['title']}\n Staff Supervisor: {rotation['staffCampName']}\n Attending Unit: {rotation['unitName']}\n")



def unit_report():
    unit_name = input("Enter the name of the unit: ")
    session_name = input("Enter the name of the session: ")
    unit_total_mins = [
        {
            "$match":{
                "title":session_name
            }
        },
        {
            "$unwind":{
                "path":"$units"
            }
        },
        {
            "$lookup":{
                "from": "rotations",
                "localField": "units._id",
                "foreignField": "schedule.unitId",
                "as": "unitSessions"
            }
        },
        {
            "$unwind":{
                "path":"$unitSessions"
            }
        },
        {
            "$unwind":{
                "path": "$unitSessions.schedule"
            }
        },
        {
            "$match":{
                "unitSessions.schedule.unitName":unit_name
            }
        },
        {
            "$project":{
                "activityName":"$unitSessions.schedule.activityName",
                "duration":{
                    "$dateDiff": {
                    "startDate": "$unitSessions.startTime",
                    "endDate": "$unitSessions.endTime",
                    "unit": "minute"
                    }
                }
            }
        },
        {
            "$group":{
                "_id": "$activityName",
                "totalDuration": {
                    "$sum": "$duration"
                }
            }
        }
    ]

    results = db['sessions'].aggregate(unit_total_mins)
    print("Unit name: ", unit_name)

    for activity in results:
        pprint(f"Activity Name: {activity['_id']}  Total Minutes: {activity['totalDuration']}")
        
main_menu()