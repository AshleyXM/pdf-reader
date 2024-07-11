from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from config.constants import SECRET_KEY, ALGORITHM, SUCCESS
from config.constants import TOKEN_FIELD_1, TOKEN_FIELD_2, TOKEN_FIELD_1_VAL, TOKEN_FIELD_2_VAL


# Define the OAuth2PasswordBearer instance
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # automatically extract the token from the Authorization header


# Function to verify the token
def verify_token(token: str = Depends(oauth2_scheme)):
    # Define an unauthorized exception
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_field_1: str = payload.get(TOKEN_FIELD_1)
        token_field_2: str = payload.get(TOKEN_FIELD_2)
        if token_field_1 != TOKEN_FIELD_1_VAL or token_field_2 != TOKEN_FIELD_2_VAL:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return SUCCESS
