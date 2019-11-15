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
        self.FL = 0
        self.branchtable = {
            0b00000001: self.HLT_handle,
            0b10000010: self.LDI_handle,
            0b01000111: self.PRN_handle,
            0b10100010: self.MUL_handle,
            0b10100000: self.ADD_handle,
            0b01000101: self.PUSH_handle,
            0b01000110: self.POP_handle,
            0b01010000: self.CALL_handle,
            0b00010001: self.RET_handle,
            0b10100111: self.CMP_handle,
            0b01010100: self.JMP_handle,
            0b01011010: self.JGE_handle,
            0b01010110: self.JNE_handle,
            0b01010101: self.JEQ_handle,
            0b10101000: self.AND_handle,
            0b10101010: self.OR_handle,
            0b10101011: self.XOR_handle,
            0b01101001: self.NOT_handle,
            0b10101100: self.SHL_handle,
            0b10101101: self.SHR_handle,
            0b10100100: self.MOD_handle
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
        elif op == "CMP": 
            if self.reg[reg_a] > self.reg[reg_b]:
                self.FL = 0b00000010
            if self.reg[reg_a] < self.reg[reg_b]:
                self.FL = 0b00000100
            else:
                self.FL = 0b00000001
        elif op == 'AND':
            self.reg[reg_a] &= self.reg[reg_b]
        elif op == 'OR':
            self.reg[reg_a] |= self.reg[reg_b]
        elif op == 'XOR':
            self.reg[reg_a] ^= self.reg[reg_b]
        elif op == 'NOT':
            self.reg[reg_a] = ~self.reg[reg_a]
        elif op == 'SHL':
            self.reg[reg_a] << self.reg[reg_b]
        elif op == 'SHR':
            self.reg[reg_a] >> self.reg[reg_b]
        elif op == 'MOD':
            if self.reg[reg_b] == 0: 
                print('You cannnot divide by 0')
            else:
                self.reg[reg_a] %= self.reg[reg_b]
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
    def CMP_handle(self, operand_a, operand_b, *args):
        self.alu('CMP', operand_a, operand_b)
        self.set_PC = False
    def JMP_handle(self, operand_a, *args):
        self.PC = self.reg[operand_a]
        self.set_PC = True
    def JGE_handle(self, operand_a, *args):
        if self.FL == 0b00000010 or self.FL == 0b00000001:
            self.PC = self.reg[operand_a]
            self.set_PC = True
    def JEQ_handle(self, operand_a, *args):
        if self.FL == 1:
            self.PC = self.reg[operand_a]
            self.set_PC = True
    def JNE_handle(self, operand_a, *args):
        if self.FL != 0b00000001: 
            self.PC = self.reg[operand_a]
            self.set_PC = True
    def AND_handle(self, operand_a, operand_b, *args):
        self.alu('AND', operand_a, operand_b)
        self.set_PC = False
    def OR_handle(self, operand_a, operand_b, *args):
        self.alu('OR', operand_a, operand_b)
        self.set_PC = False
    def XOR_handle(self, operand_a, operand_b, *args):
        self.alu('XOR', operand_a, operand_b)
        self.set_PC = False
    def NOT_handle(self, operand_a, operand_b, *args):
        self.alu('NOT', operand_a, operand_b)
        self.set_PC = False
    def SHL_handle(self, operand_a, operand_b, *args):
        self.alu('SHL', operand_a, operand_b)
        self.set_PC = False
    def SHR_handle(self, operand_a, operand_b, *args):
        self.alu('SHR', operand_a, operand_b)
        self.set_PC = False
    def MOD_handle(self, operand_a, operand_b, *args):
        self.alu('MOD', operand_a, operand_b)
        self.set_PC = False
    
    def run(self):
        while True:

            IR = self.ram_read(self.PC)
            operands_num = IR >> 6
            operand_a = self.ram_read(self.PC + 1)
            operand_b = self.ram_read(self.PC + 2)
            self.branchtable[IR](operand_a, operand_b)
            if not self.set_PC:
                self.PC += (operands_num + 1)