class Helper:
    """Utility helper class for testing"""
    def __init__(self):
        self.name = "helper"
    
    def help(self):
        return f"Help from {self.name}"

    def process(self, data):
        return f"Processing {data} with {self.name}"
