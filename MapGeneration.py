import configuration as cf
import random


def standardJudge():
    standard = 1  # 判断是否符合规则
    # 两个store不能在相同的位置
    for i in range(0,cf.storeNum):
        if store_position.count(store_position[i]) > 1:
            standard = 0
            break
    # store不能占有4个角
    corner = 0
    for i in range(0, cf.storeNum):
        if store_position[i] == [0,0] or store_position[i] == [0,2*cf.storeNum-2] or store_position[i] == [2*cf.storeNum-2,0] or store_position[i] == [2*cf.storeNum-2,2*cf.storeNum-2]:
            corner = corner+1
    if corner == 4:
        standard = 0
    # 同一行/列的store至少要相隔两幢建筑
    for i in range(0, cf.storeNum-1):
        for j in range(i+1, cf.storeNum):
            if (store_position[i][0] == store_position[j][0] and abs(store_position[i][1] - store_position[j][1]) <= 4) or \
                    (store_position[i][1] == store_position[j][1] and abs(store_position[i][0] - store_position[j][0]) <= 4):
                standard = 0
                break
    # 两个store不能是knight's move
    for i in range(0, cf.storeNum-1):
        for j in range(i+1, cf.storeNum):
            if (abs(store_position[i][0] - store_position[j][0]) == 2 and abs(store_position[i][1] - store_position[j][1]) == 4) or \
                    (abs(store_position[i][0] - store_position[j][0]) == 4 and abs(store_position[i][1] - store_position[j][1]) == 2):
                print('false1')
                standard = 0
                break
    # 两个store不能在斜对面
    for i in range(0, cf.storeNum-1):
        for j in range(i+1, cf.storeNum):
            if abs(store_position[i][0] - store_position[j][0]) == 2 and abs(store_position[i][1] - store_position[j][1]) == 2:
                print('false2')
                standard = 0
                break
    return standard

def map_generation():
    global store_position
    maze = []
    store_position = []
    # 生成全为0的地图
    for i in range(0, cf.blockEachLine * 2 - 1):
        maze.append([])
    for i in range(0, cf.blockEachLine * 2 - 1):
        for j in range(0, cf.blockEachLine * 2 - 1):
            maze[i].append(0)

    # 在有建筑的地方标上1
    for i in range(0, cf.blockEachLine):
        for j in range(0, cf.blockEachLine):
            maze[2 * i][2 * j] = 1

    # 随机生成store的位置，然后判断符不符合规则
    for i in range(0, cf.storeNum):
        store_position.append([2 * random.randint(0, 5), 2 * random.randint(0, 5)])

    while standardJudge() == 0:
        print(store_position)
        print('false')
        store_position = []
        for i in range(0, cf.storeNum):
            store_position.append([2 * random.randint(0, 5), 2 * random.randint(0, 5)])
        standardJudge()
    print(store_position)
    # 在有store的位置重新打标记
    for i in range(0, cf.storeNum):
        maze[store_position[i][0]][store_position[i][1]] = i + 2

    return maze
