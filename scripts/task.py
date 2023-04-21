class Task:
    def __init__(self, task_type, duration, message=None):
        self.task_type = task_type
        self.duration = duration
        self.message = message