import ttkbootstrap as ttk

class ChatWindow():
    def __init__(self):
        # 更改主题
        ttk.Style().theme_use("solar")

        self.toplevel = ttk.Toplevel(
            resizable=None,  # 设置窗口是否可以更改大小
            alpha=1.0,  # 设置窗口的透明度(0.0完全透明）
        )

        self.char_area = ttk.ScrolledText(self.toplevel, width=100, height=30, name="chat_area")
        self.char_area.grid(row=0, column=0, padx=5)
        self.char_area.tag_config('blue', foreground='#4169E1', font=("微软雅黑", 12,))
        self.char_area.tag_config('white', foreground='#FFFFFF', font=("微软雅黑", 14,))

        self.text = ttk.Text(self.toplevel, name="text", width=100, height=5)
        self.text.grid(row=1, column=0)

        self.button = ttk.Button(self.toplevel, name="button", width=10, text="\n     发送     \n")
        self.button.grid(row=1, column=1)

        # 创建表格
        self.tree = ttk.Treeview(self.toplevel, show='headings', height=30)
        # 定义列
        self.tree["columns"] = ["username"]
        self.tree.grid(row=0, column=1, padx=15, pady=10)
        # 设置列宽度
        self.tree.column("username", width=150, anchor=ttk.CENTER)
        # 添加列名
        self.tree.heading("username", text="当前在线用户")


if __name__ == '__main__':
    pass
