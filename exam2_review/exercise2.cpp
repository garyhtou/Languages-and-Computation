#include <vector>
#include <math.h>
#include <algorithm>
#include <iostream>

using namespace std;

struct Point
{
	float x;
	float y;
};

// [=] (value)
// [&] (reference)
// [] (nothing)

int main()
{
	vector<Point> coordList{{1, 3}, {0.3, -0.9}, {-12, 0.1}, {21, 32}, {1, -1}, {2, 2}, {1, -4}};

	Point p;
	p.x = 5;
	p.y = 6;
	coordList.push_back(p);

	Point p2;
	p2.x = 3;
	p2.y = 2;
	coordList.push_back(p2);

	sort(coordList.begin(), coordList.end(), [](Point a, Point b)
			 { return sqrt(pow(a.x, 2) + pow(a.y, 2)) < sqrt(pow(b.x, 2) + pow(b.y, 2)); });

	for_each(coordList.begin(), coordList.end(),
					 [](Point a)
					 { cout << "(" << a.x << ", " << a.y << ")" << endl; });

	return 0;
}