# 64、强化学习之Advantage Actor-Critic算法

## A2C

Advantage Actor-Critic算法

REINFORCE算法必须等待整个 Episode（回合）结束，计算出从当前状态到结束的所有累积奖励 $G_t$，然后用这个 $G_t$ 来更新策略

A2C算法不需要等待回合结束，它可以进行单步更新（或 N步更新）。它利用 Critic 估计的 $V(s)$ 来代替完整的 $G_t$

## Actor（演员）：策略函数 $\pi_\theta(s, a)$

Actor 的任务是学习一个策略，即在特定状态下选择动作的概率分布。

输入： 当前状态 $s$。

输出： 动作 $a$ 的概率分布。

目标： 调整参数 $\theta$，使得能够获得高分的动作出现概率更高。

## Critic（评论家）：价值函数 $V_\phi(s)$

Critic 的任务是评估当前状态的好坏。

输入： 当前状态 $s$。

输出： 一个标量值 $V(s)$，代表在该状态下的期望长期收益。

目标： 调整参数 $\phi$，使得预测的价值尽量接近真实的奖励总和。

```python
import random
import pygame

TRAP_COUNT = 1  # 陷阱数量
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
    traps = random.sample(all_positions, min(TRAP_COUNT, len(all_positions)))
    # traps = [(2, 1), (3,4), (1,6)]
    return traps, goal

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
        reward = 10
        is_terminated = True
    elif next_state in traps:
        # 遇到陷阱
        reward = -5
        is_terminated = True
    else:
        # 普通步骤
        # reward = 0
        # reward = -0.01  # 扣太少，可能导致原地踏步
        reward = -0.1

    return str(next_state), reward, is_terminated
```

```plaintext
pygame 2.6.1 (SDL 2.28.4, Python 3.10.18)
Hello from the pygame community. https://www.pygame.org/contribute.html
```

```python
from torch.distributions import Categorical
from torch import optim
from torch import nn
import torch

ACTIONS = ['up', 'down', 'left', 'right']
traps, goal = init_environment()
gui = MazeGUI(traps, goal)
GAMMA = 0.99

# 定义AC网络
class ActorCriticNet(nn.Module):
    def __init__(self, n_states, n_actions):
        super(ActorCriticNet, self).__init__()
        # 共享特征提取层
        self.base = nn.Sequential(
            nn.Linear(n_states, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU()
        )
        # Actor头部：输出动作概率
        self.actor = nn.Sequential(
            nn.Linear(128, n_actions),
            nn.Softmax(dim=-1)
        )
        # Critic头部：输出状态价值 V(s)
        self.critic = nn.Sequential(
            nn.Linear(128, 1)
        )

    def forward(self, x):
        features = self.base(x)
        probs = self.actor(features)
        value = self.critic(features)
        return probs, value

def state_to_tensor(state_str):
    r, c = eval(state_str)
    one_hot = torch.zeros(GRID_COUNT * GRID_COUNT)
    one_hot[r * GRID_COUNT + c] = 1.0
    return one_hot


model = ActorCriticNet(GRID_COUNT * GRID_COUNT, len(ACTIONS))
optimizer = optim.Adam(model.parameters(), lr=0.001)
success_count = 0
for episode in range(3000):
    current_state = "(0, 0)"
    step = 0

    log_probs = []
    values = []
    rewards = []

    # 执行一个回合
    for t in range(20):
        gui.draw(current_state, episode, step)
        state_tensor = state_to_tensor(current_state)
        probs, value = model(state_tensor) # 同时获取动作概率和状态价值

        m = Categorical(probs)
        action = m.sample()

        next_state, reward, is_terminated = get_env_feedback(current_state, ACTIONS[action.item()], goal, traps)

        log_probs.append(m.log_prob(action))
        values.append(value)
        rewards.append(reward)

        current_state = next_state
        step += 1
        if is_terminated:
            if reward > 0: success_count += 1
            break

    # 计算这一个回合中每个步骤的奖励
    returns = []
    G = 0
    for r in reversed(rewards):
        G = r + GAMMA * G
        returns.insert(0, G)

    # 变成二维
    returns = torch.tensor(returns).unsqueeze(1) # [steps, 1]
    values = torch.stack(values)                 # [steps, 1]

    # returns是回合中每个动作获得的实际收益
    # values是回合中每个状态预测的收益
    # advantage表示回合中每个步骤的实际收益和预测收益的差值，如果大于0，表示动作有用，需要提高该动作发生的概率，反之则需要降低该动作发生的概率
    # 就算某个动作得到的收益为负，比如-10，如果预测收益为-20，那么-10-(-20)=10，也是一个正数，也表示该动作是有用的（比之前的动作要好）
    advantage = returns - values.detach()

    # 梯度下降是要减小loss，按以下公式，Actor模型为了要减小actor_loss，就是要增大log_probs*advantage，所以模型就会增大log_probs，也就是提高当前回合中动作发生的概率
    actor_loss = -(torch.stack(log_probs).unsqueeze(1) * advantage).sum()

    # returns是回合中每个动作获得的实际收益
    # values是回合中每个状态预测的收益
    # Critic模型为了减小critic_loss，就会让预测收益越接近实际收益，也就是预测的更准
    critic_loss = nn.functional.mse_loss(values, returns)

    # 减小loss，也就是减小actor_loss和critic_loss
    loss = actor_loss + critic_loss

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if episode % 100 == 0:
        print(f"Episode {episode}, Successes: {success_count}")

# 训练结束后演示
print("训练完成！")
```

```plaintext
Episode 0, Successes: 0
Episode 100, Successes: 0
Episode 200, Successes: 0
Episode 300, Successes: 0
Episode 400, Successes: 0
Episode 500, Successes: 0
Episode 600, Successes: 0
Episode 700, Successes: 0
Episode 800, Successes: 0
Episode 900, Successes: 0
Episode 1000, Successes: 0
Episode 1100, Successes: 0
Episode 1200, Successes: 0
Episode 1300, Successes: 0
Episode 1400, Successes: 4
Episode 1500, Successes: 83
Episode 1600, Successes: 183
Episode 1700, Successes: 283
Episode 1800, Successes: 383
Episode 1900, Successes: 483
Episode 2000, Successes: 583
Episode 2100, Successes: 681
Episode 2200, Successes: 781
Episode 2300, Successes: 881
Episode 2400, Successes: 981
Episode 2500, Successes: 1081
Episode 2600, Successes: 1181
Episode 2700, Successes: 1281
Episode 2800, Successes: 1381
Episode 2900, Successes: 1481
训练完成！
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
        probs, _ = model(state_tensor)
        action_idx = torch.argmax(probs).item()
        action = ACTIONS[action_idx]

    next_state, reward, is_terminated = get_env_feedback(current_state, action, goal, traps)
    current_state = next_state
    step += 1

    if is_terminated:
        gui.draw(current_state, 1, step) # 画出最后一步
        pygame.time.delay(1000) # 终点停留 1 秒
        if reward > 0:
            print(f"成功到达终点！步数：{step}")
        else:
            print(f"不幸掉入陷阱！")
```

```plaintext
成功到达终点！步数：14
```