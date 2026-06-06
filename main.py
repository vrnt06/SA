# app_ui.py
import tkinter as tk
from tkinter import ttk, messagebox

# Import our decoupled logic module cleanly
import algorithms


class MobileSchedulerApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Mobile OS Scheduling Engine")
        self.root.geometry("600x700")
        self.root.configure(bg="#1c1c1e")

        # In-memory database pipeline state
        self.process_pipeline = [
            {"pid": "Camera Framework", "at": 0, "bt": 5},
            {"pid": "Network Thread", "at": 2, "bt": 3},
            {"pid": "UI Sync Engine", "at": 4, "bt": 1},
        ]

        self.setup_styles()
        self.create_widgets()
        self.refresh_simulation()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure(
            "Treeview",
            background="#2c2c2e",
            foreground="white",
            fieldbackground="#2c2c2e",
            rowheight=30,
        )
        self.style.configure(
            "Treeview.Heading",
            background="#3a3a3c",
            foreground="white",
            relief="flat",
        )

    def create_widgets(self):
        # Header title
        title = tk.Label(
            self.root,
            text="Mobile OS Core Engine Scheduler",
            fg="#00adb5",
            bg="#1c1c1e",
            font=("Arial", 16, "bold"),
        )
        title.pack(pady=15)

        # -----------------------------
        # Input Form Container Box
        # -----------------------------
        form_frame = tk.Frame(self.root, bg="#2c2c2e", bd=0)
        form_frame.pack(fill="x", padx=15, pady=5)

        tk.Label(
            form_frame, text="App Name", fg="white", bg="#2c2c2e", font=("Arial", 10)
        ).grid(row=0, column=0, padx=8, pady=4, sticky="w")
        tk.Label(
            form_frame, text="Arrival", fg="white", bg="#2c2c2e", font=("Arial", 10)
        ).grid(row=0, column=1, padx=8, pady=4, sticky="w")
        tk.Label(
            form_frame, text="Burst Time", fg="white", bg="#2c2c2e", font=("Arial", 10)
        ).grid(row=0, column=2, padx=8, pady=4, sticky="w")

        self.entry_pid = tk.Entry(
            form_frame, bg="#3a3a3c", fg="white", bd=0, insertbackground="white"
        )
        self.entry_at = tk.Entry(
            form_frame, bg="#3a3a3c", fg="white", bd=0, insertbackground="white"
        )
        self.entry_bt = tk.Entry(
            form_frame, bg="#3a3a3c", fg="white", bd=0, insertbackground="white"
        )

        self.entry_pid.grid(row=1, column=0, padx=8, pady=8, sticky="ew")
        self.entry_at.grid(row=1, column=1, padx=8, pady=8, sticky="ew")
        self.entry_bt.grid(row=1, column=2, padx=8, pady=8, sticky="ew")

        btn_add = tk.Button(
            form_frame,
            text="Deploy Thread",
            command=self.add_process,
            bg="#4caf50",
            fg="white",
            relief="flat",
            font=("Arial", 9, "bold"),
        )
        btn_add.grid(row=1, column=3, padx=10, pady=8)

        # -----------------------------
        # Logic Engine Configuration Framework Selector
        # -----------------------------
        config_frame = tk.Frame(self.root, bg="#1c1c1e")
        config_frame.pack(fill="x", padx=15, pady=10)

        tk.Label(
            config_frame,
            text="Strategy Core Framework Target:",
            fg="white",
            bg="#1c1c1e",
        ).pack(side="left")
        self.algo_var = tk.StringVar(value="FCFS")
        self.algo_menu = ttk.Combobox(
            config_frame, textvariable=self.algo_var, values=["FCFS", "SJF"], width=10
        )
        self.algo_menu.pack(side="left", padx=10)
        self.algo_menu.bind("<<ComboboxSelected>>", self.refresh_simulation)

        # -----------------------------
        # Live Horizontal Gantt Container Box Panel View Map
        # -----------------------------
        tk.Label(
            self.root,
            text="Live Core Thread Gantt Execution Tracker View",
            fg="#00adb5",
            bg="#1c1c1e",
            font=("Arial", 11, "bold"),
        ).pack(anchor="w", padx=15, pady=(15, 5))

        self.gantt_canvas = tk.Canvas(
            self.root, height=75, bg="#2c2c2e", highlightthickness=0
        )
        self.gantt_canvas.pack(fill="x", padx=15)

        # -----------------------------
        # Core Output Analytics Metric Dashboard Panels Rows
        # -----------------------------
        self.metrics_frame = tk.Frame(self.root, bg="#1c1c1e")
        self.metrics_frame.pack(fill="x", padx=15, pady=15)

        self.lbl_fcfs_metric = tk.Label(
            self.metrics_frame,
            text="FCFS Latency: 0.0s",
            fg="#ff6b6b",
            bg="#2c2c2e",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=10,
        )
        self.lbl_fcfs_metric.pack(side="left", expand=True, fill="x", padx=(0, 5))

        self.lbl_sjf_metric = tk.Label(
            self.metrics_frame,
            text="SJF Latency: 0.0s",
            fg="#4ecdc4",
            bg="#2c2c2e",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=10,
        )
        self.lbl_sjf_metric.pack(side="right", expand=True, fill="x", padx=(5, 0))

        # -----------------------------
        # Production Table Database Logging Grid Data
        # -----------------------------
        self.tree = ttk.Treeview(
            self.root,
            columns=("PID", "AT", "BT", "CT", "TAT", "WT"),
            show="headings",
            height=6,
        )
        for col in ("PID", "AT", "BT", "CT", "TAT", "WT"):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=80)
        self.tree.pack(fill="both", expand=True, padx=15, pady=10)

    def add_process(self):
        pid = self.entry_pid.get().strip()
        try:
            at = int(self.entry_at.get().strip())
            bt = int(self.entry_bt.get().strip())
            if at < 0 or bt <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Metric Configuration Error",
                "Please verify target thread constraints parameters.",
            )
            return

        self.process_pipeline.append({"pid": pid, "at": at, "bt": bt})
        self.entry_pid.delete(0, tk.END)
        self.entry_at.delete(0, tk.END)
        self.entry_bt.delete(0, tk.END)
        self.refresh_simulation()

    def refresh_simulation(self, event=None):
        if not self.process_pipeline:
            return

        # 1. Run engine models calculations decoupled from tracking views layers
        fcfs_res, _ = algorithms.first_come_first_served(
            [dict(p) for p in self.process_pipeline]
        )
        sjf_res, sjf_gantt = algorithms.shortest_job_first(
            [dict(p) for p in self.process_pipeline]
        )
        _, fcfs_gantt = algorithms.first_come_first_served(
            [dict(p) for p in self.process_pipeline]
        )

        avg_wt_fcfs = sum(r["wt"] for r in fcfs_res) / len(fcfs_res)
        avg_wt_sjf = sum(r["wt"] for r in sjf_res) / len(sjf_res)

        self.lbl_fcfs_metric.config(text=f"FCFS Avg Latency:\n{avg_wt_fcfs:.2f}s")
        self.lbl_sjf_metric.config(text=f"SJF Avg Latency:\n{avg_wt_sjf:.2f}s")

        active_results, active_gantt = (
            (fcfs_res, fcfs_gantt)
            if self.algo_var.get() == "FCFS"
            else (sjf_res, sjf_gantt)
        )

        # 2. Render Canvas Object View Data Representations Maps
        self.gantt_canvas.delete("all")
        if active_gantt:
            max_time = active_gantt[-1]["end"]
            canvas_width = 570
            scale = (
                (canvas_width - 60) / max_time if max_time > 0 else (canvas_width - 60)
            )

            for i, seg in enumerate(active_gantt):
                x_start = 30 + (seg["start"] * scale)
                x_end = 30 + (seg["end"] * scale)

                self.gantt_canvas.create_rectangle(
                    x_start,
                    15,
                    x_end,
                    50,
                    fill="#3a3a3c",
                    outline="#00adb5",
                    width=1.5,
                )
                self.gantt_canvas.create_text(
                    (x_start + x_end) / 2,
                    26,
                    text=seg["pid"],
                    fill="white",
                    font=("Arial", 8, "bold"),
                )
                self.gantt_canvas.create_text(
                    (x_start + x_end) / 2,
                    42,
                    text=f"{seg['start']}-{seg['end']}s",
                    fill="#00adb5",
                    font=("Arial", 7),
                )

        # 3. Refresh display view listings
        for row in self.tree.get_children():
            self.tree.delete(row)
        for r in active_results:
            self.tree.insert(
                "",
                "end",
                values=(r["pid"], r["at"], r["bt"], r["ct"], r["tat"], r["wt"]),
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = MobileSchedulerApp(root)
    root.mainloop()