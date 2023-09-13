# ChineseChess
基于Python的PyGame模块开发的中国象棋游戏
需要两个人在同一台电脑上游玩同一个象棋窗口
目前还没有实现AI和局域网联机

# 效果展示
<picture>
 <source media="(prefers-color-scheme: dark)" srcset="https://github.com/AndewSteve/ChineseChess/blob/main/preview/GamePreview.png">
 <source media="(prefers-color-scheme: light)" srcset="https://github.com/AndewSteve/ChineseChess/blob/main/preview/GamePreview.png">
 <img alt="YOUR-ALT-TEXT" src="https://github.com/AndewSteve/ChineseChess/blob/main/preview/GamePreview.png">
</picture>

# 使用说明
程序依赖Python环境以及Pygame第三方库，运行程序前需要手动安装PyGame库或者使用我们配置好的虚拟环境venvForPyGame

## 准备工作-安装PyGame
### 方法一：配置全局环境
你可以在windows的PowerShell终端中，或者在你的pycharm、VSCode等IDE的终端中直接输入
```
pip install pygame
```

### 方法二：使用虚拟环境
如果你使用的IDE是VSCode，你可以输入快捷键"ctrl+shift+P"选择解释器，定位到项目文件夹中的"ChineseChess\venvForPygame\Scripts\python.exe"

你也可以选择通过终端手动激活虚拟环境
```
cd ./venvForPygame/Scripts
./activate
```

## 开始游戏
配置好pygame环境后，运行ChineseChess.py即可开始游戏
```
python ./ChineseChess.py
```

# 游戏说明
具体象棋规则见[http://www.homygame.com/ngscom/help/xiangqi.htm]

1.本游戏仅支持两个人操作一台机器游玩，左侧会提示行动方

2.你可以在游戏未出胜负时点击右侧“保存”按键保存局面到
```
save/save00.json
```

3.在保存棋局后可以点击“离开”按键退出游戏，其余情况只能点击右上角的X来退出游戏

4.在游戏进程中可以点击“重来”按钮重置棋盘
