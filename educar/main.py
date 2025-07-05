from model import criar_tabelas
from view import App

   
def main():
    # Garante que as tabelas do banco de dados estejam criadas
    criar_tabelas()

    # Inicia o aplicativo (interface gráfica)
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
