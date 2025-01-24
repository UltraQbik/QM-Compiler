"""
Compiler classes
"""


from typing import Any
from enum import StrEnum
from dataclasses import dataclass
from source.exceptions import *


class TagType(StrEnum):
    UNDEFINED = "undefined"
    BUILT_IN = "built-in"
    POINTER = "pointer"
    NUMBER = "number"

    def __repr__(self):
        return self.value


@dataclass
class Tag:
    """
    TagType - value pair
    """

    value: Any | None = None
    type: TagType = TagType.UNDEFINED


class Word:
    """
    Instruction word
    """

    def __init__(self, tags: list[Tag] | None = None):
        self.tags: list[Tag] = tags if tags is not None else list()


class Scope:
    """
    Scope of instruction words
    """

    def __init__(self, words: list | None = None):
        self.words: list[Word | Scope] = words if words is not None else list()

    def add(self, word: Word | Any):
        """
        Adds a word / scope to scope
        """

        if isinstance(word, (Word, Scope)):
            self.words.append(word)
        else:
            raise CompilerError("Attempted to append wrong type to scope")


class MacroScope(Scope):
    """
    Special type of scope used for macros
    """


class SubroutineScope(Scope):
    """
    Special type of scope used for subroutines
    """


class GlobalScope(Scope):
    """
    Global scope
    """
