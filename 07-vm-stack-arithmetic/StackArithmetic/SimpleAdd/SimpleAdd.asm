// push constant 7
    @7
    D=A
    @SP
    M=M+1
    A=M-1
    M=D

// push constant 8
    @8
    D=A
    @SP
    M=M+1
    A=M-1
    M=D

// add
    @SP
    AM=M-1
    D=M
    @SP
    AM=M-1
    A=M
    D=A+D
    @SP
    M=M+1
    A=M-1
    M=D

// Infinite Loop (Terminator)
(END)
    @END
    0;JMP
