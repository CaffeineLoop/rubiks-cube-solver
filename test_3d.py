"""
3D Visualization Diagnostic Tool
This will tell us exactly what's wrong with your 3D setup
"""

import sys
print("Python version:", sys.version)
print("="*50)

# Test 1: Basic imports
print("1. TESTING IMPORTS:")
try:
    import pygame
    print("✓ pygame imported successfully")
    print(f"  pygame version: {pygame.version.ver}")
except ImportError as e:
    print(f"✗ pygame import failed: {e}")
    print("  FIX: pip install pygame")
    sys.exit(1)

try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
    print("✓ OpenGL imported successfully")
except ImportError as e:
    print(f"✗ OpenGL import failed: {e}")
    print("  FIX: pip install PyOpenGL PyOpenGL_accelerate")
    sys.exit(1)

# Test 2: Pygame initialization
print("\n2. TESTING PYGAME INITIALIZATION:")
try:
    pygame.init()
    print("✓ pygame.init() successful")
except Exception as e:
    print(f"✗ pygame.init() failed: {e}")
    sys.exit(1)

# Test 3: Display system
print("\n3. TESTING DISPLAY SYSTEM:")
try:
    pygame.display.init()
    print("✓ Display system initialized")
    
    # Get available display modes
    modes = pygame.display.list_modes()
    print(f"  Available display modes: {len(modes)} modes found")
    
    # Get display driver
    driver = pygame.display.get_driver()
    print(f"  Display driver: {driver}")
    
except Exception as e:
    print(f"✗ Display system failed: {e}")
    sys.exit(1)

# Test 4: Basic display creation
print("\n4. TESTING BASIC DISPLAY:")
try:
    screen = pygame.display.set_mode((200, 200))
    print("✓ Basic display created successfully")
    pygame.display.quit()
except Exception as e:
    print(f"✗ Basic display failed: {e}")
    print("  This indicates a serious graphics system problem")
    sys.exit(1)

# Test 5: OpenGL display creation
print("\n5. TESTING OPENGL DISPLAY:")
try:
    # Set minimal OpenGL attributes
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 2)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 1)
    pygame.display.gl_set_attribute(pygame.GL_DOUBLEBUFFER, 1)
    
    # Create OpenGL display
    screen = pygame.display.set_mode((400, 300), pygame.DOUBLEBUF | pygame.OPENGL)
    print("✓ OpenGL display created successfully")
    
    # Test OpenGL context
    version = glGetString(GL_VERSION)
    if version:
        print(f"✓ OpenGL version: {version.decode()}")
    else:
        print("✗ No OpenGL version returned")
        
    renderer = glGetString(GL_RENDERER)
    if renderer:
        print(f"  Graphics card: {renderer.decode()}")
        
    # Clean up
    pygame.display.quit()
    
except Exception as e:
    print(f"✗ OpenGL display failed: {e}")
    print("  This is likely your main problem")

print("\n" + "="*50)
print("DIAGNOSTIC COMPLETE")
print("="*50)

# Test 6: Simple 3D test
print("\n6. RUNNING SIMPLE 3D TEST:")
choice = input("Run a simple 3D window test? (y/n): ").lower().strip()

if choice == 'y':
    try:
        # Create window
        screen = pygame.display.set_mode((400, 300), pygame.DOUBLEBUF | pygame.OPENGL)
        pygame.display.set_caption("3D Test - Press ESC to exit")
        
        # Set up OpenGL
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.0, 0.0, 0.5, 1.0)  # Blue background
        
        # Set up camera
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 400/300, 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -5.0)
        
        # Main loop
        clock = pygame.time.Clock()
        rotation = 0
        running = True
        
        print("✓ 3D window opened successfully!")
        print("  You should see a rotating white triangle")
        print("  Press ESC to close")
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
            
            # Clear and draw
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
            glPushMatrix()
            glRotatef(rotation, 0, 1, 0)
            
            # Draw a simple triangle
            glColor3f(1.0, 1.0, 1.0)  # White
            glBegin(GL_TRIANGLES)
            glVertex3f(0.0, 1.0, 0.0)
            glVertex3f(-1.0, -1.0, 0.0)
            glVertex3f(1.0, -1.0, 0.0)
            glEnd()
            
            glPopMatrix()
            
            pygame.display.flip()
            rotation += 1
            clock.tick(60)
        
        pygame.quit()
        print("✓ 3D test completed successfully!")
        print("  Your 3D system is working!")
        
    except Exception as e:
        print(f"✗ 3D test failed: {e}")
        pygame.quit()

print("\nIf you reached this point, your 3D system should be working.")
print("The problem might be in your Rubik's cube visualizer code.")
