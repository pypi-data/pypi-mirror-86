QBinder
-------

    **Python Qt 数据绑定框架** `Wiki
    文档 <https://wiki.l0v0.com/Python/QBinder/>`__

.. figure:: https://cdn.jsdelivr.net/gh/FXTD-ODYSSEY/CG_wiki@gh-pages/Python/QBinder/_img/04_slider.gif
   :alt: slider 案例

   slider 案例
      slider 最大值最小值同步检测。

--------------

.. figure:: https://cdn.jsdelivr.net/gh/FXTD-ODYSSEY/CG_wiki@gh-pages/Python/QBinder/_img/05_todo.gif
   :alt: todo 案例

   todo 案例
`案例代码 <https://github.com/FXTD-ODYSSEY/QBinder/blob/master/example/todo_app/todo.py>`__

    |   这个案例是模仿 Vue 文档提供的 todo MVC 案例做的
    `链接 <https://vuejs.org/v2/examples/todomvc.html>`__
    |   配合 setStyleSheet 绑定样式表，实现样式动态更新。
    |   可以在独立环境运行。

特性
----

-  利用 lambda 参数绑定数据 操作简单
-  数据自动存储和记载
-  QEventHook 全局事件钩子
-  Python 2 & 3 兼容
-  纯 Python 编写 兼容 DCC 软件

同步机制
--------

      关于 QBinder 的前世今生以及 绑定的实现机制可以参阅我博客的文章
    `链接 <https://blog.l0v0.com/posts/301b3c35.html>`__
