from abc import ABC, abstractmethod
from config.database import user_collection

# Interface for Login Repository
# This interface defines the contract for any repository that handles user-related database operations.
class ILoginRepository(ABC):
    @abstractmethod
    async def get_user_by_email(self, email: str):
        pass

# Implementation of the Login Repository
# This class implements the ILoginRepository interface and interacts with the database.
class UserRepository(ILoginRepository):
    async def get_user_by_email(self, email: str):
        return await user_collection.find_one({"email": email})