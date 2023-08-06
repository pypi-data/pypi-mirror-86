import asyncio

from asynctest import TestCase

from mechanicus.core.executor import QueueExecutor, TaskExecutor


async def source(data):
    for item in data:
        yield item
        await asyncio.sleep(0.01)


class ExecutorTester(TestCase):

    async def test(self):
        data = [i for i in range(20)]

        class TestExecutor(TaskExecutor[int, int]):
            async def execute(self, task: int):
                await asyncio.sleep(0.02)
                return task

        executor = QueueExecutor(TestExecutor(), 2)
        result = await executor.execute(source(data))
        self.assertEqual(set(result), set(data))
