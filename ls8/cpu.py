"""CPU functionality."""

import sys



class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0]*256
        self.reg = [0]*8
        self.PC = 0
        self.address = 0
        self.SP = self.reg[7] = 0xF4
        self.set_PC = False
        self.branchtable = {
            0b00000001: self.HLT_handle,
            0b10000010: self.LDI_handle,
            0b01000111: self.PRN_handle,
            0b10100010: self.MUL_handle,
            0b10100000: self.ADD_handle,
            0b01000101: self.PUSH_handle,
            0b01000110: self.POP_handle,
            0b01010000: self.CALL_handle,
            0b00010001: self.RET_handle
        }

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value


    def load(self, command):
        """Load a program into memory."""
        self.ram[self.address] = command
        self.address += 1

    def reset_address(self):
        self.address = 0


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            #self.fl,
            #self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def HLT_handle(self, *args):
        sys.exit(1)
        self.set_PC = False
    def LDI_handle(self, operand_a, operand_b, *args):
        self.reg[operand_a] = operand_b
        self.set_PC = False
    def PRN_handle(self, operand_a, *args):
        print(self.reg[operand_a])
        self.set_PC = False
    def MUL_handle(self, operand_a, operand_b, *args):
        self.alu('MUL', operand_a, operand_b)
        self.set_PC = False
    def ADD_handle(self, operand_a, operand_b, *args):
        self.alu('ADD', operand_a, operand_b)
        self.set_PC = False
    def PUSH_handle(self, operand_a, *args):
        self.SP -= 1
        self.ram[self.SP] = self.reg[operand_a]
        self.set_PC = False
    def POP_handle(self, operand_a, *args):
        self.reg[operand_a] = self.ram[self.SP]
        self.SP += 1
        self.set_PC = False
    def CALL_handle(self, operand_a, *args):
        self.SP -=1
        self.ram[self.SP] = self.PC + 2
        self.PC = self.reg[operand_a]
        self.set_PC = True
    def RET_handle(self, *args):
        self.PC = self.ram[self.SP]
        self.SP += 1
        self.set_PC = True

    def run(self):
        while True:

            IR = self.ram_read(self.PC)
            operands_num = IR >> 6
            operand_a = self.ram_read(self.PC + 1)
            operand_b = self.ram_read(self.PC + 2)
            self.branchtable[IR](operand_a, operand_b)
            if not self.set_PC:
                self.PC += (operands_num + 1)