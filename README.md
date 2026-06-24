## python 虚拟环境管理

```shell
# 创建虚拟环境（env 是环境名称，可自定义）
python -m venv env


# 删除虚拟环境
# Windows (cmd/powershell)
rmdir /s env

# 或者使用 del
rm -rf env

# macOS/Linux
rm -rf env

```

## Git相关

### git tag
```sh
git tag -a tag_name -m "tag 相关信息"

git push origin --tags

```

## 冒泡排序 (Bubble Sort)

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

print(bubble_sort([64, 34, 25, 12, 22, 11, 90]))
# 输出：[11, 12, 22, 25, 34, 64, 90]
```

