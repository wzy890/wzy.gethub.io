## 查看当前日期
```cpp
//显示日期的命令
in> date
//显示指定格式的日期
in> data +%Y/%m/%d_%H:%M:%S
out> 2021/07/18_16:13:36
```
## 查看日历
```cpp
//显示日历的命令
in> cal
//cal命令的语法： cal [month] [year]
```
## 计算器：bc
```cpp 
in> bc
//bc默认输出整数，若想要输出小数，则需要用 scale=number, number为小数点位数
//退出bc时 输入quit
```

## 热键：

> [TAP]:

接在command（第一个字段）后面即为命令补全

接在文件名（第二个字段）后面即为文件补全

>[Ctrl] + c ：

中断目前程序的运行，例如在 [find /] 时输入 [Ctrl] + c 即可终止程序运行

>[Ctrl] + d :

相当于 exit 可直接离开命令行模式

>[Shift] + [Page UP]|[Page Down] :

命令行界面上下翻页

