from sqlite3 import Date

from models.registration import Registration

def create_registration(curr, registration):
    try:
        curr.execute("INSERT INTO REGISTRY (registration_no, registration_date, expiration_date, registration_status, license_no, plate_no) VALUES (?, ?, ?, ?, ?, ?)", registration.get_tuple())
        
        # Change the license_no of the VEHICLE with registration.plate_no to registration.license_no
        curr.execute("UPDATE VEHICLE SET license_no=? WHERE plate_no=?", (registration.license_no, registration.plate_no))
        
        return True
    except Exception as e:
        print(f"Error creating registration: {e}")
        return False

def update_registration(curr, registration):
    try:
        curr.execute(
            "UPDATE REGISTRY SET registration_date=?, expiration_date=?, registration_status=?, license_no=?, plate_no=? WHERE registration_no=?", 
            (registration.registration_date, registration.expiration_date, registration.registration_status, registration.license_no, registration.plate_no, registration.registration_no)
        )
        
        # Change the license_no of the VEHICLE with registration.plate_no to registration.license_no
        curr.execute("UPDATE VEHICLE SET license_no=? WHERE plate_no=?", (registration.license_no, registration.plate_no))

        return True
    except Exception as e:
        print(f"Error updating registration: {e}")
        return False

def delete_registration(curr, registration_no):
    try:
        curr.execute("DELETE FROM REGISTRY WHERE registration_no=?", (registration_no,))
        return True
    except Exception as e:
        print(f"Error deleting registration: {e}")
        return False

def search_registration(curr, value):
    try:
        curr.execute("SELECT * FROM REGISTRY WHERE registration_no LIKE ? OR license_no LIKE ? OR plate_no LIKE ? OR registration_status LIKE ?", (f"%{value}%", f"%{value}%", f"%{value}%", f"%{value}%"))
        row = curr.fetchall()
        if row:
            return [Registration(*r) for r in row]
        else:
            return None
        
    except Exception as e:
        print(f"Error retrieving registration: {e}")
        return None
    
def get_all_registrations(curr):
    try:
        # Calculate the registration status then update the REGISTRY table accordingly
        curr.execute("UPDATE REGISTRY SET registration_status = CASE WHEN registration_status = 'Suspended' THEN 'Suspended' WHEN CURDATE() > expiration_date THEN 'Expired' ELSE 'Active' END")

        curr.execute("SELECT * FROM REGISTRY")
        rows = curr.fetchall()
        return [Registration(*row) for row in rows]
    except Exception as e:
        print(f"Error retrieving all registrations: {e}")
        return []
