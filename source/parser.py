"""
Compiling code
"""


from source.classes import *
from source.built_ins import *


class Parser:
    """
    Parser class
    """

    def __init__(self):
        self.current_scope: Scope = Scope()

    def import_scope(self, scope: Scope):
        """
        Imports scope into parser
        """

        self.current_scope = scope

    def _parse_first_stage(self):
        """
        First stage of parsing

        Basic syntax checking stage
        """

        for word in self.current_scope:
            word: Word  # help type hinting

            # check 'macro' and 'subr' keywords
            if word[0].value in ["macro", "subr"] and word[1].type is not TagType.POINTER:
                raise CompilerSyntaxError(
                    f"built-in '{word[0].value}' followed by a non-pointer argument",
                    line=word.line)

            # check 'uses' keyword
            for idx, tag in enumerate(word):
                tag: Tag  # help type hinting
                if tag.value == "uses":
                    break
            for tag in word[idx+1:]:
                if tag.type is not TagType.POINTER:
                    raise CompilerSyntaxError(
                        f"built-in '{word[idx].value}' followed by a non-pointer argument(s)",
                        line=word.line)

    def _parse_second_stage(self):
        """
        Second stage of parsing

        Builds AST
        """

        idx = -1
        while idx < len(self.current_scope)-1:
            idx += 1
            word: Word = self.current_scope[idx]

            # create macro and subroutine scopes
            if word[0].value in ["macro", "subr"]:
                # create scope
                scope = MacroScope() if word[0].value == "macro" else SubroutineScope()
                idx += 1
                for word_ in self.current_scope[idx:]:
                    word_: Word  # help type hinting
                    if not (word_[0].type is TagType.INTERNAL and word_[0].value == ">"):
                        break
                    word_.pop(0)
                    scope.add(self.current_scope.pop(idx))
                # recursively parse scopes to make AST (Abstract Syntax Tree)
                new_parser = Parser()
                new_parser.import_scope(scope)
                new_parser.parse()

                # insert back into current scope
                self.current_scope.insert(idx, scope)
            elif word[0].type is TagType.INTERNAL and word[0].value == ">":
                raise CompilerIndentationError(
                    "Unexpected indent",
                    line=word.line)

    def parse(self):
        """
        Parses imported scope
        """

        self._parse_first_stage()
        self._parse_second_stage()
