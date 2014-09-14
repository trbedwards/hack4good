#include "glutMain.h"

void renderScene(void){
  //clear color and depth buffers
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
  //reset transformations
  glLoadIdentity();

  computeDir();
  computePos();
  
  // Set the camera
  // Default is at the origin and faces +z
  // 3 vectors: position, line-of-sight, orientation
  gluLookAt(	cx, cy, cz,
		cx+lx, cy+ly,  cz+lz,
		0.0f, 1.0f,  0.0f);
  // Draw brown ground
  glColor3f(0.9f, 0.9f, 0.9f);
  glBegin(GL_QUADS);
    glVertex3f(   0.0f, 0.0f,    0.0f);
    glVertex3f(   0.0f, 0.0f,  100.0f);
    glVertex3f( 100.0f, 0.0f,  100.0f);
    glVertex3f( 100.0f, 0.0f,    0.0f);
  glEnd();
  //draw
  %(triangulate)s
  glutSwapBuffers();
}

int main(int argc, char **argv){
  glutMain(argc, argv);
  glutDisplayFunc(renderScene);
  glutIdleFunc(renderScene);
  // enter GLUT event processing loop
  glutMainLoop();
  return 1;
}

