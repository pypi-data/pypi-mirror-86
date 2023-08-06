from abstraction.models import Object 



class Color (Object): pass
class Blue (Color): pass
class Red (Color): pass
class Green (Color): pass


class A(Object): pass 
class B(A): pass 
class C(B): pass


Color()
Blue()
Red()
Green()

A()
B()
C()



print ()
print ("Blue:", Blue.objects)
print ("Red:", Red.objects)
print ("Green:", Green.objects)
print ("Color:", Color.objects)

print ()
print ("C:", C.objects)
print ("B:", B.objects)
print ("A:", A.objects)

print ()
print ("Object:", Object.objects)

Object()
Object()
Object()
Color()
B()

print ()
print ("Object:", Object.objects)








"""
### Output ###

Blue: [<Blue>]
Red: [<Red>]
Green: [<Green>]
Color: [<Color>, <Blue>, <Red>, <Green>]

C: [<C>]
B: [<B>, <C>]
A: [<A>, <B>, <C>]

Object: [<Color>, <Blue>, <Red>, <Green>, <A>, <B>, <C>]

Object: [<Color>, <Blue>, <Red>, <Green>, <A>, <B>, <C>, <Object>, <Object>, <Object>, <Color>, <B>]
"""