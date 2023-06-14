#include "vector2d.h"
#include <iostream>
using algebra::Vec2d;
using std::cout;
using std::endl;
        
int main(){
    Vec2d v1 = Vec2d(2.1,2.2);
    Vec2d v2 = Vec2d(2.3,2.4);
    Vec2d v3 = v1+v2;
    cout << v3.x<<endl;
    cout << v3.y<<endl;
}