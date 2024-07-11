from datetime import datetime, timedelta
from jose import jwt

from config.constants import SECRET_KEY, ALGORITHM
from config.constants import TOKEN_FIELD_1, TOKEN_FIELD_2, TOKEN_FIELD_1_VAL, TOKEN_FIELD_2_VAL


# Function to create access token
def create_access_token(verification_data: dict, expires_delta: timedelta | None = None, no_expiration: bool = False):
    """
    Generate an access token to access PDF extraction service
    :param verification_data: verification data
    :param expires_delta: the expiration period, default to be 15 minutes
    :param no_expiration: whether the token would expire, default to expire
    :return: access token value
    """
    to_encode = verification_data.copy()
    if not no_expiration:
        expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
        to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Example usage
data = {TOKEN_FIELD_1: TOKEN_FIELD_1_VAL, TOKEN_FIELD_2: TOKEN_FIELD_2_VAL}
access_token_1 = create_access_token(data, no_expiration=True)  # without expiration
print(access_token_1)

access_token_2 = create_access_token(data)  # expire in 15 minutes
print(access_token_2)

access_token_3 = create_access_token(data, timedelta(seconds=60))  # expire in 60 seconds
print(access_token_3)
