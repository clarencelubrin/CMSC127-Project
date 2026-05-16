def isLicenseNumberValid(license_no: str) -> bool:
    return license_no and len(license_no) == 13 and license_no[3] == '-' and license_no[6] == '-'

def isPlateNumberValid(plate_no: str) -> bool:
    return plate_no and len(plate_no) == 8 and plate_no[3] == '-'
