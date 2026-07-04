import app

def validate_app():
    try:
        app.demo
        print("App structure validated successfully.")
    except Exception as e:
        print(f"Error during validation: {e}")

if __name__ == '__main__':
    validate_app()