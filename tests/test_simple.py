"""
Simple tests for BrainPy functionality
"""

import brainpy
from brainpy import BrainPy, BrainPySyntaxError


def test_basic_operations():
    """Test basic Brainfuck operations"""
    # Test increment
    result = brainpy.execute("+.", "")
    assert result == chr(1), f"Expected chr(1), got {repr(result)}"
    
    # Test multiple increments
    result = brainpy.execute("+++.", "")
    assert result == chr(3), f"Expected chr(3), got {repr(result)}"
    
    # Test decrement
    result = brainpy.execute("+++--.", "")
    assert result == chr(1), f"Expected chr(1), got {repr(result)}"


def test_pointer_movement():
    """Test pointer movement"""
    result = brainpy.execute("+>++.", "")
    assert result == chr(2), f"Expected chr(2), got {repr(result)}"
    
    result = brainpy.execute("+>++<.", "")
    assert result == chr(1), f"Expected chr(1), got {repr(result)}"


def test_input_output():
    """Test input and output"""
    result = brainpy.execute(",.", "A")
    assert result == "A", f"Expected 'A', got {repr(result)}"
    
    result = brainpy.execute(",.", "")
    assert result == chr(0), f"Expected chr(0), got {repr(result)}"


def test_loops():
    """Test loops"""
    # Simple loop: 3 * 5 = 15
    result = brainpy.execute("+++[>+++++<-]>.", "")
    assert result == chr(15), f"Expected chr(15), got {repr(result)}"
    
    # Clear cell loop
    result = brainpy.execute("+++[-].", "")
    assert result == chr(0), f"Expected chr(0), got {repr(result)}"


def test_compilation():
    """Test compilation to Python"""
    python_code = brainpy.compile_to_python("+++.--")
    assert "def brainpy_program()" in python_code
    assert "memory = [0]" in python_code
    assert "pointer = 0" in python_code


def test_error_handling():
    """Test error handling"""
    try:
        brainpy.execute("+++[--", "")  # Missing bracket
        assert False, "Should have raised BrainPySyntaxError"
    except BrainPySyntaxError:
        pass  # Expected
    
    try:
        brainpy.execute("+++]--", "")  # Extra bracket
        assert False, "Should have raised BrainPySyntaxError"
    except BrainPySyntaxError:
        pass  # Expected


def test_class_interface():
    """Test BrainPy class interface"""
    interpreter = BrainPy(memory_size=100)
    assert interpreter.memory_size == 100
    
    result = interpreter.execute_direct("+.", "")
    assert result == chr(1)
    
    result = interpreter.execute("+.", "")
    assert result == chr(1)


def test_hello_world():
    """Test Hello World program"""
    hello_world = "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."
    result = brainpy.execute(hello_world, "")
    # Just check that it produces output and doesn't crash
    assert len(result) > 0
    assert "Hello" in result


def test_empty_program():
    """Test empty program"""
    result = brainpy.execute("", "")
    assert result == ""
    
    result = brainpy.execute("   ", "")
    assert result == ""


def test_comments_ignored():
    """Test that comments are ignored"""
    code = "This is a comment + this is another ."
    result = brainpy.execute(code, "")
    assert result == chr(1)
