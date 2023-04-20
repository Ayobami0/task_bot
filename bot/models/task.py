class Task():
    def __init__(self, task_info):
        self.service_amount = task_info['service_amount']
        self.service_date = task_info['service_date']
        self.service_number = task_info['service_number']
        self.service_type = task_info['service_type']
        self.customer_email_address = task_info['email_address']
        self._status = 'PENDING'

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        if status not in ['PENDING', 'PROCESSING', 'RESOLVED', 'CLOSED', 'CANCELED']:
            pass
        self._status = status
