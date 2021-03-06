    cls + main
    hcf

main:
.sum = 0
    ent + 1, dis
    0, stl + .sum; Initialize sum
.loop:
    stdin, tel, beq + .break; Break on EOF
    stdin, cls + get_integer_line
    fdi + 3, adi - 2
    ldl + .sum, add, stl + .sum
    bal + .loop
.break:
    ldl + .sum, stdout, cls + put_integer_line
    0, ret + 1

; [stream] -> [result]
get_integer_line:
.stream = 0, .result = 1
    ent + 2, stl + .stream
    0, stl + .result; Initialize result
    1; Positive sign
    ldl + .stream, get; First character
    dup, adi - '-', bne + .loop; If sign character
    dis; Discard sign character
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
    dis; Discard newline
    ldl + .result, mul, stl + .result; Apply sign
    ldl + .result, ret + 2

; [value, stream] -> []
put_integer_line:
.stream = 0, .value = 1
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
