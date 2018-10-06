import mpmath

#每隔500ms更新一次动画
updateDuration = 300

canvasLen = 400
# blockEachLine = 6表示环境为6X6的大小
blockEachLine = 6
# buidlingLen是每一个building的边长（px）
buidlingLen = mpmath.floor(canvasLen / blockEachLine)

# 路宽
margin = 10

# 真实地图与记忆地图的横向间隔距离
marginForMaps = 500
buidlingLen = buidlingLen - margin

#步长
step = 2


passenger_display = None

