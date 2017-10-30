#ifndef PROBLEM_STRUCT_H
#define PROBLEM_STRUCT_H


#include <vector>
#include "Arc.h"
#include <map>
#include<iostream>
#include <assert.h>

using namespace std;

class ArcRouting{
private:
	int V; // Number of vertices or nodes
	int A;
	int Q;
	int K;

	vector<int> Ad; /*This will store the index of Arcs with demand > 0*/
	vector<Arc> Arcs; /*This will store the Arcs int the networks*/

	map<int, vector<int>> startMap; /*This will store the index of arcs (int Arcs vector) correspondin to their starting point*/
	map<int, vector<int>> endMap;   /*This will store the index of arcs (int Arcs vector) correspondin to their ending point*/

	void print();
public: 
	ArcRouting();
	ArcRouting(int inV, int inA, int inQ);
	ArcRouting(const string &file);
	int getVertices();
	int getArcs();
	int getTours();
	int getMaxCapacity();
	int getWForA(int a);
	int getDemandForA(int a);
	int getAfromAd(int i);
	int getSizeOfAd();
	vector<int> getDeltaPlus(int i);
	vector<int> getDeltaMinus(int i);
};
ArcRouting::ArcRouting(){}

ArcRouting::ArcRouting(int inV, int inA, int inQ){
	V = inV;
	A = inA;
	Q = inQ;
}
void ArcRouting::print(){
	cout << "############### START MAP ##############"  << endl;
	for(int i = 0; i < V; i++){
		assert(startMap.find(i) != startmap.end());
		cout << "Start At : " << i;
		for(int j = 0; j < startMap[i].size(); j++){
			Arc a = Arcs[startMap[i][j]];
			/*if(find(endMap[a.getEnd()].begin(), endMap[a.getEnd()].end(), i) != endMap[a.getEnd()].end()){
				cout  << "  true" ;
			}else{
				cout  << "  false" ;
			}
			assert((find(endMap[a.getEnd()].begin(), endMap[a.getEnd()].end(), 0) != endMap[a.getEnd()].end()) == -1);
			*/
			cout << "  " << a.getEnd(); 
		}
		cout << endl;
	}
	cout << "############### END MAP ##############"  << endl;
	for(int i = 0; i < V; i++){
		cout << "End At : " << i;
		for(int j = 0; j < endMap[i].size(); j++){
			cout << "  " <<Arcs[endMap[i][j]].getStart(); 
		}
		cout << endl;
	}

	cout << "################# TEST ###################" << endl;
	/*
	for(int i = 0; i < V; i++){
		vector<int> ret = getDeltaPlus(10);
		for(int i = 0; i < ret.size(); i++){
			cout << Arcs[ret[i]].getEnd() << " ";
		}
		cout << endl;
	}
	*/
}
ArcRouting::ArcRouting(const string &file){
	cout << "Parsing the file : " << file << endl;
	ifstream inFile(file.c_str(), ios::in);
	if (! inFile){
		cerr << "unable to open input file: "<< file << " --bailing out! \n";
		return;
	}
	int i = 0;
	int arcCounter = 0;
	bool flag = false;
	while(!inFile.eof()){
		assert(inFile.good());
		string this_line;
		getline(inFile, this_line);
		if(i == 0){
			sscanf (this_line.c_str(),"nodes:=DATA{0..%d};",&V);
			V++;
			cout << "V = " << V << endl;
		}else if(i == 1){
			sscanf (this_line.c_str(),"routes:=DATA{0..%d};",&K);
			K++;
			cout << "K = " << K << endl;
		}else if(i == 2){
			sscanf (this_line.c_str(),"C:=%d;",&Q);
			cout << "Q = " << Q << endl;
		}else{
			if(flag){
				if(this_line.find(";")!= std::string::npos){
					break;
				}
				int i, j, d, w;
				sscanf (this_line.c_str(),"%d%d%d%d",&i,&j,&d,&w);
				Arc arc(i,j,d,w);
				Arcs.push_back(arc);
				startMap[i].push_back(arcCounter);
				endMap[j].push_back(arcCounter);
				if(d > 0) { Ad.push_back(arcCounter);}
				cout << i <<"  "<< j <<"  " << d <<"  " << w <<"  " << endl;
				arcCounter++;
			}else{
				if(this_line.find("!----- ----- ---------- ----------")!= std::string::npos){
					flag = true;
					std::cout<<"true"<<std::endl;
				}
			}
		}
		i++;
	}
	assert(Arcs.size() != arcCounter);

	print();
	cout << "END PARSING" << endl;

}

int ArcRouting::getVertices(){return V;}
int ArcRouting::getArcs(){return Arcs.size();}
int ArcRouting::getMaxCapacity(){return Q;}
int ArcRouting::getTours(){return K;}

int ArcRouting::getAfromAd(int i){
	return Ad[i];
}

int ArcRouting::getSizeOfAd(){
	return static_cast<int>(Ad.size());
}

int ArcRouting::getWForA(int a){
	return Arcs[a].getWeight();
}

int ArcRouting::getDemandForA(int a){
	return Arcs[a].getDemand();
}

vector<int> ArcRouting::getDeltaPlus(int i){
	return startMap[i];
}
vector<int> ArcRouting::getDeltaMinus(int i){
	return endMap[i];
}

#endif