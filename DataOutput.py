import megallen_model as mm
import configuration as cf

#数据输出到一个txt中。每次输入都从文件尾开始（不清空前面的数据）
#输出表头
def init_data(ID):
    global f
    f = open('magellanData_' + ID + '.txt', 'a')
    print('ID', 'Agent.row', 'Agent.column', 'Agent.direction', 'Agent.deliver', 'deliverNum', 'destination.row',
          'destination.column', 'bestDistance', 'actualDistance', 'isChange', file=f)  # isChange=1表示agent.deliver马上就要切换

#输出第二行及以后的数据
def data_output(ID):
    deliverNum = mm.Agent.passenger_num + 1
    actualDistance = cf.countStep
    if mm.Agent.deliver == 1:
        destinationRow = mm.passenger_des[mm.Agent.passenger_num][0]
        destinationColumn = mm.passenger_des[mm.Agent.passenger_num][1]
        bestDistance = abs(destinationRow - mm.passenger[mm.Agent.passenger_num][0])/2 + abs(destinationColumn - mm.passenger[mm.Agent.passenger_num][1])/2 - 1
        print(mm.Agent.agentID, mm.Agent.row, mm.Agent.column, mm.Agent.direction, mm.Agent.deliver, deliverNum, destinationRow, destinationColumn
              , bestDistance, mm.Agent.countStep, mm.Agent.isDeliverChange, file=f)
        #存储学习曲线
        if mm.Agent.isDeliverChange == 1:
            mm.singleLearningCurve.append(mm.Agent.passenger_num+1)
            mm.singleLearningCurve.append(mm.Agent.countStep - bestDistance)
            print('learningcurve'+str(mm.singleLearningCurve))
            return mm.singleLearningCurve
    return None
    """
    if mm.Agent.deliver == 0:
        destinationRow = mm.passenger[mm.Agent.passenger_num][0]
        destinationColumn = mm.passenger[mm.Agent.passenger_num][1]
        bestDistance = abs(destinationRow - mm.passenger_des[mm.Agent.passenger_num-1][0])/2 + abs(destinationColumn - mm.passenger_des[mm.Agent.passenger_num-1][1])/2 - 1
        print(ID, mm.Agent.row, mm.Agent.column, mm.Agent.direction, mm.Agent.deliver, deliverNum, destinationRow, destinationColumn,
              bestDistance, cf.countStep, cf.isChange, file=f)
    """
