#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 22:34:31 2024

@author: jakobfick
"""

# database_handler.py
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta

class ManagerDatabase:
    def __init__(self, host, user, password, database):
        self.connection = None
        self.employeeID = None
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
            return None, 1
    
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
                return None, 2
    
            # Prepare the dictionary for employee and manager (superior) info
            employee_data = {
                "Employee": {
                    "EmployeeID": employee_result["EmployeeID"],
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
    
            return employee_data, 0
    
        except Error as e:
            print(f"Error executing query: {e}")
            return None, 1
    
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


    def add_employee_to_database(self, employee_data):
        if self.connection is None:
            print("No database connection.")
            return None
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            # Retrieve the highest existing EmployeeID and calculate the next ID
            cursor.execute("SELECT MAX(EmployeeID) FROM Employees")
            result = cursor.fetchone()
            print(result)
            next_employee_id = (result['MAX(EmployeeID)'] or 0) + 1  # If result is None, start from 1
    
            # Extract the data from the employee_data dictionary
            first_name = employee_data['FirstName']
            last_name = employee_data['LastName']
            email = employee_data['Email']  # Updated field name
            password = employee_data['Password']
            position = employee_data['Position']
            # Get the ID of the newly inserted employee
            #employee_id = cursor.lastrowid
        
            # Extract manager data
            manager = employee_data.get('Manager')
            manager_id = manager['EmployeeID'] if manager else None
        
            # Insert the new employee into the Employees table
            insert_employee_query = '''
                INSERT INTO Employees (EmployeeID, FirstName, LastName, Email, Password, Position, ManagerID)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(insert_employee_query, (next_employee_id, first_name, last_name, email, password, position, manager_id))
            #connection.commit()
            
            # Update each subordinate's ManagerID to the new employee's ID
            update_subordinate_query = "UPDATE Employees SET ManagerID = %s WHERE EmployeeID = %s"
            for subordinate in employee_data['Subordinates']:
                cursor.execute(update_subordinate_query, (
                    next_employee_id,
                    subordinate['EmployeeID']
                ))
                
            self.connection.commit()
                
        except Error as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            cursor.close()
            
            
    #This method is used to remove the chosen employee from the database
    def remove_employee_from_database(self, employeeID):
        print(employeeID)
        # Establish database connection
        if self.connection is None:
            print("No database connection.")
            return None
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            # Delete all events associated with the employee
            delete_events_query = "DELETE FROM Events WHERE EmployeeID = %s"
            cursor.execute(delete_events_query, (employeeID,))
            
            # Set ManagerID to NULL for any employees managed by the chosen employee
            update_manager_query = "UPDATE Employees SET ManagerID = NULL WHERE ManagerID = %s"
            cursor.execute(update_manager_query, (employeeID,))
    
            # Delete the employee from the Employees table
            delete_employee_query = "DELETE FROM Employees WHERE EmployeeID = %s"
            cursor.execute(delete_employee_query, (employeeID,))
    
            # Commit the changes
            self.connection.commit()
            print(f"Employee with ID {employeeID} has been removed from the database.")
        
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.connection.rollback()  # Rollback if there was an error
    
        finally:
            cursor.close()
            #self.connection.close()
            


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
db = ManagerDatabase(host="localhost", user="root", password="Mu!642724", database="EmployeeDB")
db.validate_password("john.doe@example.com", "password123")
'''