import numpy as np
import random
import time
import matplotlib.pyplot as plt

class generate_map:
    def __init__(self,map_lenx = 50, map_leny = 50):
        self._map_size = [map_lenx,map_leny]
        self._map=np.zeros([self._map_size[0],self._map_size[1]])
        self._init_start_and_target_node()
        self._init_obs(obs_num=[8,8,8])
    def _init_start_and_target_node(self):
        """
        initialize start node and target node
        """
        # four corners
        left_top = [8,8]
        left_down = [8,self._map_size[1]-8]
        right_top = [self._map_size[0]-8,8]
        right_down = [self._map_size[0]-8,self._map_size[1]-8]
        position = [left_top,left_down,right_top,right_down]
        # select start seed and target seed
        seed1 = random.random()*3.9
        st_seed = position[int(seed1)]    # start seed
        position.pop(int(seed1))
        time.sleep(0.01)
        seed2 = random.random()*2.9
        tt_seed = position[int(seed2)]      # target seed
        # randomly shift the two node
        time.sleep(0.01)
        x_shift = np.floor(random.random()*8)-4
        time.sleep(0.01)
        y_shift = np.floor(random.random()*8)-4
        self._start_node = [int(st_seed[0]+x_shift),int(st_seed[1]+y_shift)]
        time.sleep(0.01)
        x_shift = np.floor(random.random()*8)-4
        time.sleep(0.01)
        y_shift = np.floor(random.random()*8)-4
        self._target_node = [int(tt_seed[0]+x_shift),int(tt_seed[1]+y_shift)]

    def _init_obs(self,obs_num):
        """
        initialize all obstacles
        :param obs_num: number of obstacles. [rectangle, circle, T]
        """
        for i in range(obs_num[0]):
            try:
                x = np.floor(random.random() * (self._map_size[0] - 1))
                y = np.floor(random.random() * (self._map_size[1] - 1))
                len_x = np.floor(random.random() * 10)
                len_y = np.floor(random.random() * 10)
                # print('rect: ',x,y,len_x,len_y)
                self._rect_obs([int(x),int(y)],len_x,len_y)
            except:
                # print('error:','-'*30)
                continue
        for i in range(obs_num[1]):
            try:
                x = np.floor(random.random() * (self._map_size[0] - 1))
                y = np.floor(random.random() * (self._map_size[1] - 1))
                r = np.floor(random.random() * 5)
                # print('circle: ',x,y,r)
                self._cir_obs([int(x),int(y)],r)
            except:
                # print('error:','-'*30)
                continue
        for i in range(obs_num[2]):
            try:
                x = np.floor(random.random() * (self._map_size[0] - 1))
                y = np.floor(random.random() * (self._map_size[1] - 1))
                len_x = np.floor(random.random() * 3)
                len_y = np.floor(random.random() * 5)
                # print('T: ',x,y,len_x,len_y)
                self._T_obs([int(x),int(y)],len_x,len_y)
            except:
                # print('error:','-'*30)
                continue
    def _rect_obs(self,pos,len_x,len_y):
        """
        generate a rectangle obstacle
        :param pos: center position, [x,y], type: int
        :param len_x: length of rectangle in x, type: int
        :param len_y: length of rectangle in y, type: int
        """
        # x
        left = np.floor(pos[0] - len_x/2)
        left = max(0,left)
        right = left+len_x
        right = min(self._map_size[0]-1,right)
        # y
        top = int(np.floor(pos[1] - len_y/2))
        top = max(0,top)
        down = top + len_y
        down = min(self._map_size[1]-1,down)
        # prevention of covering start or target node.
        for x in range(int(left),int(right)):
            for y in range(int(top),int(down)):
                if x == self._start_node[0] and y == self._start_node[1]:
                    return
                if x == self._target_node[0] and y == self._target_node[1]:
                    return
        # fill up map
        for x in range(int(left),int(right)):
            for y in range(int(top),int(down)):
                self._map[x][y] = 1

    def _cir_obs(self,pos,r):
        """
        generate a circle obstacle
        :param pos: center position of circle, [x,y], type: int
        :param r: radius, type: int
        """
        # prevention of cross boundary
        r = min(r,pos[0]-0)
        r = min(r,pos[1]-0)
        r = min(r,self._map_size[0]-pos[0])
        r = min(r,self._map_size[1]-pos[1])
        # prevention of covering start or target node.
        for x in range(int(pos[0]-r),int(pos[0]+r)):
            for y in range(int(pos[1]-r),int(pos[1]+r)):
                if x == self._start_node[0] and y == self._start_node[1]:
                    return
                if x == self._target_node[0] and y == self._target_node[1]:
                    return
        # fill up map
        for x in range(int(pos[0]-r),int(pos[0]+r)):
            for y in range(int(pos[1]-r),int(pos[1]+r)):
                if (x-pos[0])**2+(y-pos[1])**2<=r**2:
                    self._map[x][y]=1

    def _T_obs(self,pos,len_x,len_y):
        """
        generate a obstacle like a word "T"
        :param pos: [x,y] x is the center of the horizontal line, while y is the top of the perpendicular line.
        :param len_x: half length of horizontal line
        :param len_y: length of perpendicular line
        """
        # prevention of cross boundary
        len_x = min(pos[0]-0,len_x)
        len_x = min(self._map_size[0]-pos[0],len_x)
        len_y = min(len_y,self._map_size[1]-pos[1])
        # prevention of covering start or target node.
        for x in range(int(pos[0]-len_x),int(pos[0]+len_x)):
            if x == self._start_node[0] and pos[1] == self._start_node[1]:
                return
        for y in range(int(pos[1]),int(pos[1]+len_y)):
            if pos[0] == self._target_node[0] and y == self._target_node[1]:
                return
        # fill up map
        for x in range(int(pos[0]-len_x),int(pos[0]+len_x)):
            self._map[x][pos[1]] = 1
        for y in range(int(pos[1]),int(pos[1]+len_y)):
            self._map[pos[0]][y] = 1

    def get_start_node(self):
        return self._start_node
    def get_target_node(self):
        return self._target_node
    def get_map_size(self):
        return self._map_size

    def get_map(self):
        """
        :return: generated map
        """
        return self._map

    def show_map(self,straight_path=[],crooked_path=[]):
        """
        show the map
        """
        pic = plt.figure(figsize=[15,15])
        plt.axis('scaled')
        plt.xlim(-3,55)
        plt.ylim(-3,55)
        plt.grid()

        for x in range(self._map_size[0]):
            for y in range(self._map_size[1]):
                if self._map[x][y] == 1:
                    plt.scatter(x,y,color='black',marker=',',linewidths=8)
        for pos in straight_path:
            plt.scatter(pos[0],pos[1],color='green', marker='o')

        if straight_path != []:
            straight_x = []
            straight_y = []
            for pos in straight_path:
                straight_x.append(pos[0])
                straight_y.append(pos[1])
            plt.plot(straight_x,straight_y,color='green')

        if crooked_path != []:
            crooked_x = []
            crooked_y = []
            for pos in crooked_path:
                crooked_x.append(pos[0])
                crooked_y.append(pos[1])
            plt.plot(crooked_x,crooked_y,color='purple')
        plt.scatter(self._start_node[0],self._start_node[1],color='red')
        plt.scatter(self._target_node[0],self._target_node[1],color='blue')
        plt.show()


if __name__ == '__main__':
    st=time.time()
    map=generate_map()
    real_map=map.get_map()
    # print(real_map)
    print('time for generate a new map',time.time()-st)
    map.show_map()
