from typing import Optional, Dict, Any
from fastapi import HTTPException

class AuthenticationService:
    def __init__(self, config):
        self.config = config
        
    async def authenticate(self, credentials_exception, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Handles authentication and returns user details with JWT token."""
        try:
            # Mock database call
            user = await get_user(username)
            
            if not user:
                raise credentials_exception
            
            if not verify_password(password, user.hashed_password):
                raise credentials_exception
                
            # Generate JWT token
            access_token_expires = datetime.utcnow() + timedelta(minutes=30)
            access_token = self._create_access_token(
                data={"sub": str(user.id)}, expires_delta=timedelta(minutes=30)
            )
            
            return {"access_token": access_token, "token_type": "bearer"}
            
        except Exception as e:
            logging.error(f"Authentication failed: {str(e)}")
            raise HTTPException(status_code=401, detail="Incorrect username or password.")

    def _create_access_token(self, data: Dict[str, Any], expires_delta: timedelta) -> str:
        """Creates a new JWT token."""
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        
        encoded_jwt = jwt.encode(
            to_encode,
            self.config["secret_key"],
            algorithm=self.config["algorithm"]
        )
        
        return encoded_jwt