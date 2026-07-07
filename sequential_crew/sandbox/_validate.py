import app


def test_blocks_instantiation():
    # Ensure the Gradio Blocks object is constructed without errors
    demo = app.demo
    # Validate that it's an instance of gr.Blocks
    assert hasattr(demo, 'launch'), "The Blocks object does not have a launch method"
    print('Blocks object constructed successfully!')


if __name__ == '__main__':
    test_blocks_instantiation()
