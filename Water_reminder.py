import tkinter as tk
from tkinter import messagebox
import time
import sys
import os
from plyer import notification

def resource_path(relative_path):
    """获取打包资源的绝对路径"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class HydrationReminder:
    def __init__(self, root):
        self.root = root
        self.root.title("喝水提醒助手")
        self.root.geometry("400x250")
        try:
            self.root.iconbitmap(resource_path('water.ico'))
        except Exception as e:
            print(f"图标加载失败: {e}")
        self.reminder_active = False

    def send_reminder(self):
        try:
            notification.notify(
                title='喝水提醒',
                message=self.message_var.get(),
                app_name='喝水助手',
                app_icon=resource_path('water.ico'),
                timeout=10
            )
            self.last_reminder_time = time.strftime("%Y-%m-%d %H:%M:%S")
            self.last_time_var.set(f"上次提醒时间: {self.last_reminder_time}")
        except Exception as e:
            messagebox.showerror("通知错误", f"发送提醒失败: {str(e)}")

    def create_widgets(self):
        # 间隔设置
        tk.Label(self.root, text="提醒间隔（分钟）:").pack(pady=5)
        self.interval_var = tk.StringVar(value="60")
        self.interval_entry = tk.Entry(self.root, textvariable=self.interval_var, width=10)
        self.interval_entry.pack(pady=5)
        
        # 自定义消息
        tk.Label(self.root, text="提醒消息:").pack(pady=5)
        self.message_var = tk.StringVar(value="该喝水啦！请补充水分")
        self.message_entry = tk.Entry(self.root, textvariable=self.message_var, width=30)
        self.message_entry.pack(pady=5)
        
        # 按钮区域
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        self.start_button = tk.Button(button_frame, text="开始提醒", command=self.start_reminder)
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        self.stop_button = tk.Button(button_frame, text="停止提醒", command=self.stop_reminder, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=10)
        
        # 状态显示
        self.status_var = tk.StringVar(value="状态: 等待启动")
        self.status_label = tk.Label(self.root, textvariable=self.status_var, font=("Arial", 10))
        self.status_label.pack(pady=10)
        
        # 最后提醒时间
        self.last_time_var = tk.StringVar(value="上次提醒时间: 无")
        self.last_time_label = tk.Label(self.root, textvariable=self.last_time_var, font=("Arial", 9))
        self.last_time_label.pack(pady=5)
        
        # 退出按钮
        tk.Button(self.root, text="退出程序", command=self.root.quit).pack(pady=10)
    
    def start_reminder(self):
        try:
            interval_minutes = float(self.interval_var.get())
            if interval_minutes <= 0:
                messagebox.showerror("错误", "间隔时间必须大于0")
                return
                
            self.reminder_active = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.interval_entry.config(state=tk.DISABLED)
            self.status_var.set(f"状态: 每 {interval_minutes} 分钟提醒一次")
            
            # 立即发送一次提醒
            self.send_reminder()
            
            # 设置定时器
            self.schedule_next_reminder(interval_minutes)
            
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字")
    
    def stop_reminder(self):
        self.reminder_active = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.interval_entry.config(state=tk.NORMAL)
        self.status_var.set("状态: 提醒已停止")
    
    def schedule_next_reminder(self, interval_minutes):
        if not self.reminder_active:
            return
            
        # 计算毫秒数
        interval_ms = int(interval_minutes * 60 * 1000)
        
        # 发送提醒
        self.send_reminder()
        
        # 安排下一次提醒
        self.root.after(interval_ms, lambda: self.schedule_next_reminder(interval_minutes))

if __name__ == "__main__":
    root = tk.Tk()
    app = HydrationReminder(root)
    root.mainloop()