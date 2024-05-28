	.section	__TEXT,__text,regular,pure_instructions
	.build_version macos, 14, 0	sdk_version 14, 4
	.globl	_add_overflow                   ; -- Begin function add_overflow
	.p2align	2
_add_overflow:                          ; @add_overflow
	.cfi_startproc
; %bb.0:
	mvn	x8, x1
	cmp	x8, x0
	b.lo	LBB0_2
; %bb.1:
	add	x9, x1, x0
	str	x9, [x2]
LBB0_2:
	cmp	x8, x0
	cset	w0, lo
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	_add_overflow2                  ; -- Begin function add_overflow2
	.p2align	2
_add_overflow2:                         ; @add_overflow2
	.cfi_startproc
; %bb.0:
	adds	x8, x0, x1
	cset	w0, hs
	str	x8, [x2]
	ret
	.cfi_endproc
                                        ; -- End function
.subsections_via_symbols
