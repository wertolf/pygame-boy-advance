## v0.1.1 (working on it)

major changes
* 架构
  * 将 clock.tick 从 update_global 以及 update_local_area 中分离出来
  * 将 update_global/update_local_area 放进 draw_everything 里面
  * 相关的代码调整以及 bug 修复
  * 在 lega.misc 里面新增 display_help 函数
* Card Prisoner
  * 实现简易的存档 (key_bindings.SAVE_GAME) 和读档 (key_bindings.LOAD_GAME)
  * 实现帮助界面 (key_bindings.DISPLAY_HELP)
    * [ ] quick start
    * [ ] background story 不妨交给 GPT
  * 适应架构调整：
    * 在游戏主循环末尾调用 view.draw_everything + scrmgr.tick 习语
    * 将 Game Over 的处理逻辑单独拿出循环，实际上也更加合理

minor changes
* 文件重命名
  * key_binding.py -> key_bindings.py
  * static.py -> static_preview.py
  * card_prisoner/main.py -> card_prisoner/card_prisoner.py
* 变量重命名
  * 将 key_binding.py 中的变量名全部大写，以表示它们的值在程序运行的过程中应保持不变
* 将 lega.draw 里面的 font_size 和 line_distance 的默认值
  从绝对大小修改为与窗口宽度相关的相对大小
* 将 FPS 的默认值从 30 改为 20
* 重构 pygame_boy_advance.py 的代码
* 一个空的 Magic Tower 界面
* Card Prisoner
  * 删除 BACK 按钮，改用 key_bindings.RETURN_TO_TITLE 键达成同样的功能
  * 进入游戏时被选中的 SideBar 选项改为 ABOUT
  * 移除 animations.py 模块

### 为什么将 display.update 与 clock.tick 相分离

* 它们本身就是 2 个独立的函数，从属于 pygame 的 2 个不同模块
* 之所以习惯于把它们放在一起，主要是受到 Sweigart 的影响
* 对于**非即时类**的游戏来说
  画面的修改是离散的、**稀疏的**
  因此完全可以在修改（尤其是局部修改）画面内容之后立即调用 display.update
  而 clock.tick 控制的是游戏主循环的迭代频率
  主循环不仅包括画面的更新 (display.update)
  还包括事件的处理以及画面的修改/绘制
  因此将 clock.tick 放在每次迭代的末尾是合理的
* clock.tick 直接决定了游戏进程对 CPU 的占用情况
  从而决定了电量消耗与热量的产生
  **power consumption 是嵌入式系统的核心关切之一**
  **因此上面的讨论并不是可有可无、没有意义的**

## v0.1.0

* 一个结构完整且基本没有冗余的项目框架
  * README
  * LICENSE
  * CHANGELOG
  * code
* 一个结构完整、有始有终的 Card Prisoner 游戏
* 一个用于启动 Card Prisoner 以及后续作品的主界面
