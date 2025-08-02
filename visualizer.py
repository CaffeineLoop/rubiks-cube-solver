"""
Multi-Size Rubik's Cube Visualizer - COMPLETE FIXED VERSION
Supports 2x2, 3x3, 4x4, and larger cube sizes with proper colors and sizing
"""

try:
    import pygame
    from pygame.locals import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
    import math
    import time
    VISUALIZATION_AVAILABLE = True
    print("✓ All 3D dependencies imported successfully")
except ImportError:
    print("Warning: pygame and/or OpenGL not available. Install with:")
    print("pip install pygame PyOpenGL PyOpenGL_accelerate")
    VISUALIZATION_AVAILABLE = False

from rubiks_cube import RubiksCube

class SimpleVisualizer:
    """Text-based 2D cube visualization - works with any cube size"""
    
    def __init__(self, cube):
        """Initialize simple text-based visualizer"""
        self.cube = cube
        self.color_chars = {
            0: 'W',  # White
            1: 'Y',  # Yellow
            2: 'R',  # Red
            3: 'O',  # Orange
            4: 'G',  # Green
            5: 'B',  # Blue
        }
        print(f"✓ Text visualizer initialized for {cube.size}x{cube.size}x{cube.size} cube")
    
    def draw_unfolded_cube(self):
        """Draw cube in unfolded 2D format - adapts to cube size"""
        size = self.cube.size
        
        print(f"\n" + "="*60)
        print(f"           {size}x{size}x{size} CUBE STATE")
        print("="*60)
        
        # Top face (Up) - face index 4
        print(f"{'':>{size*3+8}}U P   F A C E")
        up_face = self.cube.cube[4]
        for row in up_face:
            print(f"{'':>{size*3+6}}", end="")
            for cell in row:
                print(f" {self.color_chars[cell]} ", end="")
            print()
        
        print()
        
        # Middle row: Left(3), Front(0), Right(2), Back(1)
        faces = [3, 0, 2, 1]
        labels = ["L E F T", "F R O N T", "R I G H T", "B A C K"]
        
        # Print face labels
        for label in labels:
            print(f" {label:^{size*3}}", end="")
        print()
        
        # Print face contents row by row
        for i in range(size):
            print(" ", end="")
            for face_idx in faces:
                for cell in self.cube.cube[face_idx][i]:
                    print(f" {self.color_chars[cell]} ", end="")
                print(" ", end="")
            print()
        
        print()
        
        # Bottom face (Down) - face index 5
        print(f"{'':>{size*3+6}}D O W N   F A C E")
        down_face = self.cube.cube[5]
        for row in down_face:
            print(f"{'':>{size*3+6}}", end="")
            for cell in row:
                print(f" {self.color_chars[cell]} ", end="")
            print()
        
        print("="*60)
        print(f"Cube size: {size}x{size}x{size} | Total stickers: {6 * size * size}")
    
    def animate_move(self, move):
        """Show before/after states for a move"""
        print(f"\nBEFORE {move} move:")
        self.draw_unfolded_cube()
        
        self.cube.execute_moves(move)
        
        print(f"\nAFTER {move} move:")
        self.draw_unfolded_cube()

class CubeVisualizer3D:
    """3D OpenGL cube visualization - COMPLETE FIXED VERSION"""
    
    def __init__(self, cube):
        """Initialize 3D visualizer for any cube size"""
        self.cube = cube
        self.available = VISUALIZATION_AVAILABLE
        
        # Color mapping for cube faces (RGB values)
        self.colors = {
            0: (1.0, 1.0, 1.0),    # White
            1: (1.0, 1.0, 0.0),    # Yellow
            2: (1.0, 0.0, 0.0),    # Red
            3: (1.0, 0.5, 0.0),    # Orange
            4: (0.0, 1.0, 0.0),    # Green
            5: (0.0, 0.0, 1.0),    # Blue
        }
        
        # View rotation variables
        self.rotation_x = 15
        self.rotation_y = 25
        
        # FIXED: Cube size dependent variables
        self.cube_size = self.cube.size
        self.cube_spacing = 2.2 / self.cube_size  # Proper spacing based on size
        self.small_cube_size = 1.8 / self.cube_size  # Proper individual cube size
        
        print(f"✓ 3D visualizer initialized for {self.cube_size}x{self.cube_size}x{self.cube_size}")
        
        # Initialize 3D graphics if available
        if self.available:
            try:
                self.init_3d()
            except Exception as e:
                print(f"✗ 3D initialization failed: {e}")
                self.available = False
    
    def init_3d(self):
        """Initialize pygame and OpenGL for 3D rendering"""
        pygame.init()
        pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
        pygame.display.set_caption(f"Rubik's Cube 3D - {self.cube_size}x{self.cube_size}x{self.cube_size}")
        
        # Enable OpenGL features
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.1, 0.1, 0.1, 1.0)
        
        # FIXED: Adjust camera distance based on cube size
        camera_distance = -6 - (self.cube_size * 1.0)
        
        # Set up 3D perspective
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (800 / 600), 0.1, 50.0)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, camera_distance)
        
        print("✓ 3D graphics initialized successfully")
    
    def get_cube_face_color(self, cube_x, cube_y, cube_z, face_direction):
        """FIXED: Map 3D position to actual cube state colors - ALL 6 COLORS"""
        size = self.cube_size
        
        try:
            # Convert cube coordinates to array indices
            def to_array_index(coord):
                """Convert cube coordinate to array index (0 to size-1)"""
                if size % 2 == 1:  # Odd sizes (3x3, 5x5)
                    return coord + size // 2
                else:  # Even sizes (2x2, 4x4)
                    return coord + size // 2
            
            # Calculate the actual boundary values for this cube size
            if size % 2 == 1:  # Odd sizes
                min_coord = -(size // 2)
                max_coord = size // 2
            else:  # Even sizes
                min_coord = -(size // 2)
                max_coord = (size // 2) - 1
            
            # FIXED: Proper boundary detection for all cube sizes
            if face_direction == 'front' and cube_z == max_coord:
                # Front face (index 0) - GREEN
                row = size - 1 - to_array_index(cube_y)
                col = to_array_index(cube_x)
                if 0 <= row < size and 0 <= col < size:
                    color_id = self.cube.cube[0][row][col]
                    return self.colors[color_id]
                    
            elif face_direction == 'back' and cube_z == min_coord:
                # Back face (index 1) - BLUE
                row = size - 1 - to_array_index(cube_y)
                col = size - 1 - to_array_index(cube_x)
                if 0 <= row < size and 0 <= col < size:
                    color_id = self.cube.cube[1][row][col]
                    return self.colors[color_id]
                    
            elif face_direction == 'right' and cube_x == max_coord:
                # Right face (index 2) - RED
                row = size - 1 - to_array_index(cube_y)
                col = to_array_index(cube_z)
                if 0 <= row < size and 0 <= col < size:
                    color_id = self.cube.cube[2][row][col]
                    return self.colors[color_id]
                    
            elif face_direction == 'left' and cube_x == min_coord:
                # Left face (index 3) - ORANGE
                row = size - 1 - to_array_index(cube_y)
                col = size - 1 - to_array_index(cube_z)
                if 0 <= row < size and 0 <= col < size:
                    color_id = self.cube.cube[3][row][col]
                    return self.colors[color_id]
                    
            elif face_direction == 'up' and cube_y == max_coord:
                # Up face (index 4) - YELLOW
                row = size - 1 - to_array_index(cube_z)
                col = to_array_index(cube_x)
                if 0 <= row < size and 0 <= col < size:
                    color_id = self.cube.cube[4][row][col]
                    return self.colors[color_id]
                    
            elif face_direction == 'down' and cube_y == min_coord:
                # Down face (index 5) - WHITE
                row = to_array_index(cube_z)
                col = to_array_index(cube_x)
                if 0 <= row < size and 0 <= col < size:
                    color_id = self.cube.cube[5][row][col]
                    return self.colors[color_id]
            
        except (IndexError, ValueError):
            pass
        
        # Interior faces should be dark gray
        return (0.2, 0.2, 0.2)
    
    def draw_cube_face(self, face_positions, color):
        """Draw a single face of a small cube with the given color"""
        try:
            # Draw filled face
            glColor3fv(color)
            glBegin(GL_QUADS)
            for position in face_positions:
                glVertex3fv(position)
            glEnd()
            
            # Draw black edges for definition
            glColor3f(0.0, 0.0, 0.0)
            glLineWidth(2)
            glBegin(GL_LINE_LOOP)
            for position in face_positions:
                glVertex3fv(position)
            glEnd()
        except Exception:
            pass
    
    def draw_small_cube(self, x, y, z, cube_x, cube_y, cube_z):
        """Draw a single small cube with proper colors from cube state"""
        half_size = self.small_cube_size / 2
        
        # Define the 6 faces of the cube
        faces = [
            # Front face
            ([(x-half_size, y-half_size, z+half_size),
              (x+half_size, y-half_size, z+half_size),
              (x+half_size, y+half_size, z+half_size),
              (x-half_size, y+half_size, z+half_size)], 'front'),
            
            # Back face
            ([(x+half_size, y-half_size, z-half_size),
              (x-half_size, y-half_size, z-half_size),
              (x-half_size, y+half_size, z-half_size),
              (x+half_size, y+half_size, z-half_size)], 'back'),
            
            # Right face
            ([(x+half_size, y-half_size, z+half_size),
              (x+half_size, y-half_size, z-half_size),
              (x+half_size, y+half_size, z-half_size),
              (x+half_size, y+half_size, z+half_size)], 'right'),
            
            # Left face
            ([(x-half_size, y-half_size, z-half_size),
              (x-half_size, y-half_size, z+half_size),
              (x-half_size, y+half_size, z+half_size),
              (x-half_size, y+half_size, z-half_size)], 'left'),
            
            # Top face
            ([(x-half_size, y+half_size, z+half_size),
              (x+half_size, y+half_size, z+half_size),
              (x+half_size, y+half_size, z-half_size),
              (x-half_size, y+half_size, z-half_size)], 'up'),
            
            # Bottom face
            ([(x-half_size, y-half_size, z-half_size),
              (x+half_size, y-half_size, z-half_size),
              (x+half_size, y-half_size, z+half_size),
              (x-half_size, y-half_size, z+half_size)], 'down')
        ]
        
        # Draw each face with its actual color
        for face_vertices, direction in faces:
            color = self.get_cube_face_color(cube_x, cube_y, cube_z, direction)
            self.draw_cube_face(face_vertices, color)
    
    def draw_rubiks_cube(self):
        """FIXED: Draw the complete Rubik's cube with ALL 6 colors"""
        if not self.available:
            return
        
        try:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
            # Apply user rotation
            glPushMatrix()
            glRotatef(self.rotation_x, 1, 0, 0)
            glRotatef(self.rotation_y, 0, 1, 0)
            
            size = self.cube_size
            
            # FIXED: Proper coordinate calculation for any cube size
            if size % 2 == 1:  # Odd sizes (3x3, 5x5)
                coord_range = range(-(size//2), (size//2) + 1)
            else:  # Even sizes (2x2, 4x4)
                coord_range = range(-(size//2), size//2)
            
            for cube_x in coord_range:
                for cube_y in coord_range:
                    for cube_z in coord_range:
                        # 3D position for rendering
                        x = cube_x * self.cube_spacing
                        y = cube_y * self.cube_spacing
                        z = cube_z * self.cube_spacing
                        
                        self.draw_small_cube(x, y, z, cube_x, cube_y, cube_z)
            
            glPopMatrix()
            pygame.display.flip()
            
        except Exception as e:
            print(f"Drawing error: {e}")
    
    def handle_events(self):
        """Handle pygame events for user interaction"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE:
                    self.animate_scramble()
                elif event.key == pygame.K_r:
                    self.reset_view()
                elif event.key == pygame.K_u:
                    self.animate_move('U')
                elif event.key == pygame.K_d:
                    self.animate_move('D')
                elif event.key == pygame.K_l:
                    self.animate_move('L')
                elif event.key == pygame.K_f:
                    self.animate_move('F')
            elif event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    mouse_dx, mouse_dy = pygame.mouse.get_rel()
                    self.rotation_y += mouse_dx * 0.5
                    self.rotation_x += mouse_dy * 0.5
        
        return True
    
    def animate_move(self, move):
        """Animate a single move"""
        print(f"Executing move: {move} on {self.cube_size}x{self.cube_size}x{self.cube_size} cube")
        self.cube.execute_moves(move)
        
        # Simple visual feedback
        for frame in range(10):
            self.rotation_y += 1
            self.draw_rubiks_cube()
            pygame.time.wait(30)
    
    def animate_scramble(self):
        """Animate a scramble sequence"""
        size = self.cube_size
        moves = ['U', 'R', 'F', 'D', 'L', 'B']
        num_moves = min(size * 3, 15)  # Scale with cube size
        
        print(f"Scrambling {size}x{size}x{size} cube with {num_moves} moves...")
        
        for i in range(num_moves):
            move = moves[i % len(moves)]
            self.animate_move(move)
    
    def reset_view(self):
        """Reset the view rotation to default"""
        self.rotation_x = 15
        self.rotation_y = 25
        print("View reset")
    
    def run(self):
        """Main visualization loop"""
        if not self.available:
            print("3D visualization not available")
            return
        
        size = self.cube_size
        print(f"\n=== 3D {size}x{size}x{size} Rubik's Cube Visualizer ===")
        print("Controls:")
        print("  Mouse drag: Rotate view")
        print("  SPACE: Animate scramble")
        print("  U/D/L/F: Execute moves")
        print("  R: Reset view")
        print("  ESC: Exit")
        print("=" * 50)
        
        clock = pygame.time.Clock()
        running = True
        
        while running:
            running = self.handle_events()
            self.draw_rubiks_cube()
            clock.tick(60)
        
        pygame.quit()
        print(f"3D visualizer closed for {size}x{size}x{size} cube")

def demo_visualization():
    """Demonstrate visualization with different cube sizes"""
    print("=== Multi-Size Rubik's Cube Visualization Demo ===")
    
    # Test different cube sizes
    sizes_to_test = [2, 3, 4]
    
    for size in sizes_to_test:
        print(f"\n=== Testing {size}x{size}x{size} Cube Visualization ===")
        
        # Create a cube for demonstration
        cube = RubiksCube(size=size)
        
        # Always available: text visualization
        print(f"\n1. Text-based visualization for {size}x{size}x{size} cube:")
        simple_viz = SimpleVisualizer(cube)
        simple_viz.draw_unfolded_cube()
        
        # Test some moves with text visualization
        print(f"\n2. Testing moves with {size}x{size}x{size} text visualization:")
        test_move = 'U'
        input(f"Press Enter to execute {test_move} move on {size}x{size}x{size} cube...")
        simple_viz.animate_move(test_move)
        
        # 3D visualization if available
        print(f"\n3. 3D Visualization for {size}x{size}x{size} cube:")
        if VISUALIZATION_AVAILABLE:
            choice = input(f"Launch 3D visualization for {size}x{size}x{size} cube? (y/n): ").strip().lower()
            if choice == 'y':
                viz_3d = CubeVisualizer3D(cube)
                if viz_3d.available:
                    viz_3d.run()
                else:
                    print("3D visualization failed to initialize")
        else:
            print("3D visualization not available.")
            print("Install with: pip install pygame PyOpenGL PyOpenGL_accelerate")

if __name__ == "__main__":
    try:
        # Launch demonstration
        demo_visualization()
        
    except KeyboardInterrupt:
        print("\nDemo interrupted. Goodbye!")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please check your installation and try again.")
