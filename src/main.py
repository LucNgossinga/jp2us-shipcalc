from src.ui.app_ui import launch_app

if __name__ == "__main__":
    try:
        launch_app()
    except Exception as e:
        import tkinter.messagebox as mb
        mb.showerror("Unexpected Error", f"Something went wrong:\n\n{str(e)}")
        raise
