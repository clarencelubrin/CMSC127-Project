import os
from sqlite3 import Date
from turtle import color
from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from models.driver import Driver
from datetime import date as PyDate

# Import your DAOs
from dao import driver_dao, vehicle_dao, registration_dao, violation_dao
from database.connection import DBConnection
from models.registration import Registration
from models.vehicle import Vehicle
from models.violation import Violation
from models.violation_type import ViolationType # Ensure this exists based on your main.py

from functions.validator import isLicenseNumberValid, isPlateNumberValid

# Import your reporting DAO functions
from dao import reports_dao


load_dotenv()
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Database Dependency
def get_db():
    db = DBConnection()
    db.connect(
        user=os.getenv("MARIADB_USER"),
        password=os.getenv("MARIADB_USER_PASSWORD"),
        host=os.getenv("MARIADB_HOST", "localhost"),
        port=int(os.getenv("MARIADB_PORT", "3306")),
        database=os.getenv("MARIADB_DATABASE")
    )
    curr = db.cursor
    try:
        yield curr
        db.commit()
    finally:
        curr.close()
        db.disconnect()

# --- UI ROUTES ---

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={} # Add any other variables you need here
    )

# DRIVER MANAGEMENT
@app.get("/drivers")
def list_drivers(request: Request, curr=Depends(get_db)):
    drivers = driver_dao.get_all_drivers(curr)
    return templates.TemplateResponse(
        request=request,
        name="tables.html",
        context={
            "title": "Drivers Management", 
            "headers": Driver.get_headers(), 
            "table_name": "Drivers",
            "type": "driver",
            "content": [driver.serialize() for driver in drivers]
        }
    )

@app.post("/drivers/add")
async def add_driver(
    request: Request,
    license_no: str = Form(...),
    full_name: str = Form(...),
    license_type: str = Form(...),
    license_status: str = Form(...),
    address: str = Form(...),
    sex: str = Form(...),
    date_of_birth: str = Form(...),
    registration_no: int = Form(None), # Optional, can be empty
    curr=Depends(get_db)
):
    try:
        dob = Date.fromisoformat(date_of_birth)

        if not isLicenseNumberValid(license_no):
            return "Invalid license number format. Expected format: AAA-YY-CCCCCC", 400
  
        new_driver = Driver(
            license_no, full_name, license_type, license_status, 
            address, sex, dob, registration_no
        )
        
        success = driver_dao.create_driver(curr, new_driver)
        
        if success:
            return RedirectResponse(url="/drivers", status_code=303)
        else:
            return "Error saving to database", 500
            
    except Exception as e:
        print(f"Validation or Database Error: {e}")
        return f"Error: {e}", 400
    
@app.get("/drivers/search")
async def search_driver(request: Request, query: str, curr=Depends(get_db)):
    try:
        drivers = driver_dao.search_driver(curr, query)
        
        if drivers:
            driver_data = [d.serialize() for d in drivers]
        else:
            driver_data = []

        return templates.TemplateResponse(
            request=request,
            name="tables.html",
            context={
                "type": "driver",
                "table_name": "Driver",
                "title": "Driver Management",
                "headers": Driver.get_headers(),
                "content": driver_data,
                "query": query,
                "message": "No results found" if not driver_data else None
            }
        )
    except Exception as e:
        print(f"Search error: {e}")
        return templates.TemplateResponse(
            request=request,
            name="tables.html",
            context={"drivers": [], "message": f"An error occurred: {e}"}
        )

@app.post("/drivers/{license_no}/delete")
async def delete_driver(license_no: str, curr=Depends(get_db)):
    success = driver_dao.delete_driver(curr, license_no)
    if success:
        return RedirectResponse(url="/drivers", status_code=303)
    else:
        return "Error deleting driver", 500

@app.post("/drivers/update")
async def update_driver_route(
    license_no: str = Form(...),
    full_name: str = Form(...),
    license_type: str = Form(...),
    license_status: str = Form(...),
    address: str = Form(...),
    sex: str = Form(...),
    date_of_birth: str = Form(...),
    registration_no: str = Form(None), # Optional
    curr=Depends(get_db)
):
    from models.driver import Driver

    if not isLicenseNumberValid(license_no):
        return "Invalid license number format. Expected format: AAA-YY-CCCCCC", 400
    
    # Create driver object
    driver = Driver(
        license_no, full_name, license_type, license_status, 
        address, sex, Date.fromisoformat(date_of_birth), registration_no
    )
    # DAO expects tuple in specific order for UPDATE SQL
    success = driver_dao.update_driver(curr, driver)
    if success:
        return RedirectResponse(url="/drivers", status_code=303)
    else:
        return "Error updating driver", 500
    
# VEHICLE MANAGEMENT
@app.get("/vehicles")
async def list_vehicles(request: Request, curr=Depends(get_db)):
    from models.vehicle import Vehicle
    vehicles = vehicle_dao.get_all_vehicles(curr)
    
    return templates.TemplateResponse(
        request=request,
        name="tables.html",
        context={
            "type": "vehicle",
            "table_name": "Vehicle",
            "title": "Vehicle Fleet Management",
            "headers": Vehicle.get_headers(), 
            "content": [v.serialize() for v in vehicles] 
        }
    )

@app.post("/vehicles/add")
async def add_vehicle(
    request: Request,
    plate_no: str = Form(...),
    engine_no: str = Form(...),
    chassis_no: str = Form(...),
    vehicle_type: str = Form(...),
    color: str = Form(...),
    year: int = Form(...),
    model: str = Form(...),
    make: str = Form(...),
    registration_no: int = Form(None), # Optional
    license_no: str = Form(None), # Optional
    curr=Depends(get_db)
):
    try:
        if not isPlateNumberValid(plate_no):
            return "Invalid plate number format. Expected format: AAA-1234", 400
        
        new_vehicle = Vehicle(
            plate_no, engine_no, chassis_no, vehicle_type, color, 
            year, model, make, registration_no, license_no
        )
        
        success = vehicle_dao.create_vehicle(curr, new_vehicle)
        
        if success:
            return RedirectResponse(url="/vehicles", status_code=303)
        else:
            return "Error saving to database", 500
            
    except Exception as e:
        print(f"Validation or Database Error: {e}")
        return f"Error: {e}", 400
    
@app.get("/vehicles/search")
async def search_vehicle(request: Request, query: str, curr=Depends(get_db)):
    try:
        vehicles = vehicle_dao.search_vehicle(curr, query)
        
        if vehicles:
            vehicle_data = [v.serialize() for v in vehicles]
        else:
            vehicle_data = []

        return templates.TemplateResponse(
            request=request,
            name="tables.html",
            context={
                "type": "vehicle",
                "table_name": "Vehicle",
                "title": "Vehicle Fleet Management",
                "headers": Vehicle.get_headers(),
                "content": vehicle_data,
                "query": query,
                "message": "No results found" if not vehicle_data else None
            }
        )
    except Exception as e:
        print(f"Search error: {e}")
        return templates.TemplateResponse(
            request=request,
            name="tables.html",
            context={"vehicles": [], "message": f"An error occurred: {e}"}
        )

@app.post("/vehicles/{plate_no}/delete")
async def delete_vehicle(plate_no: str, curr=Depends(get_db)):
    success = vehicle_dao.delete_vehicle(curr, plate_no)
    if success:
        return RedirectResponse(url="/vehicles", status_code=303)
    else:
        return "Error deleting vehicle", 500

@app.post("/vehicles/update")
async def update_vehicle_route(
    plate_no: str = Form(...),
    engine_no: str = Form(...),
    chassis_no: str = Form(...),
    vehicle_type: str = Form(...),
    color: str = Form(...),
    year: int = Form(...),
    model: str = Form(...),
    make: str = Form(...),
    registration_no: int = Form(None), # Optional
    license_no: str = Form(None), # Optional
    curr=Depends(get_db)
):
    from models.vehicle import Vehicle

    if not isPlateNumberValid(plate_no):
        return "Invalid plate number format. Expected format: AAA-1234", 400

    vehicle = Vehicle(
        plate_no, engine_no, chassis_no, vehicle_type, 
        color, year, model, make, registration_no, license_no
    )
    success = vehicle_dao.update_vehicle(curr, vehicle)
    return RedirectResponse(url="/vehicles", status_code=303)

# VIOLATION MANAGEMENT
@app.get("/violations", response_class=HTMLResponse)
async def list_violations(request: Request, curr=Depends(get_db)):
    from models.violation import Violation
    violations = violation_dao.get_all_violations(curr)

    return templates.TemplateResponse(
        request=request,  # Must be provided explicitly
        name="tables.html", # The filename of the template
        context={
            "type": "violation",
            "table_name": "Violation",
            "title": "Violation Management",
            "headers": Violation.get_headers(), # Use the exact method name from your model
            "content": [v.serialize() for v in violations]
        }
    )


@app.post("/violations/add")
async def add_violation(
    request: Request,
    violation_id: int = Form(...),
    date: str = Form(...),
    location: str = Form(...),
    corresponding_fine_amount: float = Form(...),
    apprehending_officer: str = Form(None),
    violation_status: str = Form(...),
    license_no: str = Form(None),
    plate_no: str = Form(None),
    violation_types: str = Form(None), # Comma-separated string of violation types
    curr=Depends(get_db)
):
    try:
        # convert comma-separated violation types into list of ViolationType objects
        vt_list = []
        if violation_types:
            for vt in violation_types.split(","):
                vt_list.append(ViolationType(violation_id, vt.strip())) # Assuming ViolationType can be created with just the type name

        new_violation = Violation(
            violation_id, Date.fromisoformat(date), location, 
            corresponding_fine_amount, apprehending_officer, 
            violation_status, license_no, plate_no
        )
        new_violation.set_violation_types(vt_list)

        success = violation_dao.create_violation(curr, new_violation)
        
        if success:
            return RedirectResponse(url="/violations", status_code=303)
        else:
            return "Error saving to database", 500
            
    except Exception as e:
        print(f"Validation or Database Error: {e}")
        return f"Error: {e}", 400
    
@app.post("/violations/update")
async def update_violation_route(
    violation_id: int = Form(...),
    date: str = Form(...),
    location: str = Form(...),
    corresponding_fine_amount: float = Form(...),
    apprehending_officer: str = Form(None),
    violation_status: str = Form(...),
    license_no: str = Form(None),
    plate_no: str = Form(None),
    violation_types: str = Form(None), # Comma-separated string of violation types
    curr=Depends(get_db)
):
    try:
        
        vt_list = []
        if violation_types:
            for vt in violation_types.split(","):
                vt_list.append(ViolationType(violation_id, vt.strip())) # Assuming ViolationType can be created with just the type name

        new_violation = Violation(
            violation_id, Date.fromisoformat(date), location, 
            corresponding_fine_amount, apprehending_officer, 
            violation_status, license_no, plate_no
        )
        new_violation.set_violation_types(vt_list)

        success = violation_dao.update_violation(curr, new_violation)
        
        if success:
            return RedirectResponse(url="/violations", status_code=303)
        else:
            return "Error saving to database", 500
            
    except Exception as e:
        print(f"Validation or Database Error: {e}")
        return f"Error: {e}", 400


@app.post("/violations/{violation_id}/delete")
async def delete_violation(violation_id: int, curr=Depends(get_db)):
    success = violation_dao.delete_violation(curr, violation_id)
    if success:
        return RedirectResponse(url="/violations", status_code=303)
    else:
        return "Error deleting violation", 500

@app.get("/violations/search")
async def search_violations(request: Request, query: str, curr=Depends(get_db)):
    try:
        # Call the new general search that returns a list
        violations = violation_dao.search_violation(curr, query)
        
        if violations:
            violation_data = [v.serialize() for v in violations]
        else:
            violation_data = []

        return templates.TemplateResponse(
            request=request,
            name="tables.html",
            context={
                "type": "violation",
                "table_name": "Violation",
                "title": "Violation Search Results",
                "headers": Violation.get_headers(), 
                "content": violation_data,
                "query": query
            }
        )
    except Exception as e:
        print(f"Search error: {e}")
        # Ensure the fallback also uses keyword arguments for Python 3.14 compatibility
        return templates.TemplateResponse(
            request=request,
            name="tables.html",
            context={"type": "violation", "content": [], "message": f"Error: {e}", "headers": []}
        )
 

# Registration Management
@app.get("/registrations", response_class=HTMLResponse)
async def list_registrations(request: Request, curr=Depends(get_db)):
    registrations = registration_dao.get_all_registrations(curr)

    for r in registrations:
        print(r, r.serialize()) # Debug print to check if serialize works
    
    return templates.TemplateResponse(
        request=request,
        name="tables.html", 
        context={
            "type": "registration",
            "table_name": "Registration",
            "title": "Registration Management",
            "headers": Registration.get_headers(), # Use the exact method name from your model
            "content": [r.serialize() for r in registrations]
        }
    )
@app.post("/registrations/add")
async def add_registration(
    request: Request,
    registration_no: int = Form(...),
    registration_date: str = Form(...),
    expiration_date: str = Form(...),
    registration_status: str = Form(...),
    license_no: str = Form(None),
    plate_no: str = Form(None),
    curr=Depends(get_db)
):
    try:
        if license_no and not isLicenseNumberValid(license_no):
            return "Invalid license number format. Expected format: AAA-YY-CCCCCC", 400
        if plate_no and not isPlateNumberValid(plate_no):
            return "Invalid plate number format. Expected format: AAA-1234", 400

        reg = Registration(
            registration_no, 
            Date.fromisoformat(registration_date), 
            Date.fromisoformat(expiration_date), 
            registration_status,
            license_no,
            plate_no
        )
        success = registration_dao.create_registration(curr, reg)

        if success:
            return RedirectResponse(url="/registrations", status_code=303)
        else:
            return "Error saving to database", 500
    except Exception as e:
        print(f"Validation or Database Error: {e}")
        return f"Error: {e}", 400

@app.get("/registrations/search")
async def search_registration(request: Request, query: str, curr=Depends(get_db)):
    try:
        registration = registration_dao.search_registration(curr, query)
        print(f"DEBUG: search_registration returned: {registration}")  # Debug print to check raw output
        if registration:
            registration_data = [reg.serialize() for reg in registration]
        else:
            registration_data = []
        print(f"DEBUG: Serialized registration data: {registration_data}")  # Debug print to check serialized data  

        return templates.TemplateResponse(
            request=request,
            name="tables.html",
            context={
                "type": "registration",
                "table_name": "Registration",
                "title": "Registration Search Results",
                "headers": Registration.get_headers(), 
                "content": registration_data,
                "query": query,
                "message": "No results found" if not registration_data else None
            }
        )
    except Exception as e:
        print(f"Search error: {e}")
        return templates.TemplateResponse(
            request=request,
            name="tables.html",
            context={"type": "registration", "content": [], "message": f"Error: {e}", "headers": []}
        )    

@app.post("/registrations/update")
async def update_registration_route(
    registration_no: int = Form(...),
    registration_date: str = Form(...),
    expiration_date: str = Form(...),
    registration_status: str = Form(...),
    license_no: str = Form(None),
    plate_no: str = Form(None),
    curr=Depends(get_db)
):
    from models.registration import Registration

    # Validate license_no and plate_no formats if they are provided
    if license_no and not isLicenseNumberValid(license_no):
        return "Invalid license number format. Expected format: AAA-YY-CCCCCC", 400
    if plate_no and not isPlateNumberValid(plate_no):
        return "Invalid plate number format. Expected format: AAA-1234", 400

    print("Validation passed, creating Registration object")

    
    # Instantiate model with data from form
    reg = Registration(
        registration_no, 
        Date.fromisoformat(registration_date), 
        Date.fromisoformat(expiration_date), 
        registration_status,
        license_no,
        plate_no
    )

    # Call DAO update
    success = registration_dao.update_registration(curr, reg)

    if success:
        return RedirectResponse(url="/registrations", status_code=303)
    else:
        return "Error updating registration", 500
    
@app.post("/registrations/{registration_no}/delete")
async def delete_registration(registration_no: int, curr=Depends(get_db)):
    success = registration_dao.delete_registration(curr, registration_no)
    if success:
        return RedirectResponse(url="/registrations", status_code=303)
    else:
        return "Error deleting registration", 500

# --- REPORT 1: DEMOGRAPHIC DRIVER FILTERING ---
@app.get("/reports/drivers-filtered", response_class=HTMLResponse)
async def report_drivers_filtered(
    request: Request,
    license_type: str = "",
    license_status: str = "",
    age_min: int = 18,
    age_max: int = 80,
    sex: str = "",
    curr=Depends(get_db)
):
    drivers = reports_dao.drivers_filtered_query(
        curr, license_type, license_status, age_min, age_max, sex
    )
    # Handle None cleanly by falling back to an empty list
    content = [d.serialize() for d in drivers] if drivers else []
    
    return templates.TemplateResponse(
        request=request,
        name="reports.html",
        context={
            "active_report": "drivers_filtered",
            "title": "Demographic Driver Filtering Results",
            "filters": {
                "license_type": license_type,
                "license_status": license_status,
                "age_min": age_min,
                "age_max": age_max,
                "sex": sex
            },
            "content_list": content
        }
    )

# --- REPORT 2: VEHICLES BY DRIVER OWNER LINK ---
@app.get("/reports/vehicles-by-driver", response_class=HTMLResponse)
async def report_vehicles_by_driver(request: Request, license_no: str = None, curr=Depends(get_db)):
    content = []
    if license_no:
        vehicles = reports_dao.vehicles_by_driver_query(curr, license_no)
        content = [v.serialize() for v in vehicles] if vehicles else []

    return templates.TemplateResponse(
        request=request,
        name="reports.html",
        context={
            "active_report": "vehicles_by_driver",
            "title": f"Fleet Summary — License Holder #{license_no}" if license_no else "Fleet Tracking by Owner",
            "filters": {"license_no": license_no},
            "content_list": content
        }
    )

# --- REPORT 3: EXPIRED REGISTRATIONS AS OF DATE ---
@app.get("/reports/expired-registrations", response_class=HTMLResponse)
async def report_expired_registrations(request: Request, as_of_date: str = None, curr=Depends(get_db)):
    content = []
    if as_of_date:
        vehicles = reports_dao.expired_registrations_query(curr, as_of_date)
        content = [v.serialize() for v in vehicles] if vehicles else []

    return templates.TemplateResponse(
        request=request,
        name="reports.html",
        context={
            "active_report": "expired_registrations",
            "title": f"Expired Registrations as of {as_of_date}",
            "filters": {"as_of_date": as_of_date},
            "content_list": content
        }
    )

# --- REPORT 4: DRIVERS WITH EXPIRED OR SUSPENDED STATUS ---
@app.get("/reports/invalid-licenses", response_class=HTMLResponse)
async def report_invalid_licenses(request: Request, curr=Depends(get_db)):
    drivers = reports_dao.drivers_with_expired_or_suspended_licenses_query(curr)
    content = [d.serialize() for d in drivers] if drivers else []

    return templates.TemplateResponse(
        request=request,
        name="reports.html",
        context={
            "active_report": "invalid_licenses",
            "title": "Non-Compliant Invalid Licenses Registry",
            "filters": {},
            "content_list": content
        }
    )

# --- REPORT 5: VIOLATIONS BY DRIVER WINDOW TIMELINE ---
@app.get("/reports/violations-range", response_class=HTMLResponse)
async def report_violations_range(
    request: Request, 
    license_no: str = None, 
    start_date: str = None, 
    end_date: str = None, 
    curr=Depends(get_db)
):
    content = []
    if license_no and start_date and end_date:
        violations = reports_dao.violations_by_driver_date_range_query(curr, license_no, start_date, end_date)
        content = [v.serialize() for v in violations] if violations else []

    return templates.TemplateResponse(
        request=request,
        name="reports.html",
        context={
            "active_report": "violations_range",
            "title": f"Violations Timeline — Driver #{license_no}",
            "filters": {"license_no": license_no, "start_date": start_date, "end_date": end_date},
            "content_list": content
        }
    )

# --- REPORT 6: VIOLATION TYPE COUNTS BY ANNUAL AGGREGATION ---
@app.get("/reports/violation-aggregates", response_class=HTMLResponse)
async def report_violation_aggregates(request: Request, year: str = "2026", curr=Depends(get_db)):
    # This query directly returns raw aggregated database tuples: (violation_type, count)
    raw_data = reports_dao.violations_count_by_type_for_year_query(curr, year)
    rows = raw_data if raw_data else []

    return templates.TemplateResponse(
        request=request,
        name="reports.html",
        context={
            "active_report": "violation_aggregates",
            "title": f"Violation Volume Breakdown for Year {year}",
            "filters": {"year": year},
            "raw_data_rows": rows
        }
    )

# --- REPORT 7: VEHICLES IN VIOLATIONS BY REGIONAL LOCALITY ---
@app.get("/reports/regional-incidents", response_class=HTMLResponse)
async def report_regional_incidents(request: Request, location: str = "", curr=Depends(get_db)):
    content = []
    if location:
        vehicles = reports_dao.vehicles_in_violations_by_region_query(curr, location)
        content = [v.serialize() for v in vehicles] if vehicles else []

    return templates.TemplateResponse(
        request=request,
        name="reports.html",
        context={
            "active_report": "regional_incidents",
            "title": f"Vehicular Incident Hotspots: '{location}'",
            "filters": {"location": location},
            "content_list": content
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
