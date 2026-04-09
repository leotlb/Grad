import tkinter as tk
from db_manager import DBManager
from gui import App

if __name__ == "__main__":
    
    root = tk.Tk()
    db_manager_instance = DBManager()
    app_instance = App(root, db_manager_instance)
    root.mainloop()

    # Ao fechar a janela principal, desconectar do banco se a conexão ainda estiver ativa
    if db_manager_instance.conn:
        if app_instance.current_user_id: # Log logout se usuário estava logado
             db_manager_instance.log_user_activity(app_instance.current_user_id, "logout")
        db_manager_instance.disconnect()
