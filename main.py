from ctypes import c_uint8, c_uint16, c_bool
from consts import PROGRAM_START_ADDRESS, FONTSET_START_ADDRESS, FONTSET
from helpers import load_into_array
from random import randint

class Chip8:
    def __init__(self):
        # 16 8-bit registers (V0-VF)
        self.registers = [ [ None for x in range(8)] for y in range(16)]
        # 4k of memory (0x000-0xFFF)
        self.memory = [None] * 4096
        # 16-bit index register (stores memory addresses)
        self.index_register = [ None for x in range(16)]
        # 16-big program counter (address of next instruction)
        self.program_counter = PROGRAM_START_ADDRESS
        # stack
        self.stack = [ None for x in range(16)]
        # stack pointer
        self.stack_pointer = c_uint8()
        # delay pointer
        self.delay_timer = c_uint8()
        # sound timer
        self.sound_timer = c_uint8()
        # input keys
        self.input_keys = [ c_bool(False) for x in range(16)]
        # Output display (64x32)
        self.display = [ [c_bool(False) for x in range(64)] for y in range(32) ]
        # current opcode
        self.opcode = c_uint16()

        # Load fonts into memory
        load_into_array(self.memory, FONTSET_START_ADDRESS, FONTSET)
    
    @property
    def random(self):
        return c_uint8(randint(0,255))

    def load_rom(self, filename: str):
        with open(filename, 'rb') as f:
            # WARNING
            # Loading the file directly into memory without any error checking
            rom_contents = b.getbuffer()
            load_into_array(self.memory, PROGRAM_START_ADDRESS, rom_contents)
    
    def _00E0(self):
        """
        CLS: Clear the display
        """
        self.display = [ [c_bool(False) for x in range(64)] for y in range(32) ]

    def _00E0(self):
        """
        RET: Return from a subroutine
        """
        
        self.stack_pointer -= 1;
        self.program_counter = self.stack[self.stack_pointer]

    def _1NNN(self):
        """
        JP addr: Jump to location nnn

        Jumps don't remember the original location
        """
        pc = self.opcode & 0x0FFF

    def _2NNN(self):
        """
        CALL addr: Call the subroutine at nnn

        Unlike a jump it does store the location on the stack
        """
        self.stack[self.stack_pointer] = self.program_counter
        self.stack_pointer += 1
        self.program_counter = self.opcode & 0x0FFF

    def _3XKK(self):
        """
        Skip the next instruction of Vx = kk
        """
        # The opcode is "3xkk", this pulls out "x"
        Vx = c_uint8((self.opcode & 0x0F00) >> 8)
        byte = c_uint8(self.opcode & 0x00FF)

        if self.registers[Vx.value] == byte.value:
            self.pc += 2






