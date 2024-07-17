## TODO

### Card Prisoner

关键挑战
* [ ] 实现“库存”“商店”“技能栏”共用同一个屏幕区域并进行切换

其他
* [ ] GameController._update_default_message 在 ItemList 的不同 mode 下的工作逻辑不同
* [ ] ItemList.make_items 在设计上有点奇怪
* [ ] View.draw_everything 需要用到 Player 作为参数，好像有点奇怪
* [ ] 抽到 SSR 卡时触发额外的动画效果
* [ ] 使用 B 键开启/关闭背景音乐
* [ ] (bug fix) 全局淡出即使已经看不到内容了还是要等待一段额外的时间才能看到 game over 的文本
* [ ] ScreenManager 的 UML 类图
* [ ] 选中给定 Skill 时显示相应的说明文字

## v0.1.1 (working on it)

major changes
* 文档
  * 边整理 CHANGELOG 边回顾目前为止的所有变化
  * 使用 pptx 绘制 UML 类图
* 架构
  * 将 clock.tick 从 update_global 以及 update_local_area 中分离出来
  * 将 update_global/update_local_area 放进 draw_everything 里面
  * 相关的代码调整以及 bug 修复
  * 新增 display_help 函数
  * 新增 take_screenshot 函数：基于 pygame.image.save 实现截图功能
  * 修改 ScreenManager 类
    * 新增 font_size_normal 属性
    * 新增 font_size_large 属性
    * 新增 default_line_distance 属性
    * 新增 default_border_thickness 属性
    * 新增 default_border_radius 属性
* Card Prisoner
  * 实现简易的存档 (key_bindings.SAVE_GAME) 和读档 (key_bindings.LOAD_GAME)
  * 实现帮助界面 (key_bindings.DISPLAY_HELP)
    * basic key bindings
    * more key bindings
    * [ ] background story 不妨交给 GPT
  * 适应架构调整：
    * 在游戏主循环末尾调用 view.draw_everything + scrmgr.tick
    * 将 Game Over 的处理逻辑单独拿出循环，实际上也更加合理
  * 在 Item 类中新增 `__str__` 方法
    并对 ItemList.draw_everything 进行相应修改
  * 取消 model/view/controler 的显式目录划分，而是在 `__init__.py` 中通过注释表明各模块的性质，即不同的模块到底分别属于 model/view/controller 中的哪一类
    * 这样做的一个原因是：分成若干子目录之后，每个子目录都会多出一个 `__pycache__` 子目录，看着心烦
  * 修改 Player 类
    * health 改名为 HP
    * thirst 改名为 MP
    * 取消 sanity 属性
    * 取消 status 属性
    * 取消 token 属性
  * 重构视图相关 class
    * 将 draw_item 函数整合进 ItemList 作为 method
    * 简化：取消“切换侧边栏选项时，同时变换 ItemList 显示内容”的行为
    * 将 update_default_message 从 View 移入 GameController
      并在 GameController 的以下方法的末尾进行调用
      * on_arrow_key_up
      * on_confirm
      * on_cancel
  * 调整游戏机制
    * 简化：取消药物类卡片
* 从 mota-js 中导入素材
  并更新 README 的“许可证”一节

minor changes
* 文件重命名
  * key_binding.py -> key_bindings.py
  * static.py -> static_preview.py
  * card_prisoner/main.py -> card_prisoner/card_prisoner.py
* 变量重命名
  * 将 key_binding.py 中的变量名全部大写，以表示它们的值在程序运行的过程中应保持不变
* 将 FPS 的默认值从 30 改为 20
* 重构 pygame_boy_advance.py 的代码
* Card Prisoner
  * 删除 BACK 按钮，改用 key_bindings.RETURN_TO_TITLE 键达成同样的功能
  * 进入游戏时被选中的 SideBar 选项改为 ABOUT
  * 移除 animations.py 模块
  * 将 actions.py 与 card_prisoner.py 整合为 GameController 类
  * (bug fix) 进入 2 级列表时，索引重置为零
* Magic Tower
  * 一个空的界面
* 补上 requirements.txt
* 新建 examples 目录
  * 一个空的 story_mode.py 文件：计划用于展示使用 lega 制作剧情类游戏的潜力

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

## v0.1.0 (2024-07-14)

* 一个结构完整且基本没有冗余的项目框架
  * README
  * LICENSE
  * CHANGELOG
  * code
* 一个结构完整、有始有终的 Card Prisoner 游戏
* 一个用于启动 Card Prisoner 以及后续作品的主界面

## v0.0.2 (2024-07-14)

* 完善 README
  * 添加**环境配置**一节并新建 requirements.txt 文件
* 提高 card_prisoner 项目的可读性、可维护性
  * 新建 model 和 view 子目录以反映该项目所采用的 MVC 设计模式
  * 将 Inventory 重命名为 ItemList
  * 大规模引入 Enum
    * 将 View 的 1 和 2 两种状态改成 Enum 类型的常量 ViewMode
    * PlayerStatus
    * 将 InventoryItemIndex 和 CardEnum 分别开
      * 含义不同，前者强调的是视图中的位置，后者强调的是卡片的类型
    * 定义 SideBarOptions 枚举，将其与 actions 区分开
  * 根据 MVC 的设计思想
    * SideBar 不应该将 Player 作为其成员
    * View 也不应该将 Player 作为其成员
  * **一个重要的简化：只以整块屏幕为单位更新每一帧的内容**
    * 放弃对微不足道的性能提升的偏执
    * 简化项目的结构和设计
  * 新建 shared 子目录
    * 将 shared.py 重命名为 misc.py 并移入 shared 子目录
    * 将 draw_text 重命名为 draw_text_single_line
    * 新建 draw_text_multi_line 函数
    * 将 constants.py 移入 shared 子目录
    * 将 constants.py 重命名为 messages.py
  * 删掉部分 assert 语句的括号
    * 这是从 C 语言里带过来的习惯
  * 着手实现“商店”和“技能”选项
    * 这实际上是在维护过程中的一个副产品：因为发现当可读性提升、结构简化之后，实现它们只是顺手就能完成的事
  * 调整帮助消息 (messages) 的内部传递机制
    * 之前用的是字典，现在改成更为简单的 View.update_default_message 方法中的条件分支
  * 调整游戏机制
    * 每天 Health 和 Thirst 的减少量都是 20
    * [x] 抽不到 SSR 和补给卡时 Sanity 会降低
    * [ ] Sanity 为 0 时晚上有一定概率死亡
    * [x] 抽到 SSR 时 Sanity 会回升
    * [ ] 抽到 SSR 时 Sanity 低于 20 会死亡
    * [ ] 新的一天开始时 Sanity 会回升
  * 引入 Item 和 ShopItem 类
  * 按住 D 键连续抽卡
    * 刚按下时抽 1 次卡
    * 按下 KEYDOWN_INITIAL_INTERVAL 秒后进入长按状态
    * 长按状态下，每隔 DRAW_CARD_TIME_INTERVAL 秒抽 1 次卡
  * bug fix: 失败动画播放结束后不应该重绘游戏界面

## v0.0.1 (2024-07-11)

* polish README
  * 完善基本结构
  * 将 Mini Jumper 重命名为 Chinese Checkers 并做了一些历史考据
* 将许可证更改为 MIT 许可证
* 完善 Home 界面
  * 添加 Chinese Checkers 选项
  * 添加 Magic Tower 选项
  * 从 Card Prisoner 界面返回时重新设定窗口的 caption 为 Pygame Boy Advance
* 完善 Card Prisoner 游戏界面
  * 初始化时设定窗口的 caption 为 Card Prisoner
  * 完善 inventory 的 item 的种类及其背后的数据逻辑
  * 按 D 键可以抽卡
  * 添加 WATER 相关逻辑
    * drink_water
    * DIE OF THIRST
  * 使用 lega.an.fade_out.FadeOut 实现胜利动画和失败动画

## v0.0.0 (2024-07-10)

* 实现基本的 Home 界面，可以使用上下方向键选择不同的选项
* 实现 Card Prisoner 游戏界面
  * 可以使用上下方向键选择左侧栏中的不同 action
  * 在变换选择的同时变换右上角文本框中的内容
  * 引入 View - 还是觉得 OOP 在传参数这件事上真的很方便
  * 引入 mode 实现 1 级列表 SideBar.actions 和 2 级列表 Inventory.items 之间的切换
  * bug fix: should not change action (in view) when view.mode != 1
  * 可以使用上下左右方向键在 2 级列表中切换选项
  * bug fix: 2 级列表右下角按右键会出现 list out of range
    * solution: n_rows * n_cols - 1
  * 进入 2 级列表后在 TextBox 中显示 2 级列表相关的帮助
  * bug fix: unexpected help message on start up
  * bug fix: unexpected help message on mode switch
  * 实现 End Today 的基本功能
  * 显示 Game Over 信息
  * Game Over 之后按 R 键重新开始游戏
  * bug fix: shared.calculate_centery when n_lines is even
