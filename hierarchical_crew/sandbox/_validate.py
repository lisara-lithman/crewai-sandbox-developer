import app

# The purpose of this validation script is to ensure that the Gradio Blocks object
# in app.py initializes without error. We simply import the app module, which constructs
# the Blocks (demo) object, but we do not call demo.launch().

# Optionally, we can access the demo object to confirm its type.

if __name__ == '__main__':
    demo = app.demo
    print('Gradio Blocks object instantiated successfully:', type(demo))
