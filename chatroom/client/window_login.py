import ttkbootstrap as ttk

class LoginWindow():
    def __init__(self):
        # 登录窗口初始化
        self.root = ttk.Window(
            title="聊天室登录",  # 设置窗口的标题
            themename="solar",  # 设置主题
            size=(370, 175),  # 窗口的大小
            resizable=None,  # 设置窗口是否可以更改大小
            alpha=1.0,  # 设置窗口的透明度(0.0完全透明）
        )
        self.root.place_window_center()  # 让显现出的窗口居中
        self.root.resizable(False, False)  # 让窗口不可更改大小

        self.label1 = ttk.Label(self.root, name="label1")
        self.label1['text'] = "用户名"
        self.label1.grid(row=0, column=0, padx=10, pady=10)

        self.entry1 = ttk.Entry(self.root, name="entry1")
        self.entry1.grid(row=0, column=1, padx=5, pady=10)
        self.entry1['width'] = 30

        self.label2 = ttk.Label(self.root, name="label2")
        self.label2['text'] = "密码"
        self.label2.grid(row=1, column=0, padx=10, pady=10)

        self.entry2 = ttk.Entry(self.root, name="entry2")
        self.entry2.grid(row=1, column=1, padx=5, pady=10)
        self.entry2['width'] = 30
        self.entry2['show'] = '*'

        self.frame1 = ttk.Frame(self.root, name="frame1")
        self.button1 = ttk.Button(self.frame1, name="button1")
        self.button1["text"] = "      登录      "
        self.button1.pack(side=ttk.LEFT, padx=20)


        self.button2 = ttk.Button(self.frame1, name="button2")
        self.button2["text"] = "      清空      "
        self.button2.pack(side=ttk.LEFT)


        self.frame1.grid(row=2, columnspan=2, pady=5)

if __name__ == '__main__':
    LoginWindow().root.mainloop()