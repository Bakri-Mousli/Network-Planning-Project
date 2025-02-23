import networkx as nx

def build_network_graph(activity_widgets):
    """
    تأخذ قائمة الأنشطة وتبني الرسم الشبكي (graph) مع حساب العلاقات بين الأنشطة.
    تُرجع الرسم الشبكي (DiGraph).
    """
    graph = nx.DiGraph()
    my_task = {}
    my_lastmy_task = {}
    list_node = []
    cont_node = 1

    # بناء العقد والحواف بناءً على المدخلات
    for task_label, entry_duration, entry_dependencies in activity_widgets:
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
    # إضافة الحواف باستخدام مدة الأنشطة
    for task_label, entry_duration, entry_dependencies in activity_widgets:
        task = task_label.cget("text")
        duration = entry_duration.get().strip()
        try:
            taskk = my_task[task]
        except KeyError:
            taskk = cont_node
        # إضافة الحافة إلى الرسم الشبكي
        graph.add_edge(my_lastmy_task.get(task, 1), taskk, weight=int(duration), label=f"{task} : {duration}")
        # تحديد تسميات العقد
        graph.nodes[my_lastmy_task.get(task, 1)]["label"] = task
        graph.nodes[taskk]["label"] = task

    return graph

def compute_critical_path(graph):
    """
    حساب المسار الحرج ومدة المسار الحرج من الرسم الشبكي.
    تُرجع (critical_path_nodes, critical_duration).
    """
    critical_path_nodes = nx.dag_longest_path(graph, weight="weight")
    critical_duration = nx.dag_longest_path_length(graph, weight="weight")
    return critical_path_nodes, critical_duration
