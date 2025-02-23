import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from config import PRIMARY_COLOR, SECONDARY_COLOR, BACKGROUND_MAIN, BACKGROUND_PANEL, FONT_MAIN, FONT_TITLE, STYLE_BUTTON_OPTIONS, STYLE_LABEL_OPTIONS
from network_diagram import build_network_graph, compute_critical_path
from utils import save_figure_as_image

class NetworkDiagramApp:
    def __init__(self, root):
        self.root = root
        self.root.title("رسم المخططات الشبكية")
        self.root.geometry("1200x650")
        self.root.configure(bg=BACKGROUND_MAIN)
        self.activities = {}
        self.graph = nx.DiGraph()
        self.critical_path_tasks = []
        self.st = 0
        self.laststart = 0
        self.activity_widgets = []

        # إعداد الأنماط العامة باستخدام ttk Style
        # style = ttk.Style()
        # style.configure("TButton", **STYLE_BUTTON_OPTIONS)
        # style.configure("TLabel", **STYLE_LABEL_OPTIONS)
        style = ttk.Style()
        style.theme_use("clam")  # استخدام ثيم 'clam' لدعم تغييرات الخلفية في الأزرار
        style.configure("TButton", **STYLE_BUTTON_OPTIONS)
        # إطار الإدخال (لوحة جانبية)
        self.frame_input = tk.Frame(self.root, bg=BACKGROUND_PANEL)
        self.frame_input.pack(side=tk.RIGHT, fill=tk.Y)

        ttk.Label(self.frame_input, text="عدد الأنشطة").grid(row=0, column=2, padx=5, pady=5)
        self.entry_num_activities = ttk.Entry(self.frame_input, width=10)
        self.entry_num_activities.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(self.frame_input, text="تحديد الأنشطة", command=self.set_activities).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(self.frame_input, text="حفظ الرسم", command=self.save_network_image).grid(row=1, column=0, padx=5, pady=10)

        # إطار الرسم
        self.frame_canvas = tk.Frame(self.root, bg="white")
        self.frame_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def set_activities(self):
        if hasattr(self, 'frame_input1'):
            self.frame_input1.destroy()

        self.frame_input1 = tk.Frame(self.frame_input, bg=BACKGROUND_PANEL)
        self.frame_input1.grid(row=6, column=0, columnspan=3, padx=0, pady=0, sticky="nsew")

        canvas = tk.Canvas(self.frame_input1, bg=BACKGROUND_PANEL, height=500)
        canvas.grid(row=0, column=0, sticky="nsew")

        scrollbar = tk.Scrollbar(self.frame_input1, orient="vertical", command=canvas.yview, width=10)
        scrollbar.grid(row=0, column=1, sticky="ns")
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollable_frame = tk.Frame(canvas, bg=BACKGROUND_PANEL)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        try:
            num_activities = int(self.entry_num_activities.get())
            if num_activities <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("خطأ", "يرجى إدخال عدد صحيح موجب للأنشطة.")
            return

        # تنظيف الواجهات السابقة
        for task_label, entry_duration, entry_dependencies in self.activity_widgets:
            task_label.destroy()
            entry_duration.destroy()
            entry_dependencies.destroy()
        self.activity_widgets.clear()

        # عناوين الأعمدة
        ttk.Label(scrollable_frame, text="النشاط").grid(row=3, column=2, padx=10, pady=10)
        ttk.Label(scrollable_frame, text="الأنشطة السابقة").grid(row=3, column=1, padx=10, pady=10)
        ttk.Label(scrollable_frame, text="المدة").grid(row=3, column=0, padx=10, pady=10)

        # إنشاء المدخلات لكل نشاط
        for i in range(num_activities):
            task_label = ttk.Label(scrollable_frame, text=chr(65 + i))
            task_label.grid(row=i + 4, column=2, padx=10, pady=10)

            entry_dependencies = ttk.Entry(scrollable_frame, width=10)
            entry_dependencies.grid(row=i + 4, column=1, padx=10, pady=10)

            entry_duration = ttk.Entry(scrollable_frame, width=10)
            entry_duration.grid(row=i + 4, column=0, padx=10, pady=10)

            self.activity_widgets.append([task_label, entry_duration, entry_dependencies])

        ttk.Button(scrollable_frame, text="عرض المخطط", command=self.draw_network).grid(
            row=num_activities + 6, column=1, padx=10, pady=10)

        scrollable_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def draw_network(self):
        # بناء الرسم الشبكي باستخدام الدالة المفصولة
        self.graph = build_network_graph(self.activity_widgets)
        critical_path_nodes, critical_duration = compute_critical_path(self.graph)
        self.critical_path_tasks = []
        for i in range(len(critical_path_nodes) - 1):
            edge_data = self.graph.get_edge_data(critical_path_nodes[i], critical_path_nodes[i + 1])
            if edge_data and "label" in edge_data:
                task_name = edge_data["label"].split(":")[0].strip()
                self.critical_path_tasks.append(task_name)

        # رسم الرسم الشبكي وتلوين المسار الحرج
        fig, ax = plt.subplots(figsize=(10, 8))
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_size=2000, node_color="lightblue", ax=ax)
        edge_labels = nx.get_edge_attributes(self.graph, "label")
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, ax=ax)

        critical_edges = [(critical_path_nodes[i], critical_path_nodes[i + 1])
                          for i in range(len(critical_path_nodes) - 1)]
        nx.draw_networkx_edges(self.graph, pos, edgelist=critical_edges, edge_color="red", width=2.5, ax=ax)

        critical_path_str = " -> ".join(self.critical_path_tasks)
        ax.set_title(f"{critical_path_str} = {critical_duration}", fontsize=14, color="darkred")

        # تحديث منطقة الرسم في الواجهة
        for widget in self.frame_canvas.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, master=self.frame_canvas)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.add_interactivity(canvas, pos, critical_edges)

    def add_interactivity(self, canvas, pos, critical_edges):
        def on_click(event):
            if event.xdata is not None and event.ydata is not None:
                for node, (x, y) in pos.items():
                    if (event.xdata - x) ** 2 + (event.ydata - y) ** 2 < 0.01:
                        canvas.moving_node = node
                        break

        def on_release(event):
            canvas.moving_node = None

        def on_motion(event):
            if hasattr(canvas, "moving_node") and canvas.moving_node:
                pos[canvas.moving_node] = (event.xdata, event.ydata)
                # تحديث الرسم مع إعادة حساب المسار الحرج
                critical_path_nodes, critical_duration = compute_critical_path(self.graph)
                critical_path_tasks = []
                for i in range(len(critical_path_nodes) - 1):
                    edge_data = self.graph.get_edge_data(critical_path_nodes[i], critical_path_nodes[i + 1])
                    if edge_data and "label" in edge_data:
                        task_name = edge_data["label"].split(":")[0].strip()
                        critical_path_tasks.append(task_name)
                critical_path_str = " -> ".join(critical_path_tasks)
                canvas.figure.clear()
                ax = canvas.figure.add_subplot(111)
                nx.draw(self.graph, pos, with_labels=True, node_size=2000, node_color="lightblue", ax=ax)
                edge_labels = nx.get_edge_attributes(self.graph, "label")
                nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, ax=ax)
                nx.draw_networkx_edges(self.graph, pos, edgelist=critical_edges, edge_color="red", width=2.5, ax=ax)
                ax.set_title(f"{critical_path_str} = {critical_duration}", fontsize=14, color="darkred")
                canvas.draw()

        canvas.mpl_connect("button_press_event", on_click)
        canvas.mpl_connect("button_release_event", on_release)
        canvas.mpl_connect("motion_notify_event", on_motion)

    def save_network_image(self):
        # إعادة رسم الرسم الشبكي وحفظه باستخدام الدالة المساعدة
        fig, ax = plt.subplots(figsize=(10, 8))
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_size=2000, node_color="lightblue", ax=ax)
        edge_labels = nx.get_edge_attributes(self.graph, "label")
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, ax=ax)

        critical_path_nodes, _ = compute_critical_path(self.graph)
        critical_edges = [(critical_path_nodes[i], critical_path_nodes[i + 1])
                          for i in range(len(critical_path_nodes) - 1)]
        nx.draw_networkx_edges(self.graph, pos, edgelist=critical_edges, edge_color="red", width=2.5, ax=ax)
        save_figure_as_image(fig)





