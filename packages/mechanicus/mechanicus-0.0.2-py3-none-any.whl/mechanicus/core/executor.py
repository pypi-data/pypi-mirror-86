import asyncio
import logging
import multiprocessing
from typing import Generic, TypeVar, List, Union, Iterable, AsyncIterable

T = TypeVar("T")
R = TypeVar("R")


END = object()


async def __aiterable__(iterable: Iterable) -> AsyncIterable:
    for item in iterable:
        yield item


class TaskExecutor(Generic[T, R]):

    async def execute(self, task: T) -> R:
        raise NotImplementedError


class QueueExecutor(Generic[T, R]):
    PARALLEL: int = multiprocessing.cpu_count()
    logger = logging.getLogger("executor")

    def __init__(self, executor: TaskExecutor[T, R], parallel: int = PARALLEL):
        self._executor = executor
        self._parallel = parallel

    async def execute_task(self, task: T) -> R:
        return await self._executor.execute(task)

    async def _reader(self, source: AsyncIterable[T], queue: asyncio.Queue):
        async for task in source:
            await queue.put(task)
        for _ in range(self._parallel):
            await queue.put(END)

    async def _execute(self, queue: asyncio.Queue) -> List[R]:
        result = []
        while True:
            task = await queue.get()
            if task is END:
                break
            self.logger.debug("Run task %s", task)
            result.append(await self.execute_task(task))
            self.logger.debug("Complete task %s", task)
        return result

    async def execute(self, source: Union[AsyncIterable[T], Iterable[T]]) -> List[R]:
        if isinstance(source, Iterable):
            source = __aiterable__(source)
        queue = asyncio.Queue(self._parallel)
        result = await asyncio.gather(
            self._reader(source, queue),
            *(self._execute(queue) for _ in range(self._parallel)),
        )
        return sum(result[1:], [])
