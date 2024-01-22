from datetime import timedelta, datetime

SECRET_KEY: str = "4308592e98006d3297e3a0807883ff3d33a006d80a32e256597af75aafea47ac"
ALGORITHM: str = "HS256"
EXP_DATE: datetime = datetime.utcnow() + timedelta(hours=2)
