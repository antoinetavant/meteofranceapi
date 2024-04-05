import xmltodict

class MissingParameterError(Exception):
    def __init__(self, text: str):
        #parse the error message with xmltodict
        data = xmltodict.parse(text)
        message = data["am:fault"]["am:message"]
        description = data["am:fault"]["am:description"]
        self.message = f"{message}\n {description}"
        super().__init__(self.message)

class MissingDataError(Exception):
    def __init__(self, text: str):
        #parse the error message with xmltodict
        data = xmltodict.parse(text)
        exception = data["mw:fault"]["mw:description"]["ns0:ExceptionReport"]["ns0:Exception"]
        code = exception["@exceptionCode"]
        locator = exception["@locator"]
        text = exception["ns0:ExceptionText"]
        message = (f"Error code: {code}\n"
                   f"Locator: {locator}\n"
                   f"Text: {text}")
        self.message = message
        super().__init__(self.message)
