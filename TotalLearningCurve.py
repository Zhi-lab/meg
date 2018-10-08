import configuration as cf
import megallen_model as mm

total_curve = []
cityNum = 1  # 已经走过了多少个城市
for i in range(0, mm.passengerTotal):
    total_curve.append(i+1)
    total_curve.append(0)

def TotalCurve():
    global cityNum
    if len(cf.singleLearningCurve) == 2*mm.passengerTotal:
        curve_store = cf.singleLearningCurve
        cityNum = cityNum + 1
        for i in range(0, mm.passengerTotal):
            total_curve[2*i] = total_curve[2*i] + curve_store[2*i]
            total_curve[2*i] = total_curve[2*i] / cityNum
        return total_curve
