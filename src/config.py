import os

class configurations :

    def __init__(self) :

        # host configuration
        self.host = "0.0.0.0"
        self.port = int(os.environ.get('PORT',5000))

