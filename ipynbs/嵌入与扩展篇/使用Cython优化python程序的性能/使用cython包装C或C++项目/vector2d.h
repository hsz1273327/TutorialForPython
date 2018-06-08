
namespace algebra {
    class Vec2d {
    public:
        double x, y;
        Vec2d();
        Vec2d(double x, double y);
        ~Vec2d();
        Vec2d operator+(const Vec2d& b);
        Vec2d operator*(double k);
        
    };
}