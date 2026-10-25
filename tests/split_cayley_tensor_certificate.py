#!/usr/bin/env python3
"""Exact coefficient certificates for finite-field split Cayley tensor identities.

Requires SymPy. Assertions are polynomial equalities over Z[1/2], hence
transfer to fields of odd characteristic. They do not use floating point.
"""
import sympy as sp

def dot(x,y):
    return sum((a*b for a,b in zip(x,y)),sp.Integer(0))

def cross(x,y):
    return (x[1]*y[2]-x[2]*y[1],
            x[2]*y[0]-x[0]*y[2],
            x[0]*y[1]-x[1]*y[0])

def add(x,y):
    return (x[0]+y[0],
            tuple(a+b for a,b in zip(x[1],y[1])),
            tuple(a+b for a,b in zip(x[2],y[2])),x[3]+y[3])

def mul(x,y):
    a,u,v,b=x;c,w,z,d=y
    return (a*c+dot(u,z),
            tuple(a*w[i]+d*u[i]+cross(v,z)[i] for i in range(3)),
            tuple(c*v[i]+b*z[i]-cross(u,w)[i] for i in range(3)),
            b*d+dot(v,w))

def smul(a,x):
    return (a*x[0],tuple(a*t for t in x[1]),
            tuple(a*t for t in x[2]),a*x[3])

def sub(x,y):
    return add(x,smul(-1,y))

def norm(x):
    return x[0]*x[3]-dot(x[1],x[2])

def B(x,y):
    return (x[0]*y[3]+y[0]*x[3]-dot(x[1],y[2])-dot(y[1],x[2]))/2

def pure(a):
    return (a[0],a[1:4],a[4:7],-a[0])

def cpure(x,y):
    return smul(sp.Rational(1,2),sub(mul(x,y),mul(y,x)))

def assoc(x,y,z):
    return sub(mul(mul(x,y),z),mul(x,mul(y,z)))

def check(name, polynomials):
    for e in polynomials:
        if sp.expand(e)!=0:
            raise AssertionError(f"{name}: {sp.expand(e)}")
    print("PASS:", name)

def coords(x):
    return (x[0],*x[1],*x[2],x[3])

def main():
    sym=sp.symbols("x0:7 y0:7 z0:7")
    X,Y,Z=(pure(sym[i*7:(i+1)*7]) for i in range(3))
    g=sp.symbols("a b c d e f g h j k l m n p r s")
    def general(start):
        a=g[start:start+8]
        return (a[0],a[1:4],a[4:7],a[7])
    P,Q=general(0),general(8)
    check("Zorn norm composition",[norm(mul(P,Q))-norm(P)*norm(Q)])
    conj=lambda x:(x[3],tuple(-t for t in x[1]),tuple(-t for t in x[2]),x[0])
    one=(sp.Integer(1),(0,0,0),(0,0,0),sp.Integer(1))
    check("conjugation norm law",
          [a-b for r in (mul(P,conj(P)),mul(conj(P),P))
           for a,b in zip(coords(r),coords(smul(norm(P),one)))])
    check("left alternativity",
          [a-b for a,b in zip(coords(mul(mul(X,X),Y)),
                              coords(mul(X,mul(X,Y))))])
    check("right alternativity",
          [a-b for a,b in zip(coords(mul(mul(Y,X),X)),
                              coords(mul(Y,mul(X,X))))])
    check("Moufang middle",
          [a-b for a,b in zip(coords(mul(mul(X,Y),mul(Z,X))),
                              coords(mul(mul(X,mul(Y,Z)),X)))])
    T=cpure(X,Y)
    check("cross norm & orthogonality",
          [norm(T)-norm(X)*norm(Y)+B(X,Y)**2,B(T,X),B(T,Y)])
    phi=lambda x,y,z:B(cpure(x,y),z)
    check("alternating 3-form",
          [phi(X,Y,Z)+phi(Y,X,Z),phi(X,Y,Z)+phi(X,Z,Y)])
    K2=cpure(X,cpure(X,Z))
    K2goal=sub(smul(B(X,Z),X),smul(norm(X),Z))
    check("cross operator quadratic identity",
          [a-b for a,b in zip(coords(K2),coords(K2goal))])
    t=sp.symbols("t")
    D=1+t*t*norm(X)
    def rotor_num(z):
        return add(sub(smul(D,z),smul(2*t,cpure(X,z))),
                   smul(2*t*t,cpure(X,cpure(X,z))))
    check("guarded rational isometry polynomial kernel",
          [B(rotor_num(Y),rotor_num(Z))-D*D*B(Y,Z)])
    mat=[[B(u,v) for v in (X,Y,Z)] for u in (X,Y,Z)]
    det=sp.det(sp.Matrix(mat),method="berkowitz")
    check("associator Gram/phi norm",
          [norm(assoc(X,Y,Z))-4*(det-phi(X,Y,Z)**2)])
    u,v,w,a,b,c=sp.symbols("u v w a b c")
    L=u*v*w
    s1=1-a*a/(u*v);s2=1-b*b/(v*w);s3=1-c*c/(w*u)
    defect=(s1+s2+s3)**2-2*(s1*s1+s2*s2+s3*s3)-4*s1*s2*s3
    delta_plus=L+2*a*b*c-w*a*a-u*b*b-v*c*c
    delta_minus=L-2*a*b*c-w*a*a-u*b*b-v*c*c
    check("triple-spread defect cleared polynomial",
          [sp.cancel(defect*L*L+delta_plus*delta_minus)])
    print("All exact coefficient certificates passed.")

if __name__=="__main__":
    main()
