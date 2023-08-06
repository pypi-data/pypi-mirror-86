import os
import tempfile

from asynctest import TestCase

from mechanicus.core.executor import QueueExecutor
from mechanicus.downloader import Downloader, DownloadTask


class DownloaderTester(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.tasks = [
            DownloadTask(
                "https://file-examples-com.github.io/uploads/2017/02/file_example_CSV_5000.csv",
                os.path.join(tempfile.gettempdir(), "example.csv"),
            ),
            DownloadTask(
                "https://file-examples-com.github.io/uploads/2017/02/file_example_JSON_1kb.json",
                os.path.join(tempfile.gettempdir(), "example.json"),
            )
        ]

    def tearDown(self) -> None:
        super().tearDown()
        for task in self.tasks:
            if os.path.exists(task.filename):
                os.remove(task.filename)

    async def test(self):
        executor = QueueExecutor(Downloader(), 2)
        await executor.execute(self.tasks)
        for task in self.tasks:
            self.assertTrue(os.path.exists(task.filename))
