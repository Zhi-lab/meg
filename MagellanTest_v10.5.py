import random
import math

maze = [[1,0,1,0,4,0,1,0,1,0,1],
        [0,0,0,0,0,0,0,0,0,0,0],
        [1,0,1,0,1,0,1,0,1,0,1],
        [0,0,0,0,0,0,0,0,0,0,0],
        [3,0,1,0,1,0,1,0,1,0,6],
        [0,0,0,0,0,0,0,0,0,0,0],
        [1,0,1,0,1,0,1,0,1,0,1],
        [0,0,0,0,0,0,0,0,0,0,0],
        [1,0,1,0,1,0,5,0,1,0,1],
        [0,0,0,0,0,0,0,0,0,0,0],
        [2,0,1,0,1,0,1,0,1,0,1]]

subject_map = [[0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0]]

passenger_map = [[0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0]]

#agent的位置、头朝向、视觉参数、记忆参数、总体目标、下一步目标、有无乘客、已送乘客数量
class Agent:
    row = 0
    column = 0
    direction = 0 #1北2南3西4东
    vision = 1
    memory = 32
    passenger_memory = 600
    final_des = [0,0]
    next_des = [0,0]
    deliver = 0 #0代表无乘客，1代表有乘客
    passenger_num = 0

#某些常用变量：每一行建筑数量；乘客数量；步长；store数量
blockEachLine = 6
passengerTotal = 15
step = 2
storeNum = 5

#存储store位置
class MazePos:
    store = []
    #i为行，j为列，k为store的标签
    for i in range(0,blockEachLine*2-1):
        for j in range(0,blockEachLine*2-1):
            for k in range(2,2+storeNum):
                if maze[i][j] == k:
                    store.append([i,j])
#print(MazePos.store)

#存储passenger位置和passenger的目的地。store和下一个passenger不能在一条线上
passenger = []
passenger_des = []
for i in range(0,passengerTotal):
    passenger.append([0,0])
    passenger_des.append(([0,0]))
passenger[0] = [2*random.randint(1,5)-1,2*random.randint(1,5)-1]
def passenger_destination():
    global passenger
    global passenger_des
    #以随机顺序遍历完所有store之后，才会开始下一轮store的遍历
    store_block1 = store_block2 = store_block3 = [0,1,2,3,4]
    random.shuffle(store_block1)
    random.shuffle(store_block2)
    random.shuffle(store_block3)
    for i in range(0,int(passengerTotal/3)):
        passenger_des[i] = MazePos.store[store_block1[i]]
    for i in range(int(passengerTotal/3),int(passengerTotal*2/3)):
        passenger_des[i] = MazePos.store[store_block2[i-int(passengerTotal/3)]]
    for i in range(int(passengerTotal*2/3),passengerTotal):
        passenger_des[i] = MazePos.store[store_block3[i-int(passengerTotal*2/3)]]
    #根据上一个passenger的目的地，设置下一个passenger的出现位置
    for j in range(1,passengerTotal):
        passenger[j] = [2 * random.randint(1, 5) - 1, 2 * random.randint(1, 5) - 1]
        while abs(passenger[j][0] - passenger_des[j-1][0]) == 1 or abs(passenger[j][1] - passenger_des[j-1][1] == 1):
            passenger[j] = [2 * random.randint(1, 5) - 1, 2 * random.randint(1, 5) - 1]

#初始化agent位置、头朝向、目标
def init_agent():
    Agent.row = passenger[0][0]
    Agent.column = passenger[0][1]
    Agent.final_des = passenger[0]
    Agent.next_des = passenger[0]
    Agent.direction = random.randint(1,4)
    #如果agent的初始位置在边界上，头朝向墙壁，那么把头转向相反的方向
    if Agent.row == blockEachLine*2-3 and Agent.direction == 1:
        Agent.direction = Agent.direction + 1
    elif Agent.row == 0 and Agent.direction == 2:
        Agent.direction = Agent.direction - 1
    elif Agent.column == blockEachLine*2-3 and Agent.direction == 3:
        Agent.direction = Agent.direction + 1
    elif Agent.column == 0 and Agent.direction == 4:
        Agent.direction = Agent.direction - 1
    #agent最开始出现在passenger[0]的位置上，这里根据头朝向，把agent移开一步
    if Agent.direction == 1:
        Agent.row = Agent.row + step
    elif Agent.direction == 2:
        Agent.row = Agent.row - step
    elif Agent.direction == 3:
        Agent.column = Agent.column + step
    elif Agent.direction == 4:
        Agent.column = Agent.column - step

#确定要加入模块的建筑，并将这些建筑的记忆强度设为1
def v_module():
    global subject_map
    #把agent斜前方的建筑加入认知地图模块（具体加入几排，取决于vision参数）
    for i in range(1,Agent.vision+1):
        if Agent.direction == 1:
            subject_map[Agent.row - i][Agent.column - 1] = 1
            subject_map[Agent.row - i][Agent.column + 1] = 1
        elif Agent.direction == 2:
            subject_map[Agent.row + i][Agent.column - 1] = 1
            subject_map[Agent.row + i][Agent.column + 1] = 1
        elif Agent.direction == 3:
            subject_map[Agent.row - 1][Agent.column - i] = 1
            subject_map[Agent.row + 1][Agent.column - i] = 1
        elif Agent.direction == 4:
            subject_map[Agent.row - 1][Agent.column + i] = 1
            subject_map[Agent.row + 1][Agent.column + i] = 1

#subject_map的遗忘
def forget():
    for i in range(0,blockEachLine):
        for j in range(0,blockEachLine):
            if subject_map[2*i][2*j] > 0:
                subject_map[2*i][2*j] = subject_map[2*i][2*j] - 1/Agent.memory

#agent移动一步，并遗忘（只有移动了才会遗忘）。如果agent已经在边界上，并且头朝向边界，则不会移动
def move():
    if Agent.direction == 1 and Agent.row > 1:
        Agent.row = Agent.row - step
        forget()
    elif Agent.direction == 2 and Agent.row < blockEachLine*2-3:
        Agent.row = Agent.row + step
        forget()
    elif Agent.direction == 3 and Agent.column > 1:
        Agent.column = Agent.column - step
        forget()
    elif Agent.direction == 4 and Agent.column < blockEachLine*2-3:
        Agent.column = Agent.column + step
        forget()

#地图边界检测
def judge_edge():
    #agent位于建筑之间，而subject_map的边界可能不平整，所以dist1、dist2分别表示东方边界上，agent南北两行建筑离agent的距离。
    dist1 = dist2 = dist3 = dist4 = dist5 = dist6 = dist7 = dist8 = 0
    #检测subject_map东方和南方的边界
    for i in range(0,blockEachLine*2-1):
        if subject_map[Agent.row+1][i] > 0:
            dist1 = i-Agent.column
        if subject_map[Agent.row-1][i] > 0:
            dist2 = i-Agent.column
        if subject_map[i][Agent.column+1] > 0:
            dist3 = i-Agent.row
        if subject_map[i][Agent.column-1] > 0:
            dist4 = i-Agent.row
    dist_east = min(dist1,dist2)
    dist_south = min(dist3,dist4)
    #如果subject_map的边界就在城镇的边界上，那么被试离该边界的距离无穷大
    if dist_east == (blockEachLine*2-2)-Agent.column:
        dist_east = math.inf
    if dist_south == (blockEachLine*2-2)-Agent.row:
        dist_south = math.inf
    #检测subject_map北方和西方的边界
    for i in range(0,blockEachLine*2-1):
        if subject_map[Agent.row+1][i] > 0:
            dist5 = Agent.column-i
            break
    for i in range(0,blockEachLine*2-1):
        if subject_map[Agent.row-1][i] > 0:
            dist6 = Agent.column-i
            break
    for i in range(0,blockEachLine*2-1):
        if subject_map[i][Agent.column+1] > 0:
            dist7 = Agent.row-i
            break
    for i in range(0,blockEachLine*2-1):
        if subject_map[i][Agent.column-1] > 0:
            dist8 = Agent.row-i
            break
    dist_west = min(dist5,dist6)
    dist_north = min(dist7,dist8)
    if dist_west == Agent.column:
        dist_west = math.inf
    if dist_north == Agent.row:
        dist_north = math.inf
    #dist_list用于存放agent离subject_map四个边界的距离
    dist_list = (dist_north,dist_south,dist_west,dist_east)
    #取dist_list中四个距离的最小值，返回对应方向的头朝向。如果同时有几个最小值，随机返回其中一个方向对应的头朝向
    #如果此时agent在边界上，那么其离该边界的距离应为inf，所以头朝向不会取向该边界
    return_list = []
    if min(dist_list) == dist_north:
        return_list.append(1)
    if min(dist_list) == dist_south:
        return_list.append(2)
    if min(dist_list) == dist_west:
        return_list.append(3)
    if min(dist_list) == dist_east:
        return_list.append(4)
    return_num = random.choice(return_list)
    return return_num

#路线规划和下一步目标（头朝向）的设置
def r_module():
    short_route = [0,0]
    if Agent.final_des:
        #如果目标不为空，则生成最短路径
        if Agent.deliver == 0:
            short_route = [Agent.final_des[0]-Agent.row, Agent.final_des[1]-Agent.column]
        if Agent.deliver == 1:
            if Agent.final_des[0]-Agent.row > 0 and Agent.final_des[1]-Agent.column > 0:
                short_route = [Agent.final_des[0]-Agent.row-1, Agent.final_des[1]-Agent.column-1]
            if Agent.final_des[0]-Agent.row > 0 and Agent.final_des[1]-Agent.column < 0:
                short_route = [Agent.final_des[0]-Agent.row-1, Agent.final_des[1]-Agent.column+1]
            if Agent.final_des[0]-Agent.row < 0 and Agent.final_des[1]-Agent.column < 0:
                short_route = [Agent.final_des[0]-Agent.row+1, Agent.final_des[1]-Agent.column+1]
            if Agent.final_des[0]-Agent.row < 0 and Agent.final_des[1]-Agent.column > 0:
                short_route = [Agent.final_des[0]-Agent.row+1, Agent.final_des[1]-Agent.column-1]
        # 规划沿着最短路径的下一步（即确定头朝向）
        if short_route[0] > 0 and short_route[1] > 0:
            Agent.direction = random.choice([2,4])
        if short_route[0] > 0 and short_route[1] < 0:
            Agent.direction = random.choice([2,3])
        if short_route[0] < 0 and short_route[1] < 0:
            Agent.direction = random.choice([1,3])
        if short_route[0] < 0 and short_route[1] > 0:
            Agent.direction = random.choice([1,4])
        if short_route[0] == 0 and short_route[1] > 0:
            Agent.direction = 4
        if short_route[0] == 0 and short_route[1] < 0:
            Agent.direction = 3
        if short_route[0] > 0 and short_route[1] == 0:
            Agent.direction = 2
        if short_route[0] < 0 and short_route[1] == 0:
            Agent.direction = 1
    #如果目标为空，则调用边界检测函数，确定头朝向
    if not Agent.final_des:
        Agent.direction = judge_edge()

#--------------------------------------------------------------
#寻找乘客（启用passenger_map）
#每次开始寻找乘客，都需要刷新passenger_map
def init_find_passenger():
    global passenger_map
    passenger_map = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
#将自己所在的格子和自己前面vision格加入passenger_map（vision为视觉参数）
def passenger_v_module():
    for i in range(0,Agent.vision+1):
        if Agent.direction == 1:
            passenger_map[Agent.row - i][Agent.column] = 1
        elif Agent.direction == 2:
            passenger_map[Agent.row + i][Agent.column] = 1
        elif Agent.direction == 3:
            passenger_map[Agent.row][Agent.column - i] = 1
        elif Agent.direction == 4:
            passenger_map[Agent.row][Agent.column + i] = 1

def passenger_forget():
    for i in range(0,blockEachLine-1):
        for j in range(0,blockEachLine-1):
            if passenger_map[2*i+1][2*j+1] > 0:
                passenger_map[2*i+1][2*j+1] = passenger_map[2*i+1][2*j+1] - 1/Agent.passenger_memory
#每走一步就遗忘。采用passenger_memory作为遗忘参数
def passenger_move():
    if Agent.direction == 1 and Agent.row > 1:
        Agent.row = Agent.row - step
        forget()
    elif Agent.direction == 2 and Agent.row < blockEachLine*2-3:
        Agent.row = Agent.row + step
        forget()
    elif Agent.direction == 3 and Agent.column > 1:
        Agent.column = Agent.column - step
        forget()
    elif Agent.direction == 4 and Agent.column < blockEachLine*2-3:
        Agent.column = Agent.column + step
        forget()

#找乘客时的寻路和送乘客时不同。只要agent相邻的格子有未探索过的（记忆强度为0），则走向这个方向。如果有>=2个方向未探索过，随机选择一个，
#如果4个方向都未探索过，随机选择一个。
def direction_detection():
    return_list = []
    #如果agent在边界上，那么某些朝向就不能被取到
    if Agent.row < blockEachLine*2-3:
        if passenger_map[Agent.row+step][Agent.column] == 0:
            return_list.append(2)
    if Agent.row > 1:
        if passenger_map[Agent.row-step][Agent.column] == 0:
            return_list.append(1)
    if Agent.column < blockEachLine*2-3:
        if passenger_map[Agent.row][Agent.column+step] == 0:
            return_list.append(4)
    if Agent.column > 1:
        if passenger_map[Agent.row][Agent.column-step] == 0:
            return_list.append(3)
    if not return_list:
        return random.choice([1,2,3,4])
    else:
        return_num = random.choice(return_list)
        return return_num

#如果已经和乘客在同一行或者同一列，则将乘客定为最终目标。否则，将头朝向的下一步定为最终目标
def passenger_final_des_set():
    if Agent.row == passenger[Agent.passenger_num][0] or Agent.column == passenger[Agent.passenger_num][1]:
        Agent.final_des = passenger[Agent.passenger_num]
    else:
        Agent.direction = direction_detection()
        if Agent.direction == 1:
            Agent.final_des = [Agent.row-step,Agent.column]
        if Agent.direction == 2:
            Agent.final_des = [Agent.row+step,Agent.column]
        if Agent.direction == 3:
            Agent.final_des = [Agent.row,Agent.column-step]
        if Agent.direction == 4:
            Agent.final_des = [Agent.row,Agent.column+step]

#初始化passenger_map后进入循环：将格子加入认知地图→移动一步→确定最终目标→根据最终目标规划路线并确定头朝向→...
#到达乘客的位置后跳出函数
def find_passenger():
    init_find_passenger()
    while Agent.deliver == 0:
        passenger_v_module()
        passenger_move()
        passenger_final_des_set()
        r_module()
        if Agent.row == passenger[Agent.passenger_num][0] and Agent.column == passenger[Agent.passenger_num][1]:
            return
            #break
        print([Agent.row,Agent.column])
        print(Agent.direction)
        print(passenger_map)
#--------------------------------------------------------------

#设定agent的最终目标（乘客数量送到之后才会+1）
def final_des_set():
    #找到乘客之后，判断乘客的目标在不在认知地图中，如果在，将其设为最终目标，如果不在，最终目标为空
    if Agent.row == passenger[Agent.passenger_num][0] and Agent.column == passenger[Agent.passenger_num][1] and Agent.deliver == 0:
        Agent.deliver = 1
        if subject_map[passenger_des[Agent.passenger_num][0]][passenger_des[Agent.passenger_num][1]] > 0:
            Agent.final_des = passenger_des[Agent.passenger_num]
        elif subject_map[passenger_des[Agent.passenger_num][0]][passenger_des[Agent.passenger_num][1]] == 0:
            Agent.final_des = None
    #送到乘客之后，调用find_passenger()开始找乘客。跳出find_passenger()后，调用一次自身，从而继续设定最终目标
    if abs(Agent.row - passenger_des[Agent.passenger_num][0]) == 1 and abs(Agent.column - passenger_des[Agent.passenger_num][1]) == 1 and Agent.deliver == 1:
        Agent.deliver = 0
        Agent.passenger_num = Agent.passenger_num+1
        if Agent.passenger_num < passengerTotal:
            find_passenger()
            final_des_set()
            #Agent.final_des = passenger[Agent.passenger_num] #简化版，直接朝乘客走

#just run!
init_agent()
passenger_destination()
while Agent.passenger_num < passengerTotal:
    v_module() #改变了头朝向，所以调用一次V模块
    move()
    v_module() #进行了一次移动，所以调用一次V模块。否则agent就会位于subject_map的边界之外
    final_des_set()
    r_module()
    #print([Agent.row, Agent.column])
    #print(subject_map)