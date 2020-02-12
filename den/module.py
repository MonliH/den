import llvmlite.binding as llvm
import os

try:
    from parser import DenParser
    from lexer import DenLexer
    from codegen import ModuleCodeGen
    from errors.logger import Logger
    from helpers.color import Color
    from helpers.llvm_gen import compile_ir
except ImportError:
    from den.parser import DenParser
    from den.lexer import DenLexer
    from den.codegen import ModuleCodeGen
    from den.errors.logger import Logger
    from den.helpers.color import Color
    from den.helpers.llvm_gen import compile_ir


class DenModule:
    def __init__(self, filename, text="", debug=False):
        self.lexer = DenLexer()
        self.parser = DenParser()
        self.filename = filename
        self.text = text
        self.logger = Logger(self.filename, text, debug=debug)

        self.parser.set_logger(self.logger)
        self.lexer.set_logger(self.logger)

    def generate(self, folder=None):
        fullpath = os.path.abspath(self.filename)
        self.logger.log("Started Lexing")
        self.logger.status(f"{Color.BOLD}{Color.GREEN}Lexing{Color.RESET} {fullpath}")

        tokens = self.lexer.tokenize(self.text)

        self.logger.log("Started Parsing")
        self.logger.status(f"{Color.BOLD}{Color.GREEN}Parsing{Color.RESET}  {fullpath}")

        self.result = self.parser.parse(tokens)
        self.logger.throw()

        self.result.add_name(self.filename)

        self.logger.log("Started Codegen")
        self.logger.status(
            f"{Color.BOLD}{Color.GREEN}Generating{Color.RESET} {fullpath}"
        )

        self.module = ModuleCodeGen(self.logger)
        self.ir = self.module.generate(self.result)
        self.logger.throw()

        if folder is None:
            folder = self.result.name

        self.logger.status(
            f"{Color.BOLD}{Color.GREEN}Writing to{Color.RESET} {os.path.abspath(folder)}/{self.result.name}.o"
        )

        # Generate object file that is linked to excecutable
        mod, target_machine = compile_ir(self.ir)

        if not os.path.exists(folder):
            os.makedirs(folder)

        with open(f"{folder}/{self.result.name}.o", "wb+") as o:
            o.write(target_machine.emit_object(mod))

        print(f"{Color.BOLD}{Color.BLUE}All Done!{Color.RESET} 🎉")

    def add_text(self, text):
        self.text = text
