from fastapi import HTTPException, status

not_found_user_register_login = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail= {
        "detail": "User not found", 
        "body": "Invalid password or email"
    }
)

already_exists_user = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail= {
        "detail": "User already exists", 
        "body": "User already exists"
    }
)
