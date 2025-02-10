#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 14:01:50 2024

@author: jakobfick
"""

# database_handler.py
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta

class CustomerDatabase:
    def __init__(self, host, user, password, database):
        self.connection = None
        #self.employeeID = None
        self.dateID = None
        self.date = None
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            if self.connection.is_connected():
                print("Connected to the database")
                #self.update_days_table()  # Call the update method only if connected
        except Error as e:
            print(f"Error while connecting to the database: {e}")
            
    
    def get_available_slots(self, employee_id, date):
        '''
        # Establish the connection to the database
        connection = mysql.connector.connect(
            host="localhost",
            user="your_username",
            password="your_password",
            database="EmployeeDB"
        )
        '''
        try:
            cursor = self.connection.cursor()
            
            # Query to get the events for the employee on the specified date
            query = """
            SELECT DATE_FORMAT(e.StartTime, '%H:%i') AS StartTime, DATE_FORMAT(e.EndTime, '%H:%i') AS EndTime
            FROM Events e
            JOIN Days d ON e.DayID = d.DayID
            WHERE e.EmployeeID = %s AND d.Date = %s
            """
            cursor.execute(query, (employee_id, date))
            
            # Store events' start and end times in a list
            events = [(row[0], row[1]) for row in cursor.fetchall()]
            #print(events)
            
            # Define the time range of the workday (e.g., 8:00 AM to 5:00 PM)
            start_of_day = datetime.strptime("08:00", "%H:%M").time()
            end_of_day = datetime.strptime("17:00", "%H:%M").time()
            
            # List to store available 1-hour time slots
            available_slots = []
    
            # Iterate over 30-minute intervals within the workday range
            current_time = start_of_day
            #print(type(current_time))
            print(date)
            print(type(date))
            
            while (datetime.combine(date, current_time) + timedelta(hours=1)).time() <= end_of_day:
                # Define a 1-hour slot
                next_hour = (datetime.combine(date, current_time) + timedelta(hours=1)).time()
                
                # Check if the slot overlaps with any existing events
                is_free = True
                for start, end in events:
                    startTime = datetime.strptime(start, "%H:%M").time()
                    endTime = datetime.strptime(end, "%H:%M").time()
                    # Check if the slot is within an event's duration
                    if (current_time < endTime and next_hour > startTime):
                        is_free = False
                        break
                
                # If the slot is free, add it to the available_slots list
                if is_free:
                    slot = f"{datetime.combine(date, current_time).strftime('%I:%M %p')} - {datetime.combine(date, next_hour).strftime('%I:%M %p')}"
                    available_slots.append(slot)
                
                # Move to the next 30-minute interval
                current_time = (datetime.combine(date, current_time) + timedelta(minutes=30)).time()
            
            return available_slots
    
        except mysql.connector.Error as error:
            print(f"Database error: {error}")
            return []
        
        finally:
            cursor.close()
            #self.connection.close()
            
            
    def get_company_representatives(self):
        """Retrieve the EmployeeID, FirstName, and LastName of all employees with the position 'Company Representative'."""
        try:
            cursor = self.connection.cursor()
            query = """
            SELECT EmployeeID, FirstName, LastName
            FROM Employees
            WHERE Position = 'Company Representative'
            """
            cursor.execute(query)
            
            # Fetch all results
            representatives = cursor.fetchall()
            
            # Format results as a list of dictionaries
            result = [{"EmployeeID": emp_id, "FirstName": first_name, "LastName": last_name} 
                      for emp_id, first_name, last_name in representatives]
            
            return result
        
        except Error as e:
            print(f"Error executing query: {e}")
            return None
        
        finally:
            cursor.close()
            
            
    def find_meeting_times(self, date):
        representatives = self.get_company_representatives()
        for rep in representatives:
            available_slots = self.get_available_slots(rep.get("EmployeeID"), date)
            rep.update({"Slots": available_slots})
        return representatives
    
    
    def add_event(self, employeeID, event_name, event_date, start_time, end_time, description):
        """Adds a new event to the database for a given employee on a specified date.
        Checks for time conflicts before scheduling the event."""
        try:
            cursor = self.connection.cursor()

            # First, check if the date exists in the Days table, if not insert it
            query_day = "SELECT DayID FROM Days WHERE Date = %s"
            cursor.execute(query_day, (event_date,))
            result = cursor.fetchone()

            if result:
                day_id = result[0]  # DayID already exists
            else:
                # Insert new day if it doesn't exist
                insert_day = "INSERT INTO Days (Date) VALUES (%s)"
                cursor.execute(insert_day, (event_date,))
                day_id = cursor.lastrowid  # Get the newly created DayID

            # Check for conflicting events on the same day for the employee
            check_conflict = """
            SELECT EventID, StartTime, EndTime FROM Events 
            WHERE EmployeeID = %s AND DayID = %s AND (
                (StartTime < %s AND EndTime > %s) OR  -- New event starts during another event
                (StartTime < %s AND EndTime > %s) OR  -- New event ends during another event
                (StartTime >= %s AND EndTime <= %s)   -- New event completely overlaps another event
            )
            """
            cursor.execute(check_conflict, (employeeID, day_id, end_time, end_time, start_time, start_time, start_time, end_time))
            conflict = cursor.fetchone()

            if conflict:
                conflict_id, conflict_start, conflict_end = conflict
                print(f"Error: Event conflicts with an existing event (ID {conflict_id}) "
                      f"from {conflict_start} to {conflict_end}.")
                return  # Stop if a conflict is found

            # No conflicts, proceed to insert the event
            insert_event = """
            INSERT INTO Events (EmployeeID, DayID, EventName, StartTime, EndTime, Description)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_event, (employeeID, day_id, event_name, start_time, end_time, description))

            # Commit the transaction
            self.connection.commit()
            print("Event added successfully.")
            return True

        except Exception as e:
            print(f"An error occurred while adding the event: {e}")
            self.connection.rollback()  # Rollback in case of error
            return False

        finally:
            cursor.close()
    
            
    '''            
    def validate_password(self, email, password):
        print(email)
        ID, db_password, position = self.get_employee_by_email(email)
        
        if ID is None:
            # Username not found
            return False
        else:
            if password != db_password:
                # Password does not match
                return False
            else:
                if position == "System Manager":
                    # Successful login, show welcome message with first and last name
                    self.employeeID = ID
                    
                    return True
                else:
                    return False
        

    def get_employee_by_email(self, email):
        """Retrieve employee details based on email."""
        if self.connection is None:
            print("No database connection.")
            return None, None, None  # Return three None values for ID, password, and position
    
        try:
            cursor = self.connection.cursor()
            query = """
            SELECT EmployeeID, Password, Position
            FROM Employees
            WHERE Email = %s
            """
            cursor.execute(query, (email,))
            result = cursor.fetchone()  # Fetch the first matching record
    
            if result:
                employee_id, password, position = result
                return employee_id, password, position  # Return employee details
                
            else:
                print(f"No employee found with email: {email}")
                return None, None, None  # Return three None values if no record is found
        except Error as e:
            print(f"Error executing query: {e}")
            return None, None, None  # Return three None values if an error occurs
        finally:
            cursor.close()
            
    
    def get_subordinates(self):
        """Retrieve the first name, last name, and employee ID of all subordinates of a given manager."""
        if self.connection is None:
            print("No database connection.")
            return None
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
            SELECT e2.EmployeeID, e2.FirstName, e2.LastName
            FROM Employees e1
            JOIN Employees e2 ON e1.EmployeeID = e2.ManagerID
            WHERE e1.EmployeeID = %s
            """
            cursor.execute(query, (self.MainEmployeeID,))
            result = cursor.fetchall()
            
            if result:
                subordinates = [
                    {
                        "employee_id": row["EmployeeID"],
                        "first_name": row["FirstName"],
                        "last_name": row["LastName"]
                    }
                    for row in result
                ]
                return subordinates
            else:
                print(f"No subordinates found for manager with EmployeeID {self.MainEmployeeID}")
                return []
        except Error as e:
            print(f"Error executing query: {e}")
            return []
        finally:
            cursor.close()
            
    
    def set_subordinate_ID(self, ID):
        self.employeeID = ID
        
    def reset_employee_ID(self):
        self.employeeID = self.MainEmployeeID     
    
    def get_employee_hierarchy(self, email):
        """Retrieve employee details, their superior's details, and subordinates' details."""
        if self.connection is None:
            print("No database connection.")
            return None
    
        try:
            cursor = self.connection.cursor(dictionary=True)
    
            # 1. Retrieve employee details
            query_employee = """
            SELECT e.EmployeeID, e.FirstName, e.LastName, e.Email AS Username, e.Password, e.Position,
                   m.FirstName AS ManagerFirstName, m.LastName AS ManagerLastName, m.Email AS ManagerUsername, m.Position AS ManagerPosition
            FROM Employees e
            LEFT JOIN Employees m ON e.ManagerID = m.EmployeeID
            WHERE e.Email = %s
            """
            cursor.execute(query_employee, (email,))
            employee_result = cursor.fetchone()
    
            if not employee_result:
                print(f"No employee found with email: {email}")
                return None
    
            # Prepare the dictionary for employee and manager (superior) info
            employee_data = {
                "Employee": {
                    "FirstName": employee_result["FirstName"],
                    "LastName": employee_result["LastName"],
                    "Username": employee_result["Username"],
                    "Password": employee_result["Password"],
                    "Position": employee_result["Position"]
                },
                "Manager": None,
                "Subordinates": []
            }
    
            if employee_result["ManagerFirstName"]:
                employee_data["Manager"] = {
                    "FirstName": employee_result["ManagerFirstName"],
                    "LastName": employee_result["ManagerLastName"],
                    "Username": employee_result["ManagerUsername"],
                    "Position": employee_result["ManagerPosition"]
                }
    
            # 2. Retrieve subordinates (direct reports) details
            query_subordinates = """
            SELECT FirstName, LastName, Email AS Username, Position
            FROM Employees
            WHERE ManagerID = %s
            """
            cursor.execute(query_subordinates, (employee_result["EmployeeID"],))
            subordinates_result = cursor.fetchall()
    
            # Add subordinates as a list of dictionaries
            if subordinates_result:
                employee_data["Subordinates"] = [
                    {
                        "FirstName": sub["FirstName"],
                        "LastName": sub["LastName"],
                        "Username": sub["Username"],
                        "Position": sub["Position"]
                    }
                    for sub in subordinates_result
                ]
    
            return employee_data
    
        except Error as e:
            print(f"Error executing query: {e}")
            return None
    
        finally:
            cursor.close()
            
    #When searching for information about an employees   
    def get_employee_info(self, email):
        """Retrieve employee's ID, first name, last name, email, and position based on their email."""
        if self.connection is None:
            print("No database connection.")
            return None
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
            SELECT EmployeeID, FirstName, LastName, Email, Position
            FROM Employees
            WHERE Email = %s
            """
            cursor.execute(query, (email,))
            result = cursor.fetchone()

            if result:
                return result  # This will return a dictionary with employee details
            else:
                print(f"No employee found with email: {email}")
                return None
        except Error as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            cursor.close()


    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")
            
            
    def logout(self):
        self.employeeID = None
        self.MainEmployeeID = None
        self.dateID = None
        self.date = None
    '''
            
'''     
db = CustomerDatabase(host="localhost", user="root", password="Mu!642724", database="EmployeeDB")
employee_id = 162455
date = datetime.strptime("2024-09-12", "%Y-%m-%d").date()
available_slots = db.get_available_slots(employee_id, date)
#print("Available 1-hour slots:", available_slots)
representatives = db.get_company_representatives();
slots = db.find_meeting_times(date)
print(slots)
'''