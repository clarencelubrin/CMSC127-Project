"""
    Reports DAO: SQL report generators for various queries.
"""
from models.driver import Driver
from models.vehicle import Vehicle
from models.violation import Violation

def drivers_filtered_query(curr, license_type, license_status, age_min, age_max, sex):
    """View all registered drivers filtered by: License type, License status, Age range, Sex"""
    try:
        # FIX: Replaced strftime with MariaDB's YEAR(CURDATE()) and YEAR(date_of_birth)
        query = """
            SELECT * FROM DRIVER 
            WHERE license_type LIKE ? 
              AND license_status LIKE ? 
              AND sex LIKE ? 
              AND (YEAR(CURDATE()) - YEAR(date_of_birth)) BETWEEN ? AND ?
        """
        curr.execute(query, (f"%{license_type}%", f"%{license_status}%", f"%{sex}%", age_min, age_max))
        row = curr.fetchall()
        if row:
            return [Driver(*r) for r in row]
        return None
    except Exception as e:
        print(f"Error retrieving driver: {e}")
        return None

def vehicles_by_driver_query(curr, license_no):
    """View all vehicles owned by a given driver."""
    try:
        curr.execute("SELECT * FROM VEHICLE WHERE license_no=?", (license_no,))
        row = curr.fetchall()
        if row:
            return [Vehicle(*r) for r in row]
        return None
    except Exception as e:
        print(f"Error retrieving vehicles: {e}")
        return None

def expired_registrations_query(curr, as_of_date):
    """View all vehicles with expired registrations as of a given date."""
    try:
        query = """
            SELECT v.* FROM VEHICLE v 
            JOIN REGISTRY r ON v.license_no = r.license_no 
            WHERE r.expiration_date < ?
        """
        curr.execute(query, (as_of_date,))
        row = curr.fetchall()
        if row:
            return [Vehicle(*r) for r in row]
        return None
    except Exception as e:
        print(f"Error retrieving expired registrations: {e}")
        return None

def drivers_with_expired_or_suspended_licenses_query(curr):
    """View all drivers with expired or suspended licenses."""
    try:
        curr.execute("SELECT * FROM DRIVER WHERE license_status IN ('Expired', 'Suspended')")
        row = curr.fetchall()
        if row:
            return [Driver(*r) for r in row]
        return None
    except Exception as e:
        print(f"Error retrieving drivers with expired or suspended licenses: {e}")
        return None

def violations_by_driver_date_range_query(curr, license_no, start_date, end_date):
    """View all traffic violations committed by a given driver within a specified date range."""
    try:
        curr.execute("SELECT * FROM VIOLATION WHERE license_no=? AND date BETWEEN ? AND ?", (license_no, start_date, end_date))
        row = curr.fetchall()
        if row:
            return [Violation(*r) for r in row]
        return None
    except Exception as e:
        print(f"Error retrieving violations: {e}")
        return None

def violations_count_by_type_for_year_query(curr, year):
    """View the total number of violations per violation type for a given year."""
    try:
        # FIX: Replaced strftime('%Y', v.date) with MariaDB's YEAR(v.date)
        query = """
            SELECT vvt.violation_type, COUNT(*) 
            FROM VIOLATION_VIOLATION_TYPE vvt 
            JOIN VIOLATION v ON vvt.violation_id = v.violation_id 
            WHERE YEAR(v.date) = ? 
            GROUP BY vvt.violation_type
        """
        curr.execute(query, (year,))
        row = curr.fetchall()
        if row:
            return row
        return None
    except Exception as e:
        print(f"Error retrieving violations count: {e}")
        return None

def vehicles_in_violations_by_region_query(curr, location):
    """View all vehicles involved in violations within a given city or region."""
    try:
        curr.execute(
            "SELECT v.* FROM VEHICLE v JOIN VIOLATION vi ON v.plate_no = vi.plate_no WHERE vi.location LIKE ?",
            (f"%{location}%",)
        )
        row = curr.fetchall()
        if row:
            return [Vehicle(*r) for r in row]
        return None
    except Exception as e:
        print(f"Error retrieving vehicles in violations: {e}")
        return None