from datetime import datetime

class Task():
    def __init__(self, task):
        self.task = task
        self._status = 'PENDING'

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        if status not in ['PENDING', 'PROCESSING', 'RESOLVED', 'CLOSED', 'CANCELED']:
            pass
        self._status = status
    
    def __repr__(self) -> Task:
        return self.task
