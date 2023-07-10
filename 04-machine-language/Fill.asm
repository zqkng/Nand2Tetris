// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen
// by writing 'black' in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen by writing
// 'white' in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// ASSEMBLY CODE:
	// Store the max mem. address for screen in @max
	@KBD
	D=A	// D=24576
	@max
	M=D	// max=24576

(START)
	// Set index to initial mem. address (start of screen)
	@SCREEN
	D=A	// D=16384
	@index
	M=D	// index=16384

(CHECK)
	// check for keyboard input
	@KBD
	D=M	// D=24576
	@CLEAR
	D;JEQ	// If no keyboard input, clear screen
	@BLACKEN
	0;JMP	// else blacken screen

(CLEAR)
	// check to see if screen has been blacken
	// if so, reset index for clearing
	@SCREEN
	D=M
	@START
	D;JGT

	@index
	D=M	// D=RAM[index]
	@max
	D=D-M	// D=D-max
	@START
	D;JGE	// If (index-max) >= 0 goto START

	// clear the screen bits
	@index
	D=M	// D=RAM[index]
	@SCREEN
	A=D
	M=0
	
	@index
	M=M+1	// index++ (increment address)
	@CHECK
	0;JMP	// Goto CHECK
	
(BLACKEN)
	@index
	D=M	// D=RAM[index]
	@max
	D=D-M	// D=D-max
	@START
	D;JGE	// If (index-max) >= 0 goto START

	// Blackens the screen bits
	@index
	D=M	// D=RAM[index]
	@SCREEN
	A=D
	M=-1
	
	@index
	M=M+1	// index++ (increment address)
	@CHECK
	0;JMP	// Goto CHECK
(END)
	0;JMP	// Infinite Loop (Terminator)
