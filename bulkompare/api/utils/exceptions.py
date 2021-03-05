class StopError(Exception):
    """Stop what we are doing and report"""


class CustomError(Exception):
    """Raise this exception in case of problem with custom operation"""
    pass
