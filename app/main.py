import tkinter as tk

from app.views.main_view import MainView



root = tk.Tk()
root.configure(bg='green')
root.geometry("1920x1080")
MainView(root)
root.mainloop()


