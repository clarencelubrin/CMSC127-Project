from models.driver import Driver

def create_driver(curr, driver):
    try:
        curr.execute("INSERT INTO DRIVER (license_no, full_name, license_type, license_status, address, sex, date_of_birth) VALUES (?, ?, ?, ?, ?, ?, ?)", driver.get_tuple())
        return True
    except Exception as e:
        print(f"Error creating driver: {e}")
        return False

def update_driver(curr, driver):
    try:
        curr.execute(
            "UPDATE DRIVER SET license_type=?, full_name=?, license_status=?, address=?, sex=?, date_of_birth=? WHERE license_no=?", 
            (driver.license_type, driver.full_name, driver.license_status, driver.address, driver.sex, driver.date_of_birth, driver.license_no)
        )
        return True
    except Exception as e:
        print(f"Error updating driver: {e}")
        return False

def delete_driver(curr, license_no):
    try:
        curr.execute("DELETE FROM DRIVER WHERE license_no=?", (license_no,))
        return True
    except Exception as e:
        print(f"Error deleting driver: {e}")
        return False

def search_driver(curr, value):
    try:
        curr.execute(
            "SELECT * FROM DRIVER WHERE license_no LIKE ? OR full_name LIKE ? OR address LIKE ? OR sex LIKE ? OR date_of_birth LIKE ? OR license_type LIKE ? OR license_status LIKE ?", 
            (f"%{value}%", f"%{value}%", f"%{value}%", f"%{value}%", f"%{value}%", f"%{value}%", f"%{value}%")
        )
        row = curr.fetchall()
        if row:
            return [Driver(*r) for r in row]
        else:
            return None
    except Exception as e:
        print(f"Error retrieving driver: {e}")
        return None
    
def get_all_drivers(curr):
    try:
        curr.execute("SELECT * FROM DRIVER")
        rows = curr.fetchall()
        return [Driver(*row) for row in rows]
    except Exception as e:
        print(f"Error retrieving all drivers: {e}")
        return []