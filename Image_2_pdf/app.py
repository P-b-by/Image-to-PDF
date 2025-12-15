import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
class ImageToPdfConverter:
    def __init__(self, root):
        self.root = root
        # theme colors
        self.bg_color = "#ffecea"
        self.fg_color = "#000000"
        self.accent = "#f9e7c9"
        self.accent_hover = "#30360e"

        self.root.configure(bg=self.bg_color)

        self.selected_images_listsbox=tk.Listbox(root, selectmode=tk.MULTIPLE)
        self.image_path = []
        self.output_pdf_name = tk.StringVar()
        self.initialize_ui()
        

    def initialize_ui(self):
        title_label=tk.Label(self.root, text="Image to PDF Converter", font=("Helvetica", 16))  
        title_label.pack(pady=10)
        title_label.config(bg=self.bg_color, fg=self.fg_color)
        instr_label = tk.Label(self.root, text="Use 'Add Images' to add files. Select items and use 'Remove Selected' or 'Clear All' as needed.", font=("Helvetica", 9))
        instr_label.pack(pady=(0, 8))
        instr_label.config(bg=self.bg_color, fg=self.fg_color)
        # controls frame
        controls_frame = tk.Frame(self.root)
        controls_frame.pack(pady=(0, 10), fill=tk.X, padx=20)
        select_image_button=tk.Button(controls_frame, text="Add Images", font=("Helvetica", 12), command=self.select_images)
        select_image_button.pack(side=tk.LEFT)
        remove_button=tk.Button(controls_frame, text="Remove Selected", font=("Helvetica", 12), command=self.remove_selected_images)
        remove_button.pack(side=tk.LEFT, padx=(10, 0))
        clear_button=tk.Button(controls_frame, text="Clear All", font=("Helvetica", 12), command=self.clear_all_images)
        clear_button.pack(side=tk.LEFT, padx=(10, 0))
        # style buttons
        self._style_button(select_image_button)
        self._style_button(remove_button)
        self._style_button(clear_button)

        self.selected_images_listsbox.pack(pady=(0, 10), fill=tk.BOTH, expand=True, padx=20)
        self.selected_images_listsbox.config(bg="#f9e7c9", fg=self.fg_color, selectbackground="#f9e7c9", selectforeground=self.fg_color, highlightthickness=0)
        label=tk.Label(self.root, text="Output PDF Name:", font=("Helvetica", 12))  
        label.pack(pady=(0, 5)) 
        label.config(bg=self.bg_color, fg=self.fg_color)
        output_entry=tk.Entry(self.root, textvariable=self.output_pdf_name, font=("Helvetica", 12), width=40, justify="center")  
        output_entry.pack(pady=(0, 10), fill=tk.X, padx=20)
        output_entry.config(bg="#EF7626", fg=self.fg_color, insertbackground=self.fg_color)
        Convert_pdf=tk.Button(self.root, text="Convert to pdf", font=("Helvetica", 16), command=self.convert_images_to_pdf)
        Convert_pdf.pack(pady=(0, 10))
        self._style_button(Convert_pdf, big=True)
        # progressbar (hidden until conversion)
        self.progress = ttk.Progressbar(self.root, mode='indeterminate', length=260)
    def select_images(self):
        new_paths = filedialog.askopenfilenames(title="Select Images", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if not new_paths:
            return
        # add new images preserving order and avoiding duplicates
        for p in new_paths:
            if p not in self.image_path:
                self.image_path.append(p)
        self.Update_selected_images_listsbox()

    def remove_selected_images(self):
        selected_indices = list(self.selected_images_listsbox.curselection())
        if not selected_indices:
            return
        # remove from the end so indices stay valid
        for idx in reversed(selected_indices):
            try:
                del self.image_path[idx]
            except IndexError:
                pass
        self.Update_selected_images_listsbox()

    def clear_all_images(self):
        self.image_path = []
        self.Update_selected_images_listsbox()
    def _style_button(self, btn, big=False):
        pad_y = 8 if big else 4
        btn.config(bg=self.accent, fg=self.fg_color, activebackground=self.accent_hover, activeforeground=self.fg_color, bd=0, padx=10, pady=pad_y)
        btn.bind("<Enter>", lambda e: btn.config(bg=self.accent_hover))
        btn.bind("<Leave>", lambda e: btn.config(bg=self.accent))
        btn.bind("<Enter>", lambda e, t=btn['text']: self._show_tooltip(e.widget, t))
        btn.bind("<Leave>", lambda e: self._hide_tooltip())

    def _show_tooltip(self, widget, text):
        x = widget.winfo_rootx() + 20
        y = widget.winfo_rooty() + 20
        self._tooltip = tk.Toplevel(self.root)
        self._tooltip.wm_overrideredirect(True)
        self._tooltip.wm_geometry(f"+{x}+{y}")
        lbl = tk.Label(self._tooltip, text=text, bg="#fa6a0a", fg=self.fg_color, font=("Helvetica", 9), padx=6, pady=3)
        lbl.pack()

    def _hide_tooltip(self):
        try:
            self._tooltip.destroy()
        except Exception:
            pass
    def Update_selected_images_listsbox(self):
        self.selected_images_listsbox.delete(0, tk.END)
        for image in self.image_path:
            self.selected_images_listsbox.insert(tk.END, os.path.basename(image))   
        # style listbox after updating
        self.selected_images_listsbox.config(bg="#f9e7c9", fg=self.fg_color, selectbackground="#f9e7c9", selectforeground=self.fg_color, highlightthickness=0)
    def convert_images_to_pdf(self):
        from PIL import Image
        if not self.image_path:
            messagebox.showerror("Error", "No images selected!")
            return
        output_name = self.output_pdf_name.get().strip()
        if not output_name:
            messagebox.showerror("Error", "Please enter an output PDF name!")
            return
        images = []
        # show progress
        try:
            self.progress.pack(pady=(0, 10))
            self.progress.start(10)
        except Exception:
            pass
        for img_path in self.image_path:
            img = Image.open(img_path)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            images.append(img)
        pdf_path = f"{output_name}.pdf"
        try:
            images[0].save(pdf_path, save_all=True, append_images=images[1:])
            messagebox.showinfo("Success", f"PDF saved as {pdf_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create PDF: {e}")
        finally:
            try:
                self.progress.stop()
                self.progress.pack_forget()
            except Exception:
                pass
def main():
    root = tk.Tk()
    app = ImageToPdfConverter(root)
    root.title("Image to PDF")
    root.geometry("600x450")
    
    root.mainloop()
if __name__ == "__main__":
    main()