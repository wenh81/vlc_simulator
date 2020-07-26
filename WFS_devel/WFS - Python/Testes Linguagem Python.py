
import math

varA = 0.0

def func_alter_var():
	global varA
	varA = 2.0

def main():
	global varA
	print("Hello World")
	print(varA)
	varA = 1.0
	print(varA)
	func_alter_var()
	print(varA)

#main()

listA = [[0.0] * 2] * 2 
listA[0][0] += 1
print(listA)