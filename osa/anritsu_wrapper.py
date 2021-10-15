import pyvisa as visa


class Anritsu:
    def __init__(self, visa_search_term):
        rm = visa.ResourceManager()
        self.inst = rm.open_resource(visa_search_term)

        print("Connected to ", self.identify())

    def query(self, query_text: str):
        """
        Enter a query text for testing purpose
        Args:
            query_text: anything according to Remote Operation Manuel
        Returns:

        """
        return self.inst.query(query_text)

    def write(self, command_text: str) -> None:
        """
        For writing command
        Args:
            command_text: anything according to Remote Operation Manuel
        """
        self.inst.write(command_text)

    def identify(self):
        """
        Returns:
            str: The response from an `*IDN?`query.
        """
        return self.query('*IDN?')