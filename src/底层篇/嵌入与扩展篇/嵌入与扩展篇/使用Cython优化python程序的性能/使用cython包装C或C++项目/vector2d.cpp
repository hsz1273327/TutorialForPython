#include "vector2d.h"

namespace algebra {

    Vec2d::Vec2d() {
        x=0;
        y=0;
    }

    Vec2d::Vec2d(double x, double y) {
        this->x = x;
        this->y = y;
    }

    Vec2d::~Vec2d() { }
    
    Vec2d Vec2d::operator+(const Vec2d& other){

        Vec2d r = Vec2d(this->x+other.x,this->y+other.y);
        return r;
    }
    Vec2d Vec2d::operator*(double k){
        Vec2d r = Vec2d(this->x*k,this->y*k);
        return r;
    }
}