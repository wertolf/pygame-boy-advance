## v0.1.1 (working on it)

major changes
* 架构
  * 将 clock.tick 从 update_global 以及 update_local_area 中分离出来
  * 将 update_global/update_local_area 放进 draw_everything 里面
  * 相关的代码调整以及 bug 修复
* Card Prisoner
  * 实现简易的存档 (S) 和读档 (L)
  * 实现帮助界面 (H)
  * 适应架构调整：
    * 在游戏主循环末尾调用 view.draw_everything 加 scrmgr.tick 习语
    * 将 Game Over 的处理逻辑单独拿出循环，实际上也更加合理

minor changes
* 文件重命名
  * key_binding.py -> key_bindings.py
  * static.py -> static_preview.py
  * card_prisoner/main.py -> card_prisoner/card_prisoner.py
* 将 lega.draw 里面的 font_size 和 line_distance 的默认值
  从绝对大小修改为与窗口宽度相关的相对大小
* 将 FPS 的默认值从 30 改为 20
* 重构 pygame_boy_advance.py 的代码
* 一个空的 Magic Tower 界面

## v0.1.0

* 一个结构完整且基本没有冗余的项目框架
  * README
  * LICENSE
  * CHANGELOG
  * code
* 一个结构完整、有始有终的 Card Prisoner 游戏
* 一个用于启动 Card Prisoner 以及后续作品的主界面
