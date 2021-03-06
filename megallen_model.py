import mpmath
import random
import configuration as cf
import DataOutput as out
import MapGeneration as mg

#示例地图
"""
mapList[Agent.city_num] = [[1,0,1,0,4,0,1,0,1,0,1],
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
"""
#mapList[Agent.city_num] = mg.map_generation()

#认知地图
subject_map = mg.subjectMapGeneration(cf.blockEachLine)

""" For test
[[0,0,0,0,0,0,0,0,0,0,0],
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
"""

#找乘客用的地图
passenger_map = mg.subjectMapGeneration(cf.blockEachLine)
"""
[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
"""

#存储excess path distance
resultList = []

# 存储学习曲线的数组
singleLearningCurve = []
# 存储平均学习曲线的数组
totalCurve = []

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
    #isDeliverChange = 1 表示Agent.deliver马上就要切换。此时应当记录学习曲线数据
    isDeliverChange = 0
    countStep = 0
    agentID = None
    isStop = 0
    city_num = 0

#总共的乘客数量
passengerTotal = 15
passenger = []

#总共要走的城市数量
cityTotal = 12

mapList = []
for i in range(cityTotal):
    mapList.append(mg.map_generation())

#if passengerTotal = 15, passenger = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
for counter in range(0,passengerTotal):
    passenger.append([0,0])

#store的ID是2，3，4，5，6，遍历地图数组，将值为2，3，4，5，6总任一个的元素的行数和列数存储在store数组
class MazePos:
    store = []
    for i in range(0,cf.blockEachLine*2-1):
        #j对应的是列
        for j in range(0,cf.blockEachLine*2-1):
            for k in range(2,2+cf.storeNum):
                if mapList[Agent.city_num][i][j] == k:
                    store.append([i,j])
                    break
def initMazePos():
    MazePos.store = []
    #i对应的是行
    for i in range(0,cf.blockEachLine*2-1):
        #j对应的是列
        for j in range(0,cf.blockEachLine*2-1):
            for k in range(2,2+cf.storeNum):
                if mapList[Agent.city_num][i][j] == k:
                    MazePos.store.append([i,j])
                    break

#passenger[0] = [2*random.randint(1,5)-1,2*random.randint(1,5)-1]
#乘客的目标地点，总共是15个目的地
passenger_des = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]

def passenger_destination():
    store_block = []
    for i in range(0, cf.storeNum):
        store_block.append(i)
    passenger_count = 0
    while passenger_count < passengerTotal:
        random.shuffle(store_block)
        for j in range(0, cf.storeNum):
            passenger_des[j+cf.storeNum*int(passenger_count/cf.storeNum)] = MazePos.store[store_block[j]]
            passenger_count = passenger_count+1
    """
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
    """
    passenger[0] = [2 * random.randint(1, cf.blockEachLine-1) - 1, 2 * random.randint(1, cf.blockEachLine-1) - 1]
    while abs(passenger[0][0] - passenger_des[0][0]) == 1 and abs(passenger[0][1] - passenger_des[0][1]) == 1:
        passenger[0] = [2 * random.randint(1, cf.blockEachLine - 1) - 1, 2 * random.randint(1, cf.blockEachLine - 1) - 1]

    #乘客和上一个目标不能在邻行邻列
    for j in range(1,passengerTotal):
        passenger[j] = [2 * random.randint(1, cf.blockEachLine - 1) - 1, 2 * random.randint(1, cf.blockEachLine - 1) - 1]
        while abs(passenger[j][0] - passenger_des[j-1][0]) == 1 or abs(passenger[j][1] - passenger_des[j-1][1]) == 1 \
                or (abs(passenger[j][0] - passenger_des[j][0]) == 1 and abs(passenger[j][1] - passenger_des[j][1]) == 1) :
            passenger[j] = [2 * random.randint(1, cf.blockEachLine - 1) - 1, 2 * random.randint(1, cf.blockEachLine - 1) - 1]

def easy_passenger_destination():
    store_block = []
    for i in range(0, cf.storeNum):
        store_block.append(i)
    passenger_count = 0
    while passenger_count < passengerTotal:
        random.shuffle(store_block)
        for j in range(0, cf.storeNum):
            passenger_des[j+cf.storeNum*int(passenger_count/cf.storeNum)] = MazePos.store[store_block[j]]
            passenger_count = passenger_count+1
    passenger[0] = [2 * random.randint(1, cf.blockEachLine-1) - 1, 2 * random.randint(1, cf.blockEachLine-1) - 1]
    while abs(passenger[0][0] - passenger_des[0][0]) == 1 or abs(passenger[0][1] - passenger_des[0][1]) == 1:
        passenger[0] = [2 * random.randint(1, cf.blockEachLine - 1) - 1, 2 * random.randint(1, cf.blockEachLine - 1) - 1]
    for j in range(1,passengerTotal):
        #passenger[j] = [2 * random.randint(1, cf.blockEachLine-1) - 1, 2 * random.randint(1, cf.blockEachLine-1) - 1]
        """
        while (abs(passenger[j][0] - passenger_des[j-1][0]) != 3 or abs(passenger[j][1] - passenger_des[j-1][1]) != 3) \
                or (abs(passenger[j][0] - passenger_des[j][0]) == 1 or abs(passenger[j][1] - passenger_des[j][1]) == 1):
            passenger[j] = [2 * random.randint(1, cf.blockEachLine-1) - 1, 2 * random.randint(1, cf.blockEachLine-1) - 1]
        """
        if random.randint(1, 2) > 1:
            xOffset = 3
        else:
            xOffset = -3
        if random.randint(1, 2) > 1:
            yOffset = 3
        else:
            yOffset = -3
        passenger[j][0] = passenger_des[j-1][0] + xOffset
        passenger[j][1] = passenger_des[j-1][1] + yOffset
        #while #passenger[j][0] <= 0 or passenger[j][0] > cf.blockEachLine * 2 - 3 \
        #while passenger[j][1] <= 0 or passenger[j][1] > cf.blockEachLine * 2 - 3 \
        print("passenger[j]")
        print(passenger[j])
        print("passenger_des[j]")
        print(passenger_des[j])
        print("\n")
        while passenger[j][0] <= 0 or passenger[j][0] > cf.blockEachLine * 2 - 3  or \
            passenger[j][1] <= 0 or passenger[j][1] > cf.blockEachLine * 2 - 3 :
            if random.randint(1, 2) > 1:
                xOffset = 3
            else:
                xOffset = -3
            if random.randint(1, 2) > 1:
                yOffset = 3
            else:
                yOffset = -3
            passenger[j][0] = passenger_des[j-1][0] + xOffset
            passenger[j][1] = passenger_des[j-1][1] + yOffset

            while (abs(passenger[j][0] - passenger_des[j][0]) == 1 and abs(passenger[j][1] - passenger_des[j][1]) == 1):
                if passenger[j][0] < passenger_des[j][0]:
                    if passenger[j][0] - 2 > 0:
                        passenger[j][0] -= 2
                else:
                    if passenger[j][0] + 2 <= cf.blockEachLine * 2 - 3:
                        passenger[j][0] += 2
                if passenger[j][1] < passenger_des[j][1]:
                    if passenger[j][1] - 2 > 0:
                        passenger[j][1] -= 2
                else:
                    if passenger[j][1] + 2 <= cf.blockEachLine * 2 - 3:
                        passenger[j][1] += 2

            print("passenger[j]")
            print(passenger[j])
            print("passenger_des[j]")
            print(passenger_des[j])
            print("\n")
#初始化agent位置、头朝""向、目标
#agent的位置、头朝向、视觉参数、记忆参数、总体目标、下一步目标、有无乘客、已送乘客数量

def init_agent():
    Agent.row = passenger[0][0]
    Agent.column = passenger[0][1]
    Agent.final_des = passenger[0]
    Agent.next_des = passenger[0]
    Agent.direction = random.randint(1,4)

    if Agent.row == 2 * cf.blockEachLine-3 and Agent.direction == 1:
        Agent.direction = Agent.direction + 1
    elif Agent.row == 1 and Agent.direction == 2:
        Agent.direction = Agent.direction - 1
    elif Agent.column == 2 * cf.blockEachLine-3 and Agent.direction == 3:
        Agent.direction = Agent.direction + 1
    elif Agent.column == 1 and Agent.direction == 4:
        Agent.direction = Agent.direction - 1

    if Agent.direction == 1:
        Agent.row = Agent.row + cf.step
    elif Agent.direction == 2:
        Agent.row = Agent.row - cf.step
    elif Agent.direction == 3:
        Agent.column = Agent.column + cf.step
    elif Agent.direction == 4:
        Agent.column = Agent.column - cf.step

#初始化乘客信息
def init_passenger():
    #passenger[0] = [2*random.randint(1,5)-1,2*random.randint(1,5)-1]
    easy_passenger_destination()
    #passenger_destination()

#每一步寻路前初始化一些参数，目前只需更新isDeliverChange
def start_navigation():
    Agent.isDeliverChange = 0

#确定要加入模块的建筑，并将这些建筑的记忆强度设为1
def v_module():
    visionBoundary = Agent.vision*2
    for i in range(1,visionBoundary,2):
        if Agent.row - i >= 0:
            if Agent.direction == 1:
                if subject_map[Agent.row - i][Agent.column - 1] >= 0:
                    subject_map[Agent.row - i][Agent.column - 1] = 1
                if subject_map[Agent.row - i][Agent.column + 1] >= 0:
                    subject_map[Agent.row - i][Agent.column + 1] = 1
        if  Agent.row + i < cf.blockEachLine*2 - 1:
            if Agent.direction == 2:
                if subject_map[Agent.row + i][Agent.column - 1] >= 0:
                    subject_map[Agent.row + i][Agent.column - 1] = 1
                if subject_map[Agent.row + i][Agent.column + 1] >= 0:
                    subject_map[Agent.row + i][Agent.column + 1] = 1
        if  Agent.column - i >= 0:
            if Agent.direction == 3:
                if subject_map[Agent.row - 1][Agent.column - i] >= 0:
                    subject_map[Agent.row - 1][Agent.column - i] = 1
                if subject_map[Agent.row + 1][Agent.column - i] >= 0:
                    subject_map[Agent.row + 1][Agent.column - i] = 1
        if  Agent.column + i < cf.blockEachLine*2 - 1:
            if Agent.direction == 4:
                if subject_map[Agent.row - 1][Agent.column + i] >= 0:
                    subject_map[Agent.row - 1][Agent.column + i] = 1
                if subject_map[Agent.row + 1][Agent.column + i] >= 0:
                    subject_map[Agent.row + 1][Agent.column + i] = 1

#subject_map的遗忘
def forget():
    for i in range(0, cf.blockEachLine):
        for j in range(0, cf.blockEachLine):
            if subject_map[2*i][2*j] > 0:
                subject_map[2*i][2*j] = subject_map[2*i][2*j] - 1/Agent.memory
                #避免subject_map里的值为负值
                #subject_map[2*i][2*j] = max(subject_map[2*i][2*j],0)
                if subject_map[2*i][2*j] - 1/Agent.memory < 0:
                    subject_map[2*i][2*j] = 0


#agent移动一步，并遗忘（只有移动了才会遗忘）
def move():
    if Agent.direction == 1 and Agent.row > 1:
        Agent.row = Agent.row - cf.step
    elif Agent.direction == 2 and Agent.row < cf.blockEachLine*2-3:
        Agent.row = Agent.row + cf.step
    elif Agent.direction == 3 and Agent.column > 1:
        Agent.column = Agent.column - cf.step
    elif Agent.direction == 4 and Agent.column < cf.blockEachLine*2-3:
        Agent.column = Agent.column + cf.step
    else :
        return
    forget()
    Agent.countStep += 1
    resultList = out.data_output(Agent.agentID)

#路线规划和下一步目标（头朝向）的设置
def r_module():
    short_route = [0,0]
    print("Agent.final_des")
    print(Agent.final_des)
    if Agent.final_des != None:
        #生成最短路径
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
        # 规划沿着最短路径的下一步
        # 最短路径方向朝东或朝北
        if short_route[0] > 0 and short_route[1] > 0:
            Agent.direction = random.choice([2,4])
        # 最短路径方向朝西或朝北
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
    if not Agent.final_des:
        Agent.direction = judge_edge_v2()
    print("current direction")
    print(Agent.direction)

#地图边界检测
def judge_edge():
    #agent位于建筑之间，而subject_map的边界可能不平整，所以dist1、dist2分别表示东方边界上，agent南北两行建筑离agent的距离。
    dist1 = dist2 = dist3 = dist4 = dist5 = dist6 = dist7 = dist8 = 0
    for i in range(0,cf.blockEachLine*2-1):
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
    if dist_east == (cf.blockEachLine*2-2)-Agent.column:
        dist_east = mpmath.inf
    if dist_south == (cf.blockEachLine*2-2)-Agent.row:
        dist_south = mpmath.inf

    for i in range(0,cf.blockEachLine*2-1):
        if subject_map[Agent.row+1][i] > 0:
            dist5 = Agent.column-i
            break
    for i in range(0,cf.blockEachLine*2-1):
        if subject_map[Agent.row-1][i] > 0:
            dist6 = Agent.column-i
            break
    for i in range(0,cf.blockEachLine*2-1):
        if subject_map[i][Agent.column+1] > 0:
            dist7 = Agent.row-i
            break
    for i in range(0,cf.blockEachLine*2-1):
        if subject_map[i][Agent.column-1] > 0:
            dist8 = Agent.row-i
            break
    dist_west = min(dist5,dist6)
    dist_north = min(dist7,dist8)
    if dist_west == Agent.column:
        dist_west = mpmath.inf
    if dist_north == Agent.row:
        dist_north = mpmath.inf
    dist_list = [dist_north,dist_south,dist_west,dist_east]

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
    print(dist_list)
    return return_num

def judge_edge_v2():
    count_west = 0
    count_east = 0
    count_north = 0
    count_south = 0

    #朝北寻找最近的未知格
    i = Agent.row - 1
    while i >= 0 and i <= cf.blockEachLine*2 - 1:
        if subject_map[i][Agent.column - 1] > 0 and subject_map[i][Agent.column + 1] > 0:
            count_north += 1
            i -= cf.step
            if count_north == (Agent.row + 1) / 2:
                count_north = mpmath.inf
                break
            continue
        else:
            break


    #朝南寻找最近的未知格
    i = Agent.row + 1
    while i >= 0 and i <= cf.blockEachLine*2 - 1:
        if subject_map[i][Agent.column - 1] > 0 and subject_map[i][Agent.column + 1] > 0:
            count_south += 1
            i += cf.step
            if count_south == (cf.blockEachLine*2 - 1 - Agent.row) / 2:
                count_south = mpmath.inf
                break
            continue
        else:
            break


    #朝西寻找最近的未知格
    i = Agent.column - 1
    while i >= 0 and i <= cf.blockEachLine*2 - 1:
        if subject_map[Agent.row - 1][i] > 0 and subject_map[Agent.row + 1][i] > 0:
            count_west += 1
            i -= 2
            if count_west == (Agent.column + 1) / 2:
                count_west = mpmath.inf
                break
            continue
        else:
            break


    #朝东寻找最近的未知格
    i = Agent.column + 1
    while i >= 0 and i <= cf.blockEachLine*2 - 1:
        if subject_map[Agent.row - 1][i] > 0 and subject_map[Agent.row + 1][i] > 0:
            count_east += 1
            i += 2
            if count_east == (cf.blockEachLine*2 - 1 - Agent.column) / 2:
                count_east = mpmath.inf
                break
            continue
        else:
            break


    """
    for i in range(Agent.row, 0, int(-1)):
        if subject_map[i][Agent.column - 1] > 0 and subject_map[i][Agent.column + 1] > 0:
            count_north = count_north + 1
        else:
            break
    for i in range(Agent.row, cf.blockEachLine*2-2):
        if subject_map[i][Agent.column - 1] > 0 or subject_map[i][Agent.column + 1] > 0:
            count_south = count_south + 1
        else:
            break
    for i in range(Agent.column, 0, int(-1)):
        if subject_map[Agent.row - 1][i] > 0 or subject_map[Agent.row + 1][i] > 0:
            count_west = count_west + 1
        else:
            break
    for i in range(Agent.column, cf.blockEachLine*2-2):
        if subject_map[Agent.row - 1][i] > 0 or subject_map[Agent.row + 1][i] > 0:
            count_east = count_east + 1
        else:
            break
    if count_north == Agent.row:
        count_north = mpmath.inf
    if count_south == (cf.blockEachLine*2-2)-Agent.row:
        count_south = mpmath.inf
    if count_west == Agent.column:
        count_west = mpmath.inf
    if count_east == (cf.blockEachLine*2-2)-Agent.column:
        count_east = mpmath.inf
    """
    count_list = [count_north, count_south, count_west, count_east]
    print("count_list")
    print(count_list)

    return_list = []
    if min(count_list) == count_north:
        return_list.append(1)
    if min(count_list) == count_south:
        return_list.append(2)
    if min(count_list) == count_west:
        return_list.append(3)
    if min(count_list) == count_east:
        return_list.append(4)
    return_num = random.choice(return_list)
    return return_num

#设定agent的最终目标（乘客数量送到之后才会+1）
def final_des_set():
    #passenger_destination()
    print(subject_map)
    if Agent.row == passenger[Agent.passenger_num][0] and Agent.column == passenger[Agent.passenger_num][1] and Agent.deliver == 0:
        # Agent.isDeliverChange = 1
        # out.data_output() # 在送到/接到乘客的位置点输出一次数据，从而给这一步打上isChange=1的标记
        Agent.deliver = 1
        # 计步器在接到乘客或者送到乘客之后清零，每走一步就加一，接到乘客或者送到乘客之后清零
        Agent.countStep = 0
        if subject_map[passenger_des[Agent.passenger_num][0]][passenger_des[Agent.passenger_num][1]] > 0:
            Agent.final_des = passenger_des[Agent.passenger_num]
        #elif subject_map[passenger_des[Agent.passenger_num][0]][passenger_des[Agent.passenger_num][1]] == 0:
        else:
            Agent.final_des = None
    #当将乘客送达目的地时，将乘客放下
    if Agent.deliver == 1:
        if subject_map[passenger_des[Agent.passenger_num][0]][passenger_des[Agent.passenger_num][1]] > 0:
            Agent.final_des = passenger_des[Agent.passenger_num]
        # agent可能刚开始知道目标，但是走着走着不记得了
        else:
            Agent.final_des = None
        #如果走到目标store了，将已送达乘客+1,目标转为下一乘客，刷新找乘客用的记忆地图
        if abs(Agent.row - passenger_des[Agent.passenger_num][0]) == 1 and abs(Agent.column - passenger_des[Agent.passenger_num][1]) == 1:
            Agent.isDeliverChange = 1
            resultList = out.data_output(Agent.agentID)
            cf.countStep = 0  # 计步器，每走一步就加一，接到乘客或者送到乘客之后清零;且先进行数据清算
            Agent.deliver = 0
            print("goal")
            #if Agent.passenger_num < passengerTotal:
            Agent.passenger_num = Agent.passenger_num + 1
            init_find_passenger()

def find_passenger():
    init_find_passenger()
    """
    #while Agent.deliver == 0:
        passenger_v_module()
        passenger_move()
        passenger_final_des_set()
        r_module()
        if Agent.row == passenger[Agent.passenger_num][0] and Agent.column == passenger[Agent.passenger_num][1]:
            return
            #break
        print(passenger_map)
        print([Agent.row-passenger[Agent.passenger_num][0],Agent.column-passenger[Agent.passenger_num][1]])
    """
def passenger_final_des_set():
    if Agent.row == passenger[Agent.passenger_num][0] or Agent.column == passenger[Agent.passenger_num][1]:
        Agent.final_des = passenger[Agent.passenger_num]
    else:
        Agent.direction = direction_detection()
        if Agent.direction == 1:
            Agent.final_des = [Agent.row - cf.step,Agent.column]
        if Agent.direction == 2:
            Agent.final_des = [Agent.row + cf.step,Agent.column]
        if Agent.direction == 3:
            Agent.final_des = [Agent.row, Agent.column - cf.step]
        if Agent.direction == 4:
            Agent.final_des = [Agent.row,Agent.column + cf.step]

#寻找乘客（启用passenger_map）
def init_find_passenger():
    global passenger_map
    passenger_map = mg.subjectMapGeneration(cf.blockEachLine)

def passenger_v_module():
    visionBoundary = Agent.vision+1
    for i in range(0,visionBoundary):
        if Agent.row - i >= 0:
            if Agent.direction == 1:
                passenger_map[Agent.row - i][Agent.column] = 1
        if Agent.row + i < cf.blockEachLine * 2 -1:
            if Agent.direction == 2:
                passenger_map[Agent.row + i][Agent.column] = 1
        if  Agent.column - i >= 0:
            if Agent.direction == 3:
                passenger_map[Agent.row][Agent.column - i] = 1
        if Agent.column + i < cf.blockEachLine * 2 -1:
            if Agent.direction == 4:
                passenger_map[Agent.row][Agent.column + i] = 1

def passenger_forget():
    for i in range(0,cf.blockEachLine - 1):
        for j in range(0,cf.blockEachLine -1):
            if passenger_map[2*i+1][2*j+1] > 0:
                passenger_map[2*i+1][2*j+1] -= 1/Agent.passenger_memory#= passenger_map[2*i+1][2*j+1] - 1/Agent.passenger_memory
                #避免subject_map里的值为负值
                #passenger_map[2*i+1][2*j+1] = max(0,passenger_map[2*i+1][2*j+1])
                if passenger_map[2*i+1][2*j+1] - 1/Agent.passenger_memory < 0:
                    passenger_map[2*i+1][2*j+1] = 0

def passenger_move():
    if Agent.direction == 1 and Agent.row > 1:
        Agent.row = Agent.row - cf.step
    elif Agent.direction == 2 and Agent.row < cf.blockEachLine*2-3:
        Agent.row = Agent.row + cf.step
    elif Agent.direction == 3 and Agent.column > 1:
        Agent.column = Agent.column - cf.step
    elif Agent.direction == 4 and Agent.column < cf.blockEachLine*2-3:
        Agent.column = Agent.column + cf.step
    else:
        return
    passenger_forget()
    forget()

def direction_detection():
    return_list = []
    if Agent.row < cf.blockEachLine*2-3:
        if passenger_map[Agent.row+cf.step][Agent.column] == 0:
            return_list.append(2)
    if Agent.row > 1:
        if passenger_map[Agent.row-cf.step][Agent.column] == 0:
            return_list.append(1)
    if Agent.column < cf.blockEachLine*2-3:
        if passenger_map[Agent.row][Agent.column+cf.step] == 0:
            return_list.append(4)
    if Agent.column > 1:
        if passenger_map[Agent.row][Agent.column-cf.step] == 0:
            return_list.append(3)
    if not return_list:
        return random.choice([1,2,3,4])
    else:
        return_num = random.choice(return_list)
        return return_num