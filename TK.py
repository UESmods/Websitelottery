# import Main
import tkinter
import tkinter as tk
import webbrowser
import socket
import tkinter.ttk as ttk

selected_mode = None
_poll_job = None

top = tkinter.Tk()
top.title("域名查询工具")
top.resizable(False,False)
top.geometry("250x500")
top.config(bg="#F0F0F0")

button_frame = tkinter.Frame(top)
button_frame.pack(side=tkinter.TOP, anchor=tkinter.N, pady=10)

#猴子模式与输入模式只能按下一个
Button1 = tkinter.Button(button_frame, text="猴子模式")
Button2 = tkinter.Button(button_frame, text="输入模式")
Button3 = tkinter.Button(button_frame, text="  开始  ")

Button1.pack(side=tkinter.LEFT, padx=10)
Button2.pack(side=tkinter.LEFT, padx=10)
Button3.pack(side=tkinter.LEFT, padx=10)

button_input = tkinter.Frame(top)
button_input.pack(side=tkinter.TOP, anchor=tkinter.N, pady=10)

progress = ttk.Progressbar(top, length=220, mode="determinate")
progress.pack(side=tkinter.TOP, pady=(0,5))

TwoInput = tkinter.Entry(button_input,width=19)
Button4 = tkinter.Button(button_input,text="  停止  ")

TwoInput.pack(side=tkinter.LEFT, padx=10)
Button4.pack(side=tkinter.LEFT, padx=10)

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

def on_canvas_configure(event):
    canvas.itemconfig(canvas_window, width=event.width)

def init_progress(max_value):
    top.after(0, lambda: _init_progress(max_value))

def _init_progress(max_value):
    progress['maximum'] = max_value
    progress['value'] = 0

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
    socket.setdefaulttimeout(3)
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
    Button1.config(relief=tk.RAISED, bg="#F0F0F0", fg="black")
    Button2.config(relief=tk.RAISED, bg="#F0F0F0", fg="black")
    Button3.config(relief=tk.RAISED, bg="#F0F0F0", fg="black")
    Button4.config(relief=tk.RAISED, bg="#F0F0F0", fg="black")

#按钮闪烁
flash_job = None
def flash_start_button():
    global flash_job
    current_bg = Button3.cget("bg")
    if current_bg == "#00A241":
        Button3.config(bg="#7cfc00", fg="#ffffff")
    else:
        Button3.config(bg="#00a241", fg="#ffffff")
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

