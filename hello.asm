; Prints "hello world" to the screen. 
; OS/X requires system call arguments to be pushed onto the stack in reversed 
; order, with an extra 4 bytes (DWORD) at the end. 
;
; Build with: 
;   nasm -f macho hello.asm
;   ld -o hello hello.o
;
; Run with: 
;   ./hello
;
; Author: PotatoMaster101



SECTION .data           ; initialised data section

Msg: db "hello world", 10           ; message to print
MsgLen: equ $ - Msg                 ; length of message


SECTION .text           ; code section

global start
start:

    ; printing message, use write()
    ; system call 4 syntax: 
    ; user_ssize_t write(int fd, user_addr_t cbuf, user_size_t nbyte)
    push dword MsgLen   ; length of message to print
    push dword Msg      ; message to print
    push dword 1        ; FD of 1 for standard output
    sub esp, 4          ; OS/X requires extra 4 bytes after arguments
    mov eax, 4          ; 4 - write() system call
    int 80H             ; perform system call
    add esp, 16         ; restore stack (16 bytes pushed: 3 * dword + 4)

    ; program exit, use sys_exit()
    push dword 0        ; exit value of 0 returned to the OS
    sub esp, 4          ; OS/X requires extra 4 bytes after arguments
    mov eax, 1          ; 1 - sys_exit() system call
    int 80H             ; perform system call
    ; no need to restore stack, code after this line will not be executed 
    ; (program exit)
