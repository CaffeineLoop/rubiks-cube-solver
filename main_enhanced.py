"""
Enhanced Main Interface for Rubik's Cube Solver - Hackathon Edition
Supports LBL and CFOP solving methods with comprehensive features
"""

from rubiks_cube import RubiksCube
from solver import RubiksCubeSolver
from visualizer import SimpleVisualizer, CubeVisualizer3D, VISUALIZATION_AVAILABLE
import threading
import time

def main_menu():
    """Display enhanced main menu with LBL and CFOP support"""
    # Start with default 3x3 cube
    cube = RubiksCube(size=3)
    current_size = 3
    solving_method = "LBL"  # Default method
    
    while True:
        print("\n" + "="*70)
        print(f"    RUBIK'S CUBE SOLVER - HACKATHON EDITION")
        print(f"    Current: {current_size}x{current_size}x{current_size} | Method: {solving_method}")
        print("="*70)
        print("1. Display current cube state")
        print("2. Execute manual moves")
        print("3. Scramble cube")
        print("4. Auto-solve cube (LBL method)")
        print("5. Auto-solve cube (CFOP method)")
        print("6. Reset cube to solved state")
        print("7. Text visualization demo")
        print("8. 3D visualization (if available)")
        print("9. Complete demo")
        print("10. Cube size information")
        print("11. Change cube size")
        print("12. Change solving method")
        print("13. Compare different cube sizes")
        print("14. Advanced solver statistics")
        print("15. Exit")
        print("="*70)
        print(f"Current cube: {current_size}x{current_size}x{current_size} | Method: {solving_method} | Solved: {cube.is_solved()}")
        print("="*70)
        
        try:
            choice = input("Enter your choice (1-15): ").strip()
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        
        if choice == '1':
            display_cube_state(cube, current_size)
        elif choice == '2':
            manual_moves(cube, current_size)
        elif choice == '3':
            scramble_cube(cube, current_size)
        elif choice == '4':
            solve_cube(cube, current_size, "LBL")
        elif choice == '5':
            solve_cube(cube, current_size, "CFOP")
        elif choice == '6':
            reset_cube(cube, current_size)
        elif choice == '7':
            text_visualization_demo(cube, current_size)
        elif choice == '8':
            launch_3d_visualization(cube, current_size)
        elif choice == '9':
            complete_demo(current_size, solving_method)
        elif choice == '10':
            show_cube_size_info(current_size)
        elif choice == '11':
            cube, current_size = change_cube_size(current_size)
        elif choice == '12':
            solving_method = change_solving_method(solving_method)
        elif choice == '13':
            compare_cube_sizes()
        elif choice == '14':
            advanced_solver_statistics(cube, current_size, solving_method)
        elif choice == '15':
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Please enter 1-15.")

def display_cube_state(cube, size):
    """Display current cube state with size information"""
    print(f"\n=== Current {size}x{size}x{size} Cube State ===")
    viz = SimpleVisualizer(cube)
    viz.draw_unfolded_cube()
    print(f"Cube size: {size}x{size}x{size}")
    print(f"Total stickers: {6 * size * size}")
    print(f"Solved: {cube.is_solved()}")
    print(f"Move history length: {len(cube.move_history)}")
    if cube.move_history:
        recent_moves = cube.move_history[-10:] if len(cube.move_history) > 10 else cube.move_history
        print(f"Recent moves: {' '.join(recent_moves)}")
    else:
        print("No moves executed yet")

def manual_moves(cube, size):
    """Allow user to input manual moves with size awareness"""
    print(f"\n=== Manual Move Input for {size}x{size}x{size} Cube ===")
    print("Enter moves separated by spaces (e.g., U R F' D2)")
    print("Available moves: U, D, R, L, F, B and their variants (', 2)")
    
    if size == 2:
        print("Note: 2x2 cube uses same notation as 3x3 but only has corner pieces")
    elif size >= 4:
        print("Note: For 4x4+ cubes, advanced slice moves (M, E, S) are available")
    
    print("Type 'back' to return to main menu")
    
    while True:
        moves = input(f"\nEnter moves for {size}x{size}x{size} cube: ").strip()
        if moves.lower() == 'back':
            break
        
        try:
            initial_state = cube.get_state_string()
            cube.execute_moves(moves)
            final_state = cube.get_state_string()
            
            print(f"Executed: {moves}")
            if initial_state != final_state:
                print("✓ Cube state changed")
            else:
                print("⚠ No change detected - moves may have cancelled out")
            
            viz = SimpleVisualizer(cube)
            viz.draw_unfolded_cube()
            
        except Exception as e:
            print(f"Error executing moves: {e}")

def scramble_cube(cube, size):
    """Scramble the cube with size-appropriate number of moves"""
    default_moves = {2: 8, 3: 20, 4: 30, 5: 40}
    suggested_moves = default_moves.get(size, size * 8)
    
    try:
        num_moves = input(f"Number of scramble moves for {size}x{size}x{size} cube (default {suggested_moves}): ").strip()
        num_moves = int(num_moves) if num_moves else suggested_moves
    except ValueError:
        num_moves = suggested_moves
    
    print(f"\nScrambling {size}x{size}x{size} cube with {num_moves} moves...")
    cube.scramble(num_moves)
    
    viz = SimpleVisualizer(cube)
    viz.draw_unfolded_cube()
    
    print(f"Scramble complete! Cube complexity increased.")
    print(f"Total stickers: {6 * size * size}")

def solve_cube(cube, size, method):
    """Attempt to solve the cube with specified method"""
    if cube.is_solved():
        print(f"{size}x{size}x{size} cube is already solved!")
        return
    
    print(f"\n=== Starting {method} Auto-Solver for {size}x{size}x{size} Cube ===")
    
    if size == 2:
        print("Note: 2x2 solving uses corner-only algorithms")
        if method == "CFOP":
            print("Note: CFOP method adapted for 2x2 cube")
    elif size >= 4:
        print("Warning: 4x4+ cubes require advanced parity algorithms")
        print("Current solver uses 3x3 method approximation")
    
    solver = RubiksCubeSolver(cube, method)
    
    print(f"Cube state before solving:")
    viz = SimpleVisualizer(cube)
    viz.draw_unfolded_cube()
    
    solution = solver.solve()
    
    print(f"Cube state after solving:")
    viz.draw_unfolded_cube()
    
    stats = solver.get_solving_statistics()
    print(f"\nSolver Statistics for {size}x{size}x{size} cube ({method}):")
    print(f"Total moves attempted: {stats['total_moves']}")
    print(f"Successfully solved: {stats['is_solved']}")
    print(f"Solving method: {stats['solving_method']}")
    print(f"Efficiency score: {stats['efficiency_score']}")
    print(f"Cube complexity: {6 * size * size} stickers")
    
    if stats['moves_breakdown']:
        print(f"Move breakdown:")
        for move, count in stats['moves_breakdown'].items():
            print(f"  {move}: {count} times")

def reset_cube(cube, size):
    """Reset cube to solved state"""
    cube.reset()
    print(f"\n{size}x{size}x{size} cube reset to solved state!")
    viz = SimpleVisualizer(cube)
    viz.draw_unfolded_cube()

def text_visualization_demo(cube, size):
    """Demonstrate text-based visualization with size awareness"""
    print(f"\n=== Text Visualization Demo for {size}x{size}x{size} Cube ===")
    
    if size == 2:
        moves = ['U', 'R']
    elif size == 3:
        moves = ['U', 'R', 'F', 'D']
    else:
        moves = ['U', 'R', 'F']
    
    for move in moves:
        print(f"\nExecuting {move} move on {size}x{size}x{size} cube...")
        viz = SimpleVisualizer(cube)
        viz.animate_move(move)
        input("Press Enter to continue...")

def launch_3d_visualization(cube, size):
    """Launch 3D visualization with size information"""
    if VISUALIZATION_AVAILABLE:
        print(f"\nLaunching 3D visualization for {size}x{size}x{size} cube...")
        print("Controls: ESC to exit, mouse to rotate")
        print(f"Note: Visualizer will show {size}x{size}x{size} grid structure")
        viz_3d = CubeVisualizer3D(cube)
        viz_3d.run()
    else:
        print(f"\n3D visualization not available for {size}x{size}x{size} cube!")
        print("Install required packages with:")
        print("pip install pygame PyOpenGL PyOpenGL_accelerate")

def complete_demo(size, method):
    """Run a complete demonstration with specified cube size and method"""
    print(f"\n=== Complete {size}x{size}x{size} Rubik's Cube Demo ({method}) ===")
    
    demo_cube = RubiksCube(size=size)
    
    print(f"1. Starting with solved {size}x{size}x{size} cube:")
    viz = SimpleVisualizer(demo_cube)
    viz.draw_unfolded_cube()
    input("Press Enter to continue...")
    
    scramble_moves = {2: 8, 3: 15, 4: 25}.get(size, size * 5)
    print(f"\n2. Scrambling {size}x{size}x{size} cube with {scramble_moves} moves...")
    demo_cube.scramble(scramble_moves)
    viz.draw_unfolded_cube()
    input("Press Enter to continue...")
    
    print(f"\n3. Attempting to solve {size}x{size}x{size} cube using {method} method...")
    solver = RubiksCubeSolver(demo_cube, method)
    solution = solver.solve()
    
    print(f"\n4. Final result:")
    viz.draw_unfolded_cube()
    
    stats = solver.get_solving_statistics()
    print(f"\nDemo completed for {size}x{size}x{size} cube ({method})!")
    print(f"Moves used: {stats['total_moves']}")
    print(f"Solved: {stats['is_solved']}")
    print(f"Efficiency score: {stats['efficiency_score']}")
    print(f"Cube complexity: {6 * size * size} total stickers")

def show_cube_size_info(current_size):
    """Display information about different cube sizes"""
    print(f"\n=== Cube Size Information (Current: {current_size}x{current_size}x{current_size}) ===")
    
    cube_info = {
        2: {
            "name": "Pocket Cube / Mini Cube",
            "pieces": "8 corner pieces only",
            "stickers": 24,
            "difficulty": "Beginner",
            "solving": "Corner permutation algorithms"
        },
        3: {
            "name": "Standard Rubik's Cube",
            "pieces": "8 corners + 12 edges + 6 centers",
            "stickers": 54,
            "difficulty": "Intermediate",
            "solving": "Layer-by-layer, CFOP, Roux methods"
        },
        4: {
            "name": "Rubik's Revenge",
            "pieces": "56 pieces total with parity issues",
            "stickers": 96,
            "difficulty": "Advanced",
            "solving": "Reduction method + parity algorithms"
        },
        5: {
            "name": "Professor's Cube",
            "pieces": "98 pieces with complex center solving",
            "stickers": 150,
            "difficulty": "Expert",
            "solving": "Advanced reduction methods"
        }
    }
    
    for size, info in cube_info.items():
        status = " ← CURRENT" if size == current_size else ""
        print(f"\n{size}x{size}x{size} - {info['name']}{status}")
        print(f"  Pieces: {info['pieces']}")
        print(f"  Total stickers: {info['stickers']}")
        print(f"  Difficulty: {info['difficulty']}")
        print(f"  Solving method: {info['solving']}")

def change_cube_size(current_size):
    """Allow user to change cube size"""
    print(f"\n=== Change Cube Size (Current: {current_size}x{current_size}x{current_size}) ===")
    print("Available sizes:")
    print("2 - 2x2x2 (Pocket Cube)")
    print("3 - 3x3x3 (Standard Cube)")
    print("4 - 4x4x4 (Rubik's Revenge)")
    print("5 - 5x5x5 (Professor's Cube)")
    print("6+ - Larger cubes (experimental)")
    
    try:
        new_size = int(input("Enter desired cube size (2-10): ").strip())
        
        if new_size < 2:
            print("Minimum cube size is 2x2x2")
            return RubiksCube(size=current_size), current_size
        elif new_size > 10:
            print("Warning: Very large cubes may be slow")
        
        print(f"Creating new {new_size}x{new_size}x{new_size} cube...")
        new_cube = RubiksCube(size=new_size)
        
        print(f"✓ Successfully created {new_size}x{new_size}x{new_size} cube!")
        print(f"  Total stickers: {6 * new_size * new_size}")
        print(f"  Complexity increase: {((new_size**2) / (current_size**2)):.1f}x")
        
        viz = SimpleVisualizer(new_cube)
        viz.draw_unfolded_cube()
        
        return new_cube, new_size
        
    except ValueError:
        print("Invalid input! Keeping current cube size.")
        return RubiksCube(size=current_size), current_size
    except Exception as e:
        print(f"Error creating cube: {e}")
        return RubiksCube(size=current_size), current_size

def change_solving_method(current_method):
    """Allow user to change solving method"""
    print(f"\n=== Change Solving Method (Current: {current_method}) ===")
    print("Available methods:")
    print("LBL - Layer-by-Layer (Beginner friendly)")
    print("CFOP - Cross, F2L, OLL, PLL (Advanced)")
    
    try:
        new_method = input("Enter desired method (LBL/CFOP): ").strip().upper()
        
        if new_method in ["LBL", "CFOP"]:
            print(f"✓ Changed solving method to {new_method}")
            return new_method
        else:
            print("Invalid method! Keeping current method.")
            return current_method
            
    except Exception as e:
        print(f"Error changing method: {e}")
        return current_method

def compare_cube_sizes():
    """Compare different cube sizes side by side"""
    print("\n=== Cube Size Comparison ===")
    
    sizes = [2, 3, 4, 5]
    cubes = {}
    
    print("Creating cubes of different sizes...")
    for size in sizes:
        try:
            cubes[size] = RubiksCube(size=size)
            print(f"✓ {size}x{size}x{size} cube created")
        except Exception as e:
            print(f"✗ Failed to create {size}x{size}x{size} cube: {e}")
    
    print("\nComparison Table:")
    print("Size | Stickers | Complexity | Status")
    print("-" * 40)
    
    for size in sizes:
        if size in cubes:
            stickers = 6 * size * size
            complexity = "Low" if size <= 2 else "Medium" if size <= 3 else "High" if size <= 4 else "Very High"
            status = "✓ Ready"
        else:
            stickers = "N/A"
            complexity = "N/A"
            status = "✗ Failed"
        
        print(f"{size}x{size}  | {str(stickers):>8} | {complexity:>10} | {status}")
    
    print("\nDemonstrating scrambles:")
    for size in sizes:
        if size in cubes:
            print(f"\n{size}x{size}x{size} cube after 5 moves:")
            cubes[size].scramble(5)
            viz = SimpleVisualizer(cubes[size])
            viz.draw_unfolded_cube()

def advanced_solver_statistics(cube, size, method):
    """Display advanced solver statistics and analysis"""
    print(f"\n=== Advanced Solver Statistics for {size}x{size}x{size} Cube ===")
    
    if cube.is_solved():
        print("Cube is already solved - no solving statistics available.")
        return
    
    print("Creating solver instance for analysis...")
    solver = RubiksCubeSolver(cube, method)
    
    print(f"\nCube Analysis:")
    print(f"  Size: {size}x{size}x{size}")
    print(f"  Total stickers: {6 * size * size}")
    print(f"  Current state: {'Solved' if cube.is_solved() else 'Scrambled'}")
    print(f"  Move history: {len(cube.move_history)} moves")
    
    if cube.move_history:
        print(f"  Recent moves: {' '.join(cube.move_history[-5:])}")
        
        # Analyze move patterns
        move_count = {}
        for move in cube.move_history:
            base_move = move[0] if move else 'U'
            move_count[base_move] = move_count.get(base_move, 0) + 1
        
        print(f"\nMove Pattern Analysis:")
        for move, count in sorted(move_count.items(), key=lambda x: x[1], reverse=True):
            print(f"  {move}: {count} times ({count/len(cube.move_history)*100:.1f}%)")
    
    print(f"\nSolver Capabilities:")
    print(f"  Method: {method}")
    print(f"  Supported sizes: 2x2, 3x3")
    print(f"  Algorithms: Layer-by-Layer, CFOP")
    print(f"  Features: Move tracking, efficiency scoring, state detection")
    
    # Estimate solving complexity
    complexity_factors = {
        2: {"pieces": 8, "complexity": "Low"},
        3: {"pieces": 26, "complexity": "Medium"},
        4: {"pieces": 56, "complexity": "High"},
        5: {"pieces": 98, "complexity": "Very High"}
    }
    
    if size in complexity_factors:
        factor = complexity_factors[size]
        print(f"\nComplexity Assessment:")
        print(f"  Total pieces: {factor['pieces']}")
        print(f"  Difficulty level: {factor['complexity']}")
        print(f"  Estimated solve time: {size * 2}-{size * 5} minutes")
    
    print(f"\nHackathon Features:")
    print(f"  ✓ Multi-size cube support")
    print(f"  ✓ Multiple solving methods")
    print(f"  ✓ Real-time visualization")
    print(f"  ✓ Move tracking and statistics")
    print(f"  ✓ Efficiency scoring")
    print(f"  ✓ State prediction logic")

def quick_test():
    """Quick functionality test for multi-size cubes"""
    print("=== Quick Multi-Size Cube Test ===")
    
    test_sizes = [2, 3, 4]
    
    for size in test_sizes:
        try:
            print(f"\nTesting {size}x{size}x{size} cube:")
            
            # Test cube creation
            cube = RubiksCube(size=size)
            print(f"  ✓ {size}x{size}x{size} cube created")
            
            # Test initial state
            assert cube.is_solved(), f"{size}x{size}x{size} cube should start solved"
            print(f"  ✓ Initial state is solved")
            
            # Test basic move
            cube.move_U()
            assert not cube.is_solved(), f"{size}x{size}x{size} cube should change after move"
            print(f"  ✓ Move execution works")
            
            # Test move history
            assert len(cube.move_history) == 1, f"{size}x{size}x{size} cube should track moves"
            print(f"  ✓ Move history tracking works")
            
            # Test reset
            cube.reset()
            assert cube.is_solved(), f"{size}x{size}x{size} cube should be solved after reset"
            print(f"  ✓ Reset functionality works")
            
            # Test visualizer
            viz = SimpleVisualizer(cube)
            print(f"  ✓ Visualizer created successfully for {size}x{size}x{size}")
            
        except Exception as e:
            print(f"  ✗ Error testing {size}x{size}x{size} cube: {e}")
            return False
    
    print("\n✓ All multi-size cube tests passed!")
    return True

if __name__ == "__main__":
    try:
        print("Starting Enhanced Rubik's Cube Solver - Hackathon Edition...")
        
        # Run quick test first
        test_passed = quick_test()
        
        if test_passed:
            input("\nPress Enter to launch main program...")
            # Launch main program
            main_menu()
        else:
            print("Tests failed. Please check your cube implementation.")
            
    except KeyboardInterrupt:
        print("\nProgram interrupted. Goodbye!")
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure all required files (rubiks_cube.py, solver.py, visualizer.py) are present.")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please check your installation and file structure.") 