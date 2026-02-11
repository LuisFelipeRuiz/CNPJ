import customtkinter as ctk

ctk.set_appearance_mode("dark")

app = ctk.CTk()
app.title("Sistema de Login")
app.geometry("300x400")

# Centraliza o frame na janela
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)

frame = ctk.CTkFrame(app, fg_color="transparent")
frame.grid(row=0, column=0)

# Conteúdo do login (tudo centralizado)
usuario = ctk.CTkLabel(frame, text="Usuário")
usuario.grid(row=0, column=0, pady=(0, 8))

c_usuario = ctk.CTkEntry(frame, placeholder_text="Digite seu usuário", width=200)
c_usuario.grid(row=1, column=0, pady=(0, 20))

senha = ctk.CTkLabel(frame, text="Senha")
senha.grid(row=2, column=0, pady=(0, 8))

c_senha = ctk.CTkEntry(frame, placeholder_text="Digite sua senha", show="*", width=200)
c_senha.grid(row=3, column=0)

app.mainloop()
