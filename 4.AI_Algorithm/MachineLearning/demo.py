from sklearn.linear_model import LogisticRegression

"""
常见搭配公式：
1. 标准二分类（最常用）
LogisticRegression(class_weight='balanced', max_iter=100)

2. 带L1正则化 + 特征选择
LogisticRegression(penalty='l1', solver='saga', C=0.5, max_iter=100)

3. 多分类任务
LogisticRegression(multi_class='multinomial', solver='saga', max_iter=100)
"""

# 创建模型
model = LogisticRegression(
    solver='lbfgs',              # 优化器：用什么方法求最优解。作用：模型用什么方法“找到最优答案”
    penalty='l2',                # 正则化：L2 防止过拟合，泛化能力更强（让权重参数不要太大）
    C=1.0,                       # 正则化强度的倒数：C 越小惩罚越强、越能防过拟合；C 越大越贴合训练数据
    class_weight='balanced',     # 类别权重：按各类样本占比的反比加权，自动平衡，缓解类别不平衡
    max_iter=100,                # 最大迭代次数：若不收敛（会告警）就调大，如 1000
    multi_class='multinomial'    # 多分类策略：multinomial 用 softmax 交叉熵损失，适合真正的多分类
)