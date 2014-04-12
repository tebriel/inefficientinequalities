# Inefficient Inequalities #

>3 >=2.1 <=4.5 !=5.0 ???

>3 <=4.5 !!!

Satisfying version inequalities is a common need among virtually all
programming languages and package managers. Here we challenge you to solve a
real problem using a toy constraint language similar to (but not the same as!)
Python's own.

1) Let's define operators and versions in the following fashion:

| Operators | Example Versions |
|:---------:|:----------------:|
| >  <      | 1.0              |
| >= <=     | 4.7.0.3          |
| == !=     | 2.10.5           |

2) A Single inequality is expressed as <operator><value>.

__Examples__

*  >=3.0
*  !=2.1.1
*  ==3.14159265
*  <23

3) Gotchas:

*  2.10 is not the same as 2.1 (2.10 > 2.1)
*  3 == 3.0 and 3.0 == 3.0.0 (but 3.0.1 != 3.1)

A whitespace-separated list of inequalities is implicitly combined via "and":

*  >=2 <3 !=2.2

This can be read as: "Version must be larger than 2 (inclusive) and less than 3
(exclusive) and cannot be 2.2."

It's possible however for these lists to be redundant:

*  >2 >=2.1 <4 !=4.5

The inequalities >2 and !=4.5 are redundant: >2 can be omitted since if >=2.1
is satsified,  >2 is always satisfied. !=4.5 can be omitted because it will
always be true if <4 is satisfied. In other words, given >2 >=2.1 <4 !=4.5, the
minimum list of equivalent inequalities is >=2.1 <4.

Gotcha: The input may not stri tly be a subset of the output, e.g. ">3 !=3" is
equivalent to ">3".

Challenge: Write a program that reads a list of whitespace-separated
inequalities on a single line from raw_input and prints the minimum list of
inequalities that satisfies the same requirement. The program should read one
input line and produce one output line and then exit. If the inequalities are
unsatisfiable (e.g. "<1 >2"), print "unsatisfiable".

E-mail your solution to [pycon2014@twitter.com](mailto:pycon2014@twitter.com)
as an attachment named 'solution.py' by midnight Saturday for a chance to win
cool Twitter swag!
