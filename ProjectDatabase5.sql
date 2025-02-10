-- Drop and create the database
DROP DATABASE IF EXISTS EmployeeDB;
CREATE DATABASE EmployeeDB;
USE EmployeeDB;

-- Create Employees table
CREATE TABLE Employees (
    EmployeeID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Email VARCHAR(100),
    Password VARCHAR(100),
    Position VARCHAR(50),
    ManagerID INT,
    FOREIGN KEY (ManagerID) REFERENCES Employees(EmployeeID)
);

-- Create Days table
CREATE TABLE Days (
    DayID INT AUTO_INCREMENT PRIMARY KEY,
    Date DATE
);

-- Create Events table
CREATE TABLE Events (
    EventID INT AUTO_INCREMENT PRIMARY KEY,
    EmployeeID INT,
    DayID INT,
    EventName VARCHAR(100),
    StartTime TIME,
    EndTime TIME,
    Description TEXT,
    FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID),
    FOREIGN KEY (DayID) REFERENCES Days(DayID)
);

-- Insert Employee Objects into the database
INSERT INTO Employees (EmployeeID, FirstName, LastName, Email, Password, Position, ManagerID) VALUES (162455, 'John', 'Doe', 'john.doe@example.com', 'password123', 'System Manager', NULL); -- John has no manager
INSERT INTO Employees (EmployeeID, FirstName, LastName, Email, Password, Position, ManagerID) VALUES (2, 'Jane', 'Smith', 'jane.smith@example.com', 'password456', 'Company Representative', 162455); -- Jane's manager is John
INSERT INTO Employees (EmployeeID, FirstName, LastName, Email, Password, Position, ManagerID) VALUES (3, 'Alice', 'Johnson', 'alice.johnson@example.com', 'password789', 'Company Representative', 162455); -- Alice's manager is John
INSERT INTO Employees (EmployeeID, FirstName, LastName, Email, Password, Position, ManagerID) VALUES (4, 'Bob', 'Brown', 'bob.brown@example.com', 'password101', 'System Manager', 2); -- Bob's manager is Jane

-- Insert Days into the database
INSERT INTO Days (Date) VALUES ('2024-09-12');
INSERT INTO Days (Date) VALUES ('2024-09-13');
INSERT INTO Days (Date) VALUES ('2024-09-14');
INSERT INTO Days (Date) VALUES ('2024-09-15');

-- Insert Events into the database
INSERT INTO Events (EmployeeID, DayID, EventName, StartTime, EndTime, Description) VALUES (162455, 1, 'Meeting', '09:00:00', '10:00:00', 'Team meeting to discuss project progress');
INSERT INTO Events (EmployeeID, DayID, EventName, StartTime, EndTime, Description) VALUES (162455, 2, 'Workshop', '11:00:00', '12:00:00', 'Workshop on new software tools');
INSERT INTO Events (EmployeeID, DayID, EventName, StartTime, EndTime, Description) VALUES (162455, 3, 'Conference', '13:00:00', '14:00:00', 'Annual conference with keynote speakers');
INSERT INTO Events (EmployeeID, DayID, EventName, StartTime, EndTime, Description) VALUES (162455, 4, 'Training', '15:00:00', '16:00:00', 'Training session on company policies');

-- Create views for Company Representatives and System Managers
CREATE VIEW CompanyRepresentatives AS
SELECT * FROM Employees WHERE Position = 'Company Representative';

CREATE VIEW SystemManagers AS
SELECT * FROM Employees WHERE Position = 'System Manager';

-- Query to get an employee's events
SELECT e.FirstName, e.LastName, d.Date, ev.EventName, ev.StartTime, ev.EndTime
FROM Employees e
JOIN Events ev ON e.EmployeeID = ev.EmployeeID
JOIN Days d ON ev.DayID = d.DayID
WHERE e.EmployeeID = 162455;

-- Query to get events on a specific day
SELECT d.Date, e.FirstName, e.LastName, ev.EventName, ev.StartTime, ev.EndTime
FROM Days d
JOIN Events ev ON d.DayID = ev.DayID
JOIN Employees e ON ev.EmployeeID = e.EmployeeID
WHERE d.DayID = 1;

-- Query to get an employee's subordinates
SELECT e1.FirstName AS ManagerFirstName, e1.LastName AS ManagerLastName, e2.FirstName AS SubordinateFirstName, e2.LastName AS SubordinateLastName
FROM Employees e1
JOIN Employees e2 ON e1.EmployeeID = e2.ManagerID
WHERE e1.EmployeeID = 1; -- Replace 1 with the EmployeeID of the manager you want to query