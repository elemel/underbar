from underbar.operations import MNEMONIC_TO_OPCODE, OPCODE_TO_OPERATION

for mnemonic, opcode in sorted(MNEMONIC_TO_OPCODE.items()):
	operation = OPCODE_TO_OPERATION[opcode]
	print(f'{mnemonic} = {opcode}; {operation.__name__}')
