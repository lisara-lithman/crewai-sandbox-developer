import app

# Instantiate the Gradio Blocks object without launching the app
ui = app.create_ui()

# Confirm that the Blocks object has been created successfully
print('Gradio UI constructed successfully: ', type(ui))
