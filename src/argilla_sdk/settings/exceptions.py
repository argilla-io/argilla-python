class SettingsException(Exception):
    # TODO: define the base exception for the settings module
    pass


class InvalidFieldException(SettingsException):
    # TODO: define the exception for invalid fields
    pass


class InvalidSettingsException(SettingsException):
    # TODO: define the exception for invalid settings
    pass


class InvalidQuestionException(SettingsException):
    # TODO: define the exception for invalid questions
    pass
