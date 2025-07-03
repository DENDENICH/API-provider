from typing import Protocol, Self
from core.db.core import db_core
from fastapi import HTTPException
from service.repositories.user import UserRepository
from logger import logger

class CtxException(HTTPException):
	def __init__(self, detail: str, status_code: int = 500) -> None:
		super().__init__(status_code=status_code, detail=detail)

class ITransactionContext(Protocol):
	def __init__(self) -> None:
		...

	async def __aenter__(self) -> Self:
		...

	async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
		...

	async def commit(self) -> None:
		...

	async def rollback(self) -> None:
		...

class TransactionContext(ITransactionContext):
	def __init__(self) -> None:
		self.session = None
		self.session_factory = db_core.session_getter

	async def __aenter__(self) -> Self:
		self.session = await self.session_factory().__anext__()
		self.users = UserRepository(session=self.session)
		return self

	async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
		if exc_type:
			raise CtxException('Error in transaction ctx')
		logger.warning('Exit from transaction ctx')
		try:
			await self.commit()
			logger.warning('Commit in transaction ctx')
		except:
			logger.warning('Error in transaction ctx')
			await self.rollback()
			raise CtxException('Error in transaction ctx')

	async def commit(self) -> None:
		await self.session.commit()

	async def rollback(self) -> None:
		await self.session.rollback()