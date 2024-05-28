	.file	"overflow.c"
	.text
	.p2align 4
	.globl	add_overflow
	.type	add_overflow, @function
add_overflow:
.LFB0:
	.cfi_startproc
	endbr64
	addq	%rdi, %rsi
	jc	.L3
	movq	%rsi, (%rdx)
	xorl	%eax, %eax
	ret
.L3:
	movl	$1, %eax
	ret
	.cfi_endproc
.LFE0:
	.size	add_overflow, .-add_overflow
	.p2align 4
	.globl	add_overflow2
	.type	add_overflow2, @function
add_overflow2:
.LFB1:
	.cfi_startproc
	endbr64
	addq	%rsi, %rdi
	movq	%rdi, (%rdx)
	setc	%al
	ret
	.cfi_endproc
.LFE1:
	.size	add_overflow2, .-add_overflow2
	.ident	"GCC: (Ubuntu 13.2.0-23ubuntu4) 13.2.0"
	.section	.note.GNU-stack,"",@progbits
	.section	.note.gnu.property,"a"
	.align 8
	.long	1f - 0f
	.long	4f - 1f
	.long	5
0:
	.string	"GNU"
1:
	.align 8
	.long	0xc0000002
	.long	3f - 2f
2:
	.long	0x3
3:
	.align 8
4:
