class error:
    name = __qualname__


class syntax_error(error):
    name = __qualname__


class unrecognized_character_error(error):
    name = __qualname__


class undefined_variable_error(error):
    name = __qualname__


class uninitialized_variable_error(error):
    name = __qualname__


class undefined_function_error(error):
    name = __qualname__


class function_redefinition_error(error):
    name = __qualname__


class type_error(error):
    name = __qualname__


class import_error(error):
    name = __qualname__


class not_implemented_error(error):
    name = __qualname__


class duplicate_symbol_error(error):
    name = __qualname__
