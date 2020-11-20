#version 330

in vec2 vert;
in vec2 in_text;
out vec2 UV;

void main() {
   gl_Position = vec4(vert, 0.0, 1.0);

   UV = in_text;
 }
