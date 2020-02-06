from .node import Node
import uuid

# Meta code sections

class meta:
    class Program(Node):
        def __init__(self, block, position, name=None):
            self.block = block
            if name is None:
                self.name = f"{uuid.uuid4()}"
            self.name = name
            self.position = position
        
        def add_name(self, name):
            self.name = name

        def dump(self):
            return f"package {self.name}"

    class Block(Node):
        def __init__(self, statements, position):
            self.statements = statements
            self.position = position

        def push(self, statement):
            self.statements.append(statement)