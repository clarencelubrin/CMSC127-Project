-- QUERY
-- 1.
SELECT * FROM DRIVER WHERE license_type = 'driver' AND license_status = 'registered' AND (date_of_birth BETWEEN '1990-01-01' AND '1990-12-31') AND sex = 'M';

-- 2. 
SELECT * FROM VEHICLE WHERE licence_no = 'XYZ2345';

-- 3. 
SELECT V.* FROM VEHICLE V JOIN REGISTRY R 
   ON V.registration_no = R.registration_no
   WHERE R.expiration_date < current_date
   OR R.registration_status = 'EXPIRED';

-- 4. 
SELECT * FROM DRIVER WHERE license_status IN ('EXPIRED', 'SUSPENDED');

-- 5.
 SELECT V.*, VT.violation_type FROM VIOLATION V LEFT JOIN VIOLATION_VIOLATION_TYPE VT 
   ON V.violation_id = VT.violation_id
   WHERE V.licence_no = ''
   AND V.date >= '2000'
   AND V.date <= '2001';

-- 6. 
SELECT VT.violation_type, COUNT(*) AS total_violations
   FROM VIOLATION VI JOIN VIOLATION_VIOLATION_TYPE VT ON VI.violation_id = VT.violation_id
   WHERE YEAR(VI.date) = '2000'
   GROUP BY VT.violation_type;

-- 7. 
SELECT DISTINCT V.* FROM VEHICLE V JOIN VIOLATION VI 
   ON V.plate_no = VI.plate_no
   WHERE VI.date LIKE '2004-10-09' AND VI.location LIKE 'Calamba City, Laguna'; 