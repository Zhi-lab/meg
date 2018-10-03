import random

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
    x = 0 #x为纵坐标，y为横坐标。二维数组中，x在前，y在后
    y = 0
    direction = 0 #1北2南3西4东
    vision = 1
    memory = 32
    passenger_memory = 600
    final_des = [0,0]
    next_des = [0,0]
    deliver = 0 #0代表无乘客，1代表有乘客
    passenger_num = 0

#某些常用变量
blockEachLine = len(maze)
passengerTotal = 15
step = 2

#存储store位置
class MazePos:
    store = [[0,0],[0,0],[0,0],[0,0],[0,0]]
    for i in range(0,blockEachLine):
        for j in range(0,blockEachLine):
            for k in range(2,7):
                if maze[i][j] == k:
                    store[k-2] = [i,j]
#print(MazePos.store)

#存储passenger位置和passenger的目的地。store和下一个passenger不能在一条线上
passenger = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
passenger[0] = [2*random.randint(1,5)-1,2*random.randint(1,5)-1]
passenger_des = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
def passenger_destination():
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

    for j in range(1,passengerTotal):
        passenger[j] = [2 * random.randint(1, 5) - 1, 2 * random.randint(1, 5) - 1]
        while abs(passenger[j][0] - passenger_des[j-1][0]) == 1 or abs(passenger[j][1] - passenger_des[j-1][1] == 1):
            passenger[j] = [2 * random.randint(1, 5) - 1, 2 * random.randint(1, 5) - 1]

#初始化agent位置、头朝向、目标
def init_agent():
    Agent.x = passenger[0][0]
    Agent.y = passenger[0][1]
    Agent.final_des = passenger[0]
    Agent.next_des = passenger[0]
    Agent.direction = random.randint(1,4)

    if Agent.x == blockEachLine-1 and Agent.direction == 1:
        Agent.direction = Agent.direction + 1
    elif Agent.x == 0 and Agent.direction == 2:
        Agent.direction = Agent.direction - 1
    elif Agent.y == blockEachLine-1 and Agent.direction == 3:
        Agent.direction = Agent.direction + 1
    elif Agent.y == 0 and Agent.direction == 4:
        Agent.direction = Agent.direction - 1

    if Agent.direction == 1:
        Agent.x = Agent.x + step
    elif Agent.direction == 2:
        Agent.x = Agent.x - step
    elif Agent.direction == 3:
        Agent.y = Agent.y + step
    elif Agent.direction == 4:
        Agent.y = Agent.y - step

#初始化乘客信息
def init_passenger():
    passenger_destination()
    for k in range(0,passengerTotal):
        a=passenger[k][0]
        b=passenger[k][1]
        passenger_map[a][b]=k+1

#确定要加入模块的建筑，并将这些建筑的记忆强度设为1
def v_module():
    for i in range(1,Agent.vision+1):
        if Agent.direction == 1:
            subject_map[Agent.x - i][Agent.y - 1] = 1
            subject_map[Agent.x - i][Agent.y + 1] = 1
        elif Agent.direction == 2:
            subject_map[Agent.x + i][Agent.y - 1] = 1
            subject_map[Agent.x + i][Agent.y + 1] = 1
        elif Agent.direction == 3:
            subject_map[Agent.y - i][Agent.x - 1] = 1
            subject_map[Agent.y - i][Agent.x + 1] = 1
        elif Agent.direction == 4:
            subject_map[Agent.y + i][Agent.x - 1] = 1
            subject_map[Agent.y + i][Agent.x + 1] = 1

#subject_map的遗忘
def forget():
    for i in range(0,int(blockEachLine/2)+1):
        for j in range(0,int(blockEachLine/2)+1):
            if subject_map[2*i][2*j] > 0:
                subject_map[2*i][2*j] = subject_map[2*i][2*j] - 1/Agent.memory

#agent移动一步，并遗忘（只有移动了才会遗忘）
def move():
    if Agent.direction == 1 and Agent.x > 1:
        Agent.x = Agent.x - step
        forget()
    elif Agent.direction == 2 and Agent.x < blockEachLine-2:
        Agent.x = Agent.x + step
        forget()
    elif Agent.direction == 3 and Agent.y > 1:
        Agent.y = Agent.y - step
        forget()
    elif Agent.direction == 4 and Agent.y < blockEachLine-2:
        Agent.y = Agent.y + step
        forget()

#设定agent的最终目标（乘客数量送到之后才会+1）
def final_des_set():
    #passenger_destination()
    if Agent.x == passenger[Agent.passenger_num][0] and Agent.y == passenger[Agent.passenger_num][1] and Agent.deliver == 0:
        Agent.deliver = 1
        if subject_map[passenger_des[Agent.passenger_num][0]][passenger_des[Agent.passenger_num][1]] > 0:
            Agent.final_des = passenger_des[Agent.passenger_num]
        elif subject_map[passenger_des[Agent.passenger_num][0]][passenger_des[Agent.passenger_num][1]] == 0:
            Agent.final_des = [999,999]
    if abs(Agent.x - passenger_des[Agent.passenger_num][0]) == 1 and abs(Agent.y - passenger_des[Agent.passenger_num][1]) == 1 and Agent.deliver == 1:
        Agent.deliver = 0
        Agent.passenger_num = Agent.passenger_num+1
        if Agent.passenger_num < passengerTotal:
            Agent.final_des = passenger[Agent.passenger_num] #待改

#地图边界检测
def judge_edge():
    dist1 = dist2 = dist3 = dist4 = dist5 = dist6 = dist7 = dist8 = 0
    for i in range(0,blockEachLine):
        if subject_map[Agent.x+1][i] > 0:
            dist1 = i-Agent.y
        if subject_map[Agent.x-1][i] > 0:
            dist2 = i-Agent.y
        if subject_map[i][Agent.y+1] > 0:
            dist3 = i-Agent.x
        if subject_map[i][Agent.y-1] > 0:
            dist4 = i-Agent.x
    dist_east = min(dist1,dist2)
    dist_south = min(dist3,dist4)
    if dist_east == (blockEachLine-1)-Agent.y:
        dist_east = 999
    if dist_south == (blockEachLine-1)-Agent.x:
        dist_south = 999

    for i in range(0,blockEachLine):
        if subject_map[Agent.x+1][i] > 0:
            dist5 = Agent.y-i
            break
    for i in range(0,blockEachLine):
        if subject_map[Agent.x-1][i] > 0:
            dist6 = Agent.y-i
            break
    for i in range(0,blockEachLine):
        if subject_map[i][Agent.y+1] > 0:
            dist7 = Agent.x-i
            break
    for i in range(0,blockEachLine):
        if subject_map[i][Agent.y-1] > 0:
            dist8 = Agent.x-i
            break
    dist_west = min(dist5,dist6)
    dist_north = min(dist7,dist8)
    if dist_west == Agent.y:
        dist_west = 999
    if dist_north == Agent.x:
        dist_north = 999
    dist_list = (dist_north,dist_south,dist_west,dist_east)
    print(dist_list)

    j = 0
    return_list = [0,0,0,0]
    if min(dist_list) == dist_north:
        return_list[j] = 1
        j = j+1
    if min(dist_list) == dist_south:
        return_list[j] = 2
        j = j+1
    if min(dist_list) == dist_west:
        return_list[j] = 3
        j = j+1
    if min(dist_list) == dist_east:
        return_list[j] = 4
        j = j+1
    return_num = random.choice(return_list)
    while return_num == 0:
        return_num = random.choice(return_list)
    return return_num

#路线规划和下一步目标（头朝向）的设置
def r_module():
    short_route = [0,0]
    if Agent.final_des != [999,999]:
        #生成最短路径
        if Agent.deliver == 0:
            short_route = [Agent.final_des[0]-Agent.x, Agent.final_des[1]-Agent.y]
        if Agent.deliver == 1:
            if Agent.final_des[0]-Agent.x > 0 and Agent.final_des[1]-Agent.y > 0:
                short_route = [Agent.final_des[0]-Agent.x-1, Agent.final_des[1]-Agent.y-1]
            if Agent.final_des[0]-Agent.x > 0 and Agent.final_des[1]-Agent.y < 0:
                short_route = [Agent.final_des[0]-Agent.x-1, Agent.final_des[1]-Agent.y+1]
            if Agent.final_des[0]-Agent.x < 0 and Agent.final_des[1]-Agent.y < 0:
                short_route = [Agent.final_des[0]-Agent.x+1, Agent.final_des[1]-Agent.y+1]
            if Agent.final_des[0]-Agent.x < 0 and Agent.final_des[1]-Agent.y > 0:
                short_route = [Agent.final_des[0]-Agent.x+1, Agent.final_des[1]-Agent.y-1]
        # 规划沿着最短路径的下一步
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
    if Agent.final_des == [999,999]:
        Agent.direction = judge_edge()

#just run!
init_agent()
init_passenger()
while Agent.passenger_num < passengerTotal:
    v_module()
    move()
    final_des_set()
    r_module()
    print([Agent.x, Agent.y])
    #print(subject_map)
