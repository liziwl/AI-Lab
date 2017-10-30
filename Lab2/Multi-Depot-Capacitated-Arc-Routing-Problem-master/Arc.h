#ifndef ARC_H
#define ARC_H

#include <iostream>
#include <vector>

using namespace std;

class Arc{
private:
	int start;
	int end;
	int demand;
	int weight;
public:
	Arc(int s, int e, int d, int w);
	int getDemand();
	int getWeight();
	int getStart();
	int getEnd();
};

Arc::Arc(int s, int e, int d, int w){ start = s; end = e; demand = d; weight = w;}
int Arc::getDemand(){return demand;}
int Arc::getWeight(){return weight;}
int Arc::getStart(){return start;}
int Arc::getEnd(){return end;}

#endif