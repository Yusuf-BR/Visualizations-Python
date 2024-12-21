-- Alter the table to make EmployeeID an auto-increment column
ALTER TABLE EmployeeProfiles
alter  EmployeeID INT IDENTITY(1,1) PRIMARY KEY;
