bits 16
org 0x7c00
boots:
;jump disk table
jmp ees
nop
oem             db      'MY OEM  '
bsector         dw      200h
scluster        db      1h 
rsector         dw      1h
tfat            db      2h
rent            dw      0e0h
tsectors        dw      0b40h
media           db      0f0h 
sfat            dw      9h
strak           dw      12h
head            dw      2h
hidden          dd      0h
large           dd      0h
drive           db      0h
flag            db      0h
sig             db      29h
vol             dd      0ffffffffh
label           db      'MY LABEL    '
id              db      'FAT12   '
;--------------------------------------------------------
;calcalation of root directory sector this sector + sfat X tfat 
eess            dw      0
;calculation strack X HEADS
ees1            dw      0
nop
ees:
;--------------------------------------------------------
;calculation strack X HEADS		
		cs
		mov ax,[strak]
		cs
		mov bx,[head]
		mov cx,0
		mov dx,0
		clc
		mul bx
		cs
		mov [ees1],ax
;--------------------------------------------------------		
;calcalation of root directory sector this sector + sfat X tfat 
		mov ax,0
		cs
		mov bx,[sfat]
		cs
		mov al,[tfat]
		mov dx,0
		mov cx,0
		clc
		mul bx
		cs
		mov bx,[hidden]
		clc
		add ax,bx
		inc ax
		mov bx,ax
		cs
		mov [eess],ax
        mov ax,1000h
        mov es,ax
        mov ax,bx
;load root directory
call func
;--------------------------------------------------------
mov bp,100h
;find #.COM in the root directory
;loop finde char 35
mloop:
	es
	mov al,[bp]
	cmp al,35
	jz mloop1
	add bp,32
	cmp bp,300h
jb mloop  
;if not find #.com jump to halt 
jmp halts
mloop1:
;--------------------------------------------------------
;retrive sector number of root directory table
    add bp,1ah
    es
    mov ax,[bp]
;add root dir + sector number of file
	cs
	mov bx,[eess]
    add ax,bx
    add ax,29
 ;load #.COM kernel into address 1000h:100h
call func
;--------------------------------------------------------
;clear int vector 20h
call vectors
jmp kernel
gdt_start:

gdt_null:
    dd 0x0
    dd 0x0

gdt_code:
    dw 0xffff
    dw 0x0
    db 0x0
    db 10011010b
    db 11001111b
    db 0x0

gdt_data:
    dw 0xffff
    dw 0x0
    db 0x0
    db 10010010b
    db 11001111b
    db 0x0

gdt_end:

gdt_descriptor:
    dw gdt_end - gdt_start
    dd gdt_start

CODE_SEG equ gdt_code - gdt_start
DATA_SEG equ gdt_data - gdt_start
kernel:
    mov ax, 0
    mov ss, ax
    mov sp, 0xFFFC

    mov ax, 0
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax

    cli
    lgdt[gdt_descriptor]
    mov eax, cr0
    or eax, 0x1
    mov cr0, eax
    jmp CODE_SEG:b32

[bits 32]
nop 

b32:
    mov ax, DATA_SEG
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov ss, ax

    mov ebp, 0x90000
    mov esp, ebp
;start eax ebx ecx edx to enter on program
    mov eax,0
    mov ebx,0
    mov ecx,0xf000
    mov edx,0
    mov esi,0
    mov edi,0
    ds
    call dword 0x10000
exits:
haltss:
    jmp haltss
;--------------------------------------------------------
;if it fail reboot
       mov ax,202
int 19h
        ret
;--------------------------------------------------------
;function to load sectores and directory root to memory
func:
;ipush
        push bp
        push dx
        push cx
        push bx
        push ax
        
        xor dx,dx
        xor cx,cx
        cs
;calculation sectorer 
        mov bx,[ees1]
        clc
        idiv bx
        push ax
        mov ax,dx

        xor dx,dx
        xor cx,cx
        cs
;calculation sectorer
        mov bx,[strak]
        clc
        idiv bx
        push ax
        mov ax,dx
        inc dx
        mov cl,dl
        pop ax
        mov dh,al
        pop ax
        mov ch,al
        
        
        
;load into 1000h:100h
        mov ax,1000h
        mov bx,100h
        mov es,ax
        mov al,30
        mov ah,2
        mov dl,0
;int load sectores into memory
int 13h
;ipop        

        pop ax
        pop bx
        pop cx
        pop dx
        pop bp
        ret
;--------------------------------------------------------
;define int 20h and 21h to reset iret
vectors:
	mov cl,64
	mov ax,0
	mov ds,ax
	mov ax,vectorsi
	mov dx,0
	mov di,128
vectors1:
	ds
	mov [di],ax
	add di,2
	ds
	mov [di],dx
	add di,2
	dec cl
	cmp cl,0
	jnz vectors1
ret
;--------------------------------------------------------
;clear iret call
vectorsi:
iret
ret
;--------------------------------------------------------
;debug print function
printe:
jmp haltss
;--------------------------------------------------------
;if #.COM not find enter in halt mode to turn pc
halts:
jmp halts
spere:
times  510-(spere-boots) db 0 
signature:
dw 0xaa55
