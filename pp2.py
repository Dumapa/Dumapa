print("Hello, World")

print("Hello, World")

print("Hello World!")
print("I am learning Python.")
print("It is awesome!")

print("Hello, World!" , end=" ")
print("i will print on the same line.")

x = str(3)    # x will be '3'
y = int(3)    # y will be 3
z = float(3)  # z will be 3.0

x = 5
y = "John"
print(type(x))
print(type(y))

fruits_list = ["apple", "banana", "cherry"]
x, y, z = fruits_list
print(x)
print(y)
print(z)

x = "Python"
y = "is"
z = "awesome"
print(x, y, z) #not together

x = "Python "
y = "is "
z = "awesome"
print(x + y + z) #together

x = 5
y = "John"
print(x + y) #error

x = 5
y = "John"
print(x, y) #not error

x = "awesome"

def myfunc():
  print("Python is " + x)

myfunc()

x = "awesome"

def myfunc():
  x = "fantastic"
  print("Python is " + x)

myfunc()

print("Python is " + x)

def myfunc():
  global x
  x = "fantastic"

myfunc()

print("Python is " + x) #to change me variable inside function 

#x = str("Hello World")	str	
#x = int(20)	int	
#x = float(20.5)	float	
#x = complex(1j)	complex	
#x = list(("apple", "banana", "cherry"))	list	
#x = tuple(("apple", "banana", "cherry"))	tuple	
#x = range(6)	range	
#x = dict(name="John", age=36)	dict	
#x = set(("apple", "banana", "cherry"))	set	
#x = frozenset(("apple", "banana", "cherry"))	frozenset	
#x = bool(5)	bool	
#x = bytes(5)	bytes	
#x = bytearray(5)	bytearray	
#x = memoryview(bytes(5))	memoryview

x = 1    # int
y = 2.8  # float
z = 1j   # complex

#convert from int to float:
a = float(x)

#convert from float to int:
b = int(y)

#convert from int to complex:
c = complex(x)

print(a)
print(b)
print(c)

print(type(a))
print(type(b))
print(type(c))

import random

print(random.randrange(1, 10))

x = int(1)   # x will be 1
y = int(2.8) # y will be 2
z = int("3") # z will be 3

x = float(1)     # x will be 1.0
y = float(2.8)   # y will be 2.8
z = float("3")   # z will be 3.0
w = float("4.2") # w will be 4.2

x = str("s1") # x will be 's1'
y = str(2)    # y will be '2'
z = str(3.0)  # z will be '3.0'

a = """Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua."""
print(a)

a = "Hello, World!"
print(a[1])

for x in "banana":
  print(x)

a = "Hello, World!"
print(len(a))

txt = "The best things in life are free!"
print("free" in txt)

txt = "The best things in life are free!"
if "free" in txt:
  print("Yes, 'free' is present.")

txt = "The best things in life are free!"
print("expensive" not in txt)

txt = "The best things in life are free!"
if "expensive" not in txt:
  print("No, 'expensive' is NOT present.")

b = "Hello, World!"
print(b[2:5]) #Get the characters from position 2 to position 5 (not included)

b = "Hello, World!"
print(b[:5]) #Get the characters from the start to position 5 (not included)

b = "Hello, World!"
print(b[2:]) #Get the characters from position 2, and all the way to the end

b = "Hello, World!"
print(b[-5:-2]) 

a = "Hello, World!"
print(a.upper())

a = "Hello, World!"
print(a.lower())

a = " Hello, World! "
print(a.strip()) # returns "Hello, World!"
"""From: "o" in "World!" (position -5)


a = "Hello, World!"
print(a.replace("H", "J"))

To, but not included: "d" in "World!" (position -2):"""
a = "Hello, World!"
print(a.split(",")) # returns ['Hello', ' World!']

age = 36
txt = f"My name is John, I am {age}"
print(txt)
txt = "We are the so-called \"Vikings\" from the north."

"""----------------------------------------------------------------------------------------------------------------------------------------"""
x = input()

def myfunc():
  print("Hello, " + x + "!")

myfunc()
"""----------------------------------------------------------------------------------------------------------------------------------------"""
