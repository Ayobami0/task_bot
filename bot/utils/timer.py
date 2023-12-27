import asyncio


class CountDownExecutor:
    """Counts down to the specified duration then executes the supplied function"""

    def __init__(self, duration, callback):
        self._duration = duration * 60  # converts duration in minutes to seconds
        self._callback = callback

    async def _start(self):
        await asyncio.sleep(self._duration)
        await self._callback

    def run(self):
        loop = asyncio.get_event_loop()  # schedule task in already existing loop
        loop.create_task(self._start())
