# pygame 文档阅读笔记

## notes on event handling

According to https://www.pygame.org/docs/ref/event.html:
> To get the state of various input devices,
> you can forego the event queue and access the input devices directly
> with their appropriate modules:
> `pygame.mouse`,
> `pygame.key`,
> and `pygame.joystick`.
> If you use this method,
> remember that pygame requires some form of communication
> with the system window manager and other parts of the platform.
> To keep pygame in sync with the system,
> you will need to call `pygame.event.pump()` to keep everything current.
> Usually, this should be called once per game loop.

这里让我想到，
如果想同时处理两个按键的长按，
可以直接放弃事件队列，
然后使用 pygame.key.get_pressed 检测相应的按键是否处于被按下的状态，
然后设置相应的计时器 (timer) 实现长按效果

这是因为在 pygame 2.6.0 中，
即使使用 pygame.key.set_repeat 激活了库函数对长按效果的处理，
如果同时按下两个按键，还是只有较晚按下的那个会连续触发 KEYDOWN 事件

当然，一般来说并不需要处理两个按键长按的情况，
即使需要在一个 2D 游戏中进行任意方向的移动，比如同时按下左方向键和上方向键，
只需要在相应的 KEYDOWN 中将相应的 bool 变量设为 True 即可处理角色的移动
