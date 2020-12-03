#!/usr/bin/env python
# -*- coding: utf-8 -*-



class Tri_b_spline():
    def __init__(self,x,y,m,p=3):
        """
        :param x: list of x
        :param y: list of y
        :param m: number of control points
        :param p: cubic spline
        """
        self.x=x
        self.y=y
        # print(self.x)
        self.m=m
        self.p=p
        # print(self.x)
        # print(self.y)

        self.set_param()

    def set_param(self):
        self.x_new=[]
        self.y_new=[]
        self.arg = [[-1, 3, -3, 1], [3, -6, 0, 4], [-3, 3, 3, 1], [1, 0, 0, 0]]

    def Ba(self,t, coefficient):
        # print(float((coefficient[0] * t ** 3 + coefficient[1] * t ** 2 + coefficient[2] * t + coefficient[3]) / 6))
        return float((coefficient[0] * t ** 3 + coefficient[1] * t ** 2 + coefficient[2] * t + coefficient[3])*0.166666666667)

    def creat(self,n):
        for i in range(21):
            # print("i:",i)
            t = float(i * 0.05)
            # print('t:',t)
            # print(self.x[n+0],self.x[n+1],self.x[n+2],self.x[n+3])

            self.x_new.append(
                self.x[n + 0] * self.Ba(t, self.arg[0]) + self.x[n + 1] * self.Ba(t, self.arg[1]) + self.x[n + 2] * self.Ba(t, self.arg[2]) + self.x[n + 3] * self.Ba(t,self.arg[3]))
            self.y_new.append(
                self.y[n + 0] * self.Ba(t, self.arg[0]) + self.y[n + 1] * self.Ba(t, self.arg[1]) + self.y[n + 2] * self.Ba(t, self.arg[2]) + self.y[n + 3] * self.Ba(t, self.arg[3]))

    def run(self):
        for i in range(self.m-self.p):
            self.creat(i)
        # print('B-spline,x_new,y_new:')
        # print(len(self.x_new))
        # print(self.x_new)
        # print(self.y_new)
        # print('-'*30)

def run(path):
    x=[]
    y=[]
    x.append(path[i][0] for i in range(len(path)))
    y.append(path[i][1] for i in range(len(path)))
    temp=Tri_b_spline(x,y,len(x))
    temp.run()
    path=[]
    for i in range(len(temp.x_new)):
        path.append([temp.x_new[i],temp.y_new[i]])
    return path

if __name__ == '__main__':
    x=[0,1,2,3,4,5]
    y=[0,-1,1,-1,1,0]
    temp=Tri_b_spline(x,y,len(x))
    temp.run()
    print(temp.x_new)
