#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 10:17:40 2024

@author: jakobfick
"""

# database_handler.py
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta

class EmployeeDatabase:
    def __init__(self, host, user, password, database):
        self.connection = None
        self.employeeID = None
        self.MainEmployeeID = None
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
                self.update_days_table()  # Call the update method only if connected
        except Error as e:
            print(f"Error while connecting to the database: {e}")
            
            
    def validate_password(self, email, password):
        print(email)
        ID, db_password = self.get_employee_by_email(email)
        
        if ID is None:
            # Username not found
            return False, 1
        else:
            if password != db_password:
                # Password does not match
                return False, 2
            else:
                # Successful login, show welcome message with first and last name
                self.employeeID = ID
                self.MainEmployeeID = ID
                
                return True, 0
        

    def get_employee_by_email(self, email):
        """Retrieve employee details based on email."""
        if self.connection is None:
            print("No database connection.")
            return None, None
        
        try:
            cursor = self.connection.cursor()
            query = """
            SELECT EmployeeID, Password
            FROM Employees
            WHERE Email = %s
            """
            cursor.execute(query, (email,))
            result = cursor.fetchone()  # Fetch the first matching record

            if result:
                employee_id, password = result
                print("employee_id, password")
                print(employee_id)
                print(password)
                return employee_id, password
            
            else:
                print(f"No employee found with email: {email}")
                return None, None
        except Error as e:
            print(f"Error executing query: {e}")
            return None, None
        finally:
            cursor.close()
            

    def get_schedule_by_date(self, date):
        """Retrieve the schedule of events for an employee on a specific date and set the dateID."""
        if self.connection is None:
            print("No database connection.")
            return None

        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
            SELECT e.EventID, DATE_FORMAT(e.StartTime, '%H:%i') AS StartTime, DATE_FORMAT(e.EndTime, '%H:%i') AS EndTime, 
                   e.EventName, d.DayID
            FROM Events e
            JOIN Days d ON e.DayID = d.DayID
            WHERE e.EmployeeID = %s AND d.Date = %s
            """
            cursor.execute(query, (self.employeeID, date))
            result = cursor.fetchall()
            print(result)

            if result:
                # Get the DayID from the first result
                self.dateID = result[0]["DayID"]  # Assuming all events on the same date have the same DayID
                self.date = date
                print(date)

                # Convert the query result to a list of schedules
                schedule = [
                    {
                        "event_id": row["EventID"],
                        "start_time": str(row["StartTime"]),
                        "end_time": str(row["EndTime"]),
                        "event": row["EventName"],
                    }
                    for row in result
                ]
                return schedule
            else:
                print(f"No events found for employee ID {self.employeeID} on {date}")
                # Get the DayID from the first result
                self.dateID = None  # Assuming all events on the same date have the same DayID
                self.date = date
                print(date)
                return []
        except Error as e:
            print(f"Error executing query: {e}")
            return []
        finally:
            cursor.close()

            
    def add_event(self, event_name, event_date, start_time, end_time, description):
        """Adds a new event to the database for a given employee on a specified date.
        Checks for time conflicts before scheduling the event."""
        try:
            cursor = self.connection.cursor()
            print(start_time)
            print(type(start_time))

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
            cursor.execute(check_conflict, (self.employeeID, day_id, end_time, end_time, start_time, start_time, start_time, end_time))
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
            cursor.execute(insert_event, (self.employeeID, day_id, event_name, start_time, end_time, description))

            # Commit the transaction
            self.connection.commit()
            print("Event added successfully.")

        except Exception as e:
            print(f"An error occurred while adding the event: {e}")
            self.connection.rollback()  # Rollback in case of error

        finally:
            cursor.close()
            
            
    def get_next_day(self):
        return datetime.strptime(self.date, '%Y-%m-%d') + timedelta(days=1)
    
    
    def get_prev_day(self):
        return datetime.strptime(self.date, '%Y-%m-%d') - timedelta(days=1)
    
    
    def get_event_by_id(self, event_id):
        """Fetch event details, including event date and employee name, by event ID from the database."""
        if self.connection is None:
            print("No database connection.")
            return None
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
            SELECT e.EventName, DATE_FORMAT(e.StartTime, '%H:%i') AS StartTime, DATE_FORMAT(e.EndTime, '%H:%i') AS EndTime, e.Description,
                   DATE_FORMAT(d.Date, '%m-%d-%Y') AS EventDate, emp.FirstName, emp.LastName
            FROM Events e
            JOIN Days d ON e.DayID = d.DayID
            JOIN Employees emp ON e.EmployeeID = emp.EmployeeID
            WHERE e.EventID = %s
            """
            cursor.execute(query, (event_id,))
            result = cursor.fetchone()
            
            if result:
                return result
            else:
                print(f"No event found with ID {event_id}")
                return None
        except Error as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            cursor.close()
            
            
    def delete_event(self, event_id):
        print(event_id)
        """Delete an event from the database by event ID."""
        if self.connection is None:
            print("No database connection.")
            return False

        try:
            cursor = self.connection.cursor()
            delete_query = "DELETE FROM Events WHERE EventID = %s"
            cursor.execute(delete_query, (event_id,))
            self.connection.commit()  # Commit the changes
            print(f"Event with ID {event_id} deleted successfully.")
            return True
        except Error as e:
            print(f"Error deleting event: {e}")
            return False
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
        


    def update_days_table(self):
        if self.connection is None or not self.connection.is_connected():
            print("Not connected to the database.")
            return

        cursor = None
        try:
            cursor = self.connection.cursor()

            # Current date, 6 months in the past, and 1 year in the future
            today = datetime.today().date()
            past_date = today - timedelta(days=180)  # 6 months back
            future_date = today + timedelta(days=365)  # 1 year forward

            # Remove outdated days
            delete_query = "DELETE FROM Days WHERE Date < %s"
            cursor.execute(delete_query, (past_date,))
            self.connection.commit()
            print(f"Outdated 'Day' records older than {past_date} have been deleted.")

            # Insert new days
            current_date = past_date
            while current_date <= future_date:
                # Check if the day already exists
                check_query = "SELECT DayID FROM Days WHERE Date = %s"
                cursor.execute(check_query, (current_date,))
                result = cursor.fetchone()

                # Insert if the day does not exist
                if not result:
                    insert_query = "INSERT INTO Days (Date) VALUES (%s)"
                    cursor.execute(insert_query, (current_date,))
                    print(f"Inserted {current_date} into Days table.")
                
                current_date += timedelta(days=1)  # Move to the next day

            self.connection.commit()
            print("Days table has been updated with new dates.")
        except Error as e:
            print(f"Error while updating Days table: {e}")
        finally:
            if cursor is not None:
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
db = EmployeeDatabase(host="localhost", user="root", password="Mu1642724", database="EmployeeDB")
db.validate_password("john.doe@example.com", "password123")
db.get_schedule_by_date(datetime.now().strftime('%Y-%m-%d'))
'''
