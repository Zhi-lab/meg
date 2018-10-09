import mpmath

#每隔500ms更新一次动画
updateDuration = 100

canvasLen = 1000
mapLen = 350

#折线图的x轴长
xAxisLen = mapLen
#y轴长
yAxisLen = 250

#折线图距离地图的纵向距离
yMargin = 80

# blockEachLine = 6表示环境为6X6的大小
blockEachLine = 6
# buidlingLen是每一个building的边长（px）
buidlingLen = mpmath.floor(mapLen / blockEachLine)

# 路宽
margin = 10

#orign指的是折线图左上角的坐标值
diagramOrigin = [margin, yMargin + mapLen]

# 商店数量。为了每个商店去相同的次数，乘客的数量应该为商店数量的整数倍
storeNum = 5



# 真实地图与记忆地图的横向间隔距离
marginForMaps = 500
buidlingLen = buidlingLen - margin

#步长
step = 2

# 计步器，每走一步就加一，接到乘客或者送到乘客之后清零
countStep = 0
# isDeliverChange = 1 表示Agent.deliver马上就要切换。此时应当记录学习曲线数据
#isDeliverChange = 0

 # 存储学习曲线的数组
singleLearningCurve = []

scaleLabelList = []
#passenger_display = None

