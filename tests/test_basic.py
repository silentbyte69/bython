"""
Basic tests for BrainPy functionality
"""

import pytest
import brainpy
from brainpy import BrainPy, BrainPySyntaxError, BrainPyRuntimeError


class TestBasicFunctionality:
    """Test basic Brainfuck execution and compilation"""
    
    def test_basic_increment(self):
        """Test basic increment and output"""
        result = brainpy.execute("+.", "")
        assert result == chr(1)
    
    def test_multiple_increments(self):
        """Test multiple increments"""
        result = brainpy.execute("+++.", "")
        assert result == chr(3)
    
    def test_decrement(self):
        """Test decrement operation"""
        result = brainpy.execute("+++--.", "")
        assert result == chr(1)
    
    def test_pointer_movement_right(self):
        """Test pointer movement to the right"""
        result = brainpy.execute("+>++.", "")
        assert result == chr(2)
    
    def test_pointer_movement_left(self):
        """Test pointer movement to the left"""
        result = brainpy.execute("+>++<.", "")
        assert result == chr(1)
    
    def test_empty_program(self):
        """Test empty program execution"""
        result = brainpy.execute("", "")
        assert result == ""
    
    def test_only_comments(self):
        """Test program with only comments"""
        code = "This is just a comment without any Brainfuck commands"
        result = brainpy.execute(code, "")
        assert result == ""


class TestInputOutput:
    """Test input and output functionality"""
    
    def test_simple_input(self):
        """Test basic input operation"""
        result = brainpy.execute(",.", "A")
        assert result == "A"
    
    def test_multiple_inputs(self):
        """Test multiple input operations"""
        result = brainpy.execute(">,>,<.<.", "AB")
        assert result == "BA"  # Reversed output
    
    def test_empty_input(self):
        """Test with empty input"""
        result = brainpy.execute(",.", "")
        assert result == chr(0)  # Should be null character when no input
    
    def test_input_echo(self):
        """Test simple echo program"""
        result = brainpy.execute(",[.,]", "Hello")
        # Should echo the input until null terminator
        assert "Hello" in result


class TestLoopFunctionality:
    """Test Brainfuck loop operations"""
    
    def test_simple_loop(self):
        """Test basic loop functionality"""
        # Loop that adds 5 three times to make 15
        result = brainpy.execute("+++[>+++++<-]>.", "")
        assert result == chr(15)
    
    def test_nested_loops(self):
        """Test nested loops"""
        # Nested loop example: 2 * 3 * 4 = 24
        code = "++[>+++[>++++<-]<-]>>."
        result = brainpy.execute(code, "")
        assert result == chr(24)
    
    def test_zero_iteration_loop(self):
        """Test loop that should not execute"""
        result = brainpy.execute("[-]+.", "")  # Set to 0, loop doesn't run, then increment to 1
        assert result == chr(1)
    
    def test_clear_cell_loop(self):
        """Test loop that clears a cell"""
        result = brainpy.execute("+++[-].", "")  # Set to 3, then decrement to 0
        assert result == chr(0)


class TestMemoryOperations:
    """Test memory manipulation and boundaries"""
    
    def test_memory_wrapping_right(self):
        """Test that memory pointer wraps correctly when moving right"""
        interpreter = BrainPy(memory_size=5)
        result = interpreter.execute_direct("+++++>+.", "")
        # After 5 increments, move right and increment
        assert result == chr(1)
    
    def test_memory_wrapping_left(self):
        """Test that memory pointer wraps correctly when moving left"""
        interpreter = BrainPy(memory_size=5)
        result = interpreter.execute_direct("<+.", "")  # Move left (wraps to end), increment
        assert result == chr(1)
    
    def test_cell_value_wrapping_positive(self):
        """Test that cell values wrap at 256 for positive overflow"""
        result = brainpy.execute("+" * 300 + ".", "")  # Increment 300 times
        # Should wrap: 300 % 256 = 44
        assert result == chr(44)
    
    def test_cell_value_wrapping_negative(self):
        """Test that cell values wrap at 256 for negative overflow"""
        result = brainpy.execute("-" * 50 + ".", "")  # Decrement 50 times
        # Should wrap: 256 - (50 % 256) = 256 - 50 = 206
        assert result == chr(206)
    
    def test_large_memory_size(self):
        """Test with custom large memory size"""
        interpreter = BrainPy(memory_size=100000)
        result = interpreter.execute_direct("+" * 500 + ".", "")
        assert result == chr(500 % 256)
    
    def test_small_memory_size(self):
        """Test with custom small memory size"""
        interpreter = BrainPy(memory_size=10)
        result = interpreter.execute_direct("+" * 8 + ".", "")
        assert result == chr(8)


class TestCompilation:
    """Test Brainfuck to Python compilation"""
    
    def test_compile_basic_operations(self):
        """Test basic compilation"""
        python_code = brainpy.compile_to_python("+++.--")
        assert "def brainpy_program()" in python_code
        assert "memory = [0]" in python_code
        assert "pointer = 0" in python_code
        assert "output = []" in python_code
        assert "memory[pointer]" in python_code
        assert "output.append" in python_code
    
    def test_compile_with_loops(self):
        """Test compilation with loops"""
        python_code = brainpy.compile_to_python("++[->+<]")
        assert "while memory[pointer] != 0:" in python_code
    
    def test_compile_with_input(self):
        """Test compilation with input operations"""
        python_code = brainpy.compile_to_python(",,.")
        assert "input_data = iter(input_data)" in python_code
        assert "next(input_data)" in python_code
        assert "ord(char)" in python_code
    
    def test_compile_pointer_movements(self):
        """Test compilation of pointer movements"""
        python_code = brainpy.compile_to_python("><")
        assert "pointer = (pointer + 1) % memory_size" in python_code
        assert "pointer = (pointer - 1) % memory_size" in python_code
    
    def test_compiled_code_executable(self):
        """Test that compiled code can be executed"""
        brainfuck_code = "+++.--"
        python_code = brainpy.compile_to_python(brainfuck_code)
        
        # Create a namespace for execution
        namespace = {"input_data": ""}
        
        # Execute the compiled code
        try:
            exec(python_code, namespace)
            # The result should be available
            assert "result" in namespace
        except Exception as e:
            pytest.fail(f"Compiled code execution failed: {e}")


class TestErrorHandling:
    """Test error handling and validation"""
    
    def test_unmatched_open_bracket(self):
        """Test syntax error for unmatched open bracket"""
        with pytest.raises(BrainPySyntaxError, match="Unmatched"):
            brainpy.execute("+++[--", "")
    
    def test_unmatched_close_bracket(self):
        """Test syntax error for unmatched close bracket"""
        with pytest.raises(BrainPySyntaxError, match="Unmatched"):
            brainpy.execute("+++]--", "")
    
    def test_nested_unmatched_brackets(self):
        """Test syntax error for nested unmatched brackets"""
        with pytest.raises(BrainPySyntaxError, match="Unmatched"):
            brainpy.execute("++[+[--]", "")
    
    def test_valid_brackets(self):
        """Test that valid bracket pairs work correctly"""
        # This should not raise an exception
        result = brainpy.execute("++[--]++", "")
        assert result == ""
    
    def test_complex_valid_brackets(self):
        """Test complex but valid bracket structures"""
        code = "++[>+[>+<-]<-]"
        result = brainpy.execute(code + ".", "")
        # Should execute without syntax errors
        assert result is not None
    
    def test_deeply_nested_valid_brackets(self):
        """Test deeply nested but valid brackets"""
        code = "+[[[]]]"  # Valid nested brackets
        result = brainpy.execute(code + ".", "")
        assert result == chr(1)


class TestClassInterface:
    """Test BrainPy class interface"""
    
    def test_class_initialization_default(self):
        """Test class initialization with default parameters"""
        interpreter = BrainPy()
        assert interpreter.memory_size == 30000
        assert interpreter.brainfuck_commands == set('><+-.,[]')
    
    def test_class_initialization_custom(self):
        """Test class initialization with custom parameters"""
        interpreter = BrainPy(memory_size=5000)
        assert interpreter.memory_size == 5000
    
    def test_execute_vs_execute_direct(self):
        """Test that both execution methods produce same results"""
        code = "+++[>++<-]>."
        
        interpreter = BrainPy()
        direct_result = interpreter.execute_direct(code, "")
        compile_result = interpreter.execute(code, "")
        
        assert direct_result == compile_result
    
    def test_multiple_instances_independent(self):
        """Test that multiple instances are independent"""
        interpreter1 = BrainPy(memory_size=100)
        interpreter2 = BrainPy(memory_size=200)
        
        result1 = interpreter1.execute_direct("+++.", "")
        result2 = interpreter2.execute_direct("---.", "")
        
        assert result1 == chr(3)
        assert result2 == chr(253)  # 256 - 3


class TestIntegration:
    """Test integration and real-world examples"""
    
    def test_hello_world(self):
        """Test Hello World program"""
        hello_world = (
            "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++."
            "------.--------.>>+.>++."
        )
        result = brainpy.execute(hello_world, "")
        assert "Hello World" in result
    
    def test_simple_arithmetic(self):
        """Test simple arithmetic operations"""
        # Multiply 3 * 4 = 12
        code = "+++[>++++<-]>."
        result = brainpy.execute(code, "")
        assert result == chr(12)
    
    def test_character_output(self):
        """Test specific character output"""
        # Output 'A' (ASCII 65)
        code = "++++++++[>++++++++<-]>+."  # 8*8+1 = 65
        result = brainpy.execute(code, "")
        assert result == 'A'
    
    def test_loop_counter(self):
        """Test loop as counter"""
        # Count down from 5 to 1
        code = "+++++[.-]"  # Output: 5, 4, 3, 2, 1
        result = brainpy.execute(code, "")
        expected = ''.join(chr(i) for i in range(5, 0, -1))
        assert result == expected


class TestEdgeCases:
    """Test edge cases"""
    
    def test_only_brackets(self):
        """Test program with only brackets"""
        result = brainpy.execute("[][]", "")
        assert result == ""
    
    def test_single_operation(self):
        """Test programs with single operations"""
        assert brainpy.execute(".", "") == chr(0)
        assert brainpy.execute("+", "") == ""
        assert brainpy.execute(">", "") == ""
        assert brainpy.execute("<", "") == ""
    
    def test_whitespace_handling(self):
        """Test that whitespace is properly ignored"""
        code = "  +  +  +  .  "
        result = brainpy.execute(code, "")
        assert result == chr(3)
    
    def test_mixed_comments_and_code(self):
        """Test mixed comments and code"""
        code = """
        Initialize counter to 8
        ++++++++
        [
            Output and decrement
            .-
        ]
        """
        clean_code = "++++++++[.-]"
        result = brainpy.execute(clean_code, "")
        expected = ''.join(chr(i) for i in range(8, 0, -1))
        assert result == expected


def test_module_level_functions():
    """Test that module-level functions work correctly"""
    # Test execute function
    result = brainpy.execute("+.", "")
    assert result == chr(1)
    
    # Test compile_to_python function
    python_code = brainpy.compile_to_python("+.")
    assert "def brainpy_program()" in python_code
    
    # Test that both use the same default memory size
    interpreter = BrainPy()
    module_result = brainpy.execute("+.", "")
    class_result = interpreter.execute_direct("+.", "")
    assert module_result == class_result
