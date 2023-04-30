from enum import Enum


class Status(Enum):
    processing = 'PROCESSING'
    pending = 'PENDING'
    resolved = 'RESOLVED'
    refunded = 'REFUNDED'
    closed = 'CLOSED'
    canceled = 'CANCELED'
