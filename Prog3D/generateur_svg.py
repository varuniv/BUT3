#!/usr/bin/env python
import svgwrite
from math import *


def translater(input, vectTrans):
  x,y=input
  tx,ty=vectTrans
  return ((x+tx,y+ty))

def rotation10(angle):
 return (cos(angle), sin(angle))

def rotation01(angle):
    return (sin(angle), cos(angle))

def rotation(point, angle):
 x, y = point
 v1x,v1y =rotation10(angle)
 v2x, v2y = rotation01(angle)


 out=(x*v1x+y*v1y, -x*v2x+y*v2y)
 return out


def prodMatVect(Mat, Vect ):
    x, y = Vect
    ( (a11,a12), (a21, a22) ) = Mat

    x2 = a11 * x + a12 * y
    y2 = a21 * x + a22 * y

    return (x2,y2)


def Matrotation(angle):
     return (((cos(angle), sin(angle)),
                    (-sin(angle), cos(angle))))


def Matdilatation(coefDilatation):
  return ((coefDilatation,0),
                  (0, coefDilatation))

def dilatation(point, coefDilatation):
 x, y = point
 matDilat=Matdilatation(coefDilatation)
 out=prodMatVect(matDilat, point)
 return out

def prodMatMat(MatA, MatB ):

   ( (a11,a12), (a21, a22) ) = MatA
   ( (B11,B12), (B21, B22) ) = MatB

   return ( (a11*B11+a12* B21 , a11*B12+a12*B22  ), (  a21*B11+a22*B21 , a21*B12+a22*B22   ) )



#exercice 1
dessin  = svgwrite.Drawing('exercice_1.svg', size=(800,600))
triangle=[(0,300),(400,300),(200,0)]
carre=[(0,0),(100,0),(100,100),(0,100)]
dessin.add(dessin.polygon(carre, fill="#09FF00",\
                          stroke="#000000", opacity=0.7 ))
dessin.add(dessin.polygon(triangle, fill="#FF0000",\
                          stroke="#000000", opacity=0.7 ))
dessin.save()

#exercice 2
dessin = svgwrite.Drawing('exercice_carre_trans.svg', size=(800,600))

carre=[(-100,-100),(100,-100),(100,100),(-100,100)]

trans=(200,200)


carre_out=[translater(sommet,trans) for sommet in carre]

dessin.add(dessin.polygon(carre_out, fill="#FFFFFF", stroke="#000000", opacity=0.7))

angle=pi/10

carre_trans=[rotation(sommet,angle) for sommet in carre]

dessin.add(dessin.polygon(carre_trans, fill='#FF0000',stroke="#000000", opacity=0.7))



dessin.save()


#exercice 3
dessin = svgwrite.Drawing('question3.svg', size=(800,600))
carre=[(-50,-50),(50,-50),(50,50),(-50,50)]
for i in range(5):
  caree_dil=[translater(prodMatVect(Matdilatation(0.5**i),sommet),(i*100+50,50)) for sommet in carre]
  dessin.add(dessin.polygon(caree_dil, fill="#D400FF", stroke="#000000", opacity=0.7))
dessin.save()

#exercice 4
dessin = svgwrite.Drawing('question4.svg', size=(800,600))
carre=[(-50,-50),(50,-50),(50,50),(-50,50)]
for i in range(5):
   caree_dil=[translater(prodMatVect(Matdilatation(0.5**i),sommet),(100,100)) for sommet in carre]
   dessin.add(dessin.polygon(caree_dil, fill="#D400FF", stroke="#000000", opacity=0.7))
dessin.save()



matModelisation=prodMatMat(Matrotation(angle),Matdilatation(0.5))
carre_out=[translater(prodMatVect(matModelisation,sommet),trans) for sommet in carre]



#Chat 
dessin = svgwrite.Drawing('chat.svg', size=(800,600))
aux=100
points=[(aux, aux),(-aux, aux),(-aux, -aux),(aux, -aux)]
triangles=[0,1,2,0,2,3]



def compose(points,triangles):
  liste_point=[]
  colors=("blue","red","green","purple","yellow","white","coral","darkblue")
  for i in range(0,len(triangles)//3):
      print(triangles[3*i],triangles[3*i+1],triangles[3*i+2])
      dessin.add(dessin.polygon((points[triangles[3*i]],points[triangles[3*i+1]],points[triangles[3*i+2]]), fill=colors[(i%(len(colors)*2))//2],  opacity=0.5,stroke='black'))

points=[(0,50),(-100, 0),(-100, -70),(-50, 0),(0,-30),(50,0),(100,-70),(100,0)]
triangles=[0,1,7,1,2,3,3,4,5,5,6,7]
translation = [translater(point,(200,200)) for point in points]
#compose(translation,triangles)
for i in range(5):
    angle = (pi / 6) *i
    dilatation=Matdilatation(0.8)
    rotation_mat = Matrotation(angle)
    rotated_points = [prodMatVect(rotation_mat, point) for point in points]
    trans=[translater(prodMatVect(Matdilatation(0.5**i),sommet),(100*i+200,200)) for sommet in rotated_points]
    compose(trans, triangles)
dessin.save()



#Cube
dessin = svgwrite.Drawing('cube.svg', size=(800,600))
aux=100
points=[[-aux, -aux, aux], #point 0 (face devant)
        [-aux, aux, aux],#point 1   (face devant)
        [aux, -aux, aux],#point 2   (face devant)
        [aux, aux, aux],#point 3    (face devant)
        [-aux, -aux, -aux],#point 4 (face arrière)
        [-aux,aux,-aux],#point 5
        [aux,-aux,-aux],#point 6
        [aux,aux,-aux]#point 7
        ]
cube=[0,1,2,   #triangle 1 face 1 (devant)
    1,2,3,     #triangle 2 face 1
    4,5,6,     #triangle 1 face 2 (arriere)
    5,6,7,     #triangle 2 face 2
    0,1,5,     #triangle 1 face 3 (gauche)
    0,4,5,     #triangle 2 face 3
    2,3,7,     #triangle 1 face 4 (droite)
    2,6,7,     #triangle 2 face 4
    1,3,7,     #triangle 1 face 5 (haut)
    1,5,7,     #triangle 2 face 5
    0,2,6,     #triangle 1 face 6 (bas)
    0,4,6      #triangle 2 face 6
    ]

def projection(point3d):
    return((point3d[0],point3d[1]))

def centrage(point, direction):
    x, y, z = point
    dx, dy, dz = direction
    return (x + dx, y + dy, z + dz)


def prodMatVect3D(Mat, Vect ):
    x, y,z = Vect
    ( (a11,a12,a13), (a21, a22,a23), (a31, a32,a33) ) = Mat

    x2 = a11 * x + a12 * y+ a13 * z
    y2 = a21 * x + a22 * y+ a23 * z
    z2 = a31 * x + a32 * y+ a33 * z

    return (x2,y2,z2)

def prodMatMat3D(MatA, MatB ):

    ( (a11,a12,a13),
    (a21, a22,a23),
    (a31, a32,a33) )  = MatA

    ( (b11,b12,b13),
    (b21, b22,b23),
    (b31, b32,b33) )  = MatB

    return ( (a11*b11+a12* b21+a13*b31 , a11*b12+a12* b22+a13*b32,a11*b13+a12* b23+a13*b33  ),
     (  a21*b11+a22* b21+ a23*b31, a21*b12+a22* b22 +a23*b32,  a21*b13+a22* b23+a23*b33),
     (  a31*b11+a32* b21+ a33*b31, a31*b12+a32* b22 +a33*b32,  a31*b13+a32* b23+a33*b33))

def Matdilatation3D(coefDilatation):
         return ((coefDilatation,0,0),
                         (0, coefDilatation , 0),
                         (0, 0,coefDilatation))

def Matrotation3DY(angle):
     return (
            (cos(angle), 0,sin(angle)),
            (0,1,0,),
            (-sin(angle),0, cos(angle)))

points_proj = [projection(centrage(sommet,(100,100,100))) for sommet in points ]
compose(points_proj,cube)
dessin.save()