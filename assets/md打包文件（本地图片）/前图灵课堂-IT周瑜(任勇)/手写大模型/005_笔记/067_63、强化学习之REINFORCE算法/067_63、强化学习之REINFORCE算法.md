# 63、强化学习之REINFORCE算法

## REINFORCE算法

```python
import pygame

TRAP_COUNT = 3  # 陷阱数量
GRID_COUNT = 8  # 迷宫大小 (N x N)
SCREEN_WINDOW = 1000
CELL_SIZE = (SCREEN_WINDOW - 100) // GRID_COUNT
MAZE_SIZE = CELL_SIZE * GRID_COUNT
OFFSET_Y = 60  # 顶部文字区域高度

# 颜色定义
COLOR_BG = (245, 245, 245)
COLOR_TEXT = (44, 62, 80)
COLOR_LINE = (189, 195, 199)
COLOR_AGENT = (52, 152, 219)  # 蓝色
COLOR_GOAL = (46, 204, 113)  # 绿色
COLOR_TRAP = (231, 76, 60)  # 红色


## 初始化游戏界面
class MazeGUI:
    def __init__(self, traps, goal):
        pygame.init()
        self.screen = pygame.display.set_mode((MAZE_SIZE, MAZE_SIZE + OFFSET_Y))
        pygame.display.set_caption("秘境寻宝")
        self.font = pygame.font.SysFont("SimHei", 20)
        self.clock = pygame.time.Clock()
        self.traps = traps
        self.goal = goal

    def draw(self, position, episode, step):
        self.screen.fill(COLOR_BG)

        # 1. 状态信息
        info = self.font.render(f"episode: {episode + 1} | step: {step} | trap: {len(self.traps)}", True, COLOR_TEXT)
        self.screen.blit(info, (10, 15))

        # 2. 网格和元素
        for r in range(GRID_COUNT):
            for c in range(GRID_COUNT):
                rect = (c * CELL_SIZE, r * CELL_SIZE + OFFSET_Y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, COLOR_LINE, rect, 1)  # 画边框

                # 画陷阱
                if (r, c) in self.traps:
                    pygame.draw.rect(self.screen, COLOR_TRAP, (rect[0] + 4, rect[1] + 4, CELL_SIZE - 8, CELL_SIZE - 8))
                # 画终点
                elif (r, c) == self.goal:
                    pygame.draw.rect(self.screen, COLOR_GOAL, (rect[0] + 4, rect[1] + 4, CELL_SIZE - 8, CELL_SIZE - 8))

        # 3. 画探险家
        if position != 'terminal':
            r, c = eval(position)
            center = (c * CELL_SIZE + CELL_SIZE // 2, r * CELL_SIZE + OFFSET_Y + CELL_SIZE // 2)
            pygame.draw.circle(self.screen, COLOR_AGENT, center, CELL_SIZE // 3)

        pygame.display.flip()

def init_environment():
    """初始化陷阱和终点坐标"""
    all_positions = [(r, c) for r in range(GRID_COUNT) for c in range(GRID_COUNT)]
    all_positions.remove((0, 0))  # 起点不能是陷阱
    goal = (GRID_COUNT - 1, GRID_COUNT - 1)
    all_positions.remove(goal)  # 终点不能是陷阱

    # 随机选出陷阱
    # traps = random.sample(all_positions, min(TRAP_COUNT, len(all_positions)))
    traps = [(2, 1), (3,4), (1,6)]
    return traps, goal
```

```plaintext
pygame 2.6.1 (SDL 2.28.4, Python 3.10.18)
Hello from the pygame community. https://www.pygame.org/contribute.html
```

```python
# 与环境交互，获取下一个状态和奖励
def get_env_feedback(current_state, action, goal, traps):
    # current_state是字符串"(0, 0)"，用eval函数解析，r_idx表示当前状态的行索引，c_idx表示当前状态的列索引
    r_idx, c_idx = eval(current_state)

    # 根据动作决定下一个位置的坐标
    if action == 'up':
        r_idx = max(0, r_idx - 1)
    elif action == 'down':
        r_idx = min(GRID_COUNT - 1, r_idx + 1)
    elif action == 'left':
        c_idx = max(0, c_idx - 1)
    elif action == 'right':
        c_idx = min(GRID_COUNT - 1, c_idx + 1)

    next_state = (r_idx, c_idx)

    is_terminated = False
    if next_state == goal:
        # 得到宝藏
        reward = 1
        is_terminated = True
    elif next_state in traps:
        # 遇到陷阱
        reward = -1
        is_terminated = True
    else:
        # 普通步骤
        # reward = 0
        # reward = -0.01  # 扣太少，可能导致原地踏步
        reward = -0.1

    return str(next_state), reward, is_terminated
```

```python
from torch import nn

# 定义策略网络
class PolicyNet(nn.Module):
    def __init__(self, n_states, n_actions):
        super(PolicyNet, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(n_states, 128), # 输入坐标
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, n_actions),
            nn.Softmax(dim=-1)       # 输出每个动作的概率
        )

    def forward(self, x):
        return self.fc(x)
```

```python
import torch
from torch import optim
from torch.distributions import Categorical

ACTIONS = ['up', 'down', 'left', 'right']
traps, goal = init_environment()
gui = MazeGUI(traps, goal)

GAMMA = 0.9  # 未来奖励衰减因子

net = PolicyNet(GRID_COUNT * GRID_COUNT, len(ACTIONS))
optimizer = optim.Adam(net.parameters(), lr=0.001)

# 将坐标转成One-hot 编码
def state_to_tensor(state_str):
    r, c = eval(state_str)
    one_hot = torch.zeros(GRID_COUNT * GRID_COUNT)
    one_hot[r * GRID_COUNT + c] = 1.0
    return one_hot

# 开始训练
success_count = 0  # 记录到达终点的次数
for episode in range(2000):
    current_state = "(0, 0)"
    step = 0

    # 记录的是一个回合里面执行了哪些动作（动作概率，获得当前奖励）
    log_probs = []   # [0.6, 0.3, 0.5, ..., 0.3]
    rewards = []     # [-0.01, -0.01, -0.01, ..., 1]

    # 执行一个回合
    is_terminated = False
    while not is_terminated:
        # 观察当前状态
        gui.draw(current_state, episode, step)

        state_tensor = state_to_tensor(current_state)
        probs = net(state_tensor)

        # 根据概率选择一个动作
        m = Categorical(probs)
        action = m.sample()

        # 记录每个动作的概率和奖励
        next_state, reward, is_terminated = get_env_feedback(current_state, ACTIONS[action.item()], goal, traps)
        log_probs.append(m.log_prob(action))
        rewards.append(reward)

        current_state = next_state
        step += 1
        if is_terminated:
            if reward > 0: success_count += 1 # 只有奖励为1才是真正到达终点
            break

    # 计算累计回报
    # log_probs = []   # [0.6, 0.3, 0.5, ..., 0.7, 0.3]
    # rewards = []     # [-0.01, -0.01, -0.01, ..., -0.01, 1]
    # returns是奖励     # [0.68,....,0.89,1]
    returns = []
    G = 0
    for r in reversed(rewards):
        G = r + GAMMA * G
        returns.insert(0, G)

    returns = torch.tensor(returns)

    # 计算总体奖励
    # REINFORCE 的目标是最大化期望奖励，PyTorch 默认是最小化 Loss
    loss = []
    for log_prob, G in zip(log_probs, returns):
        loss.append(-log_prob * G)

    optimizer.zero_grad()
    # 梯度下降、梯度上升
    # -((a1_p*a1_r)+(a2_p*a2_r)+(a3_p*a3_r)+(a4_p*a4_r)+(a5_p*a5_r))
    loss = torch.stack(loss).sum()
    loss.backward()
    optimizer.step()

    if episode % 50 == 0:
        print(f"Episode {episode}, Success: {success_count}")
```

```plaintext
Episode 0, Success: 0
Episode 50, Success: 1
Episode 100, Success: 2
Episode 150, Success: 2
Episode 200, Success: 5
Episode 250, Success: 8
Episode 300, Success: 25
Episode 350, Success: 39
Episode 400, Success: 54
Episode 450, Success: 73
Episode 500, Success: 94
Episode 550, Success: 113
Episode 600, Success: 130
Episode 650, Success: 150
Episode 700, Success: 172
Episode 750, Success: 198
Episode 800, Success: 227
Episode 850, Success: 266
Episode 900, Success: 307
Episode 950, Success: 352
Episode 1000, Success: 402
Episode 1050, Success: 448
Episode 1100, Success: 496
Episode 1150, Success: 543
Episode 1200, Success: 591
Episode 1250, Success: 641
Episode 1300, Success: 691
Episode 1350, Success: 740
Episode 1400, Success: 790
Episode 1450, Success: 840
Episode 1500, Success: 890
Episode 1550, Success: 940
Episode 1600, Success: 990
Episode 1650, Success: 1040
Episode 1700, Success: 1089
Episode 1750, Success: 1139
Episode 1800, Success: 1189
Episode 1850, Success: 1239
Episode 1900, Success: 1288
Episode 1950, Success: 1338
```

```python
current_state = "(0, 0)"
is_terminated = False

step = 0
while not is_terminated:
    gui.draw(current_state, 1, step)
    gui.clock.tick(5)  # 推理时速度放慢，方便观察 (5 FPS)

    with torch.no_grad():
        state_tensor = state_to_tensor(current_state)
        probs = net(state_tensor)
        action_idx = torch.argmax(probs).item()
        action = ACTIONS[action_idx]

    next_state, reward, is_terminated = get_env_feedback(current_state, action, goal, traps)
    current_state = next_state
    step += 1

    if is_terminated:
        gui.draw(current_state, 1, step) # 画出最后一步
        pygame.time.delay(1000) # 终点停留 1 秒
        if reward == 1:
            print(f"成功到达终点！步数：{step}")
        else:
            print(f"不幸掉入陷阱！")
```

```plaintext
成功到达终点！步数：14
```