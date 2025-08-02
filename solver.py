"""
State-Driven Rubik's Cube Solver Implementation
True Layer-by-Layer (LBL) method with precise state analysis
Uses RubiksCube and CubeStateTracker for accurate piece tracking
"""

from rubiks_cube import RubiksCube, CubeStateTracker
import copy

class RubiksCubeSolver:
    """State-driven Rubik's Cube Solver with precise LBL implementation"""
    
    def __init__(self, cube):
        """Initialize solver with a 3x3 RubiksCube instance"""
        if not isinstance(cube, RubiksCube):
            raise ValueError("Solver requires RubiksCube instance")
        if cube.size != 3:
            raise ValueError("This solver is designed for 3x3 cubes only")
        
        self.cube = cube
        self.solution_moves = []
        
        # Ensure tracker exists
        if not hasattr(self.cube, 'tracker') or not self.cube.tracker:
            self.cube.tracker = CubeStateTracker()
        self.tracker = self.cube.tracker
        
        # Define color mappings (cube internal representation)
        # 0=WHITE, 1=YELLOW, 2=RED, 3=ORANGE, 4=GREEN, 5=BLUE
        self.WHITE = 0
        self.YELLOW = 1
        self.RED = 2
        self.ORANGE = 3
        self.GREEN = 4
        self.BLUE = 5
        
        # Face indices: FRONT=0, BACK=1, RIGHT=2, LEFT=3, UP=4, DOWN=5
        self.FRONT, self.BACK, self.RIGHT, self.LEFT, self.UP, self.DOWN = 0, 1, 2, 3, 4, 5
    
    def solve(self):
        """Main solving function using state-driven LBL method"""
        print("=== STARTING STATE-DRIVEN 3x3 LBL SOLVE ===")
        self.solution_moves = []
        
        if self.cube.is_solved():
            print("Cube is already solved!")
            return self.solution_moves
        
        # Phase 1: White Cross on Down face
        print("\nPhase 1: Solving White Cross")
        self._solve_white_cross()
        
        # Phase 2: White Corners (First Layer)
        print("\nPhase 2: Solving White Corners")
        self._solve_white_corners()
        
        # Phase 3: Middle Layer Edges
        print("\nPhase 3: Solving Middle Layer")
        self._solve_middle_layer()
        
        # Phase 4: Yellow Cross on Up face
        print("\nPhase 4: Solving Yellow Cross")
        self._solve_yellow_cross()
        
        # Phase 5: Yellow Corner Orientation
        print("\nPhase 5: Orienting Yellow Corners")
        self._orient_yellow_corners()
        
        # Phase 6: Last Layer Permutation
        print("\nPhase 6: Permuting Last Layer")
        self._permute_last_layer()
        
        print(f"\n3x3 LBL solve completed with {len(self.solution_moves)} moves!")
        print(f"Final state: {'SOLVED' if self.cube.is_solved() else 'NOT SOLVED'}")
        return self.solution_moves
    
    # ============ PHASE 1: WHITE CROSS ============
    
    def _solve_white_cross(self):
        """Solve white cross on down face using state analysis"""
        white_edge_positions = [
            (self.DOWN, 0, 1),  # Down-Front edge
            (self.DOWN, 1, 2),  # Down-Right edge  
            (self.DOWN, 2, 1),  # Down-Back edge
            (self.DOWN, 1, 0),  # Down-Left edge
        ]
        
        adjacent_centers = [self.FRONT, self.RIGHT, self.BACK, self.LEFT]
        
        for i, (face, row, col) in enumerate(white_edge_positions):
            target_center = adjacent_centers[i]
            
            if self._is_white_edge_solved(i):
                print(f"  ✓ White edge {i} already solved")
                continue
            
            print(f"  → Solving white edge {i}")
            
            # Find the white edge piece that belongs in this position
            edge_location = self._find_white_edge_for_position(i)
            if edge_location:
                self._move_white_edge_to_position(edge_location, i)
            
            # Verify the edge is now correctly placed
            if self._is_white_edge_solved(i):
                print(f"  ✓ White edge {i} solved successfully")
            else:
                print(f"  ⚠ White edge {i} needs additional work")
    
    def _is_white_edge_solved(self, edge_index):
        """Check if a specific white edge is correctly solved"""
        edge_positions = [
            ((self.DOWN, 0, 1), (self.FRONT, 2, 1)),  # Down-Front
            ((self.DOWN, 1, 2), (self.RIGHT, 2, 1)),  # Down-Right
            ((self.DOWN, 2, 1), (self.BACK, 2, 1)),   # Down-Back
            ((self.DOWN, 1, 0), (self.LEFT, 2, 1)),   # Down-Left
        ]
        
        expected_colors = [
            (self.WHITE, self.GREEN),   # White-Green edge
            (self.WHITE, self.RED),     # White-Red edge
            (self.WHITE, self.BLUE),    # White-Blue edge
            (self.WHITE, self.ORANGE),  # White-Orange edge
        ]
        
        (pos1, pos2) = edge_positions[edge_index]
        (color1, color2) = expected_colors[edge_index]
        
        actual_color1 = self.cube.cube[pos1[0]][pos1[1]][pos1[2]]
        actual_color2 = self.cube.cube[pos2[0]][pos2[1]][pos2[2]]
        
        return actual_color1 == color1 and actual_color2 == color2
    
    def _find_white_edge_for_position(self, target_position):
        """Find a white edge piece that belongs in the target position"""
        target_colors = [
            (self.WHITE, self.GREEN),   # Position 0: White-Green
            (self.WHITE, self.RED),     # Position 1: White-Red  
            (self.WHITE, self.BLUE),    # Position 2: White-Blue
            (self.WHITE, self.ORANGE),  # Position 3: White-Orange
        ]
        
        target_set = set(target_colors[target_position])
        
        # Search all edge positions for the target piece
        edge_locations = [
            # Top layer edges
            ((self.UP, 0, 1), (self.BACK, 0, 1)),
            ((self.UP, 1, 2), (self.RIGHT, 0, 1)),
            ((self.UP, 2, 1), (self.FRONT, 0, 1)),
            ((self.UP, 1, 0), (self.LEFT, 0, 1)),
            # Bottom layer edges
            ((self.DOWN, 0, 1), (self.FRONT, 2, 1)),
            ((self.DOWN, 1, 2), (self.RIGHT, 2, 1)),
            ((self.DOWN, 2, 1), (self.BACK, 2, 1)),
            ((self.DOWN, 1, 0), (self.LEFT, 2, 1)),
            # Middle layer edges
            ((self.FRONT, 1, 0), (self.LEFT, 1, 2)),
            ((self.FRONT, 1, 2), (self.RIGHT, 1, 0)),
            ((self.BACK, 1, 0), (self.RIGHT, 1, 2)),
            ((self.BACK, 1, 2), (self.LEFT, 1, 0)),
        ]
        
        for location in edge_locations:
            pos1, pos2 = location
            color1 = self.cube.cube[pos1[0]][pos1[1]][pos1[2]]
            color2 = self.cube.cube[pos2[0]][pos2[1]][pos2[2]]
            
            if set([color1, color2]) == target_set:
                return location
        
        return None
    
    def _move_white_edge_to_position(self, current_location, target_position):
        """Move a white edge from current location to target position"""
        pos1, pos2 = current_location
        color1 = self.cube.cube[pos1[0]][pos1[1]][pos1[2]]
        
        # If edge is in top layer, position it above target and insert
        if pos1[0] == self.UP:  # Edge is in top layer
            # Rotate top layer to position edge above target
            face_map = {0: 2, 1: 1, 2: 0, 3: 3}  # Map top positions to rotations needed
            current_top_pos = self._get_top_edge_position(pos1)
            rotations_needed = (target_position - current_top_pos) % 4
            
            for _ in range(rotations_needed):
                self._execute_move("U")
            
            # Insert the edge using appropriate algorithm
            if target_position == 0:  # Front
                self._execute_algorithm("F2")
            elif target_position == 1:  # Right
                self._execute_algorithm("R2")
            elif target_position == 2:  # Back
                self._execute_algorithm("B2")
            elif target_position == 3:  # Left
                self._execute_algorithm("L2")
        
        # If edge is in bottom layer but wrong position
        elif pos1[0] == self.DOWN:
            # Move to top layer first
            current_bottom_pos = self._get_bottom_edge_position(pos1)
            if current_bottom_pos == 0:  # Front
                self._execute_algorithm("F2")
            elif current_bottom_pos == 1:  # Right
                self._execute_algorithm("R2")
            elif current_bottom_pos == 2:  # Back
                self._execute_algorithm("B2")
            elif current_bottom_pos == 3:  # Left
                self._execute_algorithm("L2")
            
            # Now it's in top layer, recursively solve
            new_location = self._find_white_edge_for_position(target_position)
            if new_location:
                self._move_white_edge_to_position(new_location, target_position)
        
        # If edge is in middle layer
        else:
            # Extract to top layer using right-hand algorithm
            if pos1[0] == self.FRONT and pos1[2] == 2:  # Front-right
                self._execute_algorithm("R U R' U' F' U F")
            elif pos1[0] == self.FRONT and pos1[2] == 0:  # Front-left
                self._execute_algorithm("L' U' L U F U' F'")
            elif pos1[0] == self.RIGHT and pos1[2] == 2:  # Right-back
                self._execute_algorithm("B U B' U' R' U R")
            elif pos1[0] == self.BACK and pos1[2] == 0:  # Back-left
                self._execute_algorithm("L U L' U' B' U B")
            
            # Now it's in top layer, recursively solve
            new_location = self._find_white_edge_for_position(target_position)
            if new_location:
                self._move_white_edge_to_position(new_location, target_position)
    
    def _get_top_edge_position(self, pos):
        """Get the position index (0-3) of an edge in the top layer"""
        if pos == (self.UP, 2, 1):  # Up-Front
            return 0
        elif pos == (self.UP, 1, 2):  # Up-Right
            return 1
        elif pos == (self.UP, 0, 1):  # Up-Back
            return 2
        elif pos == (self.UP, 1, 0):  # Up-Left
            return 3
        return 0
    
    def _get_bottom_edge_position(self, pos):
        """Get the position index (0-3) of an edge in the bottom layer"""
        if pos == (self.DOWN, 0, 1):  # Down-Front
            return 0
        elif pos == (self.DOWN, 1, 2):  # Down-Right
            return 1
        elif pos == (self.DOWN, 2, 1):  # Down-Back
            return 2
        elif pos == (self.DOWN, 1, 0):  # Down-Left
            return 3
        return 0
    
    # ============ PHASE 2: WHITE CORNERS ============
    
    def _solve_white_corners(self):
        """Solve white corners using state analysis"""
        corner_positions = [
            (self.DOWN, 0, 2),  # Down-Front-Right
            (self.DOWN, 0, 0),  # Down-Front-Left
            (self.DOWN, 2, 0),  # Down-Back-Left
            (self.DOWN, 2, 2),  # Down-Back-Right
        ]
        
        for i, corner_pos in enumerate(corner_positions):
            if self._is_white_corner_solved(i):
                print(f"  ✓ White corner {i} already solved")
                continue
            
            print(f"  → Solving white corner {i}")
            
            # Find the white corner piece that belongs in this position
            corner_location = self._find_white_corner_for_position(i)
            if corner_location:
                self._move_white_corner_to_position(corner_location, i)
            
            # Verify the corner is now correctly placed
            if self._is_white_corner_solved(i):
                print(f"  ✓ White corner {i} solved successfully")
            else:
                print(f"  ⚠ White corner {i} needs additional work")
    
    def _is_white_corner_solved(self, corner_index):
        """Check if a specific white corner is correctly solved"""
        corner_positions = [
            ((self.DOWN, 0, 2), (self.FRONT, 2, 2), (self.RIGHT, 2, 0)),  # DFR
            ((self.DOWN, 0, 0), (self.FRONT, 2, 0), (self.LEFT, 2, 2)),   # DFL
            ((self.DOWN, 2, 0), (self.BACK, 2, 2), (self.LEFT, 2, 0)),    # DBL
            ((self.DOWN, 2, 2), (self.BACK, 2, 0), (self.RIGHT, 2, 2)),   # DBR
        ]
        
        expected_colors = [
            (self.WHITE, self.GREEN, self.RED),     # White-Green-Red
            (self.WHITE, self.GREEN, self.ORANGE),  # White-Green-Orange
            (self.WHITE, self.BLUE, self.ORANGE),   # White-Blue-Orange
            (self.WHITE, self.BLUE, self.RED),      # White-Blue-Red
        ]
        
        positions = corner_positions[corner_index]
        expected = set(expected_colors[corner_index])
        
        actual_colors = set([
            self.cube.cube[positions[0][0]][positions[0][1]][positions[0][2]],
            self.cube.cube[positions[1][0]][positions[1][1]][positions[1][2]],
            self.cube.cube[positions[2][0]][positions[2][1]][positions[2][2]]
        ])
        
        # Check if colors match and white is on bottom
        return (actual_colors == expected and 
                self.cube.cube[positions[0][0]][positions[0][1]][positions[0][2]] == self.WHITE)
    
    def _find_white_corner_for_position(self, target_position):
        """Find a white corner piece that belongs in the target position"""
        target_colors = [
            set([self.WHITE, self.GREEN, self.RED]),     # Position 0
            set([self.WHITE, self.GREEN, self.ORANGE]),  # Position 1
            set([self.WHITE, self.BLUE, self.ORANGE]),   # Position 2
            set([self.WHITE, self.BLUE, self.RED]),      # Position 3
        ]
        
        target_set = target_colors[target_position]
        
        # Search all corner positions
        corner_locations = [
            # Top layer corners
            ((self.UP, 2, 2), (self.FRONT, 0, 2), (self.RIGHT, 0, 0)),  # UFR
            ((self.UP, 2, 0), (self.FRONT, 0, 0), (self.LEFT, 0, 2)),   # UFL
            ((self.UP, 0, 0), (self.BACK, 0, 2), (self.LEFT, 0, 0)),    # UBL
            ((self.UP, 0, 2), (self.BACK, 0, 0), (self.RIGHT, 0, 2)),   # UBR
            # Bottom layer corners
            ((self.DOWN, 0, 2), (self.FRONT, 2, 2), (self.RIGHT, 2, 0)),  # DFR
            ((self.DOWN, 0, 0), (self.FRONT, 2, 0), (self.LEFT, 2, 2)),   # DFL
            ((self.DOWN, 2, 0), (self.BACK, 2, 2), (self.LEFT, 2, 0)),    # DBL
            ((self.DOWN, 2, 2), (self.BACK, 2, 0), (self.RIGHT, 2, 2)),   # DBR
        ]
        
        for location in corner_locations:
            pos1, pos2, pos3 = location
            colors = set([
                self.cube.cube[pos1[0]][pos1[1]][pos1[2]],
                self.cube.cube[pos2[0]][pos2[1]][pos2[2]],
                self.cube.cube[pos3[0]][pos3[1]][pos3[2]]
            ])
            
            if colors == target_set:
                return location
        
        return None
    
    def _move_white_corner_to_position(self, current_location, target_position):
        """Move a white corner from current location to target position"""
        pos1, pos2, pos3 = current_location
        
        # If corner is in top layer, position it above target and insert
        if pos1[0] == self.UP:
            # Position corner above target slot
            current_top_pos = self._get_top_corner_position(pos1)
            rotations_needed = (target_position - current_top_pos) % 4
            
            for _ in range(rotations_needed):
                self._execute_move("U")
            
            # Insert corner using R'D'RD algorithm (for position 0)
            # Adapt for other positions
            if target_position == 0:  # Front-Right
                self._insert_corner_algorithm_FR()
            elif target_position == 1:  # Front-Left
                self._insert_corner_algorithm_FL()
            elif target_position == 2:  # Back-Left
                self._insert_corner_algorithm_BL()
            elif target_position == 3:  # Back-Right
                self._insert_corner_algorithm_BR()
        
        # If corner is in bottom layer but wrong position or orientation
        elif pos1[0] == self.DOWN:
            # Extract to top layer first
            current_bottom_pos = self._get_bottom_corner_position(pos1)
            
            if current_bottom_pos == 0:  # Front-Right
                self._execute_algorithm("R' D' R D")
            elif current_bottom_pos == 1:  # Front-Left
                self._execute_algorithm("L D L' D'")
            elif current_bottom_pos == 2:  # Back-Left
                self._execute_algorithm("L' D' L D")
            elif current_bottom_pos == 3:  # Back-Right
                self._execute_algorithm("R D R' D'")
            
            # Now it's in top layer, recursively solve
            new_location = self._find_white_corner_for_position(target_position)
            if new_location:
                self._move_white_corner_to_position(new_location, target_position)
    
    def _get_top_corner_position(self, pos):
        """Get the position index (0-3) of a corner in the top layer"""
        if pos == (self.UP, 2, 2):  # Up-Front-Right
            return 0
        elif pos == (self.UP, 2, 0):  # Up-Front-Left
            return 1
        elif pos == (self.UP, 0, 0):  # Up-Back-Left
            return 2
        elif pos == (self.UP, 0, 2):  # Up-Back-Right
            return 3
        return 0
    
    def _get_bottom_corner_position(self, pos):
        """Get the position index (0-3) of a corner in the bottom layer"""
        if pos == (self.DOWN, 0, 2):  # Down-Front-Right
            return 0
        elif pos == (self.DOWN, 0, 0):  # Down-Front-Left
            return 1
        elif pos == (self.DOWN, 2, 0):  # Down-Back-Left
            return 2
        elif pos == (self.DOWN, 2, 2):  # Down-Back-Right
            return 3
        return 0
    
    def _insert_corner_algorithm_FR(self):
        """Insert corner into Front-Right position with proper orientation"""
        # Check white orientation and apply appropriate algorithm
        white_pos = self._find_white_on_corner_above_FR()
        
        if white_pos == "right":  # White on right face
            self._execute_algorithm("R' D' R D")
        elif white_pos == "front":  # White on front face
            self._execute_algorithm("F D F' D' D' R' D' R")
        else:  # White on top face
            self._execute_algorithm("R' D2 R D R' D' R")
    
    def _insert_corner_algorithm_FL(self):
        """Insert corner into Front-Left position"""
        self._execute_algorithm("L D L' D'")
    
    def _insert_corner_algorithm_BL(self):
        """Insert corner into Back-Left position"""
        self._execute_algorithm("L' D' L D")
    
    def _insert_corner_algorithm_BR(self):
        """Insert corner into Back-Right position"""
        self._execute_algorithm("R D R' D'")
    
    def _find_white_on_corner_above_FR(self):
        """Find which face has the white sticker on the corner above FR position"""
        # Check UFR corner position
        if self.cube.cube[self.UP][2][2] == self.WHITE:
            return "top"
        elif self.cube.cube[self.FRONT][0][2] == self.WHITE:
            return "front"
        elif self.cube.cube[self.RIGHT][0][0] == self.WHITE:
            return "right"
        return "top"
    
    # ============ PHASE 3: MIDDLE LAYER ============
    
    def _solve_middle_layer(self):
        """Solve middle layer edges using state analysis"""
        middle_edge_positions = [
            ((self.FRONT, 1, 0), (self.LEFT, 1, 2)),   # Front-Left edge
            ((self.FRONT, 1, 2), (self.RIGHT, 1, 0)),  # Front-Right edge
            ((self.BACK, 1, 0), (self.RIGHT, 1, 2)),   # Back-Right edge
            ((self.BACK, 1, 2), (self.LEFT, 1, 0)),    # Back-Left edge
        ]
        
        for i, edge_pos in enumerate(middle_edge_positions):
            if self._is_middle_edge_solved(i):
                print(f"  ✓ Middle edge {i} already solved")
                continue
            
            print(f"  → Solving middle edge {i}")
            
            # Find the edge piece that belongs in this position
            edge_location = self._find_middle_edge_for_position(i)
            if edge_location:
                self._move_middle_edge_to_position(edge_location, i)
            
            # Verify the edge is now correctly placed
            if self._is_middle_edge_solved(i):
                print(f"  ✓ Middle edge {i} solved successfully")
            else:
                print(f"  ⚠ Middle edge {i} needs additional work")
    
    def _is_middle_edge_solved(self, edge_index):
        """Check if a specific middle layer edge is correctly solved"""
        edge_positions = [
            ((self.FRONT, 1, 0), (self.LEFT, 1, 2)),   # Front-Left
            ((self.FRONT, 1, 2), (self.RIGHT, 1, 0)),  # Front-Right
            ((self.BACK, 1, 0), (self.RIGHT, 1, 2)),   # Back-Right
            ((self.BACK, 1, 2), (self.LEFT, 1, 0)),    # Back-Left
        ]
        
        expected_colors = [
            (self.GREEN, self.ORANGE),  # Green-Orange edge
            (self.GREEN, self.RED),     # Green-Red edge
            (self.BLUE, self.RED),      # Blue-Red edge
            (self.BLUE, self.ORANGE),   # Blue-Orange edge
        ]
        
        pos1, pos2 = edge_positions[edge_index]
        color1, color2 = expected_colors[edge_index]
        
        actual_color1 = self.cube.cube[pos1[0]][pos1[1]][pos1[2]]
        actual_color2 = self.cube.cube[pos2[0]][pos2[1]][pos2[2]]
        
        return actual_color1 == color1 and actual_color2 == color2
    
    def _find_middle_edge_for_position(self, target_position):
        """Find a middle layer edge piece that belongs in the target position"""
        target_colors = [
            set([self.GREEN, self.ORANGE]),  # Position 0: Front-Left
            set([self.GREEN, self.RED]),     # Position 1: Front-Right
            set([self.BLUE, self.RED]),      # Position 2: Back-Right
            set([self.BLUE, self.ORANGE]),   # Position 3: Back-Left
        ]
        
        target_set = target_colors[target_position]
        
        # Search top layer edges (middle layer pieces shouldn't have white/yellow)
        top_edge_locations = [
            ((self.UP, 0, 1), (self.BACK, 0, 1)),   # Up-Back
            ((self.UP, 1, 2), (self.RIGHT, 0, 1)),  # Up-Right
            ((self.UP, 2, 1), (self.FRONT, 0, 1)),  # Up-Front
            ((self.UP, 1, 0), (self.LEFT, 0, 1)),   # Up-Left
        ]
        
        # Also search current middle layer positions
        middle_edge_locations = [
            ((self.FRONT, 1, 0), (self.LEFT, 1, 2)),   # Front-Left
            ((self.FRONT, 1, 2), (self.RIGHT, 1, 0)),  # Front-Right
            ((self.BACK, 1, 0), (self.RIGHT, 1, 2)),   # Back-Right
            ((self.BACK, 1, 2), (self.LEFT, 1, 0)),    # Back-Left
        ]
        
        all_locations = top_edge_locations + middle_edge_locations
        
        for location in all_locations:
            pos1, pos2 = location
            colors = set([
                self.cube.cube[pos1[0]][pos1[1]][pos1[2]],
                self.cube.cube[pos2[0]][pos2[1]][pos2[2]]
            ])
            
            # Make sure this edge doesn't contain white or yellow
            if self.WHITE not in colors and self.YELLOW not in colors and colors == target_set:
                return location
        
        return None
    
    def _move_middle_edge_to_position(self, current_location, target_position):
        """Move a middle layer edge from current location to target position"""
        pos1, pos2 = current_location
        
        # If edge is already in middle layer but wrong position
        if pos1[0] in [self.FRONT, self.BACK, self.LEFT, self.RIGHT] and pos1[1] == 1:
            # Extract to top layer first
            self._extract_middle_edge_to_top(current_location)
            
            # Find it again in top layer
            new_location = self._find_middle_edge_for_position(target_position)
            if new_location:
                current_location = new_location
                pos1, pos2 = current_location
        
        # Now edge should be in top layer
        if pos1[0] == self.UP:
            # Position edge above target slot
            current_top_pos = self._get_top_edge_position(pos1)
            
            # Check orientation and use appropriate insertion algorithm
            edge_colors = [
                self.cube.cube[pos1[0]][pos1[1]][pos1[2]],
                self.cube.cube[pos2[0]][pos2[1]][pos2[2]]
            ]
            
            # Determine which algorithm to use based on target position and edge orientation
            if target_position == 0:  # Front-Left
                self._insert_middle_edge_FL(current_top_pos, edge_colors)
            elif target_position == 1:  # Front-Right
                self._insert_middle_edge_FR(current_top_pos, edge_colors)
            elif target_position == 2:  # Back-Right
                self._insert_middle_edge_BR(current_top_pos, edge_colors)
            elif target_position == 3:  # Back-Left
                self._insert_middle_edge_BL(current_top_pos, edge_colors)
    
    def _extract_middle_edge_to_top(self, edge_location):
        """Extract a middle layer edge to the top layer"""
        pos1, pos2 = edge_location
        
        if pos1 == (self.FRONT, 1, 2):  # Front-Right edge
            self._execute_algorithm("R U R' U' F' U F")
        elif pos1 == (self.FRONT, 1, 0):  # Front-Left edge
            self._execute_algorithm("L' U' L U F U' F'")
        elif pos1 == (self.BACK, 1, 0):  # Back-Right edge
            self._execute_algorithm("R' U' R U B U' B'")
        elif pos1 == (self.BACK, 1, 2):  # Back-Left edge
            self._execute_algorithm("L U L' U' B' U B")
    
    def _insert_middle_edge_FR(self, current_top_pos, edge_colors):
        """Insert edge from top layer to Front-Right position"""
        # Position edge above Front-Right slot
        rotations_needed = (1 - current_top_pos) % 4  # Position 1 is above FR
        for _ in range(rotations_needed):
            self._execute_move("U")
        
        # Check orientation: if front color is on front face, use right-hand algorithm
        front_color = self.cube.cube[self.FRONT][0][1]
        if front_color == self.GREEN:
            self._execute_algorithm("U R U' R' U' F' U F")  # Right-hand
        else:
            self._execute_algorithm("U' F' U F U R U' R'")  # Left-hand
    
    def _insert_middle_edge_FL(self, current_top_pos, edge_colors):
        """Insert edge from top layer to Front-Left position"""
        # Position edge above Front-Left slot
        rotations_needed = (3 - current_top_pos) % 4  # Position 3 is above FL
        for _ in range(rotations_needed):
            self._execute_move("U")
        
        # Check orientation
        front_color = self.cube.cube[self.FRONT][0][1]
        if front_color == self.GREEN:
            self._execute_algorithm("U' L' U L U F U' F'")  # Left-hand
        else:
            self._execute_algorithm("U F U' F' U' L' U L")   # Right-hand
    
    def _insert_middle_edge_BR(self, current_top_pos, edge_colors):
        """Insert edge from top layer to Back-Right position"""
        # Position edge above Back-Right slot
        rotations_needed = (0 - current_top_pos) % 4  # Position 0 is above BR
        for _ in range(rotations_needed):
            self._execute_move("U")
        
        # Check orientation
        back_color = self.cube.cube[self.BACK][0][1]
        if back_color == self.BLUE:
            self._execute_algorithm("U R' U' R U B U' B'")  # Right-hand adapted
        else:
            self._execute_algorithm("U' B U' B' U' R' U R")  # Left-hand adapted
    
    def _insert_middle_edge_BL(self, current_top_pos, edge_colors):
        """Insert edge from top layer to Back-Left position"""
        # Position edge above Back-Left slot
        rotations_needed = (2 - current_top_pos) % 4  # Position 2 is above BL
        for _ in range(rotations_needed):
            self._execute_move("U")
        
        # Check orientation
        back_color = self.cube.cube[self.BACK][0][1]
        if back_color == self.BLUE:
            self._execute_algorithm("U' L U L' U B' U' B")   # Left-hand adapted
        else:
            self._execute_algorithm("U B' U B U L U' L'")    # Right-hand adapted
    
    # ============ PHASE 4: YELLOW CROSS ============
    
    def _solve_yellow_cross(self):
        """Solve yellow cross on top face using OLL edge algorithms"""
        max_attempts = 8
        attempt = 0
        
        while not self._is_yellow_cross_complete() and attempt < max_attempts:
            cross_case = self._analyze_yellow_cross_case()
            print(f"  → Yellow cross case: {cross_case}")
            
            if cross_case == "dot":
                # No yellow edges oriented - use F R U R' U' F'
                self._execute_algorithm("F R U R' U' F'")
            elif cross_case == "line":
                # Line pattern - orient perpendicular then apply algorithm
                if self._is_yellow_line_horizontal():
                    self._execute_move("U")
                self._execute_algorithm("F R U R' U' F'")
            elif cross_case == "L":
                # L-shape - orient properly then apply algorithm
                self._orient_yellow_L_shape()
                self._execute_algorithm("F R U R' U' F'")
            
            attempt += 1
        
        if self._is_yellow_cross_complete():
            print("  ✓ Yellow cross completed!")
        else:
            print("  ⚠ Yellow cross not completed within attempts")
    
    def _is_yellow_cross_complete(self):
        """Check if yellow cross is complete on top face"""
        top = self.cube.cube[self.UP]
        return (top[1][1] == self.YELLOW and  # Center
                top[0][1] == self.YELLOW and  # Top edge
                top[1][0] == self.YELLOW and  # Left edge
                top[1][2] == self.YELLOW and  # Right edge
                top[2][1] == self.YELLOW)     # Bottom edge
    
    def _analyze_yellow_cross_case(self):
        """Analyze the current yellow cross pattern"""
        top = self.cube.cube[self.UP]
        edges = [
            top[0][1] == self.YELLOW,  # Top
            top[1][2] == self.YELLOW,  # Right
            top[2][1] == self.YELLOW,  # Bottom
            top[1][0] == self.YELLOW   # Left
        ]
        
        yellow_count = sum(edges)
        
        if yellow_count == 0:
            return "dot"
        elif yellow_count == 2:
            # Check if it's a line or L-shape
            if (edges[0] and edges[2]) or (edges[1] and edges[3]):
                return "line"
            else:
                return "L"
        elif yellow_count == 4:
            return "cross"
        else:
            return "partial"
    
    def _is_yellow_line_horizontal(self):
        """Check if yellow line is horizontal"""
        top = self.cube.cube[self.UP]
        return top[1][0] == self.YELLOW and top[1][2] == self.YELLOW
    
    def _orient_yellow_L_shape(self):
        """Orient L-shape so algorithm works correctly"""
        top = self.cube.cube[self.UP]
        
        # Find the L orientation and rotate to standard position
        if top[0][1] == self.YELLOW and top[1][0] == self.YELLOW:  # Top and Left
            pass  # Already in correct position
        elif top[0][1] == self.YELLOW and top[1][2] == self.YELLOW:  # Top and Right
            self._execute_move("U")
        elif top[1][2] == self.YELLOW and top[2][1] == self.YELLOW:  # Right and Bottom
            self._execute_algorithm("U2")
        elif top[2][1] == self.YELLOW and top[1][0] == self.YELLOW:  # Bottom and Left
            self._execute_move("U'")
    
    # ============ PHASE 5: YELLOW CORNER ORIENTATION ============
    
    def _orient_yellow_corners(self):
        """Orient yellow corners using OLL corner algorithms"""
        max_attempts = 8
        attempt = 0
        
        while not self._are_all_yellow_corners_oriented() and attempt < max_attempts:
            oriented_count = self._count_oriented_yellow_corners()
            print(f"  → {oriented_count}/4 yellow corners oriented")
            
            if oriented_count == 0:
                # Apply Sune from any position
                self._execute_algorithm("R U R' U R U2 R'")
            elif oriented_count == 1:
                # Position oriented corner at back-right and apply Sune
                self._position_oriented_corner_BR()
                self._execute_algorithm("R U R' U R U2 R'")
            elif oriented_count == 2:
                # Find the oriented corners and position appropriately
                self._position_two_oriented_corners()
                self._execute_algorithm("R U R' U R U2 R'")
            
            attempt += 1
        
        if self._are_all_yellow_corners_oriented():
            print("  ✓ All yellow corners oriented!")
        else:
            print("  ⚠ Yellow corner orientation not completed within attempts")
    
    def _are_all_yellow_corners_oriented(self):
        """Check if all corners have yellow on top face"""
        top = self.cube.cube[self.UP]
        corners = [top[0][0], top[0][2], top[2][0], top[2][2]]
        return all(corner == self.YELLOW for corner in corners)
    
    def _count_oriented_yellow_corners(self):
        """Count how many corners have yellow on top"""
        top = self.cube.cube[self.UP]
        corners = [top[0][0], top[0][2], top[2][0], top[2][2]]
        return sum(1 for corner in corners if corner == self.YELLOW)
    
    def _position_oriented_corner_BR(self):
        """Position the one oriented corner to back-right position"""
        top = self.cube.cube[self.UP]
        corners = [
            (top[0][0], 0),  # Back-Left
            (top[0][2], 1),  # Back-Right
            (top[2][0], 2),  # Front-Left
            (top[2][2], 3),  # Front-Right
        ]
        
        for color, pos in corners:
            if color == self.YELLOW:
                rotations = (1 - pos) % 4  # Move to position 1 (back-right)
                for _ in range(rotations):
                    self._execute_move("U")
                break
    
    def _position_two_oriented_corners(self):
        """Position two oriented corners appropriately for algorithm"""
        top = self.cube.cube[self.UP]
        oriented_positions = []
        
        corner_positions = [(0, 0), (0, 2), (2, 0), (2, 2)]
        for i, (row, col) in enumerate(corner_positions):
            if top[row][col] == self.YELLOW:
                oriented_positions.append(i)
        
        # Check if they're adjacent or diagonal
        if len(oriented_positions) == 2:
            pos1, pos2 = oriented_positions
            if abs(pos1 - pos2) == 2:  # Diagonal
                # Position one at back-right
                rotations = (1 - pos1) % 4
                for _ in range(rotations):
                    self._execute_move("U")
            else:  # Adjacent
                # Position them appropriately
                if pos1 == 0 and pos2 == 1:  # Back row
                    pass  # Already good
                elif pos1 == 1 and pos2 == 3:  # Right column
                    self._execute_move("U'")
                elif pos1 == 2 and pos2 == 3:  # Front row
                    self._execute_algorithm("U2")
                elif pos1 == 0 and pos2 == 2:  # Left column
                    self._execute_move("U")
    
    # ============ PHASE 6: LAST LAYER PERMUTATION ============
    
    def _permute_last_layer(self):
        """Permute last layer corners and edges using PLL algorithms"""
        # First permute corners
        print("  → Permuting corners")
        self._permute_corners()
        
        # Then permute edges
        print("  → Permuting edges")
        self._permute_edges()
    
    def _permute_corners(self):
        """Permute corners using corner PLL algorithms"""
        max_attempts = 6
        attempt = 0
        
        while not self._are_corners_permuted() and attempt < max_attempts:
            corner_case = self._analyze_corner_permutation()
            print(f"    Corner case: {corner_case}")
            
            if corner_case == "solved":
                break
            elif corner_case == "clockwise":
                self._execute_algorithm("R' F R F' R' F R F'")  # T-perm variant
            elif corner_case == "counterclockwise":
                self._execute_algorithm("F R' F' R F R' F' R")   # T-perm variant
            else:
                # Default corner 3-cycle
                self._execute_algorithm("R' F R F' R' F R F'")
                self._execute_move("U")
            
            attempt += 1
    
    def _permute_edges(self):
        """Permute edges using edge PLL algorithms"""
        max_attempts = 4
        attempt = 0
        
        while not self._are_edges_permuted() and attempt < max_attempts:
            edge_case = self._analyze_edge_permutation()
            print(f"    Edge case: {edge_case}")
            
            if edge_case == "solved":
                break
            elif edge_case == "adjacent":
                self._execute_algorithm("R U R' F' R U R' U' R' F R2 U' R'")  # T-perm
            elif edge_case == "opposite":
                self._execute_algorithm("M2 U M2 U2 M2 U M2")  # H-perm (simplified)
            else:
                # Default edge permutation
                self._execute_algorithm("R U R' F' R U R' U' R' F R2 U' R'")
                self._execute_move("U")
            
            attempt += 1
    
    def _are_corners_permuted(self):
        """Check if corners are in correct positions (ignoring orientation)"""
        # Check if each corner has the right combination of colors
        corner_positions = [
            ((self.UP, 0, 0), (self.BACK, 0, 2), (self.LEFT, 0, 0)),    # UBL
            ((self.UP, 0, 2), (self.BACK, 0, 0), (self.RIGHT, 0, 2)),   # UBR
            ((self.UP, 2, 0), (self.FRONT, 0, 0), (self.LEFT, 0, 2)),   # UFL
            ((self.UP, 2, 2), (self.FRONT, 0, 2), (self.RIGHT, 0, 0)),  # UFR
        ]
        
        expected_color_sets = [
            set([self.YELLOW, self.BLUE, self.ORANGE]),    # UBL
            set([self.YELLOW, self.BLUE, self.RED]),       # UBR
            set([self.YELLOW, self.GREEN, self.ORANGE]),   # UFL
            set([self.YELLOW, self.GREEN, self.RED]),      # UFR
        ]
        
        for i, positions in enumerate(corner_positions):
            actual_colors = set([
                self.cube.cube[positions[0][0]][positions[0][1]][positions[0][2]],
                self.cube.cube[positions[1][0]][positions[1][1]][positions[1][2]],
                self.cube.cube[positions[2][0]][positions[2][1]][positions[2][2]]
            ])
            
            if actual_colors != expected_color_sets[i]:
                return False
        
        return True
    
    def _are_edges_permuted(self):
        """Check if edges are in correct positions"""
        edge_positions = [
            ((self.UP, 0, 1), (self.BACK, 0, 1)),   # UB
            ((self.UP, 1, 2), (self.RIGHT, 0, 1)),  # UR
            ((self.UP, 2, 1), (self.FRONT, 0, 1)),  # UF
            ((self.UP, 1, 0), (self.LEFT, 0, 1)),   # UL
        ]
        
        expected_color_sets = [
            set([self.YELLOW, self.BLUE]),     # UB
            set([self.YELLOW, self.RED]),      # UR
            set([self.YELLOW, self.GREEN]),    # UF
            set([self.YELLOW, self.ORANGE]),   # UL
        ]
        
        for i, positions in enumerate(edge_positions):
            actual_colors = set([
                self.cube.cube[positions[0][0]][positions[0][1]][positions[0][2]],
                self.cube.cube[positions[1][0]][positions[1][1]][positions[1][2]]
            ])
            
            if actual_colors != expected_color_sets[i]:
                return False
        
        return True
    
    def _analyze_corner_permutation(self):
        """Analyze corner permutation pattern"""
        # Simplified analysis - in practice would check specific cycle types
        if self._are_corners_permuted():
            return "solved"
        else:
            return "clockwise"  # Default assumption
    
    def _analyze_edge_permutation(self):
        """Analyze edge permutation pattern"""
        # Simplified analysis - in practice would check specific cycle types
        if self._are_edges_permuted():
            return "solved"
        else:
            return "adjacent"  # Default assumption
    
    # ============ UTILITY METHODS ============
    
    def _execute_move(self, move):
        """Execute a single move and track it"""
        move_methods = {
            'U': self.cube.move_U, "U'": self.cube.move_U_prime, 'U2': self.cube.move_U2,
            'D': self.cube.move_D, "D'": self.cube.move_D_prime, 'D2': self.cube.move_D2,
            'R': self.cube.move_R, "R'": self.cube.move_R_prime, 'R2': self.cube.move_R2,
            'L': self.cube.move_L, "L'": self.cube.move_L_prime, 'L2': self.cube.move_L2,
            'F': self.cube.move_F, "F'": self.cube.move_F_prime, 'F2': self.cube.move_F2,
            'B': self.cube.move_B, "B'": self.cube.move_B_prime, 'B2': self.cube.move_B2,
        }
        
        if move in move_methods:
            move_methods[move]()
            self.solution_moves.append(move)
            print(f"    Executed: {move}")
        else:
            print(f"    Unknown move: {move}")
    
    def _execute_algorithm(self, algorithm):
        """Execute a sequence of moves"""
        moves = algorithm.split()
        print(f"    Algorithm: {algorithm}")
        for move in moves:
            self._execute_move(move)
    
    def get_solving_statistics(self):
        """Return comprehensive statistics about the solving process"""
        tracker_info = {}
        if self.tracker:
            try:
                validation = self.tracker.validate_state()
                tracker_info = {
                    'is_solved': self.tracker.is_cube_solved(),
                    'valid': True,
                    'solved_edges': sum(1 for i in range(12) if self.tracker.is_edge_solved(i)),
                    'solved_corners': sum(1 for i in range(8) if self.tracker.is_corner_solved(i))
                }
            except Exception as e:
                tracker_info = {'valid': False, 'error': str(e)}
        
        return {
            'total_moves': len(self.solution_moves),
            'solution_sequence': ' '.join(self.solution_moves),
            'is_solved': self.cube.is_solved(),
            'tracker_info': tracker_info,
            'efficiency_score': max(0, 100 - len(self.solution_moves)) + (50 if self.cube.is_solved() else 0)
        }

def demo_state_driven_solver():
    """Demonstrate the state-driven solver"""
    print("=== STATE-DRIVEN RUBIK'S CUBE SOLVER DEMO ===")
    
    # Create and scramble a 3x3 cube
    cube = RubiksCube(size=3)
    print("✓ Created 3x3 cube with state tracker")
    
    # Show initial state
    print("\n1. Initial solved cube:")
    cube.display_cube_compact()
    
    # Scramble the cube
    print("\n2. Scrambling cube...")
    cube.scramble(15)
    cube.display_cube_compact()
    
    # Show tracker diagnostics
    diagnostics = cube.get_tracker_diagnostics()
    print(f"\nAfter scrambling:")
    print(f"Solved edges: {diagnostics['solved_edges']}/12")
    print(f"Solved corners: {diagnostics['solved_corners']}/8")
    print(f"Tracker validation: {diagnostics['validation_status']['message']}")
    
    # Solve using state-driven method
    print("\n3. Starting state-driven LBL solve...")
    solver = RubiksCubeSolver(cube)
    solution = solver.solve()
    
    # Show final result
    print("\n4. Final result:")
    cube.display_cube_compact()
    
    # Display statistics
    stats = solver.get_solving_statistics()
    print(f"\nSOLVING STATISTICS:")
    print(f"Total moves: {stats['total_moves']}")
    print(f"Cube solved: {stats['is_solved']}")
    print(f"Efficiency score: {stats['efficiency_score']}")
    print(f"Solution: {stats['solution_sequence']}")
    
    if 'tracker_info' in stats and stats['tracker_info'].get('valid', False):
        tracker = stats['tracker_info']
        print(f"Tracker solved: {tracker['is_solved']}")
        print(f"Final solved edges: {tracker['solved_edges']}/12")
        print(f"Final solved corners: {tracker['solved_corners']}/8")

if __name__ == "__main__":
    demo_state_driven_solver()