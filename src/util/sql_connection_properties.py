class SQLConnectionProperties:
    """
    This class represents the properties of an SQL connection.

    connection_string
        Returns the formatted connection string for the SQL connection.

    """
    def __init__(self, driver, server, port, database, username, password):
        self.driver = driver
        self.server = server
        self.port = port
        self.database = database
        self.username = username
        self.password = password

    @property
    def connection_string(self):
        return (f"DRIVER={self.driver};"
                f"Server={self.server},{self.port};"
                f"Database={self.database};"
                f"UID={self.username};"
                f"PWD={self.password};"
                f"TrustServerCertificate=yes")
