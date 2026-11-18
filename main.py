
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, timedelta

from styles import (
    setup_style, create_button, create_card,
    BG, WHITE, PRIMARY, DARK, TEXT, MUTED,
    GREEN, RED, ORANGE, PURPLE
)

from database import (
    load_data, save_data, add_member,
    delete_member, update_member
)


class GymApp:

    def __init__(self, root):
        self.root = root
        self.root.title("GYM MANAGEMENT SYSTEM")
        self.root.geometry("1250x780")
        self.root.minsize(1050, 650)

        setup_style(root)

        self.data = load_data()
        self.current_filter = ""

        self.create_sidebar()
        self.create_main()
        self.refresh_all()

    # ================= SIDEBAR =================

    def create_sidebar(self):
        self.sidebar = tk.Frame(
            self.root, bg=DARK, width=220
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="GYM CENTER",
            bg=DARK,
            fg=WHITE,
            font=("Arial", 20, "bold")
        ).pack(pady=(35, 5))

        tk.Label(
            self.sidebar,
            text="MANAGEMENT SYSTEM",
            bg=DARK,
            fg="#93C5FD",
            font=("Arial", 9)
        ).pack(pady=(0, 35))

        menu_items = [
            ("▣  Tổng quan", self.dashboard),
            ("♟  Hội viên", self.member_section),
            ("◆  Gói tập", self.package_section),
            ("▤  Thống kê", self.statistics)
        ]

        for text, command in menu_items:
            tk.Button(
                self.sidebar,
                text=text,
                command=command,
                bg=DARK,
                fg=WHITE,
                activebackground=PRIMARY,
                activeforeground=WHITE,
                font=("Arial", 11, "bold"),
                relief="flat",
                anchor="w",
                padx=22,
                pady=15,
                cursor="hand2"
            ).pack(fill="x", padx=8, pady=4)

        tk.Label(
            self.sidebar,
            text="PHIÊN BẢN 1.0",
            bg=DARK,
            fg="#94A3B8",
            font=("Arial", 9)
        ).pack(side="bottom", pady=20)

    # ================= MAIN AREA =================

    def create_main(self):
        self.main = tk.Frame(self.root, bg=BG)
        self.main.pack(side="left", fill="both", expand=True)

        self.header = tk.Frame(self.main, bg=WHITE, height=75)
        self.header.pack(fill="x")
        self.header.pack_propagate(False)

        tk.Label(
            self.header,
            text="Hệ thống quản lý phòng Gym",
            bg=WHITE,
            fg=DARK,
            font=("Arial", 17, "bold")
        ).pack(side="left", padx=25)

        tk.Label(
            self.header,
            text="QUẢN LÝ HỘI VIÊN",
            bg=WHITE,
            fg=PRIMARY,
            font=("Arial", 10, "bold")
        ).pack(side="right", padx=25)

        self.content = tk.Frame(self.main, bg=BG)
        self.content.pack(fill="both", expand=True, padx=22, pady=20)

        self.create_dashboard()
        self.create_form()
        self.create_table()

    # ================= DASHBOARD =================

    def create_dashboard(self):
        tk.Label(
            self.content,
            text="TỔNG QUAN",
            bg=BG,
            fg=DARK,
            font=("Arial", 16, "bold")
        ).pack(anchor="w", pady=(0, 15))

        cards = tk.Frame(self.content, bg=BG)
        cards.pack(fill="x", pady=(0, 18))

        self.total_card, self.total_value = create_card(
            cards, "TỔNG HỘI VIÊN", "0", PRIMARY
        )

        self.registered_card, self.registered_value = create_card(
            cards, "ĐÃ ĐĂNG KÝ GÓI", "0", GREEN
        )

        self.revenue_card, self.revenue_value = create_card(
            cards, "TỔNG DOANH THU", "0 VNĐ", PURPLE
        )

        for card in (
            self.total_card,
            self.registered_card,
            self.revenue_card
        ):
            card.pack(side="left", fill="x", expand=True, padx=5)

    # ================= FORM =================

    def create_form(self):
        self.form = tk.LabelFrame(
            self.content,
            text="  THÔNG TIN HỘI VIÊN  ",
            bg=WHITE,
            fg=DARK,
            font=("Arial", 11, "bold"),
            padx=15,
            pady=12,
            bd=1,
            relief="solid"
        )
        self.form.pack(fill="x", pady=(0, 15))

        self.entries = {}

        fields = [
            ("Mã hội viên", "id"),
            ("Họ và tên", "name"),
            ("Tuổi", "age"),
            ("Số điện thoại", "phone")
        ]

        for i, (label, key) in enumerate(fields):
            row = i // 2
            col = (i % 2) * 2

            tk.Label(
                self.form,
                text=label,
                bg=WHITE,
                fg=TEXT,
                font=("Arial", 10, "bold")
            ).grid(
                row=row, column=col,
                sticky="w", padx=10, pady=8
            )

            entry = tk.Entry(
                self.form,
                font=("Arial", 11),
                relief="solid",
                bd=1,
                width=30
            )

            entry.grid(
                row=row, column=col + 1,
                sticky="ew", padx=10, pady=8, ipady=6
            )

            self.entries[key] = entry

        self.form.grid_columnconfigure(1, weight=1)
        self.form.grid_columnconfigure(3, weight=1)

        button_frame = tk.Frame(self.form, bg=WHITE)
        button_frame.grid(
            row=2, column=0, columnspan=4,
            sticky="w", pady=(12, 0)
        )

        create_button(
            button_frame, "+ THÊM MỚI",
            self.add, GREEN
        ).pack(side="left", padx=5)

        create_button(
            button_frame, "CẬP NHẬT",
            self.edit, PRIMARY
        ).pack(side="left", padx=5)

        create_button(
            button_frame, "XÓA",
            self.delete, RED
        ).pack(side="left", padx=5)

        create_button(
            button_frame, "XÓA TRẮNG",
            self.clear_form, MUTED
        ).pack(side="left", padx=5)

    # ================= TABLE =================

    def create_table(self):
        frame = tk.Frame(self.content, bg=WHITE)
        frame.pack(fill="both", expand=True)

        top = tk.Frame(frame, bg=WHITE)
        top.pack(fill="x", padx=15, pady=12)

        tk.Label(
            top,
            text="DANH SÁCH HỘI VIÊN",
            bg=WHITE,
            fg=DARK,
            font=("Arial", 12, "bold")
        ).pack(side="left")

        self.search_entry = tk.Entry(
            top, width=24, font=("Arial", 10),
            relief="solid", bd=1
        )
        self.search_entry.pack(side="right", padx=5, ipady=6)

        create_button(
            top, "TÌM KIẾM",
            self.search, ORANGE, 11
        ).pack(side="right", padx=5)

        columns = (
            "id", "name", "age",
            "phone", "package", "end_date"
        )

        self.tree = ttk.Treeview(
            frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        headings = {
            "id": "MÃ HỘI VIÊN",
            "name": "HỌ VÀ TÊN",
            "age": "TUỔI",
            "phone": "SỐ ĐIỆN THOẠI",
            "package": "GÓI TẬP",
            "end_date": "NGÀY HẾT HẠN"
        }

        widths = {
            "id": 110,
            "name": 180,
            "age": 60,
            "phone": 140,
            "package": 150,
            "end_date": 130
        }

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(
                col,
                width=widths[col],
                anchor="center"
            )

        scrollbar = ttk.Scrollbar(
            frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(
            side="left", fill="both", expand=True,
            padx=(12, 0), pady=(0, 12)
        )

        scrollbar.pack(
            side="right", fill="y", pady=(0, 12), padx=(0, 12)
        )

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.select_member
        )

        # Nút chức năng bổ sung
        bottom = tk.Frame(self.content, bg=BG)
        bottom.pack(fill="x", pady=(12, 0))

        create_button(
            bottom, "ĐĂNG KÝ GÓI TẬP",
            self.register_package, PURPLE, 19
        ).pack(side="left", padx=5)

        create_button(
            bottom, "THỐNG KÊ DOANH THU",
            self.statistics, "#0891B2", 21
        ).pack(side="left", padx=5)

        create_button(
            bottom, "LÀM MỚI DANH SÁCH",
            self.refresh_all, MUTED, 20
        ).pack(side="left", padx=5)

    # ================= FUNCTIONS =================

    def get_form_data(self):
        return {
            key: entry.get().strip()
            for key, entry in self.entries.items()
        }

    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

        self.tree.selection_remove(self.tree.selection())

    def refresh_all(self):
        self.show_members()
        self.update_dashboard()

    def show_members(self, keyword=""):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for member in self.data:
            if (
                keyword and
                keyword not in member["id"].lower()
                and keyword not in member["name"].lower()
            ):
                continue

            self.tree.insert(
                "",
                "end",
                values=(
                    member["id"],
                    member["name"],
                    member["age"],
                    member["phone"],
                    member["package"],
                    member["end_date"]
                )
            )

    def update_dashboard(self):
        total = len(self.data)

        registered = sum(
            1 for m in self.data
            if m["package"] != "Chưa đăng ký"
        )

        revenue = sum(
            m.get("total_paid", 0) for m in self.data
        )

        self.total_value.config(text=str(total))
        self.registered_value.config(text=str(registered))
        self.revenue_value.config(
            text=f"{revenue:,} VNĐ"
        )

    # ================= ADD =================

    def add(self):
        member = self.get_form_data()

        if not all(member.values()):
            messagebox.showwarning(
                "Thông báo", "Vui lòng nhập đầy đủ thông tin!"
            )
            return

        try:
            if int(member["age"]) <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Lỗi", "Tuổi không hợp lệ!")
            return

        member.update({
            "package": "Chưa đăng ký",
            "end_date": "",
            "total_paid": 0
        })

        if add_member(self.data, member):
            self.refresh_all()
            self.clear_form()
            messagebox.showinfo(
                "Thành công", "Đã thêm hội viên!"
            )
        else:
            messagebox.showerror(
                "Lỗi", "Mã hội viên đã tồn tại!"
            )

    # ================= SELECT =================

    def select_member(self, event):
        selected = self.tree.selection()

        if not selected:
            return

        values = self.tree.item(
            selected[0], "values"
        )

        for key, value in zip(
            ["id", "name", "age", "phone"], values[:4]
        ):
            self.entries[key].delete(0, tk.END)
            self.entries[key].insert(0, value)

    # ================= EDIT =================

    def edit(self):
        member = self.get_form_data()

        if not all(member.values()):
            messagebox.showwarning(
                "Thông báo", "Vui lòng chọn và nhập đủ thông tin!"
            )
            return

        try:
            if int(member["age"]) <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Lỗi", "Tuổi không hợp lệ!")
            return

        result = update_member(
            self.data,
            member["id"],
            {
                "name": member["name"],
                "age": member["age"],
                "phone": member["phone"]
            }
        )

        if result:
            self.refresh_all()
            self.clear_form()
            messagebox.showinfo(
                "Thành công", "Cập nhật hội viên thành công!"
            )
        else:
            messagebox.showerror(
                "Lỗi", "Không tìm thấy hội viên!"
            )

    # ================= DELETE =================

    def delete(self):
        member_id = self.entries["id"].get().strip()

        if not member_id:
            messagebox.showwarning(
                "Thông báo", "Vui lòng chọn hội viên!"
            )
            return

        if messagebox.askyesno(
            "Xác nhận", "Bạn có chắc muốn xóa hội viên này?"
        ):
            if delete_member(self.data, member_id):
                self.refresh_all()
                self.clear_form()
                messagebox.showinfo(
                    "Thành công", "Đã xóa hội viên!"
                )
            else:
                messagebox.showerror(
                    "Lỗi", "Không tìm thấy hội viên!"
                )

    # ================= SEARCH =================

    def search(self):
        keyword = self.search_entry.get().strip().lower()

        if not keyword:
            self.show_members()
            return

        self.show_members(keyword)

    # ================= PACKAGE =================

    def register_package(self):
        member_id = self.entries["id"].get().strip()

        if not member_id:
            messagebox.showwarning(
                "Thông báo", "Hãy chọn hội viên trong bảng trước!"
            )
            return

        member = next(
            (m for m in self.data if m["id"] == member_id),
            None
        )

        if member is None:
            messagebox.showerror("Lỗi", "Không tìm thấy hội viên!")
            return

        packages = {
            "1 tháng": (300000, 30),
            "3 tháng": (800000, 90),
            "6 tháng": (1500000, 180),
            "12 tháng": (2800000, 365)
        }

        window = tk.Toplevel(self.root)
        window.title("Đăng ký gói tập")
        window.geometry("420x390")
        window.configure(bg=BG)
        window.transient(self.root)
        window.grab_set()

        tk.Label(
            window,
            text="ĐĂNG KÝ GÓI TẬP",
            bg=BG,
            fg=DARK,
            font=("Arial", 17, "bold")
        ).pack(pady=(25, 5))

        tk.Label(
            window,
            text=f"Hội viên: {member['name']}",
            bg=BG,
            fg=MUTED,
            font=("Arial", 11)
        ).pack(pady=5)

        choice = tk.StringVar(value="1 tháng")

        for name, (price, days) in packages.items():
            tk.Radiobutton(
                window,
                text=f"{name}  |  {price:,} VNĐ",
                variable=choice,
                value=name,
                bg=BG,
                fg=TEXT,
                activebackground=BG,
                font=("Arial", 11),
                padx=30,
                pady=6
            ).pack(anchor="w")

        def confirm():
            package = choice.get()
            price, days = packages[package]

            start = datetime.now()
            end = start + timedelta(days=days)

            member["package"] = package
            member["end_date"] = end.strftime("%d/%m/%Y")
            member["total_paid"] = (
                member.get("total_paid", 0) + price
            )

            save_data(self.data)
            window.destroy()
            self.refresh_all()

            messagebox.showinfo(
                "Thành công",
                f"Đăng ký thành công!\n"
                f"Gói tập: {package}\n"
                f"Số tiền: {price:,} VNĐ"
            )

        create_button(
            window, "XÁC NHẬN ĐĂNG KÝ",
            confirm, GREEN, 23
        ).pack(pady=20)

    # ================= STATISTICS =================

    def statistics(self):
        total = len(self.data)

        registered = sum(
            1 for m in self.data
            if m["package"] != "Chưa đăng ký"
        )

        revenue = sum(
            m.get("total_paid", 0) for m in self.data
        )

        active = 0
        today = datetime.now().date()

        for member in self.data:
            if member["end_date"]:
                try:
                    end = datetime.strptime(
                        member["end_date"], "%d/%m/%Y"
                    ).date()

                    if end >= today:
                        active += 1
                except ValueError:
                    pass

        messagebox.showinfo(
            "THỐNG KÊ PHÒNG GYM",
            f"Tổng hội viên: {total}\n"
            f"Đã đăng ký gói tập: {registered}\n"
            f"Còn thời hạn: {active}\n"
            f"Đã hết hạn hoặc chưa đăng ký: {total-active}\n"
            f"Tổng doanh thu: {revenue:,} VNĐ"
        )

    # ================= SIDEBAR NAVIGATION =================

    def dashboard(self):
        self.refresh_all()
        self.search_entry.delete(0, tk.END)

    def member_section(self):
        self.clear_form()
        self.search_entry.delete(0, tk.END)
        self.show_members()

    def package_section(self):
        self.register_package()

    # ================= START =================


if __name__ == "__main__":
    root = tk.Tk()
    app = GymApp(root)
    root.mainloop()
