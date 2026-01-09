import tkinter as tk
from tkinter import ttk, messagebox
from collections import defaultdict


class TestCaseAllocator:
    def __init__(self, root):
        self.root = root
        self.root.title("测试用例分配系统")
        self.root.geometry("850x650")

        self.servers = []
        self.test_cases = []
        self.versions = []

        self.create_widgets()
        self.load_default_data()

    def create_widgets(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.server_frame = ttk.Frame(notebook)
        notebook.add(self.server_frame, text="服务器信息")
        self.create_server_tab()

        self.test_case_frame = ttk.Frame(notebook)
        notebook.add(self.test_case_frame, text="测试用例集")
        self.create_test_case_tab()

        self.version_frame = ttk.Frame(notebook)
        notebook.add(self.version_frame, text="版本信息")
        self.create_version_tab()

        self.result_frame = ttk.Frame(notebook)
        notebook.add(self.result_frame, text="分配结果")
        self.create_result_tab()

        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(button_frame, text="分配测试用例", command=self.allocate_test_cases).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="清除所有数据", command=self.clear_all_data).pack(side=tk.LEFT, padx=5)

    # ===================== 服务器 =====================
    def create_server_tab(self):
        ttk.Label(self.server_frame, text="服务器名称:").grid(row=0, column=0, sticky=tk.W)
        self.server_name = ttk.Entry(self.server_frame)
        self.server_name.grid(row=0, column=1, sticky=tk.EW)

        ttk.Label(self.server_frame, text="服务器属性(逗号分隔):").grid(row=1, column=0, sticky=tk.W)
        self.server_attrs = ttk.Entry(self.server_frame)
        self.server_attrs.grid(row=1, column=1, sticky=tk.EW)

        ttk.Button(self.server_frame, text="添加服务器", command=self.add_server).grid(row=2, column=0, columnspan=2)

        self.server_tree = ttk.Treeview(self.server_frame, columns=('name', 'attributes'), show='headings')
        self.server_tree.heading('name', text='服务器名称')
        self.server_tree.heading('attributes', text='属性')
        self.server_tree.grid(row=3, column=0, columnspan=2, sticky=tk.NSEW)

        scrollbar = ttk.Scrollbar(self.server_frame, orient=tk.VERTICAL, command=self.server_tree.yview)
        scrollbar.grid(row=3, column=2, sticky=tk.NS)
        self.server_tree.configure(yscroll=scrollbar.set)

        ttk.Button(self.server_frame, text="删除选中服务器", command=self.delete_server).grid(row=4, column=0, columnspan=2)

        self.server_frame.columnconfigure(1, weight=1)
        self.server_frame.rowconfigure(3, weight=1)

    def add_server(self):
        name = self.server_name.get().strip()
        attrs = [a.strip() for a in self.server_attrs.get().split(',') if a.strip()]
        if not name:
            return
        self.servers.append({'name': name, 'attributes': attrs})
        self.update_server_tree()
        self.server_name.delete(0, tk.END)
        self.server_attrs.delete(0, tk.END)

    def delete_server(self):
        for item in self.server_tree.selection():
            name = self.server_tree.item(item, 'values')[0]
            self.servers = [s for s in self.servers if s['name'] != name]
        self.update_server_tree()

    def update_server_tree(self):
        self.server_tree.delete(*self.server_tree.get_children())
        for s in self.servers:
            self.server_tree.insert('', tk.END, values=(s['name'], ', '.join(s['attributes'])))

    # ===================== 测试用例 =====================
    def create_test_case_tab(self):
        ttk.Label(self.test_case_frame, text="测试用例名称:").grid(row=0, column=0, sticky=tk.W)
        self.case_name = ttk.Entry(self.test_case_frame)
        self.case_name.grid(row=0, column=1, sticky=tk.EW)

        ttk.Label(self.test_case_frame, text="测试用例属性:").grid(row=1, column=0, sticky=tk.W)
        self.case_attr = ttk.Entry(self.test_case_frame)
        self.case_attr.grid(row=1, column=1, sticky=tk.EW)

        ttk.Label(self.test_case_frame, text="执行时间(h):").grid(row=2, column=0, sticky=tk.W)
        self.case_time = ttk.Entry(self.test_case_frame)
        self.case_time.grid(row=2, column=1, sticky=tk.EW)

        ttk.Button(self.test_case_frame, text="添加测试用例", command=self.add_test_case).grid(row=3, column=0, columnspan=2)

        self.case_tree = ttk.Treeview(self.test_case_frame, columns=('name', 'attributes', 'time'), show='headings')
        self.case_tree.heading('name', text='测试用例名称')
        self.case_tree.heading('attributes', text='属性')
        self.case_tree.heading('time', text='执行时间(h)')
        self.case_tree.grid(row=4, column=0, columnspan=2, sticky=tk.NSEW)

        scrollbar = ttk.Scrollbar(self.test_case_frame, orient=tk.VERTICAL, command=self.case_tree.yview)
        scrollbar.grid(row=4, column=2, sticky=tk.NS)
        self.case_tree.configure(yscroll=scrollbar.set)

        ttk.Button(self.test_case_frame, text="删除选中测试用例", command=self.delete_test_case).grid(row=5, column=0, columnspan=2)

        self.test_case_frame.columnconfigure(1, weight=1)
        self.test_case_frame.rowconfigure(4, weight=1)

    def add_test_case(self):
        self.test_cases.append({
            'name': self.case_name.get(),
            'attributes': [self.case_attr.get()],
            'time': float(self.case_time.get())
        })
        self.update_case_tree()
        self.update_case_list()
        self.case_name.delete(0, tk.END)
        self.case_attr.delete(0, tk.END)
        self.case_time.delete(0, tk.END)

    def delete_test_case(self):
        for item in self.case_tree.selection():
            name = self.case_tree.item(item, 'values')[0]
            self.test_cases = [c for c in self.test_cases if c['name'] != name]
        self.update_case_tree()
        self.update_case_list()

    def update_case_tree(self):
        self.case_tree.delete(*self.case_tree.get_children())
        for c in self.test_cases:
            self.case_tree.insert('', tk.END, values=(c['name'], ', '.join(c['attributes']), c['time']))

    # ===================== 版本（UI 优化） =====================
    def create_version_tab(self):
        ttk.Label(self.version_frame, text="版本名称:").grid(row=0, column=0, sticky=tk.W)
        self.version_name = ttk.Entry(self.version_frame)
        self.version_name.grid(row=0, column=1, sticky=tk.EW)

        ttk.Label(self.version_frame, text="包含的测试用例:").grid(row=1, column=0, sticky=tk.W)

        case_frame = ttk.Frame(self.version_frame)
        case_frame.grid(row=1, column=1, sticky=tk.NSEW)

        self.version_cases = tk.Listbox(case_frame, selectmode=tk.MULTIPLE, height=6)
        self.version_cases.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        case_scroll = ttk.Scrollbar(case_frame, orient=tk.VERTICAL, command=self.version_cases.yview)
        case_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.version_cases.configure(yscrollcommand=case_scroll.set)

        ttk.Button(self.version_frame, text="添加版本", command=self.add_version).grid(row=2, column=0, columnspan=2)

        self.version_tree = ttk.Treeview(self.version_frame, columns=('name', 'cases'), show='headings')
        self.version_tree.heading('name', text='版本名称')
        self.version_tree.heading('cases', text='包含的测试用例')
        self.version_tree.grid(row=3, column=0, columnspan=2, sticky=tk.NSEW)

        tree_scroll = ttk.Scrollbar(self.version_frame, orient=tk.VERTICAL, command=self.version_tree.yview)
        tree_scroll.grid(row=3, column=2, sticky=tk.NS)
        self.version_tree.configure(yscroll=tree_scroll.set)

        ttk.Button(self.version_frame, text="删除选中版本", command=self.delete_version).grid(row=4, column=0, columnspan=2)

        self.version_frame.columnconfigure(1, weight=1)
        self.version_frame.rowconfigure(3, weight=1)

        self.update_case_list()

    def add_version(self):
        self.versions.append({
            'name': self.version_name.get(),
            'cases': [self.version_cases.get(i) for i in self.version_cases.curselection()]
        })
        self.update_version_tree()
        self.version_name.delete(0, tk.END)

    def delete_version(self):
        for item in self.version_tree.selection():
            name = self.version_tree.item(item, 'values')[0]
            self.versions = [v for v in self.versions if v['name'] != name]
        self.update_version_tree()

    def update_version_tree(self):
        self.version_tree.delete(*self.version_tree.get_children())
        for v in self.versions:
            self.version_tree.insert('', tk.END, values=(v['name'], ', '.join(v['cases'])))

    # ===================== 分配算法 / 展示 / 默认数据（完全不动） =====================
    # ↓↓↓ 以下代码与你提供版本完全一致 ↓↓↓

    def allocate_test_cases(self):
        all_test_cases = self.generate_all_test_cases()
        allocation = self.allocate_by_duration_desc(all_test_cases)
        self.display_allocation_result(allocation)

    def generate_all_test_cases(self):
        all_cases = []
        for version in self.versions:
            for case_name in version['cases']:
                original_case = next((c for c in self.test_cases if c['name'] == case_name), None)
                if not original_case:
                    continue
                all_cases.append({
                    'name': f"{case_name}_{version['name']}",
                    'version': version['name'],
                    'attributes': original_case['attributes'],
                    'time': original_case['time'],
                })
        return all_cases

    def allocate_by_duration_desc(self, all_test_cases):
        servers = [{
            'name': s['name'],
            'attributes': set(s['attributes']),
            'allocated_cases': [],
            'total_time': 0.0
        } for s in self.servers]

        for case in sorted(all_test_cases, key=lambda c: c['time'], reverse=True):
            eligible = [s for s in servers if any(a in s['attributes'] for a in case['attributes'])]
            if not eligible:
                continue
            eligible.sort(key=lambda s: (s['total_time'], len(s['attributes'])))
            eligible[0]['allocated_cases'].append(case)
            eligible[0]['total_time'] += case['time']

        return servers

    def create_result_tab(self):
        self.result_text = tk.Text(self.result_frame, wrap=tk.WORD)
        self.result_text.pack(fill=tk.BOTH, expand=True)
        self.version_colors = ['blue', 'green', 'purple', 'orange', 'brown', 'darkcyan']

    def display_allocation_result(self, allocation):
        self.result_text.delete(1.0, tk.END)

        version_names = [v['name'] for v in self.versions]
        color_map = {v: self.version_colors[i % len(self.version_colors)] for i, v in enumerate(version_names)}

        for v, color in color_map.items():
            self.result_text.tag_config(v, foreground=color)

        total = 0.0
        for server in sorted(allocation, key=lambda s: s['name']):
            if not server['allocated_cases']:
                continue

            self.result_text.insert(tk.END, f"服务器 {server['name']} 上执行用例: ")

            cases = sorted(server['allocated_cases'], key=lambda c: (version_names.index(c['version']), c['name']))
            for i, c in enumerate(cases):
                self.result_text.insert(tk.END, c['name'], c['version'])
                if i != len(cases) - 1:
                    self.result_text.insert(tk.END, ", ")

            self.result_text.insert(tk.END, f"\n总占用时间: {server['total_time']:.1f}h\n\n")
            total += server['total_time']

        self.result_text.insert(tk.END, "----------------------------------------\n")
        self.result_text.insert(tk.END, f"所有服务器总占用时间: {total:.1f}h\n")

    def clear_all_data(self):
        self.servers.clear()
        self.test_cases.clear()
        self.versions.clear()
        self.update_server_tree()
        self.update_case_tree()
        self.update_version_tree()
        self.update_case_list()
        self.result_text.delete(1.0, tk.END)

    def update_case_list(self):
        self.version_cases.delete(0, tk.END)
        for c in self.test_cases:
            self.version_cases.insert(tk.END, c['name'])

    def load_default_data(self):
        self.servers = [
            {'name': 'ylf191_192', 'attributes': ['1v1']},
            {'name': 'ylf251_252', 'attributes': ['cc_gdr', 'muxi_gdr', '1v1', 'cc', 'nccl']},
            {'name': 'ylf193_194', 'attributes': ['h800', '1v1']},
            {'name': 'ylf253_254', 'attributes': ['1v1']},
            {'name': 'ylf215_219', 'attributes': ['1v1']}
        ]
        self.update_server_tree()

        self.test_cases = [
            {'name': 'basic', 'attributes': ['1v1'], 'time': 27},
            {'name': 'bcc', 'attributes': ['cc'], 'time': 1.0},
            {'name': 'cc_gdr', 'attributes': ['cc_gdr'], 'time': 0.3},
            {'name': 'cnp', 'attributes': ['cc'], 'time': 0.5},
            {'name': 'dcqcn', 'attributes': ['cc'], 'time': 3.5},
            {'name': 'gdr_h800', 'attributes': ['h800'], 'time': 1.0},
            {'name': 'hqos', 'attributes': ['1v1'], 'time': 0.3},
            {'name': 'max_cfg', 'attributes': ['1v1'], 'time': 0.2},
            {'name': 'mix_test', 'attributes': ['1v1'], 'time': 0.8},
            {'name': 'nccl', 'attributes': ['nccl'], 'time': 5.2},
            {'name': 'pfc', 'attributes': ['1v1'], 'time': 0.4},
            {'name': 'switch_drop_packet', 'attributes': ['1v1'], 'time': 0.5},
            {'name': 'yuncli_cmd', 'attributes': ['1v1'], 'time': 0.2},
        ]
        self.update_case_tree()
        self.update_case_list()

        self.versions = [
            {'name': 'rc5_veroce', 'cases': ['basic', 'bcc', 'cc_gdr', 'cnp', 'dcqcn', 'gdr_h800',
                                     'hqos', 'max_cfg', 'mix_test', 'nccl', 'pfc',
                                     'switch_drop_packet', 'yuncli_cmd']},
            {'name': 'rc5_rocev2', 'cases': ['basic', 'bcc', 'cc_gdr', 'cnp', 'dcqcn', 'gdr_h800',
                                     'hqos', 'max_cfg', 'mix_test', 'nccl', 'pfc',
                                     'switch_drop_packet']},
            {'name': '930RC11', 'cases': ['basic', 'yuncli_cmd']}
        ]
        self.update_version_tree()


def main():
    root = tk.Tk()
    TestCaseAllocator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
