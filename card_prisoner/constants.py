
# 窗口相关
WIN_WIDTH = 1280
WIN_HEIGHT = 720
WINDOW_CAPTION = "Card Prisoner"

# 其他
PRICE_PER_CARD = 10

KEYDOWN_INITIAL_DELAY = 1000  # 按下某键之后多长时间 (ms) 触发长按 (holding) 效果
KEYDOWN_REPEAT_DELAY = 100  # 长按状态下，每隔多长时间 (ms) 生成一个新的 KEYDOWN 事件

# 在普通卡内部的概率分配
A_PROBABILITY = 0.2
B_PROBABILITY = 0.3
C_PROBABILITY = (1 - A_PROBABILITY - B_PROBABILITY)
