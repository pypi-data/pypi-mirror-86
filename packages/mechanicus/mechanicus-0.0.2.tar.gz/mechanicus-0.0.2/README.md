# Mechanicus

Parallel execute with asyncio library

## Install

`pip3 install mechanicus`

## Dependencies

* python >=3.7
* aiohttp
* aiofiles

## Examples

### Parallel file download

```python
executor = QueueExecutor(Downloader())
await executor.execute([
    DownloadTask(
        "https://file-examples-com.github.io/uploads/2017/02/file_example_CSV_5000.csv",
        "/home/user/Downloads/example.csv",
    ),
    DownloadTask(
        "https://file-examples-com.github.io/uploads/2017/02/file_example_JSON_1kb.json",
        "/home/user/Downloads/example.json",
    )
])
```

### Parallel custom task execute

```python
async def source(count):
    for i in range(count):
        print(f"new: {i}")
        yield i
        await asyncio.sleep(0.2)

class CustomExecutor(TaskExecutor[int, int]):
    async def execute(self, task: int):
        print(f"start: {task}")
        await asyncio.sleep(0.5)
        print(f"complete: {task}")
        return task

executor = QueueExecutor(CustomExecutor())
result = await executor.execute(source(20))
print(f"result: {result}")
```
