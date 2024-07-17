# 卡片囚徒 (Card Prisoner) 设计文档

## 经验总结 (Lessons Learned)

### 道：原则 (Principles)

* 简单源于规整 (simplicity favors regularity)
* Rome wasn't built in one day.
* 李艺老师语：好的项目都是重构出来的
* 管理预期：新手很容易眼高手低，想实现的功能太多，结果完工遥遥无期，最终草草了事或者放弃

### 术：技术细节 (Techniques)

* 同样的内容，可以用简单的视觉效果呈现，也可以用复杂的效果呈现；
  为了尽快完成项目，应该先用简单的效果
* 游戏的可玩性源自数据/策划，与界面关系不大
* 善用 vscode 的 refactor 以及 find/replace 功能还有 egrep
  灵活调整标识符、文件名以及字符串字面值常量
* 不要一学什么新的语言特性或者知识点就着急在项目中使用，不一定合适
* 相对于窗口的宽度/高度设置各类长度/尺寸，尽量少用绝对的像素值

## 基本原则：简化

### 具体体现

* 只设 1 个存档
* 先用 pickle 实现持久化，觉得有必要增强安全性的时候再考虑换成 json

* 先不去纠结局部重绘可能带来的性能优化，一律使用全局重绘 (draw_everything)
* 在游戏主循环的末尾调用 view.draw_everything
  而不是在处理完每个事件之后分别调用

* 如果按钮和按键可以达成同样的目的，不妨只保留一个，
  否则会产生相同的事件处理代码，增加维护成本

## 设计细节

### rect 与 border_rect 的区别

rect 是该组件在屏幕上所占的区域

border_rect 是该组件的边框及边框内的内容**相对于 rect** 所占的区域

## Ideas

### 2024-07-17 13:00

我们本质上只是需要一个 scalable 的方式来为不同的 Item (Card, Skill, ...)
指定其缩写 (abbr) 及描述 (desc)
* abbr 用于 Item 的绘制
* desc 用于帮助文本的显示

因此 XML 和 JSON 和 Python 的 `dict` 都能完成我们的需求

既然项目整体都是基于 Python 那么不妨沿用 Python 内置的 `dict` 类型

顺便到 Real Python 上对相关知识点进行复习和深化

https://realpython.com/python-dicts/

### 2024-07-17 11:00

selected_option_index 和 selected_item_index 应该分别从属于
SideBar 和 ItemList
而不是作为 View 的成员

当接收到上/下/左/右方向键的抬起事件时，控制器需要
* 更新相应的 option index 或 item index
* 更新 textbox 的文本
* 重绘整个屏幕的内容


除 QUIT 外，Card Prisoner 实际上只需要处理两类事件：KEYUP 和 KEYDOWN
并且相应事件处理代码的结构都是
* 判断是哪个 key
  * 一连串 if/elif
  * match/case
* 执行相应的操作
  * 更新 model
  * 在 view 上反映 model 的更新：更新 view

### 2024-07-16 晚间漫步

* 取消 Sanity
* 将 Health 改为 HP
* 将 Thirst 改为 MP

* 解决滥用 Enum 的问题

### 2024-07-16 17:30

* 优化 ItemList 相关算法
* 整理 CHANGELOG
  回顾所作的修改
* 将 private 仓库中的 CHANGELOG 作为 v0.0.x 并入当前仓库
* 在文档中加入 Ideas 小节，按时间逆序记录关键想法的产生
* 用 UML 类图绘制一下几个视图 class 之间的关系

## 其他
