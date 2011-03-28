	.file	"xx.c"
	.text
.globl main
	.type	main, @function
main:
	leal	4(%esp), %ecx
	andl	$-16, %esp
	pushl	-4(%ecx)
	pushl	%ebp
	movl	%esp, %ebp
	pushl	%ecx
	subl	$16, %esp
	movl	$20, -8(%ebp)
	addl	$33, -8(%ebp)
	movl	$0, %eax
	addl	$16, %esp
	popl	%ecx
	popl	%ebp
	leal	-4(%ecx), %esp
	ret
	.size	main, .-main
	.ident	"GCC: (Gentoo 4.3.4 p1.1, pie-10.1.5) 4.3.4"
	.section	.note.GNU-stack,"",@progbits
