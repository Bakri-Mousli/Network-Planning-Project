import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageGrab

def save_figure_as_image(fig):
    """
    تحفظ الشكل (figure) كصورة باستخدام حوار حفظ الملفات.
    """
    try:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Files", "*.png"), ("SVG Files", "*.svg")]
        )
        if not file_path:
            return
        fig.savefig(file_path, dpi=300)
        messagebox.showinfo("نجاح", "تم حفظ الرسم مع المسار الحرج كصورة بنجاح!")
    except Exception as e:
        messagebox.showerror("خطأ", f"حدث خطأ أثناء الحفظ: {str(e)}")
