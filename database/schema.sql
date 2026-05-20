CREATE TABLE DRIVER(
	license_no VARCHAR(13), 	-- AAA-YY-CCCCCC
	full_name VARCHAR(100),
	license_type VARCHAR(100),
	license_status VARCHAR(100),
	address VARCHAR(100),
	sex CHAR(1),
	date_of_birth DATE,
	CONSTRAINT license_no_pk PRIMARY KEY(license_no)
);

CREATE TABLE VEHICLE(
    plate_no CHAR(8), 			-- AAA-1234
    engine_no VARCHAR(100),
    chassis_no VARCHAR(100),
    vehicle_type VARCHAR(100),
    color VARCHAR(50),
    year INT(4),
    model VARCHAR(100),
    make VARCHAR(100),
    license_no VARCHAR(13),      
    CONSTRAINT plate_no_pk PRIMARY KEY(plate_no),
    CONSTRAINT vehicle_license_fk FOREIGN KEY(license_no) REFERENCES DRIVER(license_no) ON DELETE SET NULL
);

CREATE TABLE REGISTRY(
	registration_no VARCHAR(15),
	registration_date DATE,
	expiration_date DATE,
	registration_status VARCHAR(100),
	license_no VARCHAR(13),
	plate_no CHAR(8),
	UNIQUE(plate_no), -- plate_no is associated with only one registration at a time, but a driver can have multiple registrations over time
	CONSTRAINT registration_no_pk PRIMARY KEY(registration_no),
	CONSTRAINT registry_license_fk FOREIGN KEY(license_no) REFERENCES DRIVER(license_no) ON DELETE SET NULL,
	CONSTRAINT registry_plate_fk FOREIGN KEY(plate_no) REFERENCES VEHICLE(plate_no) ON DELETE SET NULL
);

CREATE TABLE VIOLATION(
	violation_id VARCHAR(15),
	date DATE,
	location VARCHAR(200),
	corresponding_fine_amount DECIMAL,
	apprehending_officer VARCHAR(100),
	violation_status VARCHAR(100),
	license_no VARCHAR(13),
	plate_no CHAR(8),
	CONSTRAINT violation_id_pk PRIMARY KEY(violation_id),
	CONSTRAINT licence_no_fk FOREIGN KEY(license_no) REFERENCES DRIVER(license_no) ON DELETE SET NULL,
	CONSTRAINT plate_no_fk FOREIGN KEY(plate_no) REFERENCES VEHICLE(plate_no) ON DELETE SET NULL
);

CREATE TABLE VIOLATION_VIOLATION_TYPE(
	violation_id VARCHAR(15),
	violation_type VARCHAR(100),
	CONSTRAINT pk_violation_violation_type PRIMARY KEY (violation_id, violation_type)
);

CREATE TABLE IF NOT EXISTS users (
	id INT AUTO_INCREMENT PRIMARY KEY,
	username VARCHAR(50) UNIQUE NOT NULL,
	password_hash VARCHAR(255) NOT NULL
);