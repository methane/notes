	.text
	.file	"overflow.c"
	.globl	add_overflow                    # -- Begin function add_overflow
	.p2align	4, 0x90
	.type	add_overflow,@function
add_overflow:                           # @add_overflow
	.cfi_startproc
# %bb.0:
	movq	%rsi, %rax
	notq	%rax
	cmpq	%rdi, %rax
	jb	.LBB0_2
# %bb.1:
	addq	%rdi, %rsi
	movq	%rsi, (%rdx)
.LBB0_2:
	cmpq	%rdi, %rax
	setb	%al
	retq
.Lfunc_end0:
	.size	add_overflow, .Lfunc_end0-add_overflow
	.cfi_endproc
                                        # -- End function
	.globl	add_overflow2                   # -- Begin function add_overflow2
	.p2align	4, 0x90
	.type	add_overflow2,@function
add_overflow2:                          # @add_overflow2
	.cfi_startproc
# %bb.0:
	addq	%rsi, %rdi
	setb	%al
	movq	%rdi, (%rdx)
	retq
.Lfunc_end1:
	.size	add_overflow2, .Lfunc_end1-add_overflow2
	.cfi_endproc
                                        # -- End function
	.ident	"Ubuntu clang version 18.1.3 (1)"
	.section	".note.GNU-stack","",@progbits
	.addrsig
