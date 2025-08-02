"""
Multi-Size Rubik's Cube implementation with support for 2x2, 3x3, 4x4, and larger cubes
Complete implementation with all moves and state management
Enhanced with CubeStateTracker and Cube class integration
"""

import random
import copy

class CubeStateTracker:
    """Tracks piece positions and orientations for precise cube state management"""
    
    def __init__(self):
        # Define solved state for edges (12 edges total)
        self.solved_edges = [
            {'id': 'UF', 'position': 0, 'orientation': 0},  # Up-Front
            {'id': 'UR', 'position': 1, 'orientation': 0},  # Up-Right
            {'id': 'UB', 'position': 2, 'orientation': 0},  # Up-Back
            {'id': 'UL', 'position': 3, 'orientation': 0},  # Up-Left
            {'id': 'DF', 'position': 4, 'orientation': 0},  # Down-Front
            {'id': 'DR', 'position': 5, 'orientation': 0},  # Down-Right
            {'id': 'DB', 'position': 6, 'orientation': 0},  # Down-Back
            {'id': 'DL', 'position': 7, 'orientation': 0},  # Down-Left
            {'id': 'FR', 'position': 8, 'orientation': 0},  # Front-Right
            {'id': 'FL', 'position': 9, 'orientation': 0},  # Front-Left
            {'id': 'BR', 'position': 10, 'orientation': 0}, # Back-Right
            {'id': 'BL', 'position': 11, 'orientation': 0}, # Back-Left
        ]
        
        # Define solved state for corners (8 corners total)
        self.solved_corners = [
            {'id': 'UFR', 'position': 0, 'orientation': 0},  # Up-Front-Right
            {'id': 'UFL', 'position': 1, 'orientation': 0},  # Up-Front-Left
            {'id': 'UBL', 'position': 2, 'orientation': 0},  # Up-Back-Left
            {'id': 'UBR', 'position': 3, 'orientation': 0},  # Up-Back-Right
            {'id': 'DFR', 'position': 4, 'orientation': 0},  # Down-Front-Right
            {'id': 'DFL', 'position': 5, 'orientation': 0},  # Down-Front-Left
            {'id': 'DBL', 'position': 6, 'orientation': 0},  # Down-Back-Left
            {'id': 'DBR', 'position': 7, 'orientation': 0},  # Down-Back-Right
        ]
        
        # Initialize current state as solved
        self.edges = copy.deepcopy(self.solved_edges)
        self.corners = copy.deepcopy(self.solved_corners)
        
        # Define move tables for each face rotation
        self.move_tables = {
            'U': {
                'edges': [(0, 1), (1, 2), (2, 3), (3, 0)],  # UF->UR->UB->UL->UF
                'corners': [(0, 1), (1, 2), (2, 3), (3, 0)],  # UFR->UFL->UBL->UBR->UFR
                'edge_orient_flip': [],
                'corner_orient_change': [],
            },
            'D': {
                'edges': [(4, 7), (7, 6), (6, 5), (5, 4)],  # DF->DL->DB->DR->DF
                'corners': [(4, 5), (5, 6), (6, 7), (7, 4)],  # DFR->DFL->DBL->DBR->DFR
                'edge_orient_flip': [],
                'corner_orient_change': [],
            },
            'R': {
                'edges': [(1, 8), (8, 5), (5, 10), (10, 1)],  # UR->FR->DR->BR->UR
                'corners': [(0, 4), (4, 7), (7, 3), (3, 0)],  # UFR->DFR->DBR->UBR->UFR
                'edge_orient_flip': [],
                'corner_orient_change': [(0, 1), (4, 2), (7, 1), (3, 2)],  # clockwise rotation changes
            },
            'L': {
                'edges': [(3, 11), (11, 7), (7, 9), (9, 3)],  # UL->BL->DL->FL->UL
                'corners': [(1, 2), (2, 6), (6, 5), (5, 1)],  # UFL->UBL->DBL->DFL->UFL
                'edge_orient_flip': [],
                'corner_orient_change': [(1, 2), (2, 1), (6, 2), (5, 1)],
            },
            'F': {
                'edges': [(0, 9), (9, 4), (4, 8), (8, 0)],  # UF->FL->DF->FR->UF
                'corners': [(0, 1), (1, 5), (5, 4), (4, 0)],  # UFR->UFL->DFL->DFR->UFR
                'edge_orient_flip': [0, 9, 4, 8],  # Front moves flip edge orientations
                'corner_orient_change': [(0, 2), (1, 1), (5, 2), (4, 1)],
            },
            'B': {
                'edges': [(2, 10), (10, 6), (6, 11), (11, 2)],  # UB->BR->DB->BL->UB
                'corners': [(3, 2), (2, 6), (6, 7), (7, 3)],  # UBR->UBL->DBL->DBR->UBR
                'edge_orient_flip': [2, 10, 6, 11],  # Back moves flip edge orientations
                'corner_orient_change': [(3, 1), (2, 2), (6, 1), (7, 2)],
            }
        }
    
    def apply_move(self, move):
        """Apply a move to update piece positions and orientations"""
        # Handle prime moves
        if move.endswith("'"):
            base_move = move[0]
            # Apply the move 3 times (equivalent to prime)
            for _ in range(3):
                self._apply_single_move(base_move)
        elif move.endswith('2'):
            base_move = move[0]
            # Apply the move twice
            for _ in range(2):
                self._apply_single_move(base_move)
        else:
            self._apply_single_move(move)
    
    def _apply_single_move(self, move):
        """Apply a single move transformation"""
        if move not in self.move_tables:
            return
        
        table = self.move_tables[move]
        
        # Rotate edges
        self._permute_pieces(self.edges, table['edges'])
        
        # Rotate corners
        self._permute_pieces(self.corners, table['corners'])
        
        # Update edge orientations
        for idx in table['edge_orient_flip']:
            self.edges[idx]['orientation'] ^= 1  # Flip orientation (0->1, 1->0)
        
        # Update corner orientations
        for idx, delta in table.get('corner_orient_change', []):
            self.corners[idx]['orientation'] = (self.corners[idx]['orientation'] + delta) % 3
    
    def _permute_pieces(self, pieces, cycles):
        """Apply permutation cycles to pieces"""
        for cycle in cycles:
            if len(cycle) < 2:
                continue
            
            # Store the first piece
            temp = copy.deepcopy(pieces[cycle[0]])
            
            # Shift pieces along the cycle
            for i in range(len(cycle) - 1):
                pieces[cycle[i]] = copy.deepcopy(pieces[cycle[i + 1]])
            
            # Place the first piece at the end of the cycle
            pieces[cycle[-1]] = temp
    
    def is_edge_solved(self, idx):
        """Check if an edge is in its solved position and orientation"""
        edge = self.edges[idx]
        solved = self.solved_edges[idx]
        return edge['id'] == solved['id'] and edge['orientation'] == solved['orientation']
    
    def is_corner_solved(self, idx):
        """Check if a corner is in its solved position and orientation"""
        corner = self.corners[idx]
        solved = self.solved_corners[idx]
        return corner['id'] == solved['id'] and corner['orientation'] == solved['orientation']
    
    def is_cube_solved(self):
        """Check if the entire cube is solved"""
        return (all(self.is_edge_solved(i) for i in range(12)) and 
                all(self.is_corner_solved(i) for i in range(8)))
    
    def validate_state(self):
        """Validate the current cube state for consistency"""
        # Check for duplicate edge positions
        edge_positions = [e['position'] for e in self.edges]
        if len(set(edge_positions)) != 12:
            raise ValueError("Duplicate or missing edge positions detected!")
        
        # Check for duplicate corner positions
        corner_positions = [c['position'] for c in self.corners]
        if len(set(corner_positions)) != 8:
            raise ValueError("Duplicate or missing corner positions detected!")
        
        # Check edge orientation parity
        edge_orientation_sum = sum(e['orientation'] for e in self.edges)
        if edge_orientation_sum % 2 != 0:
            raise ValueError("Invalid edge orientation parity!")
        
        # Check corner orientation parity
        corner_orientation_sum = sum(c['orientation'] for c in self.corners)
        if corner_orientation_sum % 3 != 0:
            raise ValueError("Invalid corner orientation parity!")
    
    def get_state_info(self):
        """Get detailed information about current cube state"""
        return {
            'edges': copy.deepcopy(self.edges),
            'corners': copy.deepcopy(self.corners),
            'is_solved': self.is_cube_solved(),
            'edge_orientations': [e['orientation'] for e in self.edges],
            'corner_orientations': [c['orientation'] for c in self.corners]
        }

class Cube:
    """Enhanced Cube class with state tracking integration"""
    
    def __init__(self, size=3):
        self.size = size
        
        self.colors = [
            'R', 'G', 'B', 'Y', 'W', 'O'
        ]

        '''
            Initial Cube Setup
        '''
        self.state = {
            'DOWN' : [
                ['W', 'W', 'W'],
                ['W', 'W', 'W'],
                ['W', 'W', 'W']
            ],
            'FRONT' : [
                ['G', 'G', 'G'],
                ['G', 'G', 'G'],
                ['G', 'G', 'G']
            ],
            'LEFT' : [
                ['R', 'R', 'R'],
                ['R', 'R', 'R'],
                ['R', 'R', 'R']
            ],
            'RIGHT' : [
                ['O', 'O', 'O'],
                ['O', 'O', 'O'],
                ['O', 'O', 'O']
            ],
            'BACK' : [
                ['B', 'B', 'B'],
                ['B', 'B', 'B'],
                ['B', 'B', 'B']
            ],
            'UP' : [
                ['Y', 'Y', 'Y'],
                ['Y', 'Y', 'Y'],
                ['Y', 'Y', 'Y']
            ]
        }
        
        # Initialize the state tracker
        self.tracker = CubeStateTracker()

    def print(self) -> None:
        """Print cube state in unfolded format"""
        for row in self.state['UP']:
            print(f"\t\t {row}")
        print()
        for i in range(3):
            print(f"{self.state['LEFT'][i]}  {self.state['FRONT'][i]}  {self.state['RIGHT'][i]}  {self.state['BACK'][i]}")
        print()
        for row in self.state['DOWN']:
            print(f"\t\t {row}")

class RubiksCube:
    def __init__(self, size=3):
        """Initialize a solved Rubik's Cube of specified size"""
        self.size = size
        
        # Define color constants for each face
        self.COLORS = {
            0: 'WHITE',   # Front face
            1: 'YELLOW',  # Back face  
            2: 'RED',     # Right face
            3: 'ORANGE',  # Left face
            4: 'GREEN',   # Up face
            5: 'BLUE'     # Down face
        }
        
        # Face names for display
        self.FACE_NAMES = ['FRONT', 'BACK', 'RIGHT', 'LEFT', 'UP', 'DOWN']
        
        # Initialize the cube in solved state
        self.cube = self.create_solved_cube()
        self.move_history = []
        
        # Initialize state tracker for 3x3 cubes
        if size == 3:
            self.tracker = CubeStateTracker()
        else:
            self.tracker = None
    
    def create_solved_cube(self):
        """Create a solved cube - each face has all same colors"""
        cube = []
        for face_color in range(6):
            face = [[face_color for _ in range(self.size)] for _ in range(self.size)]
            cube.append(face)
        return cube
    
    def copy_cube(self):
        """Create a deep copy of the current cube state"""
        return copy.deepcopy(self.cube)
    
    def rotate_face_clockwise(self, face):
        """Rotate a face matrix 90 degrees clockwise"""
        size = len(face)
        return [[face[size-1-j][i] for j in range(size)] for i in range(size)]
    
    def rotate_face_counterclockwise(self, face):
        """Rotate a face matrix 90 degrees counterclockwise"""
        size = len(face)
        return [[face[j][size-1-i] for j in range(size)] for i in range(size)]
    
    # ============ BASIC MOVES ============
    
    def move_U(self):
        """Execute U move - rotate Up face clockwise"""
        # Rotate the Up face itself
        self.cube[4] = self.rotate_face_clockwise(self.cube[4])
        
        # Save the top row of Front face
        temp = [self.cube[0][0][i] for i in range(self.size)]
        
        # Shift: Front <- Right <- Back <- Left <- Front
        self.cube[0][0] = [self.cube[2][0][i] for i in range(self.size)]  # Front <- Right
        self.cube[2][0] = [self.cube[1][0][i] for i in range(self.size)]  # Right <- Back  
        self.cube[1][0] = [self.cube[3][0][i] for i in range(self.size)]  # Back <- Left
        self.cube[3][0] = temp  # Left <- Front (saved)
        
        self.move_history.append('U')
        
        # Update tracker for 3x3 cubes
        if self.tracker:
            self.tracker.apply_move('U')
    
    def move_D(self):
        """Execute D move - rotate Down face clockwise"""
        # Rotate the Down face
        self.cube[5] = self.rotate_face_clockwise(self.cube[5])
        
        # Save bottom row of Front face
        temp = [self.cube[0][self.size-1][i] for i in range(self.size)]
        
        # Shift: Front <- Left <- Back <- Right <- Front
        self.cube[0][self.size-1] = [self.cube[3][self.size-1][i] for i in range(self.size)]  # Front <- Left
        self.cube[3][self.size-1] = [self.cube[1][self.size-1][i] for i in range(self.size)]  # Left <- Back
        self.cube[1][self.size-1] = [self.cube[2][self.size-1][i] for i in range(self.size)]  # Back <- Right
        self.cube[2][self.size-1] = temp  # Right <- Front
        
        self.move_history.append('D')
        
        # Update tracker for 3x3 cubes
        if self.tracker:
            self.tracker.apply_move('D')
    
    def move_R(self):
        """Execute R move - rotate Right face clockwise"""
        # Rotate the Right face
        self.cube[2] = self.rotate_face_clockwise(self.cube[2])
        
        # Save right column of Front face
        temp = [self.cube[0][i][self.size-1] for i in range(self.size)]
        
        # Shift right columns: Front <- Down <- Back <- Up <- Front
        for i in range(self.size):
            self.cube[0][i][self.size-1] = self.cube[5][i][self.size-1]      # Front <- Down
            self.cube[5][i][self.size-1] = self.cube[1][self.size-1-i][0]    # Down <- Back (flipped)
            self.cube[1][self.size-1-i][0] = self.cube[4][i][self.size-1]    # Back <- Up (flipped)
            self.cube[4][i][self.size-1] = temp[i]                           # Up <- Front
        
        self.move_history.append('R')
        
        # Update tracker for 3x3 cubes
        if self.tracker:
            self.tracker.apply_move('R')
    
    def move_L(self):
        """Execute L move - rotate Left face clockwise"""
        # Rotate the Left face
        self.cube[3] = self.rotate_face_clockwise(self.cube[3])
        
        # Save left column of Front face
        temp = [self.cube[0][i][0] for i in range(self.size)]
        
        # Shift left columns: Front <- Up <- Back <- Down <- Front
        for i in range(self.size):
            self.cube[0][i][0] = self.cube[4][i][0]                      # Front <- Up
            self.cube[4][i][0] = self.cube[1][self.size-1-i][self.size-1]    # Up <- Back (flipped)
            self.cube[1][self.size-1-i][self.size-1] = self.cube[5][i][0]    # Back <- Down (flipped)
            self.cube[5][i][0] = temp[i]                                 # Down <- Front
        
        self.move_history.append('L')
        
        # Update tracker for 3x3 cubes
        if self.tracker:
            self.tracker.apply_move('L')
    
    def move_F(self):
        """Execute F move - rotate Front face clockwise"""
        # Rotate the Front face
        self.cube[0] = self.rotate_face_clockwise(self.cube[0])
        
        # Save bottom row of Up face
        temp = [self.cube[4][self.size-1][i] for i in range(self.size)]
        
        # Shift: Up <- Left <- Down <- Right <- Up
        for i in range(self.size):
            self.cube[4][self.size-1][i] = self.cube[3][self.size-1-i][self.size-1]    # Up <- Left (flipped)
            self.cube[3][self.size-1-i][self.size-1] = self.cube[5][0][self.size-1-i]  # Left <- Down (flipped)
            self.cube[5][0][self.size-1-i] = self.cube[2][i][0]                        # Down <- Right (flipped)
            self.cube[2][i][0] = temp[i]                                               # Right <- Up
        
        self.move_history.append('F')
        
        # Update tracker for 3x3 cubes
        if self.tracker:
            self.tracker.apply_move('F')
    
    def move_B(self):
        """Execute B move - rotate Back face clockwise"""
        # Rotate the Back face
        self.cube[1] = self.rotate_face_clockwise(self.cube[1])
        
        # Save top row of Up face
        temp = [self.cube[4][0][i] for i in range(self.size)]
        
        # Shift: Up <- Right <- Down <- Left <- Up
        for i in range(self.size):
            self.cube[4][0][i] = self.cube[2][self.size-1-i][self.size-1]           # Up <- Right (flipped)
            self.cube[2][self.size-1-i][self.size-1] = self.cube[5][self.size-1][self.size-1-i]  # Right <- Down (flipped)
            self.cube[5][self.size-1][self.size-1-i] = self.cube[3][i][0]           # Down <- Left (flipped)
            self.cube[3][i][0] = temp[self.size-1-i]                                # Left <- Up (flipped)
        
        self.move_history.append('B')
        
        # Update tracker for 3x3 cubes
        if self.tracker:
            self.tracker.apply_move('B')
    
    # ============ PRIME MOVES (Counter-clockwise) ============
    
    def move_U_prime(self):
        """Execute U' move - rotate Up face counter-clockwise"""
        for _ in range(3):
            self.move_U()
        # Fix move history
        self.move_history = self.move_history[:-3]
        self.move_history.append("U'")
    
    def move_D_prime(self):
        """Execute D' move - rotate Down face counter-clockwise"""
        for _ in range(3):
            self.move_D()
        self.move_history = self.move_history[:-3]
        self.move_history.append("D'")
    
    def move_R_prime(self):
        """Execute R' move - rotate Right face counter-clockwise"""
        for _ in range(3):
            self.move_R()
        self.move_history = self.move_history[:-3]
        self.move_history.append("R'")
    
    def move_L_prime(self):
        """Execute L' move - rotate Left face counter-clockwise"""
        for _ in range(3):
            self.move_L()
        self.move_history = self.move_history[:-3]
        self.move_history.append("L'")
    
    def move_F_prime(self):
        """Execute F' move - rotate Front face counter-clockwise"""
        for _ in range(3):
            self.move_F()
        self.move_history = self.move_history[:-3]
        self.move_history.append("F'")
    
    def move_B_prime(self):
        """Execute B' move - rotate Back face counter-clockwise"""
        for _ in range(3):
            self.move_B()
        self.move_history = self.move_history[:-3]
        self.move_history.append("B'")
    
    # ============ DOUBLE MOVES (180 degrees) ============
    
    def move_U2(self):
        """Execute U2 move - rotate Up face 180 degrees"""
        self.move_U()
        self.move_U()
        self.move_history = self.move_history[:-2]
        self.move_history.append("U2")
    
    def move_D2(self):
        """Execute D2 move - rotate Down face 180 degrees"""
        self.move_D()
        self.move_D()
        self.move_history = self.move_history[:-2]
        self.move_history.append("D2")
    
    def move_R2(self):
        """Execute R2 move - rotate Right face 180 degrees"""
        self.move_R()
        self.move_R()
        self.move_history = self.move_history[:-2]
        self.move_history.append("R2")
    
    def move_L2(self):
        """Execute L2 move - rotate Left face 180 degrees"""
        self.move_L()
        self.move_L()
        self.move_history = self.move_history[:-2]
        self.move_history.append("L2")
    
    def move_F2(self):
        """Execute F2 move - rotate Front face 180 degrees"""
        self.move_F()
        self.move_F()
        self.move_history = self.move_history[:-2]
        self.move_history.append("F2")
    
    def move_B2(self):
        """Execute B2 move - rotate Back face 180 degrees"""
        self.move_B()
        self.move_B()
        self.move_history = self.move_history[:-2]
        self.move_history.append("B2")
    
    # ============ SLICE MOVES (For 4x4+ cubes) ============
    
    def move_M(self):
        """Execute M move - middle slice (between L and R)"""
        if self.size < 3:
            print("M move not applicable to 2x2 cube")
            return
        
        # For odd-sized cubes, rotate the middle slice
        if self.size % 2 == 1:
            middle = self.size // 2
            # Save middle column of Front face
            temp = [self.cube[0][i][middle] for i in range(self.size)]
            
            # Shift middle columns like L' move
            for i in range(self.size):
                self.cube[0][i][middle] = self.cube[4][i][middle]
                self.cube[4][i][middle] = self.cube[1][self.size-1-i][middle]
                self.cube[1][self.size-1-i][middle] = self.cube[5][i][middle]
                self.cube[5][i][middle] = temp[i]
        
        self.move_history.append('M')
    
    def move_E(self):
        """Execute E move - equatorial slice (between U and D)"""
        if self.size < 3:
            print("E move not applicable to 2x2 cube")
            return
        
        # For odd-sized cubes, rotate the middle slice
        if self.size % 2 == 1:
            middle = self.size // 2
            # Save middle row of Front face
            temp = [self.cube[0][middle][i] for i in range(self.size)]
            
            # Shift middle rows like D move
            self.cube[0][middle] = [self.cube[3][middle][i] for i in range(self.size)]
            self.cube[3][middle] = [self.cube[1][middle][i] for i in range(self.size)]
            self.cube[1][middle] = [self.cube[2][middle][i] for i in range(self.size)]
            self.cube[2][middle] = temp
        
        self.move_history.append('E')
    
    def move_S(self):
        """Execute S move - standing slice (between F and B)"""
        if self.size < 3:
            print("S move not applicable to 2x2 cube")
            return
        
        # For odd-sized cubes, rotate the middle slice
        if self.size % 2 == 1:
            middle = self.size // 2
            # Similar to F move but for middle slice
            temp = [self.cube[4][middle][i] for i in range(self.size)]
            
            for i in range(self.size):
                self.cube[4][middle][i] = self.cube[3][self.size-1-i][middle]
                self.cube[3][self.size-1-i][middle] = self.cube[5][middle][self.size-1-i]
                self.cube[5][middle][self.size-1-i] = self.cube[2][i][middle]
                self.cube[2][i][middle] = temp[i]
        
        self.move_history.append('S')
    
    # ============ UTILITY METHODS ============
    
    def execute_moves(self, move_sequence):
        """Execute a sequence of moves from a string"""
        moves = move_sequence.split()
        
        move_map = {
            'U': self.move_U, "U'": self.move_U_prime, 'U2': self.move_U2,
            'D': self.move_D, "D'": self.move_D_prime, 'D2': self.move_D2,
            'R': self.move_R, "R'": self.move_R_prime, 'R2': self.move_R2,
            'L': self.move_L, "L'": self.move_L_prime, 'L2': self.move_L2,
            'F': self.move_F, "F'": self.move_F_prime, 'F2': self.move_F2,
            'B': self.move_B, "B'": self.move_B_prime, 'B2': self.move_B2,
            'M': self.move_M, 'E': self.move_E, 'S': self.move_S,
        }
        
        for move in moves:
            if move in move_map:
                move_map[move]()
            else:
                print(f"Unknown move: {move}")
    
    def scramble(self, num_moves=20):
        """Scramble the cube with random moves"""
        basic_moves = ['U', 'D', 'R', 'L', 'F', 'B', "U'", "D'", "R'", "L'", "F'", "B'"]
        
        # Add slice moves for larger cubes
        if self.size >= 3:
            basic_moves.extend(['M', 'E', 'S'])
        
        scramble_sequence = []
        for _ in range(num_moves):
            move = random.choice(basic_moves)
            scramble_sequence.append(move)
        
        print(f"Scrambling {self.size}x{self.size}x{self.size} cube with {num_moves} moves: {' '.join(scramble_sequence)}")
        self.execute_moves(' '.join(scramble_sequence))
    
    def display_cube(self):
        """Display the current state of the cube"""
        print(f"\nCurrent {self.size}x{self.size}x{self.size} Cube State:")
        print("=" * 50)
        
        for i, face in enumerate(self.cube):
            print(f"\n{self.FACE_NAMES[i]} Face ({self.COLORS[i]}):")
            for row in face:
                display_row = [self.COLORS[cell][0] for cell in row]
                print('  ' + ' '.join(display_row))
        
        print("=" * 50)
        print(f"Total stickers: {6 * self.size * self.size}")
    
    def display_cube_compact(self):
        """Display cube in a more compact format"""
        face_letters = ['F', 'B', 'R', 'L', 'U', 'D']
        
        print(f"\n{self.size}x{self.size}x{self.size} Cube State (Compact):")
        for i, face in enumerate(self.cube):
            print(f"{face_letters[i]}: ", end="")
            for row in face:
                for cell in row:
                    print(self.COLORS[cell][0], end="")
            print()
    
    def is_solved(self):
        """Check if the cube is in solved state"""
        for face_idx, face in enumerate(self.cube):
            for row in face:
                for cell in row:
                    if cell != face_idx:
                        return False
        return True
    
    def get_state_string(self):
        """Get a string representation of the cube state"""
        state = ""
        for face in self.cube:
            for row in face:
                for cell in row:
                    state += str(cell)
        return state
    
    def reset(self):
        """Reset cube to solved state"""
        self.cube = self.create_solved_cube()
        self.move_history = []
        
        # Reset tracker for 3x3 cubes
        if self.tracker:
            self.tracker = CubeStateTracker()
    
    def get_cube_info(self):
        """Get information about the current cube"""
        return {
            'size': self.size,
            'total_stickers': 6 * self.size * self.size,
            'total_pieces': self.calculate_total_pieces(),
            'is_solved': self.is_solved(),
            'move_count': len(self.move_history),
            'complexity': self.get_complexity_rating(),
            'has_tracker': self.tracker is not None
        }
    
    def calculate_total_pieces(self):
        """Calculate total number of pieces based on cube size"""
        if self.size == 1:
            return 6  # Just 6 center pieces
        elif self.size == 2:
            return 8  # 8 corner pieces
        elif self.size == 3:
            return 26  # 8 corners + 12 edges + 6 centers
        else:
            # For NxN cubes where N > 3
            corners = 8
            edges = 12 * (self.size - 2)
            centers = 6 * ((self.size - 2) ** 2)
            return corners + edges + centers
    
    def get_complexity_rating(self):
        """Get a complexity rating for the current cube size"""
        complexity_map = {
            1: "Trivial",
            2: "Beginner",
            3: "Standard",
            4: "Advanced",
            5: "Expert",
        }
        
        if self.size <= 5:
            return complexity_map[self.size]
        else:
            return "Master"
    
    def clone(self):
        """Create a complete copy of this cube"""
        new_cube = RubiksCube(size=self.size)
        new_cube.cube = copy.deepcopy(self.cube)
        new_cube.move_history = self.move_history.copy()
        
        # Clone tracker if it exists
        if self.tracker:
            new_cube.tracker = CubeStateTracker()
            new_cube.tracker.edges = copy.deepcopy(self.tracker.edges)
            new_cube.tracker.corners = copy.deepcopy(self.tracker.corners)
        
        return new_cube
    
    def get_tracker_diagnostics(self):
        """Get detailed tracker diagnostics for debugging"""
        if not self.tracker:
            return {
                'has_tracker': False,
                'message': 'State tracking only available for 3x3 cubes'
            }
        
        return {
            'has_tracker': True,
            'edge_positions': [e['position'] for e in self.tracker.edges],
            'edge_orientations': [e['orientation'] for e in self.tracker.edges],
            'corner_positions': [c['position'] for c in self.tracker.corners],
            'corner_orientations': [c['orientation'] for c in self.tracker.corners],
            'solved_edges': sum(1 for i in range(12) if self.tracker.is_edge_solved(i)),
            'solved_corners': sum(1 for i in range(8) if self.tracker.is_corner_solved(i)),
            'tracker_solved': self.tracker.is_cube_solved(),
            'validation_status': self.validate_cube_state()
        }
    
    def validate_cube_state(self):
        """Validate current cube state using tracker"""
        if not self.tracker:
            return {'valid': True, 'message': 'No tracker available for validation'}
        
        try:
            self.tracker.validate_state()
            return {'valid': True, 'message': 'Cube state is valid'}
        except ValueError as e:
            return {'valid': False, 'message': str(e)}
        except Exception as e:
            return {'valid': False, 'message': f'Validation error: {e}'}

# Utility functions for cube operations
def create_multiple_cubes(sizes):
    """Create multiple cubes of different sizes"""
    cubes = {}
    for size in sizes:
        try:
            cubes[size] = RubiksCube(size=size)
            print(f"✓ Created {size}x{size}x{size} cube")
        except Exception as e:
            print(f"✗ Failed to create {size}x{size}x{size} cube: {e}")
    return cubes

def compare_cube_states(cube1, cube2):
    """Compare two cubes and return if they're identical"""
    if cube1.size != cube2.size:
        return False
    return cube1.get_state_string() == cube2.get_state_string()

# Testing and demonstration functions
def test_cube_functionality():
    """Test basic cube functionality across different sizes"""
    print("=== Testing Multi-Size Cube Functionality ===")
    
    for size in [2, 3, 4]:
        print(f"\nTesting {size}x{size}x{size} cube:")
        cube = RubiksCube(size=size)
        
        # Test basic properties
        assert cube.is_solved(), "New cube should be solved"
        print(f"✓ {size}x{size}x{size} cube initializes as solved")
        
        # Test basic move
        cube.move_U()
        assert not cube.is_solved(), "Cube should not be solved after move"
        print(f"✓ {size}x{size}x{size} cube changes state after U move")
        
        # Test move history
        assert len(cube.move_history) == 1, "Move history should track moves"
        print(f"✓ {size}x{size}x{size} cube tracks move history")
        
        # Test tracker for 3x3
        if size == 3:
            assert cube.tracker is not None, "3x3 cube should have tracker"
            print(f"✓ {size}x{size}x{size} cube has state tracker")
        
        # Test reset
        cube.reset()
        assert cube.is_solved(), "Cube should be solved after reset"
        print(f"✓ {size}x{size}x{size} cube resets correctly")
    
    print("\n✓ All tests passed! Multi-size cube functionality working correctly.")

if __name__ == "__main__":
    # Run tests when file is executed directly
    test_cube_functionality()
    
    # Demo different cube sizes
    print("\n=== Multi-Size Cube Demo ===")
    for size in [2, 3, 4]:
        print(f"\nCreating {size}x{size}x{size} cube:")
        cube = RubiksCube(size=size)
        info = cube.get_cube_info()
        print(f"  Size: {info['size']}x{info['size']}x{info['size']}")
        print(f"  Total stickers: {info['total_stickers']}")
        print(f"  Total pieces: {info['total_pieces']}")
        print(f"  Complexity: {info['complexity']}")
        print(f"  Solved: {info['is_solved']}")
        print(f"  Has tracker: {info['has_tracker']}")
        
        # Test tracker diagnostics for 3x3
        if size == 3:
            diagnostics = cube.get_tracker_diagnostics()
            print(f"  Tracker solved edges: {diagnostics['solved_edges']}/12")
            print(f"  Tracker solved corners: {diagnostics['solved_corners']}/8")