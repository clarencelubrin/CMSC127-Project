from models.violation import Violation
from models.violation_type import ViolationType

def create_violation(curr, violation):
    try:
        curr.execute("INSERT INTO VIOLATION (violation_id, date, location, corresponding_fine_amount, apprehending_officer, violation_status, license_no, plate_no) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", violation.get_tuple())
        # Insert violation types into the violation_types table
        if violation.violation_types:
            for vt in violation.violation_types:
                curr.execute("INSERT INTO VIOLATION_VIOLATION_TYPE (violation_id, violation_type) VALUES (?, ?)", vt.get_tuple())
        return True
    except Exception as e:
        print(f"Error creating violation: {e}")
        return False

def search_violation(curr, search_term):
    try:
        query = """
            SELECT * FROM VIOLATION 
            WHERE violation_id LIKE ? OR location LIKE ? OR apprehending_officer LIKE ? 
            OR violation_status LIKE ? OR license_no LIKE ? OR plate_no LIKE ?
        """
        wildcard = f"%{search_term}%"
        curr.execute(query, (wildcard, wildcard, wildcard, wildcard, wildcard, wildcard))
        
        rows = curr.fetchall()
        violations = []
        print(f"Search term: {search_term}, Rows found: {len(rows)}") # Debugging line
        for row in rows:
            # Create the Violation object from the row tuple
            v = Violation(*row)
            
            sub_curr = curr.connection.cursor()
            sub_curr.execute(
                "SELECT violation_id, violation_type FROM VIOLATION_VIOLATION_TYPE WHERE violation_id=?", 
                (v.violation_id,)
            )
            
            # Populate the list of violation types
            from models.violation_type import ViolationType
            v.violation_types = [ViolationType(vt[0], vt[1]) for vt in sub_curr.fetchall()]
            sub_curr.close()
            
            violations.append(v)
            
        return violations # Now returns a list of objects
    except Exception as e:
        print(f"Error searching violations: {e}")
        return [] # Return empty list on error to prevent crashes in the UI

def update_violation(curr, violation):
    try:
        curr.execute(
            "UPDATE VIOLATION SET date=?, location=?, corresponding_fine_amount=?, apprehending_officer=?, violation_status=?, license_no=?, plate_no=? WHERE violation_id=?", 
            (violation.date, violation.location, violation.corresponding_fine_amount, violation.apprehending_officer, violation.violation_status, violation.license_no, violation.plate_no, violation.violation_id)
        )
        # Update violation types: delete existing and insert new ones
        curr.execute("DELETE FROM VIOLATION_VIOLATION_TYPE WHERE violation_id=?", (violation.violation_id,))
        if violation.violation_types:
            for vt in violation.violation_types:
                curr.execute("INSERT INTO VIOLATION_VIOLATION_TYPE (violation_id, violation_type) VALUES (?, ?)", vt.get_tuple())
        return True
    except Exception as e:
        print(f"Error updating violation: {e}")
        return False

def delete_violation(curr, violation_id):
    try:
        curr.execute("DELETE FROM VIOLATION WHERE violation_id=?", (violation_id,))
        curr.execute("DELETE FROM VIOLATION_VIOLATION_TYPE WHERE violation_id=?", (violation_id,))
        return True
    except Exception as e:
        print(f"Error deleting violation: {e}")
        return False   

def get_all_violations(curr):
    try:
        # Use the main cursor to get all violation records
        curr.execute("SELECT * FROM VIOLATION")
        rows = curr.fetchall() 
        violations = []
        
        for row in rows:
            violation = Violation(*row) #
            
            # Use the existing connection to create a fresh, temporary cursor
            # This prevents overwriting the main cursor's state
            sub_curr = curr.connection.cursor() 
            
            sub_curr.execute(
                "SELECT violation_id, violation_type FROM VIOLATION_VIOLATION_TYPE WHERE violation_id=?", 
                (violation.violation_id,)
            )
            
            # Append violation types using the temporary cursor
            for vt_row in sub_curr.fetchall():
                v_obj = ViolationType(int(vt_row[0]), vt_row[1]) #
                violation.violation_types.append(v_obj)
            
            sub_curr.close() # Always close temporary cursors
            violations.append(violation)
            
        return violations
    except Exception as e:
        print(f"Error retrieving all violations: {e}")
        return []