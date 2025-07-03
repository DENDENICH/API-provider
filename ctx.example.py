from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, FastAPI, JSONResponse, Request
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

class ExampleBadRequestException(HTTPException):
  '''Custom ROSSO API Exception'''
  def init(self, status_code: int = 400, detail: str):
    super().init(status_code=status_code, detail=detail)

# Фейк движок и SessionLocal, который для интуитивности можно назвать async_session_factory, он просто вернет новый экземпляр сессии
engine = create_async_engine('sqlite+aiosqlite:///example.db')
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def create_session() -> SessionLocal:
  return SessionLocal()

''' Annotated[AsyncSession, Depends(get_session)] уже не нужен, если выбираем путь
с прокидванием менеджера транзакций в ручку, то будет Annotated[TransactionContext, Depends(get_ctx)], но использовать контекст лучше все таки в репозитории мне кажется. Получается инкапсуляция, не наше дело, как там хенлядться ошибки в aexit

В таком случае get_ctx может выглядеть:

async def get_ctx() -> TransactionContext:
  return TransactionContext()

Если идем путем без зависимости, то есть контекст транзакции не используется в ручках, тогда в репозитории можно реализовать так:

class SomeRepository:
  def init(...) -> None:
    self.ctx = get_ctx()

  async def get_all(self):
    async with self.ctx as ctx:
      users = await ctx.users.get_all()
    return users

В таком случае в репозитории не будет работы с сессиями, а только абстрагированный контекст транзакции.
Если вдруг в строчке users = await ctx.users.get_all() будет ошибка, то она как раз таки возникла в ctx.aenter и из-за ее возниконовения вызывается ctx.aexit, там мы уже отловим ее и зарайзим нашу кастомную на которую есть хендлер у app: FastAPI
'''

class UserRepository:
  def init(self, session: AsyncSession):
    self.session = session

  async def get_all(self):
    users = await self.session.execute('SELECT * FROM users')
    return users


class TransactionContext:
  def init(self,
  # тут в принципе можно принять аргумент фабрики, но только если транзакшен контекст будет создаваться 1 раз на все приложение, в другом случае будет не удобно. Либо просто подтянуть его через настройки внутри init, но как аргумент не принимать, так можно будет всегда подменить его в настройках
  ):
    self.session_factory = create_session
    self.session: AsyncSession = None

  async def aenter(self):
    self.session = await self.session_factory()
    self.users = UserRepository(self.session)
    return self.session

  async def aexit(self, exc_type, exc_val, exc_tb):
    try:
      await self.commit()
    except:
      # можно сделать несколько эксептов как раз на те кастомные ошибки, которые райзятся внутри сервиса\репозитория. В таком случае можно будет не делать try: await self.commit(), а сделать проверку if exc_type или как-то еще, это просто идея с головы
      await self.rollback()
      raise ExampleBadRequestException(detail='Something went wrong')
    finally: # finally в принципе можно и убрать
      await self.session.close()

  async def commit(self):
    await self.session.commit()
  
  async def rollback(self):
    await self.session.rollback()


app = FastAPI()

@app.add_exception_handler(ExampleBadRequestException)
async def example_bad_request_exception_handler(request: Request, exc):
  return JSONResponse(
    status_code=exc.status_code,
    content={'detail': exc.detail}
  ) # можно будет сделать функцию, которая принимает app: FastAPI и навешивает все хендлеры


@app.get('/example/ctx')
async def example_ctx():
  async with TransactionContext() as ctx:
    users = await ctx.users.get_all()
  return users 
  # Получаем List[User] или JSONResponse, который возвращает exception_handler


'''
Пример использования вообщем:

async with TransactionContext() as ctx:
  await ctx.users.get_all()
'''

'''
Можно прокидывать экземпялр в ручку и передавать внутрь сервиса, который будет вызывать репозиторий, где уже будет написано async with, либо сделать как-то проще и вообще все экземпляры менеджера использовать только внутри репозиториев\сервисов
'''