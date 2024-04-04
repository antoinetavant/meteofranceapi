import xmltodict

class MissingParameterError(Exception):
    def __init__(self, text: str):
        #parse the error message with xmltodict
        data = xmltodict.parse(text)
        message = data["am:fault"]["am:message"]
        description = data["am:fault"]["am:description"]
        self.message = f"{message}\n {description}"
        super().__init__(self.message)
