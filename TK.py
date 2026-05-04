# import Main
import tkinter
import tkinter as tk
import webbrowser
import socket
import tkinter.ttk as ttk
import tkinter.messagebox
import sys
import os

def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_path, relative_path)
    return os.path.normpath(path)

def set_window_icon(window, icon_path):
    try:
        from PIL import Image, ImageTk
        import base64
        icon_path = get_resource_path(icon_path)
        with open(icon_path, 'rb') as f:
            img_data = f.read()
        import io
        icon = Image.open(io.BytesIO(img_data))
        icon = icon.convert('RGBA')
        photo = ImageTk.PhotoImage(icon)
        window.iconphoto(True, photo)
    except Exception as e:
        print(f"Icon error: {e}")
        pass

def clear_results():
    for widget in inner_frame.winfo_children():
        widget.destroy()

selected_mode = None
_poll_job = None

top = tkinter.Tk()
top.title("域名查询工具")
top.resizable(False,False)
top.geometry("250x500")
top.config(bg="#F0F0F0")
set_window_icon(top, "ICO/256.png")

button_frame = tkinter.Frame(top)
button_frame.pack(side=tkinter.TOP, anchor=tkinter.N, pady=10)

#猴子模式与输入模式只能按下一个
Button1 = tkinter.Button(button_frame, text="猴子模式")
Button2 = tkinter.Button(button_frame, text="输入模式")
Button3 = tkinter.Button(button_frame, text="  开始  ")

Button1.pack(side=tkinter.LEFT, padx=10)
Button2.pack(side=tkinter.LEFT, padx=10)
Button3.pack(side=tkinter.LEFT, padx=10)

#DNS超时设置 + 停止按钮（替代原文本框位置，停止不动）
button_input = tkinter.Frame(top)
button_input.pack(side=tkinter.TOP, anchor=tkinter.N, pady=10)

tkinter.Label(button_input, text="超时:", font=("微软雅黑", 8)).pack(side=tkinter.LEFT,padx=(25,0))
timeout_spin = tkinter.Spinbox(button_input, from_=1, to=10, width=3, font=("微软雅黑", 8))
timeout_spin.delete(0, tk.END)
timeout_spin.insert(0, "3")
timeout_spin.pack(side=tkinter.LEFT, padx=(2,5))
tkinter.Label(button_input, text="秒", font=("微软雅黑", 8)).pack(side=tkinter.LEFT)

Button4 = tkinter.Button(button_input, text="  停止  ")
Button4.pack(side=tkinter.RIGHT, padx=(40,0))

#进度条行
progress_frame = tkinter.Frame(top)
progress_frame.pack(side=tkinter.TOP, fill=tkinter.X, padx=10, pady=(0,5))

progress = ttk.Progressbar(progress_frame, length=140, mode="determinate")
progress.pack(side=tkinter.LEFT, fill=tkinter.X, padx=(10,0))

Button5 = tkinter.Button(progress_frame, text="  清除  ", font=("微软雅黑", 8), width=6, command=clear_results)
Button5.pack(side=tkinter.RIGHT, padx=(0,12))

#文本框行（移到进度条下方，只有输入框）
input_frame = tkinter.Frame(top)
input_frame.pack(side=tkinter.TOP, anchor=tkinter.N, pady=5)

TwoInput = tkinter.Entry(input_frame, width=29)
TwoInput.pack(side=tkinter.LEFT, padx=10)

#滚动区域
content_frame = tkinter.Frame(top, bg="#f0f0f0", relief=tk.SUNKEN, bd=2)
content_frame.pack(side=tkinter.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

scrollbar = tkinter.Scrollbar(content_frame)
scrollbar.pack(side=tkinter.RIGHT, fill=tk.Y)

canvas = tkinter.Canvas(content_frame, bg="#f0f0f0", highlightthickness=0, yscrollcommand=scrollbar.set)
canvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)
scrollbar.config(command=canvas.yview)

#内部容器
inner_frame = tkinter.Frame(canvas, bg="#f0f0f0")
inner_frame.bind("<Configure>", lambda e: canvas.config(scrollregion=canvas.bbox("all")))
canvas_window = canvas.create_window((0,0), window=inner_frame, anchor="nw")

#进度条改颜色
style = ttk.Style()
style.theme_use('clam')
style.configure("green.Horizontal.TProgressbar", background='#4a90d9', troughcolor='#e0e0e0')
style.configure("red.Horizontal.TProgressbar", background='#e74c3c', troughcolor='#e0e0e0')

#自定义DNS解析时间
def get_timeout():
    try:
        return float(timeout_spin.get())
    except ValueError:
        return 3

#完成提示函数
def finish_progress():
    top.after(0, _finish_progress)

def _finish_progress():
    progress.configure(style="red.Horizontal.TProgressbar")
    tkinter.messagebox.showinfo("完成", "域名查询已完成")

def on_canvas_configure(event):
    canvas.itemconfig(canvas_window, width=event.width)

def init_progress(max_value):
    top.after(0, lambda: _init_progress(max_value))

def _init_progress(max_value):
    progress['maximum'] = max_value
    progress['value'] = 0
    progress.configure(style="green.Horizontal.TProgressbar")

def update_progress(current):
    top.after(0, lambda: progress.configure(value=current))

def reset_progress():
    top.after(0, lambda: progress.configure(value=0))

def add_result_block(domain, ip):
    top.after(0, lambda: _add_result_block(domain, ip))

def _add_result_block(domain, ip):
    block = tkinter.Frame(inner_frame, bg="#ffffff", relief=tk.GROOVE, bd=1)
    block.pack(fill=tk.X, padx=5, pady=3)

    lbl_domain = tkinter.Label(block, text=domain, bg="#ffffff", fg="#333333", font=("微软雅黑", 9, "bold"), anchor="w")
    lbl_domain.pack(fill=tk.X, padx=8, pady=(5, 0))

    row2 = tkinter.Frame(block, bg="#ffffff")
    row2.pack(fill=tk.X, padx=8, pady=(2,5))

    lbl_ip = tkinter.Label(row2, text=f"IP: {ip}", bg="#ffffff", fg="#666666", font=("微软雅黑", 8), anchor="w")
    lbl_ip.pack(side=tk.LEFT)

    btn_visit = tkinter.Button(row2, text="访问", font=("微软雅黑", 8), bg="#4a90d9", fg="white", relief=tk.FLAT, width=7, command=lambda d=domain: webbrowser.open(f"http://{d}"))
    btn_visit.pack(side=tk.RIGHT)

def query_domain(domain):
    socket.setdefaulttimeout(get_timeout())
    try:
        ip = socket.gethostbyname(domain)
        add_result_block(domain, ip)
    except (socket.gaierror, socket.timeout):
        pass

def toggle_button(ButtonANY):
    current_relief = ButtonANY.cget("relief")
    if current_relief == tk.RAISED:
        if ButtonANY.cget("text") == "  开始  ":
            ButtonANY.config(relief=tk.SUNKEN,bg="#00A241",fg="white")
        else:
            ButtonANY.config(relief=tk.SUNKEN,bg="#A20036",fg="white")
    else:
        ButtonANY.config(relief=tk.RAISED,bg="#F0F0F0",fg="black")
    
def select_mode(mode):
    global selected_mode
    selected_mode = mode
    if mode == "猴子模式":
        Button1.config(relief=tk.SUNKEN,bg="#A20036",fg="white")
        Button2.config(relief=tk.RAISED,bg="#F0F0F0",fg="black")
        TwoInput.config(state=tk.DISABLED)
    else:
        Button2.config(relief=tk.SUNKEN,bg="#A20036",fg="white")
        Button1.config(relief=tk.RAISED,bg="#F0F0F0",fg="black")
        TwoInput.config(state=tk.NORMAL)

def reset_to_default():
    global selected_mode
    selected_mode = None
    stop_progress_poll()
    stop_flash()
    TwoInput.config(state=tk.NORMAL)
    TwoInput.delete(0, tk.END)
    progress.configure(style="green.Horizontal.TProgressbar")
    reset_progress()
    Button1.config(relief=tk.RAISED, bg="#F0F0F0", fg="black")
    Button2.config(relief=tk.RAISED, bg="#F0F0F0", fg="black")
    Button3.config(relief=tk.RAISED, bg="#F0F0F0", fg="black")
    Button4.config(relief=tk.RAISED, bg="#F0F0F0", fg="black")

#按钮闪烁
flash_job = None
def flash_start_button():
    global flash_job
    current_bg = Button3.cget("bg").lower() if isinstance(Button3.cget("bg"), str) else ""
    if current_bg == "#32d746":
        Button3.config(bg="#065927", fg="#ffffff")
    else:
        Button3.config(bg="#32d746", fg="#ffffff")
    flash_job = top.after(500, flash_start_button)
def stop_flash():
    global flash_job
    if flash_job is not None:
        top.after_cancel(flash_job)
        flash_job = None
reset_progress()

def start_progress_poll(get_value):
    global _poll_job
    stop_progress_poll()
    _poll_job = top.after(200, lambda:_do_poll(get_value))

def _do_poll(get_value):
    global _poll_job
    progress.configure(value=get_value())
    _poll_job = top.after(200, lambda: _do_poll(get_value))

def stop_progress_poll():
    global _poll_job
    if _poll_job is not None:
        top.after_cancel(_poll_job)
        _poll_job = None

canvas.bind("<Configure>", on_canvas_configure)

#鼠标滚轮事件
def on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
def on_mousewheel_linux_up(event):
    canvas.yview_scroll(-1, "units")
def on_mousewheel_linux_down(event):
    canvas.yview_scroll(1, "units")
def bind_mousewheel(event):
    canvas.bind_all("<MouseWheel>", on_mousewheel)
    canvas.bind_all("<Button-4>", on_mousewheel_linux_up)
    canvas.bind_all("<Button-5>", on_mousewheel_linux_down)
def unbind_mousewheel(event):
    canvas.unbind_all("<MouseWheel>")
    canvas.unbind_all("<Button-4>")
    canvas.unbind_all("<Button-5>")

Button1.config(command=lambda: select_mode("猴子模式"))
Button2.config(command=lambda: select_mode("输入模式"))

