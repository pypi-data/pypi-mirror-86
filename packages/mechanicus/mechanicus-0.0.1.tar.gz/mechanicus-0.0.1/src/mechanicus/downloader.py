import os
from typing import NamedTuple

import aiofiles
import aiohttp

from mechanicus.core.executor import TaskExecutor

DEFAULT_CHUNK_SIZE = 1024 * 1024


async def download_file(url: str, filename: str, chunk_size: int = DEFAULT_CHUNK_SIZE):
    async with aiohttp.ClientSession() as session:
        async with session.request(method="GET", url=url) as response:
            assert response.status == 200
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            tmp_file_name = f"{filename}.part"
            if os.path.exists(tmp_file_name):
                os.remove(tmp_file_name)
            async with aiofiles.open(tmp_file_name, "ba") as f:
                async for data in response.content.iter_chunked(chunk_size):
                    await f.write(data)
            os.rename(tmp_file_name, filename)


class FileHandler:

    def apply(self, filename: str):
        raise NotImplementedError


class DownloadTask(NamedTuple):
    url: str
    filename: str
    handler: FileHandler = None


class Downloader(TaskExecutor[DownloadTask, None]):

    def __init__(self, chunk_size: int = DEFAULT_CHUNK_SIZE):
        super().__init__()
        self._chunk_size = chunk_size

    async def execute(self, task: DownloadTask):
        await download_file(task.url, task.filename, self._chunk_size)
        if task.handler is not None:
            await task.handler.apply(task.filename)
