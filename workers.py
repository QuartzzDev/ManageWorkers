import tkinter as tk
from tkinter import ttk

class Worker:
    def __init__(self, name, position, salary, note=""):
        self.name = name
        self.position = position
        self.salary = salary
        self.note = note

class WorkerManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("İşçi Yönetimi")
        
        self.workers = []
        
        self.create_widgets()
        self.load_workers()

    def create_widgets(self):
        self.frame = ttk.Frame(self.root, padding=10)
        self.frame.grid()

        self.label_name = ttk.Label(self.frame, text="İşçi Adı:")
        self.label_name.grid(row=0, column=0, sticky=tk.W)

        self.entry_name = ttk.Entry(self.frame)
        self.entry_name.grid(row=0, column=1)

        self.label_position = ttk.Label(self.frame, text="Pozisyon:")
        self.label_position.grid(row=1, column=0, sticky=tk.W)

        self.entry_position = ttk.Entry(self.frame)
        self.entry_position.grid(row=1, column=1)

        self.label_salary = ttk.Label(self.frame, text="Maaş:")
        self.label_salary.grid(row=2, column=0, sticky=tk.W)

        self.entry_salary = ttk.Entry(self.frame)
        self.entry_salary.grid(row=2, column=1)

        self.label_note = ttk.Label(self.frame, text="Not:")
        self.label_note.grid(row=3, column=0, sticky=tk.W)

        self.entry_note = ttk.Entry(self.frame)
        self.entry_note.grid(row=3, column=1)

        self.button_add = ttk.Button(self.frame, text="İşçi Ekle", command=self.add_worker)
        self.button_add.grid(row=4, column=0, columnspan=2, pady=10)

        self.treeview = ttk.Treeview(self.frame, columns=("Name", "Position", "Salary", "Note"), show="headings")
        self.treeview.grid(row=5, column=0, columnspan=2)

        self.treeview.heading("Name", text="İşçi Adı")
        self.treeview.heading("Position", text="Pozisyon")
        self.treeview.heading("Salary", text="Maaş")
        self.treeview.heading("Note", text="Not")

        self.button_update_salary = ttk.Button(self.frame, text="Maaş Güncelle", command=self.update_salary)
        self.button_update_salary.grid(row=6, column=0, columnspan=2, pady=10)

        self.treeview.bind("<ButtonRelease-1>", self.show_worker_note)

        self.combobox_positions = ttk.Combobox(self.frame, state="readonly")
        self.combobox_positions.grid(row=7, column=0, padx=5, pady=10)

        self.button_show_workers = ttk.Button(self.frame, text="Aynı Meslekteki İşçileri Göster", command=self.show_workers_by_position)
        self.button_show_workers.grid(row=7, column=1, padx=5, pady=10)

        self.button_delete_worker = ttk.Button(self.frame, text="İşçiyi Sil", command=self.delete_worker)
        self.button_delete_worker.grid(row=8, column=0, columnspan=2, pady=10)

        self.button_save = ttk.Button(self.frame, text="Kaydet", command=self.save_workers)
        self.button_save.grid(row=9, column=0, columnspan=2, pady=10)

        self.label_producers = ttk.Label(self.frame, text="Yapımcılar:")
        self.label_producers.grid(row=10, column=0, sticky=tk.W)

        self.label_producer_name = ttk.Label(self.frame, text="QuartzzDev")
        self.label_producer_name.grid(row=10, column=1, sticky=tk.W)

        self.button_show_all = ttk.Button(self.frame, text="Tüm İşçileri Göster", command=self.show_all_workers)
        self.button_show_all.grid(row=8, column=0, columnspan=2, pady=10)
  

    def add_worker(self):
        name = self.entry_name.get()
        position = self.entry_position.get()
        salary = self.entry_salary.get()
        note = self.entry_note.get()

        if name and position and salary:
            worker = Worker(name, position, salary, note)
            self.workers.append(worker)
            self.treeview.insert("", tk.END, values=(worker.name, worker.position, worker.salary, worker.note))
            self.clear_entries()

    def update_salary(self):
        selection = self.treeview.selection()
        if selection:
            worker = self.get_selected_worker(selection)
            new_salary = self.entry_salary.get()
            if new_salary:
                worker.salary = new_salary
                self.treeview.set(selection, "Salary", new_salary)
                self.clear_entries()

    def show_worker_note(self, event):
        selection = self.treeview.selection()
        if selection:
            worker = self.get_selected_worker(selection)
            self.entry_note.delete(0, tk.END)
            self.entry_note.insert(0, worker.note)
          
    def show_all_workers(self):
        self.clear_treeview()
        for worker in self.workers:
            self.treeview.insert("", tk.END, values=(worker.name, worker.position, worker.salary, worker.note))
    
    def show_workers_by_position(self):
        position = self.combobox_positions.get()
        if position:
            self.clear_treeview()
            for worker in self.workers:
                if worker.position.lower() == position.lower():
                    self.treeview.insert("", tk.END, values=(worker.name, worker.position, worker.salary, worker.note))

    def delete_worker(self):
        selection = self.treeview.selection()
        if selection:
            worker = self.get_selected_worker(selection)
            self.workers.remove(worker)
            self.treeview.delete(selection)
            self.clear_entries()

    def save_workers(self):
        with open("workers.txt", "w") as file:
            for worker in self.workers:
                file.write(f"{worker.name},{worker.position},{worker.salary},{worker.note}\n")

    def load_workers(self):
        try:
            with open("workers.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    worker_info = line.strip().split(",")
                    name, position, salary, note = worker_info
                    worker = Worker(name, position, salary, note)
                    self.workers.append(worker)
                    if position not in self.combobox_positions["values"]:
                        self.combobox_positions["values"] = (*self.combobox_positions["values"], position)
        except FileNotFoundError:
            return
    


    def get_selected_worker(self, selection):
        values = self.treeview.item(selection, "values")
        name = values[0]
        for worker in self.workers:
            if worker.name == name:
                return worker

    def clear_entries(self):
        self.entry_name.delete(0, tk.END)
        self.entry_position.delete(0, tk.END)
        self.entry_salary.delete(0, tk.END)
        self.entry_note.delete(0, tk.END)

    def clear_treeview(self):
        for item in self.treeview.get_children():
            self.treeview.delete(item)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = WorkerManagementApp(root)
    app.run()
