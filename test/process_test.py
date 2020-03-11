from fractions import Fraction as Q
import unittest

from underbar.assembler import assemble
from underbar.process import Process
from underbar.register import Register
from underbar.stdio import StandardStream

PR = Register.PR.value
SR = Register.SR.value

STDIN = Q(StandardStream.STDIN.value)
STDOUT = Q(StandardStream.STDOUT.value)
STDERR = Q(StandardStream.STDERR.value)


class ProcessTest(unittest.TestCase):
    def test_halt(self):
        process = Process(assemble('''

                13, hcf

        '''))

        process.run()
        self.assertEqual(process.pop_data(), Q(13))

    def test_call(self):
        process = Process(assemble('''

                cli + function
                hcf

            function:
                13, ret

        '''))

        process.run()
        self.assertEqual(process.pop_data(), Q(13))

    def test_hello_world(self):
        process = Process(assemble('''

                message

            loop:
                dup, ldm
                dup
                beq + exit
                stdout, put
                adi + 1
                bal + loop

            exit:
                0, hcf

            message:
                "Hello, World!\n", 0

        '''))

        process.run()
        self.assertEqual(process.read_line(), 'Hello, World!\n')

    def test_print(self):
        process = Process(assemble('''

                13, message, stdout, cli + print
                hcf

            ; [stream, string] -> []
            print: .stream = 0
                ent + 1
                stl + .stream
            .loop:
                dup, ldm; Load character
                dup, beq + .break; Break on null character
                ldl + .stream, put; Write character to stream
                adi + 1, bal + .loop; Next character
            .break:
                pop, pop
                ret + 1

            message:
                "Hello, World!\n", 0

        '''), args=['hello'])

        process.run()
        self.assertEqual(process.pop_data(), Q(13))
        self.assertEqual(process.read_line(), 'Hello, World!\n')

    def test_echo(self):
        process = Process(assemble('''

                cli + main; Run main
                hcf; Halt program

            ; [argc, argv] -> [exit_code]
            main: .argc = 0, .argv = 1
                ent + 2, stl + .argc, stl + .argv
                0
            .loop:
                dup, ldl + .argc, sub, beq + .break; Break after last argument
                dup, beq + .first; Skip space before first argument
                ' ', stdout, put; Write space to standard output
            .first:
                dup, ldl + .argv, add, ldm; Load argument
                stdout, cli + print; Print argument to standard output
                adi + 1, bal + .loop; Next argument
            .break:
                pop
                '\n', stdout, put; Write newline to standard output
                0, ret + 2

            ; [stream, string] -> []
            print: .stream = 0
                ent + 1
                stl + .stream
            .loop:
                dup, ldm; Load character
                dup, beq + .break; Break on null character
                ldl + .stream, put; Write character to stream
                adi + 1, bal + .loop; Next character
            .break:
                pop, pop
                ret + 1

        '''), args=['hello', 'world'])

        process.run()
        self.assertEqual(process.read_line(), 'hello world\n')

    def test_get_integer_line(self):
        process = Process(assemble('''

                stdin, cli + get_integer_line
                hcf

            ; [stream] -> [result]
            get_integer_line: .stream = 0, .result = 1
                ent + 2, stl + .stream
                0, stl + .result; Initialize result
                1; Positive sign
                ldl + .stream, get; First character
                dup, adi - '-', bne + .loop; If sign character
                pop; Discard sign character
                neg; Negative sign
                ldl + .stream, get; First character after sign
            .loop:
                dup, adi - '\n', beq + .break; Break on newline
                adi - '0'; Character to digit
                ldl + .result, mli + 10; Multiply result by base
                add, stl + .result; Add digit to result
                ldl + .stream, get; Next character
                bal + .loop
            .break:
                pop; Discard newline
                ldl + .result, mul, stl + .result; Apply sign
                ldl + .result, ret + 2

        '''))

        process.write('285793423\n')
        process.run()
        self.assertEqual(process.pop_data(), 285793423)

    def test_get_integer_line_negative(self):
        process = Process(assemble('''

                stdin, cli + get_integer_line
                hcf

            ; [stream] -> [result]
            get_integer_line: .stream = 0, .result = 1
                ent + 2, stl + .stream
                0, stl + .result; Initialize result
                1; Positive sign
                ldl + .stream, get; First character
                dup, adi - '-', bne + .loop; If sign character
                pop; Discard sign character
                neg; Negative sign
                ldl + .stream, get; First character after sign
            .loop:
                dup, adi - '\n', beq + .break; Break on newline
                adi - '0'; Character to digit
                ldl + .result, mli + 10; Multiply result by base
                add, stl + .result; Add digit to result
                ldl + .stream, get; Next character
                bal + .loop
            .break:
                pop; Discard newline
                ldl + .result, mul, stl + .result; Apply sign
                ldl + .result, ret + 2

        '''))

        process.write('-618584259\n')
        process.run()
        self.assertEqual(process.pop_data(), -618584259)

    def test_put_integer_line(self):
        process = Process(assemble('''

                285793423, stdout, cli + put_integer_line
                hcf

            ; [stream, value] -> []
            put_integer_line: .stream = 0, .value = 1
                ent + 2, stl + .stream, stl + .value
                1
                ldl + .value, bge + .loop_1
                '-', ldl + .stream, put
                ldl + .value, neg, stl + .value
            .loop_1:
                mli + 10
                dup, ldl + .value, sub, ble + .loop_1
            .loop_2:
                fdi + 10
                dup, beq + .break
                dup, ldl + .value, swp, div, fdi + 1
                adi + '0', ldl + .stream, put
                dup, ldl + .value, swp, mod, stl + .value
                bal + .loop_2
            .break:
                '\n', ldl + .stream, put
                ret + 2

        '''))

        process.run()
        self.assertEqual(process.read_line(), '285793423\n')

    def test_put_integer_line_negative(self):
        process = Process(assemble('''

                -618584259, stdout, cli + put_integer_line
                hcf

            ; [stream, value] -> []
            put_integer_line: .stream = 0, .value = 1
                ent + 2, stl + .stream, stl + .value
                1
                ldl + .value, bge + .loop_1
                '-', ldl + .stream, put
                ldl + .value, neg, stl + .value
            .loop_1:
                mli + 10
                dup, ldl + .value, sub, ble + .loop_1
            .loop_2:
                fdi + 10
                dup, beq + .break
                dup, ldl + .value, swp, div, fdi + 1
                adi + '0', ldl + .stream, put
                dup, ldl + .value, swp, mod, stl + .value
                bal + .loop_2
            .break:
                '\n', ldl + .stream, put
                ret + 2

        '''))

        process.run()
        self.assertEqual(process.read_line(), '-618584259\n')


if __name__ == '__main__':
    unittest.main()
