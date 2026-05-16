
-- TEST DATA
INSERT INTO DRIVER (license_no, full_name, license_type, license_status, address, sex, date_of_birth) VALUES
('N02-24-325432', 'John Smith', 'Professional', 'Valid', '123 Main St', 'M', '1990-10-20'),
('E30-67-230023', 'Jane Doe', 'Professional', 'Valid', '456 Oak Ave', 'F', '1985-05-15'),
('F3E-93-684200', 'Mike Johnson', 'Professional', 'Expired', '789 Pine Rd', 'M', '1995-12-03');

INSERT INTO VEHICLE VALUES
('ABC-1234', 'EN123456', 'CH987654', 'Sedan', 'Black', 2020, 'Civic', 'Honda', 'N02-24-325432'),
('XYZ-5678', 'EN654321', 'CH456789', 'SUV', 'White', 2019, 'CR-V', 'Honda', 'E30-67-230023'),
('DEF-9012', 'EN789012', 'CH123456', 'Sedan', 'Silver', 2021, 'Altima', 'Nissan', 'F3E-93-684200');

INSERT INTO REGISTRY VALUES
(1001, '2022-01-15', '2025-01-15', 'Active', 'N02-24-325432', 'ABC-1234'),
(1002, '2021-06-20', '2024-06-20', 'Expired', 'E30-67-230023', 'XYZ-5678'),
(1003, '2023-03-10', '2026-03-10', 'Active', 'F3E-93-684200', 'DEF-9012');

INSERT INTO VIOLATION VALUES
(5001, '2000-10-02', 'Calamba City, Laguna', 500.00, 'Officer Garcia', 'Paid', 'N02-24-325432', 'ABC-1234'),
(5002, '2023-06-15', 'Manila City', 1000.00, 'Officer Santos', 'Unpaid', 'E30-67-230023', 'XYZ-5678'),
(5003, '2000-11-20', 'Calamba City, Laguna', 750.00, 'Officer Reyes', 'Paid', 'F3E-93-684200', 'DEF-9012');

INSERT INTO VIOLATION_VIOLATION_TYPE VALUES
(5001, 'speeding'),
(5002, 'reckless driving'),
(5003, 'illegal parking');
