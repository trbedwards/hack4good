#include <stdio.h>
#include <math.h>
#include <GL/glut.h>
#include <GL/freeglut.h>
#include <GL/freeglut_ext.h>
#include <GL/freeglut_std.h>

// position and direction for the camera
float theta = 0.0f, phi = 0.0f;
float cx = 5.0f, cy = 100.0f, cz = 0.0f;
float lx = 1.0f, ly = 0.0f, lz = 0.0f;
// status flags indicating movement
float dtheta = 0.0f, dphi = 0.0f, dMove = 0.0f;

// take care of perspective
void changeSize(int w, int h){
  float ratio;
  // Prevent a divide by zero
  if(h == 0) h = 1;
  ratio = ((float) w) / h;
  // Use the projection matrix
  glMatrixMode(GL_PROJECTION);
  // Reset matrix
  glLoadIdentity();
  // set the viewport to be the entire window
  // numbers relative to the client window, not the screen 
  glViewport(0,0,w,h);
  // set the correct perspective
  // field of view parameter in the yz plane
  //   determines the angle of the lens, smaller = zoomed in
  // ratio width to heigh of the viewport
  // near and far clipping planes
  gluPerspective(75.0f,ratio,1.0f,100.0f);
  // get back to the model view
  // model view used for setting the camera and transforming objects
  glMatrixMode(GL_MODELVIEW);
}

void processNormalKeys(unsigned char key, int x, int y){
  switch(key){
    case 27: exit(0); break;
    case 97: dMove = 0.5f; break; // a
    case 115: dMove = -0.5f; break; // s
  }
}

void processSpecialKeys(int key, int x, int y){
  switch(key){
    case GLUT_KEY_LEFT: dtheta = 0.1f; break;
    case GLUT_KEY_RIGHT: dtheta = -0.1f; break;
    case GLUT_KEY_UP : dphi = 0.1f; break;
    case GLUT_KEY_DOWN : dphi = -0.1f; break;
  }
}

void releaseNormalKeys(unsigned char key, int x, int y){
  switch(key){
    case 97: dMove = 0.0f; break;
    case 115: dMove = 0.0f; break;
  }
}

void releaseSpecialKeys(int key, int x, int y){
  switch(key){
	case GLUT_KEY_LEFT: dtheta = 0.0f; break;
	case GLUT_KEY_RIGHT: dtheta = 0.0f; break;
	case GLUT_KEY_UP: dphi = 0.0f; break;
	case GLUT_KEY_DOWN: dphi = 0.0f; break;
  }
}

void drawSnowman(){
  glColor3f(1.0f, 1.0f, 1.0f);
  // Draw body
  glTranslatef(0.0f, 0.75f, 0.0f);
  glutSolidSphere(0.75f, 20, 20);
  // Draw head
  glTranslatef(0.0f, 0.92f, 0.0f);
  glutSolidSphere(0.25f, 20, 20);
  // Draw eyes
  glPushMatrix();
  glColor3f(0.0f, 0.0f, 0.0f);
  glTranslatef(0.05f, 0.10f, 0.18f);
  glutSolidSphere(0.05f,10,10);
  glTranslatef(-0.1f, 0.0f,0.0f);
  glutSolidSphere(0.05f,10,10);
  glPopMatrix();
  // Draw nose
  glColor3f(1.0f, 0.5f, 0.5f);
  glutSolidCone(0.08f, 0.5f, 10, 2);
}

void computeDir(){
  // If dAngle is an argument, in this scope it's 2, why..?
  theta += dtheta;
  phi += dphi;
  lx =  cos(theta)*cos(phi);
  ly =  sin(phi);
  lz = -sin(theta)*cos(phi);
}

void computePos(){
  cx += dMove * lx;
  cy += dMove * ly;
  cz += dMove * lz;
}

int glutMain(int argc, char **argv){
  glutInit(&argc, argv);
  glutInitWindowPosition(100,100);
  glutInitWindowSize(320,320);
  glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH);
  glutCreateWindow("Solar Irradiance Simulation");
  
  // Register callbacks
  // called when the window changes size with the new window dim as params
  glutReshapeFunc(changeSize);
  glutKeyboardFunc(processNormalKeys);
  glutSpecialFunc(processSpecialKeys);
  glutIgnoreKeyRepeat(1);
  glutKeyboardUpFunc(releaseNormalKeys);
  glutSpecialUpFunc(releaseSpecialKeys);

  // depth buffer
  glEnable(GL_DEPTH_TEST);
  return 0;
}
