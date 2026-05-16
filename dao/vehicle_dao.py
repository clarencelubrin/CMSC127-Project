from models.vehicle import Vehicle

def create_vehicle(curr, vehicle):
    try:
        curr.execute("INSERT INTO VEHICLE (plate_no, engine_no, chassis_no, vehicle_type, color, year, model, make, license_no) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", vehicle.get_tuple())
        return True
    except Exception as e:
        print(f"Error creating vehicle: {e}")
        return False

def update_vehicle(curr, vehicle):
    try:
        curr.execute(
            "UPDATE VEHICLE SET engine_no=?, chassis_no=?, vehicle_type=?, color=?, year=?, model=?, make=?, license_no=? WHERE plate_no=?", 
            (vehicle.engine_no, vehicle.chassis_no, vehicle.vehicle_type, vehicle.color, vehicle.year, vehicle.model, vehicle.make, vehicle.license_no, vehicle.plate_no)            
        )
        return True
    except Exception as e:
        print(f"Error updating vehicle: {e}")
        return False

def delete_vehicle(curr, plate_no):
    try:
        curr.execute("DELETE FROM VEHICLE WHERE plate_no=?", (plate_no,))
        return True
    except Exception as e:
        print(f"Error deleting vehicle: {e}")
        return False

def search_vehicle(curr, search_term):
    try:
        curr.execute(
            "SELECT * FROM VEHICLE WHERE plate_no LIKE ? OR model LIKE ? OR make LIKE ? OR vehicle_type LIKE ? OR color LIKE ? OR year LIKE ? OR license_no LIKE ? OR engine_no LIKE ? OR chassis_no LIKE ?", 
            (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%")
        )
        rows = curr.fetchall()
        return [Vehicle(*row) for row in rows]
    except Exception as e:
        print(f"Error retrieving vehicle: {e}")
        return None

def get_all_vehicles(curr):
    try:
        curr.execute("SELECT * FROM VEHICLE")
        rows = curr.fetchall()
        return [Vehicle(*row) for row in rows]
    except Exception as e:
        print(f"Error retrieving all vehicles: {e}")
        return []