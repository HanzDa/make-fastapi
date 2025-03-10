from fastapi import HTTPException, status


integrity_exception = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Integrity error, object already exists",
)