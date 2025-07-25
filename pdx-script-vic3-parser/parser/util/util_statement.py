from parser.commands.statement import Statement

def find_matching_statements(statement_list:list[Statement] ,property_str:str=None,operator:str=None,value=None) -> list[Statement]:
    return_val:list[Statement] = list()
    for statement in statement_list:
        if __valid_property(statement, property_str) and __valid_operator(statement, operator) and __valid_value(statement, value):
            return_val.append(statement)
    return return_val

def __valid_property(statement:Statement,property_str:str) -> bool:
    if (property_str is None) or (statement.get_name() == property_str):
        return True
    return False

def __valid_operator(statement:Statement,operator:str) -> bool:
    if (operator is None) or (statement.get_operator() == operator):
        return True
    return False

def __valid_value(statement:Statement,value:str) -> bool:
    if (value is None) or (statement.get_value() == value):
        return True
    return False