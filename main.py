"""
Enhanced Main Interface for Rubik's Cube Solver - State-Driven Edition
Fully integrated with RubiksCube class and RubiksCubeSolver
Supports complete Layer-by-Layer solving with state tracking
"""

from rubiks_cube import RubiksCube, CubeStateTracker
from solver import RubiksCubeSolver
import time
import sys

def main_menu():
    """Display enhanced main menu with state-driven LBL support"""
    # Start with default 3x3 cube
    cube = RubiksCube(size=3)
    current_size = 3
    
    while True:
        print("\n" + "="*80)
        print(f" RUBIK'S CUBE SOLVER - STATE-DRIVEN EDITION")
        print(f" Current Cube: {current_size}x{current_size}x{current_size} | Solved: {cube.is_solved()}")
        print("="*80)
        print("1.  Display current cube state")
        print("2.  Execute manual moves")
        print("3.  Scramble cube")
        print("4.  Auto-solve cube (Layer-by-Layer)")
        print("5.  Reset cube to solved state")
        print("6.  Change cube size")
        print("7.  Cube size comparison")
        print("8.  State tracker diagnostics (3x3 only)")
        print("9.  Complete solving demo")
        print("10. Performance benchmark")
        print("11. Validate cube state")
        print("12. Clone cube")
        print("13. Move history analysis")
        print("14. Quick functionality test")
        print("15. Exit")
        print("="*80)
        
        # Display current cube info
        info = cube.get_cube_info()
        print(f"Cube Info: {info['total_stickers']} stickers | {info['total_pieces']} pieces | "
              f"{info['complexity']} difficulty | Moves: {info['move_count']}")
        
        if cube.tracker:
            print(f"State Tracker: Active | Validation: Available")
        else:
            print(f"State Tracker: Not available for {current_size}x{current_size}x{current_size}")
        print("="*80)
        
        try:
            choice = input("Enter your choice (1-15): ").strip()
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

        if choice == '1':
            display_cube_state(cube)
        elif choice == '2':
            manual_moves(cube)
        elif choice == '3':
            scramble_cube(cube)
        elif choice == '4':
            solve_cube_lbl(cube)
        elif choice == '5':
            reset_cube(cube)
        elif choice == '6':
            cube, current_size = change_cube_size(current_size)
        elif choice == '7':
            compare_cube_sizes()
        elif choice == '8':
            show_state_tracker_diagnostics(cube)
        elif choice == '9':
            complete_solving_demo(current_size)
        elif choice == '10':
            performance_benchmark(current_size)
        elif choice == '11':
            validate_cube_state(cube)
        elif choice == '12':
            clone_cube_demo(cube)
        elif choice == '13':
            analyze_move_history(cube)
        elif choice == '14':
            quick_functionality_test()
        elif choice == '15':
            print("Thank you for using the State-Driven Rubik's Cube Solver!")
            break
        else:
            print("Invalid choice! Please enter 1-15.")

def display_cube_state(cube):
    """Display comprehensive cube state information"""
    print(f"\n=== Current {cube.size}x{cube.size}x{cube.size} Cube State ===")
    
    # Display cube using both methods
    print("\n--- Detailed View ---")
    cube.display_cube()
    
    print("\n--- Compact View ---")
    cube.display_cube_compact()
    
    # Show cube information
    info = cube.get_cube_info()
    print(f"\nCube Information:")
    print(f"  Size: {info['size']}x{info['size']}x{info['size']}")
    print(f"  Total stickers: {info['total_stickers']}")
    print(f"  Total pieces: {info['total_pieces']}")
    print(f"  Complexity: {info['complexity']}")
    print(f"  Solved: {info['is_solved']}")
    print(f"  Move count: {info['move_count']}")
    print(f"  Has tracker: {info['has_tracker']}")
    
    # Show recent move history
    if cube.move_history:
        recent_moves = cube.move_history[-10:] if len(cube.move_history) > 10 else cube.move_history
        print(f"  Recent moves: {' '.join(recent_moves)}")
    else:
        print("  No moves executed yet")

def manual_moves(cube):
    """Enhanced manual move input with comprehensive move support"""
    print(f"\n=== Manual Move Input for {cube.size}x{cube.size}x{cube.size} Cube ===")
    print("Available moves:")
    print("  Basic: U, D, R, L, F, B")
    print("  Prime: U', D', R', L', F', B'")
    print("  Double: U2, D2, R2, L2, F2, B2")
    
    if cube.size >= 3:
        print("  Slice: M, E, S (for 3x3+)")
    
    print("\nExamples: 'U R F' D2', 'R U R' U R U2 R''")
    print("Type 'back' to return, 'reset' to reset cube, 'undo' to undo last sequence")
    
    last_state = None
    
    while True:
        moves_input = input(f"\nEnter moves for {cube.size}x{cube.size}x{cube.size}: ").strip()
        
        if moves_input.lower() == 'back':
            break
        elif moves_input.lower() == 'reset':
            cube.reset()
            print("✓ Cube reset to solved state")
            continue
        elif moves_input.lower() == 'undo' and last_state:
            cube.cube = last_state
            print("✓ Undid last move sequence")
            continue
        
        if moves_input:
            try:
                # Save state for undo
                last_state = cube.copy_cube()
                initial_solved = cube.is_solved()
                move_count_before = len(cube.move_history)
                
                # Execute moves
                cube.execute_moves(moves_input)
                
                # Show results
                moves_executed = len(cube.move_history) - move_count_before
                print(f"✓ Executed {moves_executed} moves: {moves_input}")
                
                if cube.is_solved() and not initial_solved:
                    print("🎉 Congratulations! Cube is now SOLVED!")
                elif not cube.is_solved() and initial_solved:
                    print("📝 Cube is now scrambled")
                
                # Show compact state
                cube.display_cube_compact()
                
            except Exception as e:
                print(f"❌ Error executing moves: {e}")
                # Restore previous state
                if last_state:
                    cube.cube = last_state

def scramble_cube(cube):
    """Enhanced scrambling with size-appropriate complexity"""
    size = cube.size
    
    # Recommended scramble lengths based on cube size
    scramble_recommendations = {
        2: {"min": 8, "default": 12, "max": 20},
        3: {"min": 15, "default": 20, "max": 30},
        4: {"min": 25, "default": 35, "max": 50},
        5: {"min": 35, "default": 45, "max": 60}
    }
    
    rec = scramble_recommendations.get(size, {"min": size*7, "default": size*10, "max": size*15})
    
    print(f"\n=== Scrambling {size}x{size}x{size} Cube ===")
    print(f"Recommended moves: {rec['min']}-{rec['max']} (default: {rec['default']})")
    
    try:
        num_input = input(f"Enter number of moves (default {rec['default']}): ").strip()
        num_moves = int(num_input) if num_input else rec['default']
        
        if num_moves < 1:
            print("Invalid number of moves!")
            return
            
    except ValueError:
        num_moves = rec['default']
    
    print(f"\nScrambling with {num_moves} moves...")
    
    # Save initial state
    was_solved = cube.is_solved()
    initial_move_count = len(cube.move_history)
    
    # Execute scramble
    cube.scramble(num_moves)
    
    # Show results
    actual_moves = len(cube.move_history) - initial_move_count
    print(f"✓ Applied {actual_moves} scramble moves")
    
    if was_solved:
        print("✓ Cube scrambled successfully!")
    
    # Display result
    cube.display_cube_compact()
    
    # Show complexity assessment
    if cube.tracker:
        diagnostics = cube.get_tracker_diagnostics()
        if diagnostics['has_tracker']:
            solved_pieces = diagnostics['solved_edges'] + diagnostics['solved_corners']
            total_pieces = 12 + 8  # edges + corners
            print(f"Scramble complexity: {((total_pieces - solved_pieces) / total_pieces * 100):.1f}% pieces displaced")

def solve_cube_lbl(cube):
    """Enhanced Layer-by-Layer solving with comprehensive feedback"""
    print(f"\n=== Layer-by-Layer Solver for {cube.size}x{cube.size}x{cube.size} Cube ===")
    
    # Check if cube is already solved
    if cube.is_solved():
        print("🎉 Cube is already solved!")
        return
    
    # Verify cube size compatibility
    if cube.size != 3:
        print(f"⚠️  Warning: Solver is optimized for 3x3 cubes.")
        print(f"   {cube.size}x{cube.size}x{cube.size} support is experimental and may not work correctly.")
        
        confirm = input("Continue anyway? (y/n): ").strip().lower()
        if confirm != 'y':
            return
    
    # Show initial state
    print("\n--- Initial Cube State ---")
    cube.display_cube_compact()
    
    if cube.tracker:
        diagnostics = cube.get_tracker_diagnostics()
        print(f"Pre-solve diagnostics:")
        print(f"  Solved edges: {diagnostics['solved_edges']}/12")
        print(f"  Solved corners: {diagnostics['solved_corners']}/8")
        print(f"  State validation: {diagnostics['validation_status']['message']}")
    
    # Initialize solver
    try:
        print("\n--- Initializing State-Driven Solver ---")
        solver = RubiksCubeSolver(cube)
        print("✓ Solver initialized with state tracking")
        
    except ValueError as e:
        print(f"❌ Solver initialization failed: {e}")
        return
    except Exception as e:
        print(f"❌ Unexpected error during solver setup: {e}")
        return
    
    # Record initial state
    initial_move_count = len(cube.move_history)
    start_time = time.time()
    
    # Execute solve
    print("\n--- Starting Layer-by-Layer Solution ---")
    try:
        solution = solver.solve()
        solve_time = time.time() - start_time
        
        print(f"\n--- Solving Completed in {solve_time:.2f} seconds ---")
        
    except Exception as e:
        print(f"❌ Error during solving: {e}")
        return
    
    # Show final state
    print("\n--- Final Cube State ---")
    cube.display_cube_compact()
    
    # Display comprehensive statistics
    stats = solver.get_solving_statistics()
    print(f"\n--- Solving Statistics ---")
    print(f"✓ Solution found: {stats['is_solved']}")
    print(f"✓ Total solution moves: {stats['total_moves']}")
    print(f"✓ Solving time: {solve_time:.2f} seconds")
    print(f"✓ Moves per second: {stats['total_moves']/solve_time:.1f}")
    print(f"✓ Efficiency score: {stats['efficiency_score']}")
    
    if stats['total_moves'] > 0:
        print(f"\nSolution sequence:")
        # Display solution in chunks of 20 moves
        moves = stats['solution_sequence'].split()
        for i in range(0, len(moves), 20):
            chunk = ' '.join(moves[i:i+20])
            print(f"  {chunk}")
    
    # Show tracker information if available
    if 'tracker_info' in stats and stats['tracker_info'].get('valid', False):
        tracker = stats['tracker_info']
        print(f"\nState Tracker Results:")
        print(f"  Tracker solved: {tracker['is_solved']}")
        print(f"  Final solved edges: {tracker['solved_edges']}/12")
        print(f"  Final solved corners: {tracker['solved_corners']}/8")
    
    # Performance assessment
    if stats['total_moves'] <= 30:
        performance = "Excellent"
    elif stats['total_moves'] <= 50:
        performance = "Good"
    elif stats['total_moves'] <= 80:
        performance = "Average"
    else:
        performance = "Needs Improvement"
    
    print(f"\nPerformance Assessment: {performance}")
    
    if stats['is_solved']:
        print("🎉 SUCCESS: Cube solved using Layer-by-Layer method!")
    else:
        print("❌ FAILURE: Cube not completely solved. This may indicate a bug.")

def reset_cube(cube):
    """Reset cube with confirmation"""
    if not cube.is_solved():
        confirm = input(f"Reset {cube.size}x{cube.size}x{cube.size} cube to solved state? (y/n): ").strip().lower()
        if confirm != 'y':
            return
    
    move_count = len(cube.move_history)
    cube.reset()
    
    print(f"✓ {cube.size}x{cube.size}x{cube.size} cube reset to solved state!")
    if move_count > 0:
        print(f"✓ Cleared {move_count} moves from history")
    
    cube.display_cube_compact()

def change_cube_size(current_size):
    """Enhanced cube size changing with detailed information"""
    print(f"\n=== Change Cube Size (Current: {current_size}x{current_size}x{current_size}) ===")
    
    size_info = {
        2: {"name": "Pocket Cube", "difficulty": "Beginner", "pieces": 8, "note": "Corner-only cube"},
        3: {"name": "Standard Cube", "difficulty": "Intermediate", "pieces": 26, "note": "Full state tracking"},
        4: {"name": "Rubik's Revenge", "difficulty": "Advanced", "pieces": 56, "note": "Parity challenges"},
        5: {"name": "Professor's Cube", "difficulty": "Expert", "pieces": 98, "note": "Complex centers"},
        6: {"name": "V-Cube 6", "difficulty": "Master", "pieces": 152, "note": "Large cube"},
        7: {"name": "V-Cube 7", "difficulty": "Master", "pieces": 218, "note": "Very large cube"}
    }
    
    print("Available cube sizes:")
    for size, info in size_info.items():
        current_marker = " ← CURRENT" if size == current_size else ""
        tracker_info = " (with state tracker)" if size == 3 else ""
        print(f"  {size}. {size}x{size}x{size} - {info['name']}{tracker_info}")
        print(f"     {info['difficulty']} | {info['pieces']} pieces | {info['note']}{current_marker}")
    
    try:
        new_size = int(input(f"\nEnter desired cube size (2-7): ").strip())
        
        if new_size < 2:
            print("❌ Minimum cube size is 2x2x2")
            return RubiksCube(size=current_size), current_size
        elif new_size > 7:
            print("⚠️  Warning: Very large cubes may be slow")
        
        if new_size == current_size:
            print(f"✓ Already using {current_size}x{current_size}x{current_size} cube")
            return RubiksCube(size=current_size), current_size
        
        print(f"\nCreating {new_size}x{new_size}x{new_size} cube...")
        
        new_cube = RubiksCube(size=new_size)
        
        info = new_cube.get_cube_info()
        complexity_change = info['total_stickers'] / (6 * current_size * current_size)
        
        print(f"✅ Successfully created {new_size}x{new_size}x{new_size} cube!")
        print(f"   Total stickers: {info['total_stickers']}")
        print(f"   Total pieces: {info['total_pieces']}")
        print(f"   Difficulty: {info['complexity']}")
        print(f"   Complexity change: {complexity_change:.1f}x")
        print(f"   State tracker: {'Available' if info['has_tracker'] else 'Not available'}")
        
        new_cube.display_cube_compact()
        return new_cube, new_size
        
    except ValueError:
        print("❌ Invalid input! Keeping current cube size.")
        return RubiksCube(size=current_size), current_size
    except Exception as e:
        print(f"❌ Error creating cube: {e}")
        return RubiksCube(size=current_size), current_size

def compare_cube_sizes():
    """Enhanced cube size comparison with detailed analysis"""
    print("\n=== Multi-Size Cube Comparison ===")
    
    sizes = [2, 3, 4, 5]
    cubes = {}
    
    print("Creating cubes of different sizes...")
    for size in sizes:
        try:
            cubes[size] = RubiksCube(size=size)
            print(f"✅ {size}x{size}x{size} cube created successfully")
        except Exception as e:
            print(f"❌ Failed to create {size}x{size}x{size} cube: {e}")
    
    # Comparison table
    print(f"\n{'Size':<6} {'Stickers':<10} {'Pieces':<8} {'Complexity':<12} {'Tracker':<8} {'Status':<8}")
    print("-" * 60)
    
    for size in sizes:
        if size in cubes:
            info = cubes[size].get_cube_info()
            stickers = info['total_stickers']
            pieces = info['total_pieces']
            complexity = info['complexity']
            tracker = "Yes" if info['has_tracker'] else "No"
            status = "✅ Ready"
        else:
            stickers = pieces = complexity = tracker = "N/A"
            status = "❌ Failed"
        
        print(f"{size}x{size}x{size:<1} {str(stickers):<10} {str(pieces):<8} {complexity:<12} {tracker:<8} {status}")
    
    # Demonstration with scrambles
    print(f"\nDemonstrating scrambled states (5 moves each):")
    for size in sizes:
        if size in cubes:
            print(f"\n{size}x{size}x{size} cube after scrambling:")
            cubes[size].scramble(5)
            cubes[size].display_cube_compact()
            
            if cubes[size].tracker:
                diagnostics = cubes[size].get_tracker_diagnostics()
                solved_total = diagnostics['solved_edges'] + diagnostics['solved_corners']
                print(f"  Pieces still solved: {solved_total}/20 ({solved_total/20*100:.1f}%)")

def show_state_tracker_diagnostics(cube):
    """Show comprehensive state tracker diagnostics"""
    print(f"\n=== State Tracker Diagnostics for {cube.size}x{cube.size}x{cube.size} Cube ===")
    
    if not cube.tracker:
        print("❌ State tracker not available for this cube size")
        print("   State tracking is only available for 3x3x3 cubes")
        return
    
    try:
        diagnostics = cube.get_tracker_diagnostics()
        
        print("--- Tracker Status ---")
        print(f"✅ State tracker: {'Active' if diagnostics['has_tracker'] else 'Inactive'}")
        print(f"✅ Validation: {diagnostics['validation_status']['message']}")
        
        print("\n--- Piece Analysis ---")
        print(f"Solved edges: {diagnostics['solved_edges']}/12 ({diagnostics['solved_edges']/12*100:.1f}%)")
        print(f"Solved corners: {diagnostics['solved_corners']}/8 ({diagnostics['solved_corners']/8*100:.1f}%)")
        print(f"Total solved pieces: {diagnostics['solved_edges'] + diagnostics['solved_corners']}/20")
        
        print(f"\n--- Overall Status ---")
        print(f"Cube solved (visual): {cube.is_solved()}")
        print(f"Cube solved (tracker): {diagnostics['tracker_solved']}")
        
        if cube.is_solved() != diagnostics['tracker_solved']:
            print("⚠️  Warning: Visual and tracker states don't match!")
        
        print(f"\n--- Edge Details ---")
        print(f"Edge positions: {diagnostics['edge_positions']}")
        print(f"Edge orientations: {diagnostics['edge_orientations']}")
        
        print(f"\n--- Corner Details ---")
        print(f"Corner positions: {diagnostics['corner_positions']}")
        print(f"Corner orientations: {diagnostics['corner_orientations']}")
        
    except Exception as e:
        print(f"❌ Error getting diagnostics: {e}")

def complete_solving_demo(size):
    """Complete demonstration of the solving process"""
    print(f"\n=== Complete {size}x{size}x{size} Solving Demo ===")
    
    # Create demo cube
    demo_cube = RubiksCube(size=size)
    
    print(f"1. Starting with solved {size}x{size}x{size} cube:")
    demo_cube.display_cube_compact()
    input("Press Enter to continue...")
    
    # Scramble
    scramble_moves = {2: 10, 3: 20, 4: 30, 5: 40}.get(size, size * 8)
    print(f"\n2. Scrambling with {scramble_moves} moves...")
    demo_cube.scramble(scramble_moves)
    demo_cube.display_cube_compact()
    
    if demo_cube.tracker:
        diagnostics = demo_cube.get_tracker_diagnostics()
        print(f"Scramble analysis: {diagnostics['solved_edges'] + diagnostics['solved_corners']}/20 pieces solved")
    
    input("Press Enter to start solving...")
    
    # Solve
    if size == 3:
        print(f"\n3. Solving {size}x{size}x{size} cube using Layer-by-Layer method...")
        
        try:
            solver = RubiksCubeSolver(demo_cube)
            start_time = time.time()
            solution = solver.solve()
            solve_time = time.time() - start_time
            
            print(f"\n4. Solution completed in {solve_time:.2f} seconds!")
            demo_cube.display_cube_compact()
            
            # Statistics
            stats = solver.get_solving_statistics()
            print(f"\nDemo Results:")
            print(f"✅ Successfully solved: {stats['is_solved']}")
            print(f"📊 Total moves used: {stats['total_moves']}")
            print(f"⏱️  Solving time: {solve_time:.2f} seconds")
            print(f"🏆 Efficiency score: {stats['efficiency_score']}")
            
        except Exception as e:
            print(f"❌ Solving failed: {e}")
    else:
        print(f"⚠️  Automatic solving not available for {size}x{size}x{size} cubes")
        print("   Only 3x3x3 cubes are supported by the current solver")

def performance_benchmark(size):
    """Run performance benchmark"""
    print(f"\n=== Performance Benchmark for {size}x{size}x{size} Cubes ===")
    
    if size != 3:
        print("❌ Performance benchmark only available for 3x3x3 cubes")
        return
    
    num_tests = 5
    print(f"Running {num_tests} solve tests...")
    
    results = []
    
    for i in range(num_tests):
        print(f"\nTest {i+1}/{num_tests}:")
        
        # Create and scramble cube
        test_cube = RubiksCube(size=3)
        test_cube.scramble(20)
        
        # Solve and measure
        solver = RubiksCubeSolver(test_cube)
        start_time = time.time()
        
        try:
            solution = solver.solve()
            solve_time = time.time() - start_time
            stats = solver.get_solving_statistics()
            
            result = {
                'test_num': i+1,
                'solved': stats['is_solved'],
                'moves': stats['total_moves'],
                'time': solve_time,
                'moves_per_sec': stats['total_moves'] / solve_time if solve_time > 0 else 0
            }
            results.append(result)
            
            print(f"  Result: {'✅ SOLVED' if result['solved'] else '❌ FAILED'} | "
                  f"Moves: {result['moves']} | Time: {result['time']:.2f}s")
            
        except Exception as e:
            print(f"  Result: ❌ ERROR - {e}")
            results.append({
                'test_num': i+1, 'solved': False, 'moves': 0, 
                'time': 0, 'moves_per_sec': 0
            })
    
    # Calculate statistics
    successful_tests = [r for r in results if r['solved']]
    
    if successful_tests:
        avg_moves = sum(r['moves'] for r in successful_tests) / len(successful_tests)
        avg_time = sum(r['time'] for r in successful_tests) / len(successful_tests)
        avg_speed = sum(r['moves_per_sec'] for r in successful_tests) / len(successful_tests)
        
        print(f"\n=== Benchmark Results ===")
        print(f"Successful solves: {len(successful_tests)}/{num_tests} ({len(successful_tests)/num_tests*100:.1f}%)")
        print(f"Average moves: {avg_moves:.1f}")
        print(f"Average time: {avg_time:.2f} seconds")
        print(f"Average speed: {avg_speed:.1f} moves/second")
        
        if len(successful_tests) == num_tests:
            print("🏆 Perfect performance! All tests passed.")
        elif len(successful_tests) >= num_tests * 0.8:
            print("👍 Good performance!")
        else:
            print("⚠️  Performance needs improvement.")
    else:
        print("❌ No successful solves in benchmark.")

def validate_cube_state(cube):
    """Validate cube state using multiple methods"""
    print(f"\n=== State Validation for {cube.size}x{cube.size}x{cube.size} Cube ===")
    
    # Basic validation
    print("--- Basic Validation ---")
    print(f"✅ Cube object valid: {isinstance(cube, RubiksCube)}")
    print(f"✅ Size consistency: {cube.size}x{cube.size}x{cube.size}")
    print(f"✅ Visual solved state: {cube.is_solved()}")
    
    # Tracker validation (for 3x3)
    if cube.tracker:
        print("\n--- State Tracker Validation ---")
        validation = cube.validate_cube_state()
        print(f"✅ Tracker validation: {validation['message']}")
        
        if validation['valid']:
            print("✅ All state tracker checks passed")
            
            diagnostics = cube.get_tracker_diagnostics()
            print(f"✅ Tracker solved state: {diagnostics['tracker_solved']}")
            
            # Check consistency
            if cube.is_solved() == diagnostics['tracker_solved']:
                print("✅ Visual and tracker states are consistent")
            else:
                print("⚠️  Warning: Visual and tracker states differ")
        else:
            print(f"❌ State tracker validation failed: {validation['message']}")
    else:
        print(f"--- No state tracker available for {cube.size}x{cube.size}x{cube.size} cubes ---")
    
    # Color count validation
    print("\n--- Color Distribution Validation ---")
    color_counts = {}
    total_stickers = 0
    
    for face in cube.cube:
        for row in face:
            for sticker in row:
                color_counts[sticker] = color_counts.get(sticker, 0) + 1
                total_stickers += 1
    
    expected_per_color = cube.size * cube.size
    expected_total = 6 * expected_per_color
    
    print(f"Expected stickers per color: {expected_per_color}")
    print(f"Expected total stickers: {expected_total}")
    print(f"Actual total stickers: {total_stickers}")
    
    valid_colors = True
    for color, count in color_counts.items():
        status = "✅" if count == expected_per_color else "❌"
        print(f"{status} Color {color}: {count}/{expected_per_color}")
        if count != expected_per_color:
            valid_colors = False
    
    if valid_colors and total_stickers == expected_total:
        print("✅ Color distribution is valid")
    else:
        print("❌ Color distribution is invalid")

def clone_cube_demo(cube):
    """Demonstrate cube cloning functionality"""
    print(f"\n=== Cube Cloning Demo for {cube.size}x{cube.size}x{cube.size} ===")
    
    # Show original cube
    print("Original cube state:")
    cube.display_cube_compact()
    original_moves = len(cube.move_history)
    print(f"Original move count: {original_moves}")
    
    # Clone the cube
    print("\nCreating clone...")
    cloned_cube = cube.clone()
    
    print("✅ Clone created successfully")
    print("Clone state:")
    cloned_cube.display_cube_compact()
    print(f"Clone move count: {len(cloned_cube.move_history)}")
    
    # Verify independence
    print("\nTesting clone independence...")
    print("Applying U move to original cube...")
    cube.move_U()
    
    print("\nAfter U move:")
    print("Original cube:")
    cube.display_cube_compact()
    print("Clone cube (should be unchanged):")
    cloned_cube.display_cube_compact()
    
    # Compare states
    states_match = cube.get_state_string() == cloned_cube.get_state_string()
    print(f"\nStates identical: {not states_match} ({'as expected' if not states_match else 'ERROR!'})")
    
    if not states_match:
        print("✅ Clone independence verified")
    else:
        print("❌ Clone independence failed")
    
    # Undo the U move
    cube.move_U()
    cube.move_U()
    cube.move_U()  # U' = U U U

def analyze_move_history(cube):
    """Analyze move history and patterns"""
    print(f"\n=== Move History Analysis for {cube.size}x{cube.size}x{cube.size} Cube ===")
    
    if not cube.move_history:
        print("❌ No move history available")
        return
    
    history = cube.move_history
    print(f"Total moves executed: {len(history)}")
    
    # Move frequency analysis
    move_counts = {}
    for move in history:
        base_move = move[0] if move else 'U'
        move_counts[base_move] = move_counts.get(base_move, 0) + 1
    
    print(f"\n--- Move Frequency Analysis ---")
    for move, count in sorted(move_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = count / len(history) * 100
        print(f"{move}: {count} times ({percentage:.1f}%)")
    
    # Recent moves
    print(f"\n--- Recent Move History ---")
    recent_count = min(20, len(history))
    recent_moves = history[-recent_count:]
    print(f"Last {recent_count} moves: {' '.join(recent_moves)}")
    
    # Pattern detection
    print(f"\n--- Pattern Analysis ---")
    
    # Check for repeated sequences
    if len(history) >= 4:
        sequences = {}
        for i in range(len(history) - 3):
            seq = ' '.join(history[i:i+4])
            sequences[seq] = sequences.get(seq, 0) + 1
        
        repeated_sequences = {k: v for k, v in sequences.items() if v > 1}
        if repeated_sequences:
            print("Repeated 4-move sequences:")
            for seq, count in sorted(repeated_sequences.items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"  '{seq}': {count} times")
        else:
            print("No repeated 4-move sequences found")
    
    # Efficiency assessment
    redundant_moves = 0
    for i in range(len(history) - 1):
        current_move = history[i]
        next_move = history[i + 1]
        
        # Check for immediate cancellation (U followed by U')
        if len(current_move) == 1 and next_move == current_move + "'":
            redundant_moves += 2
        elif current_move.endswith("'") and next_move == current_move[0]:
            redundant_moves += 2
    
    efficiency = max(0, 100 - (redundant_moves / len(history) * 100))
    print(f"\nMove efficiency: {efficiency:.1f}% ({redundant_moves} redundant moves detected)")

def quick_functionality_test():
    """Quick test of all cube functionalities"""
    print("\n=== Quick Functionality Test ===")
    
    test_sizes = [2, 3, 4]
    all_passed = True
    
    for size in test_sizes:
        print(f"\nTesting {size}x{size}x{size} cube:")
        
        try:
            # Test 1: Creation
            cube = RubiksCube(size=size)
            print(f"  ✅ Cube creation")
            
            # Test 2: Initial solved state
            if not cube.is_solved():
                print(f"  ❌ Initial solved state")
                all_passed = False
                continue
            print(f"  ✅ Initial solved state")
            
            # Test 3: Move execution
            cube.move_U()
            if cube.is_solved():
                print(f"  ❌ Move execution (cube still solved after U)")
                all_passed = False
                continue
            print(f"  ✅ Move execution")
            
            # Test 4: Move history
            if len(cube.move_history) != 1 or cube.move_history[0] != 'U':
                print(f"  ❌ Move history tracking")
                all_passed = False
                continue
            print(f"  ✅ Move history tracking")
            
            # Test 5: Reset
            cube.reset()
            if not cube.is_solved() or len(cube.move_history) != 0:
                print(f"  ❌ Reset functionality")
                all_passed = False
                continue
            print(f"  ✅ Reset functionality")
            
            # Test 6: Cloning
            clone = cube.clone()
            clone.move_R()
            if not cube.is_solved() or clone.is_solved():
                print(f"  ❌ Cloning independence")
                all_passed = False
                continue
            print(f"  ✅ Cloning independence")
            
            # Test 7: State tracker (3x3 only)
            if size == 3:
                if not cube.tracker:
                    print(f"  ❌ State tracker initialization")
                    all_passed = False
                    continue
                print(f"  ✅ State tracker initialization")
                
                # Test tracker diagnostics
                diagnostics = cube.get_tracker_diagnostics()
                if not diagnostics['has_tracker']:
                    print(f"  ❌ State tracker diagnostics")
                    all_passed = False
                    continue
                print(f"  ✅ State tracker diagnostics")
            
            # Test 8: Scramble and solve (3x3 only)
            if size == 3:
                cube.scramble(10)
                solver = RubiksCubeSolver(cube)
                solution = solver.solve()
                
                if not cube.is_solved():
                    print(f"  ❌ Solver functionality")
                    all_passed = False
                    continue
                print(f"  ✅ Solver functionality")
            
            print(f"  🎉 All tests passed for {size}x{size}x{size}")
            
        except Exception as e:
            print(f"  ❌ Exception during testing: {e}")
            all_passed = False
    
    print(f"\n=== Test Summary ===")
    if all_passed:
        print("🏆 ALL FUNCTIONALITY TESTS PASSED!")
        print("✅ Multi-size cube support working correctly")
        print("✅ State tracking and solving working correctly")
    else:
        print("❌ Some functionality tests failed")
        print("⚠️  Please check the implementation")

if __name__ == "__main__":
    try:
        print("=== State-Driven Rubik's Cube Solver ===")
        print("Enhanced with precise piece tracking and LBL solving")
        print("Supports 2x2, 3x3, 4x4+ cubes with full state analysis")
        
        # Run quick test first
        print("\nRunning startup diagnostics...")
        quick_functionality_test()
        
        input("\nPress Enter to launch main program...")
        main_menu()
        
    except KeyboardInterrupt:
        print("\nProgram interrupted. Goodbye!")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please ensure all required files are present:")
        print("  - rubiks_cube.py")
        print("  - solver.py")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
