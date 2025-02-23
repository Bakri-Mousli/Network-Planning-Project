import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import networkx as nx
import matplotlib.pyplot as plt
from PIL import ImageGrab
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class NetworkDiagramApp:
    critical_path_tasks = []
    activities = {}
    st = 0
    laststart = 0

    def __init__(self, root):
        self.root = root
        self.root.title("رسم المخططات الشبكية")
        self.root.geometry("1200x650")
        self.root.configure(bg="#f0f8ff")  # لون خلفية لطيف
        self.activities = {}
        self.graph = nx.DiGraph()

        # إعداد الأنماط
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 12), padding=6, background="blue", foreground="#0078D7")
        style.configure("TLabel", font=("Helvetica", 12), padding=4)

        # إطار الإدخال
        self.frame_input = tk.Frame(self.root, bg="#e0f7fa")
        self.frame_input.pack(side=tk.RIGHT, fill=tk.Y)



        ttk.Label(self.frame_input, text="عدد الأنشطة", background="#e0f7fa").grid(row=0, column=2, padx=5, pady=5)
        self.entry_num_activities = ttk.Entry(self.frame_input, width=10)
        self.entry_num_activities.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(self.frame_input, text="تحديد الأنشطة", command=self.set_activities).grid(row=0, column=0, padx=5, pady=5)

        ttk.Button(self.frame_input, text="حفظ الرسم", command=self.save_frame_as_image).grid(row=1, column=1, padx=5, pady=5)
        self.activity_widgets = []

        # إطار الرسم
        self.frame_canvas = tk.Frame(self.root, bg="lightgreen")
        self.frame_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


        self.activity_widgets = []

    def set_activities(self):
        if hasattr(self, 'frame_input1'):
            self.frame_input1.destroy()

        # إنشاء الـ Frame الرئيسي الذي يحتوي على المحتوى ويحتل 3 أعمدة
        self.frame_input1 = tk.Frame(self.frame_input, bg="#e0f7fa")
        self.frame_input1.grid(row=6, column=0, columnspan=3, padx=0, pady=0, sticky="nsew")

        # إنشاء الـ Canvas لتمكين التمرير
        canvas = tk.Canvas(self.frame_input1, bg="#e0f7fa" , height=500)
        canvas.grid(row=0, column=0, sticky="nsew")

        # إضافة شريط التمرير العمودي مع تقليل العرض
        scrollbar = tk.Scrollbar(self.frame_input1, orient="vertical", command=canvas.yview, width=10)
        scrollbar.grid(row=0, column=1, sticky="ns")
        canvas.configure(yscrollcommand=scrollbar.set)

        # إنشاء إطار إضافي داخل الـ Canvas
        scrollable_frame = tk.Frame(canvas, bg="#e0f7fa")
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        try:
            num_activities = int(self.entry_num_activities.get())
            if num_activities <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("خطأ", "يرجى إدخال عدد صحيح موجب للأنشطة.")
            return

        # حذف أي عناصر سابقة في القائمة
        for task_label, entry_duration, entry_dependencies in self.activity_widgets:
            task_label.destroy()
            entry_duration.destroy()
            entry_dependencies.destroy()
        self.activity_widgets.clear()

        # إضافة التسميات للأعمدة
        ttk.Label(scrollable_frame, text="النشاط", background="#e0f7fa").grid(row=3, column=2, padx=10, pady=10)
        ttk.Label(scrollable_frame, text="الأنشطة السابقة", background="#e0f7fa").grid(row=3, column=1, padx=10,
                                                                                       pady=10)
        ttk.Label(scrollable_frame, text="المدة", background="#e0f7fa").grid(row=3, column=0, padx=10, pady=10)

        # إضافة المدخلات لكل نشاط
        for i in range(num_activities):
            task_label = ttk.Label(scrollable_frame, text=chr(65 + i), background="#e0f7fa")
            task_label.grid(row=i + 4, column=2, padx=10, pady=10)

            entry_dependencies = ttk.Entry(scrollable_frame, width=10)
            entry_dependencies.grid(row=i + 4, column=1, padx=10, pady=10)

            entry_duration = ttk.Entry(scrollable_frame, width=10)
            entry_duration.grid(row=i + 4, column=0, padx=10, pady=10)

            self.activity_widgets.append([task_label, entry_duration, entry_dependencies])

        # إضافة زر "عرض المخطط"
        ttk.Button(scrollable_frame, text="عرض المخطط", command=self.draw_network).grid(row=num_activities + 6,
                                                                                        column=1, padx=10, pady=10)
        # تحديث الـ Canvas لتناسب الحجم الجديد
        scrollable_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))




    def draw_network(self):
        self.graph.clear()
        cont_node = 1
        my_task = {}
        my_lastmy_task = {}
        list_node = []
        for task_label, entry_duration, entry_dependencies in self.activity_widgets:
            task = task_label.cget("text")
            dependencies = entry_dependencies.get().strip()

            if dependencies:
                deps = dependencies.split(",")
                if deps[0] not in list_node:
                    cont_node += 1
                    for dep in deps:
                        my_task[dep] = cont_node
                        list_node.append(dep)
                elif deps[0] in list_node and len(deps) > 1:
                    for dep in deps:
                        my_task[dep] = my_task[deps[0]]
                        if dep not in list_node:
                            list_node.append(dep)



            else:
                print(task)
                if task not in list_node:
                    list_node.append(task)
                    cont_node += 1
                    my_task[task] = cont_node
                    my_lastmy_task[task] = 1

            if dependencies:
                deps = dependencies.split(",")
                for dep in deps:
                    my_lastmy_task[task] = my_task[dep]

        cont_node += 1
        for task_label, entry_duration, entry_dependencies in self.activity_widgets:
            task = task_label.cget("text")
            duration = entry_duration.get().strip()

            if not duration.isdigit():
                messagebox.showerror("خطأ", f"يرجى إدخال مدة صحيحة للنشاط {task}.")
                return

            try:
                taskk = my_task[task]
            except:
                taskk = cont_node

            if dependencies:
                self.graph.add_edge(my_lastmy_task[task], taskk, weight=int(duration), label=f"{task} : {duration}")
                self.graph.nodes[my_lastmy_task[task]]["label"] = task
                self.graph.nodes[taskk]["label"] = task
            else:
                self.graph.add_edge(my_lastmy_task[task], taskk, weight=int(duration), label=f"{task} : {duration}")
                self.graph.nodes[my_lastmy_task[task]]["label"] = task
                self.graph.nodes[taskk]["label"] = task

        self.show_critical_path()
        self.show_table()

    def show_critical_path(self):
        try:
            # حساب المسار الحرج ومدة المسار الحرج
            critical_path_nodes = nx.dag_longest_path(self.graph, weight="weight")
            critical_duration = nx.dag_longest_path_length(self.graph, weight="weight")

            # استرداد أسماء الأنشطة من الحواف بناءً على خاصية label
            critical_path_tasks = []
            for i in range(len(critical_path_nodes) - 1):
                edge_data = self.graph.get_edge_data(
                    critical_path_nodes[i], critical_path_nodes[i + 1]
                )
                if edge_data and "label" in edge_data:
                    task_name = edge_data["label"].split(":")[0].strip()  # استخراج اسم النشاط
                    self.critical_path_tasks.append(task_name)

            # رسم المخطط مع تلوين المسار الحرج
            fig, ax = plt.subplots(figsize=(10, 8))
            pos = nx.spring_layout(self.graph)
            nx.draw(self.graph, pos, with_labels=True, node_size=2000, node_color="lightblue")
            edge_labels = nx.get_edge_attributes(self.graph, "label")
            nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)

            # تلوين المسار الحرج
            critical_edges = [
                (critical_path_nodes[i], critical_path_nodes[i + 1])
                for i in range(len(critical_path_nodes) - 1)
            ]
            nx.draw_networkx_edges(
                self.graph, pos, edgelist=critical_edges, edge_color="red", width=2.5
            )

            # عرض المسار الحرج ومدته
            critical_path_str = " -> ".join(self.critical_path_tasks)
            ax.set_title(
                f" {critical_path_str} = {critical_duration}",
                fontsize=14,
                color="darkred",
            )

            # عرض الرسم
            for widget in self.frame_canvas.winfo_children():
                widget.destroy()

            canvas = FigureCanvasTkAgg(fig, master=self.frame_canvas)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            # إضافة التفاعلية مع الحفاظ على اللون
            self.add_interactivity(canvas, pos, critical_edges)

        except Exception as e:
            messagebox.showerror("خطأ", str(e))


    def add_interactivity(self, canvas, pos, critical_edges):
        def on_click(event):
            if event.xdata is not None and event.ydata is not None:
                for node, (x, y) in pos.items():
                    if (event.xdata - x) ** 2 + (event.ydata - y) ** 2 < 0.01:  # تحديد النقر على العقدة
                        canvas.moving_node = node
                        break

        def on_release(event):
            canvas.moving_node = None

        def on_motion(event):
            if hasattr(canvas, "moving_node") and canvas.moving_node:
                pos[canvas.moving_node] = (event.xdata, event.ydata)

                # إعادة حساب المسار الحرج
                critical_path_nodes = nx.dag_longest_path(self.graph, weight="weight")
                critical_duration = nx.dag_longest_path_length(self.graph, weight="weight")
                critical_path_tasks = []
                for i in range(len(critical_path_nodes) - 1):
                    edge_data = self.graph.get_edge_data(critical_path_nodes[i], critical_path_nodes[i + 1])
                    if edge_data and "label" in edge_data:
                        task_name = edge_data["label"].split(":")[0].strip()
                        critical_path_tasks.append(task_name)
                critical_path_str = " -> ".join(critical_path_tasks)

                # تحديث الرسم
                canvas.figure.clear()
                ax = canvas.figure.add_subplot(111)
                nx.draw(self.graph,pos,with_labels=True,node_size=2000,node_color="lightblue",ax=ax)
                edge_labels = nx.get_edge_attributes(self.graph, "label")
                nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, ax=ax)
                nx.draw_networkx_edges(self.graph, pos, edgelist=critical_edges, edge_color="red", width=2.5, ax=ax)

                # تحديث العنوان
                ax.set_title(f" {critical_path_str} = {critical_duration}",fontsize=14,color="darkred")

                canvas.draw()

        canvas.mpl_connect("button_press_event", on_click)
        canvas.mpl_connect("button_release_event", on_release)
        canvas.mpl_connect("motion_notify_event", on_motion)


    def show_table(self):
        if self.st==0:
            self.st = 1
            # استخراج الأنشطة وبياناتها من المدخلات

            tasks1 = []


            for task_label, entry_duration, entry_dependencies in self.activity_widgets:
                task = task_label.cget("text")
                duration = int(entry_duration.get())
                dependencies = entry_dependencies.get().strip().split(",") if entry_dependencies.get().strip() else []
                tasks1.append(dependencies)

                self.activities[task] = {"duration": duration,"dependencies": dependencies,"es": 0,"ef": 0,"ls": 0,"lf": 0, "successors": [] }


            # حساب المسار الأمامي (Forward Pass)
            maxnum = 0
            for task in self.activities:

                dependencies = self.activities[task]["dependencies"]
                if dependencies:  # إذا كانت هناك أنشطة سابقة
                    self.activities[task]["es"] = max(self.activities[dep]["ef"] for dep in dependencies)

                self.activities[task]["ef"] = self.activities[task]["es"] + self.activities[task]["duration"]
                if self.activities[task]["ef"] > maxnum:
                    maxnum = self.activities[task]["ef"]
                # إضافة الأنشطة التابعة (successors) لكل نشاط
                for task in self.activities:
                    for dep in self.activities[task]["dependencies"]:
                        self.activities[dep]["successors"].append(task)
                        if self.activities[task]["ef"] > maxnum:
                            maxnum = self.activities[task]["ef"]

            self.laststart=maxnum
            for i in reversed(range(0,len(self.critical_path_tasks))):
                task12=self.critical_path_tasks[i]
                self.activities[task12]["lf"] = self.laststart
                self.activities[task12]["ls"] = self.activities[task12]["lf"] - self.activities[task12]["duration"]
                self.laststart=self.activities[task12]["ls"]


           # حساب المسار الخلفي (Backward Pass)
            all_tasks = list(self.activities.keys())

            # تحديد LF و LS للأنشطة النهائية
            for task in reversed(all_tasks):

                if self.activities[task]["lf"] == 0 :

                    if  self.activities[task]["successors"]:  # إذا كان النشاط  له أنشطة تابعة
                        self.activities[task]["lf"] =max(self.activities[dep]["ls"] for dep in self.activities[task]["successors"])
                        self.activities[task]["ls"] = self.activities[task]["lf"] - self.activities[task]["duration"]

                    else:
                        self.activities[task]["lf"]=maxnum
                        self.activities[task]["ls"] = self.activities[task]["lf"] - self.activities[task]["duration"]

        # عرض الجدول
        table_window = tk.Toplevel(self.root)
        table_window.title("Timing Table")
        table_window.configure(bg="lightcyan")
        table_window.geometry("400x500")

        cols = ["الفائض","النهاية المتأخرة (LF)","البداية المتأخرة (LS)","النهاية المبكرة (EF)", "البداية المبكرة (ES)", "النشاط" ]
        tree = ttk.Treeview(table_window, columns=cols, show="headings")
        tree.tag_configure("oddrow", background="lightcyan")
        tree.tag_configure("evenrow", background="white")

        for col in cols:
            tree.heading(col, text=col)
        tree.pack(fill=tk.BOTH, expand=True)

        for index, (task, data) in enumerate(self.activities.items()):
            row_color = "oddrow" if index % 2 == 0 else "evenrow"

            tree.insert("", "end",values=( (data["lf"] - data["ef"]),data["lf"],data["ls"],data["ef"],data["es"],task),tags=(row_color,))
    def save_frame_as_image(self):
        """حفظ الرسم الشبكي مع تلوين المسار الحرج كصورة بجودة عالية."""
        try:
            # اختيار مكان حفظ الصورة
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG Files", "*.png"), ("SVG Files", "*.svg")])
            if not file_path:
                return

            # إعادة رسم المخطط بنفس التنسيق والتلوين
            fig, ax = plt.subplots(figsize=(10, 8))
            pos = nx.spring_layout(self.graph)

            # رسم العقد والحواف العادية
            nx.draw(self.graph, pos, with_labels=True, node_size=2000, node_color="lightblue", ax=ax)
            edge_labels = nx.get_edge_attributes(self.graph, "label")
            nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, ax=ax)

            # تحديد المسار الحرج
            critical_path_nodes = nx.dag_longest_path(self.graph, weight="weight")
            critical_edges = [(critical_path_nodes[i], critical_path_nodes[i + 1]) for i in
                              range(len(critical_path_nodes) - 1)]

            # تلوين المسار الحرج باللون الأحمر
            nx.draw_networkx_edges(self.graph, pos, edgelist=critical_edges, edge_color="red", width=2.5, ax=ax)

            # حفظ الصورة
            fig.savefig(file_path, dpi=300)
            messagebox.showinfo("نجاح", "تم حفظ الرسم مع المسار الحرج كصورة بنجاح!")
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء الحفظ: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkDiagramApp(root)
    root.mainloop()
