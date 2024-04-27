from fastapi import HTTPException, status

CREDENTIALS_EXECPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

EXPIRED_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token has expired",
    headers={"WWW-Authenticate": "Bearer"},
)

NOT_FOUND_EXCEPTION_TOKEN = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Token not found",
)

INVALID_EXCEPTION_TOKEN = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token is invalid",
    headers={"WWW-Authenticate": "Bearer"},
)
