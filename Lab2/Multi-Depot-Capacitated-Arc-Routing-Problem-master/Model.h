#ifndef MODEL
#define MODEL

#include <ilcplex/ilocplex.h>
#include "ProblemSet.h"

using namespace std;

ArcRouting arcRouting;
int K;		/* Tours */
int A;		/* Arcs	*/
int Ad;		/* Arcs with demand > 0 */
int Q;	    /* Capacity */
int V;		/* Vertexes */

string num2string(int i){
	return to_string(i);
}


int getVariableIndex(const string type, int a, int k){
	if(type == "z"){
		return A*(k) + a+1;
	}else if(type == "x"){
		return A*K + A*(k) + a+1;
	}else if(type == "u"){
		return A*K*2 + A*k + a+1;
	}else if(type == "y"){
		return 3*A*K + V*k + a+1;
	}
}

static int PopulateByColumn (CPXCENVptr env, CPXLPptr lp) {
	int status = 0;

	CPXDIM ccnt = 1;
	vector<double> obj(1,0), ub(1,0), lb(1,0);
	vector<char> xctype(1,'C'); // C means continous variable
	vector<string> cname(1,"DUMMY");

	/*Defining variable z(a,k)*/
	for(int k = 0; k < K; k++){
		for(int a = 0; a < A; a++){
			obj.push_back(arcRouting.getWForA(a));
			lb.push_back(0);			/* z(a,k) lower bound should be zero as it should be positive*/
			ub.push_back(CPX_INFBOUND); /* z(a,k) upper bound can be infinity*/
			xctype.push_back('I');		/* variable should be positive integer*/ //TODO change B to make it Integer
			cname.push_back((std::string)("z("+num2string(a)+","+num2string(k)+")"));
			if(ccnt != getVariableIndex("z", a, k)){
				cout << "CCNT " << ccnt << " INDEX " << getVariableIndex("z", a, k);
				system("PAUSE");
			}
			ccnt++;
		}
		cout << "cnt " << ccnt << endl;
	}
	/*Defining variable x(a,k)*/
	for(int k = 0; k < K; k++){
		for(int a = 0; a < A; a++){
			obj.push_back(0);
			lb.push_back(0);
			ub.push_back(1);
			xctype.push_back('B');		/* variable should be positive integer*/
			cname.push_back((std::string)("x("+num2string(a)+","+num2string(k)+")"));
			if(ccnt != getVariableIndex("x", a, k)){
				cout << "CCNT " << ccnt << " INDEX " << getVariableIndex("x", a, k);
				system("PAUSE");
			}
			ccnt++;
		}
		cout << "cnt " << ccnt << endl;
	}

	/*Defining variable u(a,k)*/
	for(int k = 0; k < K; k++){
		for(int a = 0; a < A; a++){
			obj.push_back(0);
			lb.push_back(0);
			ub.push_back(1);
			xctype.push_back('B');		/* variable should be positive integer*/
			cname.push_back((std::string)("u("+num2string(a)+","+num2string(k)+")"));
			if(ccnt != getVariableIndex("u", a, k)){
				cout << "CCNT " << ccnt << " INDEX " << getVariableIndex("u", a, k);
				system("PAUSE");
			}
			ccnt++;
		}
		cout << "cnt " << ccnt << endl;
	}
	cout << "adding varible y" << endl;
	/*Defining variable y(i,k)*/
	for(int k = 0; k < K; k++){
		for(int i = 0; i < V; i++){
			obj.push_back(0);
			lb.push_back(0);
			ub.push_back(CPX_INFBOUND);
			xctype.push_back('I');		/* variable should be positive integer*/
			cname.push_back((std::string)("y("+num2string(i)+","+num2string(k)+")"));
			if(ccnt != getVariableIndex("y", i, k)){
				cout << "CCNT " << ccnt << " INDEX " << getVariableIndex("y", i, k);
				system("PAUSE");
			}
			ccnt++;
		}
		cout << "cnt " << ccnt << endl;
	}

	assert((int)obj.size()==ccnt); 
	assert(lb.size()==ccnt); 
	assert(ub.size()==ccnt);
	assert(xctype.size()==ccnt);
	assert(cname.size()==ccnt);

	/* Add columns to problem */
	std::vector< const char*> colname; 
	for(size_t i=0; i<cname.size(); i++) {
		colname.push_back(cname[i].c_str());
	}
	// this statement is used to feed the variables to CPLEX
	status = CPXXnewcols(env, lp, ccnt, &obj[0], &lb[0], &ub[0], &xctype[0], &colname[0]);
	return status;
}
/* Constraint (1)
sum((a), da*x(a,k)) <= Q for all k in K
*/
static int Capacity_Limiting_Constraint(CPXCENVptr env, CPXLPptr lp) {

	CPXDIM rcnt  = 0; 
	CPXNNZ nzcnt = 0;
	std::vector<double>		 rhs, rmatval;
	std::vector<char>		 sense; 
	std::vector<std::string> rname;
	std::vector<CPXDIM>		 rmatind;
	std::vector<CPXNNZ>		 rmatbeg(1,0);

	for(int k = 0; k < K; k++){
		rcnt++;
		rhs.push_back(Q);
		sense.push_back('L');
		nzcnt += A;
		rname.push_back("CapacityLimitingConstraint(" +num2string(k)+ ")");
		for(int a = 0; a < A; a++){
			//	cout << a  << "  " << k << " " << getVariableIndex("x",a,k) << endl;
			rmatind.push_back(getVariableIndex("x",a,k));
			//	cout << "demand " <<  arcRouting.getDemandForA(a) << endl;
			rmatval.push_back(arcRouting.getDemandForA(a));
		}
		rmatbeg.push_back(rmatind.size());
	}

	/* Check consistency of arguments */
	const int numrows = K, numnzs = K*A;
	assert(rcnt==numrows); assert(nzcnt==numnzs);
	assert((int)rhs.size()==rcnt); assert(sense.size()==rhs.size()); assert(rname.size()==rhs.size());
	assert((int)rmatind.size()==nzcnt); assert(rmatval.size()==rmatind.size());
	rmatbeg.pop_back(); assert(rmatbeg.size()==rhs.size());

	/* Add constraints to problem */
	std::vector< const char*> rowname; for(size_t i=0; i<rname.size(); i++) rowname.push_back(rname[i].c_str());
	int status = CPXXaddrows(env, lp, 0, rcnt, nzcnt, &rhs[0], &sense[0], &rmatbeg[0], &rmatind[0], &rmatval[0], nullptr, &rowname[0]);
	return status;
}

/*
Constraint-3
sum((k) , x(a,k)) = 1 for a belongs to Ad
*/
static int Ensure_Demand_Arc_Served(CPXCENVptr env, CPXLPptr lp) {

	CPXDIM rcnt  = 0; 
	CPXNNZ nzcnt = 0;
	std::vector<double>		 rhs, rmatval;
	std::vector<char>		 sense; 
	std::vector<std::string> rname;
	std::vector<CPXDIM>		 rmatind;
	std::vector<CPXNNZ>		 rmatbeg(1,0);

	for(int a = 0; a < Ad; a++){
		rcnt++;
		rhs.push_back(1);
		sense.push_back('E');

		nzcnt += K;
		rname.push_back("EnsureDemandArcServed(" +num2string(arcRouting.getAfromAd(a))+ ")");
		for(int k = 0; k < K; k++){
			rmatind.push_back(getVariableIndex("x",arcRouting.getAfromAd(a),k));
			rmatval.push_back(1);
		}
		rmatbeg.push_back(rmatind.size());
	}

	/* Check consistency of arguments */
	const int numrows = K, numnzs = K*Ad;
	assert(rcnt==numrows); assert(nzcnt==numnzs);
	assert((int)rhs.size()==rcnt); assert(sense.size()==rhs.size()); assert(rname.size()==rhs.size());
	assert((int)rmatind.size()==nzcnt); assert(rmatval.size()==rmatind.size());
	rmatbeg.pop_back(); assert(rmatbeg.size()==rhs.size());

	/* Add constraints to problem */
	std::vector< const char*> rowname; for(size_t i=0; i<rname.size(); i++) rowname.push_back(rname[i].c_str());
	int status = CPXXaddrows(env, lp, 0, rcnt, nzcnt, &rhs[0], &sense[0], &rmatbeg[0], &rmatind[0], &rmatval[0], nullptr, &rowname[0]);
	return status;
}

/*
Constraint-4
sum((a+) , z(a+(i),k)) - sum((a-) z(a-(i), k)) = 0 for i from V and k from K
*/
static int Flow_Constraint(CPXCENVptr env, CPXLPptr lp) {

	CPXDIM rcnt  = 0; 
	CPXNNZ nzcnt = 0;
	std::vector<double>		 rhs, rmatval;
	std::vector<char>		 sense; 
	std::vector<std::string> rname;
	std::vector<CPXDIM>		 rmatind;
	std::vector<CPXNNZ>		 rmatbeg(1,0);

	for(int k = 0; k < K; k++){
		for(int i = 0; i < V ; i++){
			rcnt++;
			rhs.push_back(0);
			sense.push_back('E');
			rname.push_back("FlowConstraint(tour:" +num2string(k) + ",vertex" + num2string(i) + ")");
			vector<int> dplus = arcRouting.getDeltaPlus(i);
			vector<int> dminus = arcRouting.getDeltaMinus(i);

			nzcnt += dplus.size() + dminus.size();
			for(int a = 0; a < dplus.size(); a++){
				rmatind.push_back(getVariableIndex("z",dplus[a],k));
				rmatval.push_back(1);
			}
			for(int a = 0; a < dminus.size(); a++){
				rmatind.push_back(getVariableIndex("z",dminus[a],k));
				rmatval.push_back(-1);
			}
			rmatbeg.push_back(rmatind.size());
		}
	}

	/* Check consistency of arguments */
	const int numrows = K*V, numnzs = K*V; // TODO add a factor for dplus and dminus for aserts
	assert(rcnt==numrows);// assert(nzcnt==numnzs);
	assert((int)rhs.size()==rcnt); assert(sense.size()==rhs.size()); assert(rname.size()==rhs.size());
	assert((int)rmatind.size()==nzcnt); assert(rmatval.size()==rmatind.size());
	rmatbeg.pop_back(); assert(rmatbeg.size()==rhs.size());

	/* Add constraints to problem */
	std::vector< const char*> rowname; for(size_t i=0; i<rname.size(); i++) rowname.push_back(rname[i].c_str());
	int status = CPXXaddrows(env, lp, 0, rcnt, nzcnt, &rhs[0], &sense[0], &rmatbeg[0], &rmatind[0], &rmatval[0], nullptr, &rowname[0]);
	return status;
}

/*
Constraint-5
x(a,k) <= z(a,k) a from Ad and k from K
*/
static int Traversed_Demand_Arc_Constraint(CPXCENVptr env, CPXLPptr lp) {

	CPXDIM rcnt  = 0; 
	CPXNNZ nzcnt = 0;
	std::vector<double>		 rhs, rmatval;
	std::vector<char>		 sense; 
	std::vector<std::string> rname;
	std::vector<CPXDIM>		 rmatind;
	std::vector<CPXNNZ>		 rmatbeg(1,0);

	for(int k = 0; k < K; k++){
		for(int a = 0; a < Ad ; a++){
			rcnt++;
			rhs.push_back(0);
			sense.push_back('L');
			nzcnt += 2;
			rmatind.push_back(getVariableIndex("x",arcRouting.getAfromAd(a),k));
			rmatval.push_back(1);
			rmatind.push_back(getVariableIndex("z",arcRouting.getAfromAd(a),k));
			rmatval.push_back(-1);
			rname.push_back("TraversedDemandArcConstraint(tour:" +num2string(k) + ",vertex" + num2string(a) + ")");
			rmatbeg.push_back(rmatind.size());

		}
	}

	/* Check consistency of arguments */
	const int numrows = K*Ad, numnzs = K*Ad*2;
	assert(rcnt==numrows);// assert(nzcnt==numnzs);
	assert((int)rhs.size()==rcnt); assert(sense.size()==rhs.size()); assert(rname.size()==rhs.size());
	assert((int)rmatind.size()==nzcnt); assert(rmatval.size()==rmatind.size());
	rmatbeg.pop_back(); assert(rmatbeg.size()==rhs.size());

	/* Add constraints to problem */
	std::vector< const char*> rowname; for(size_t i=0; i<rname.size(); i++) rowname.push_back(rname[i].c_str());
	int status = CPXXaddrows(env, lp, 0, rcnt, nzcnt, &rhs[0], &sense[0], &rmatbeg[0], &rmatind[0], &rmatval[0], nullptr, &rowname[0]);
	return status;
}

/*
Constraint-6
sum((a), u(a,k)) == 0 for k in K
*/
static int Traversed_Demand_Arc_Constraint(CPXCENVptr env, CPXLPptr lp) {

	CPXDIM rcnt  = 0; 
	CPXNNZ nzcnt = 0;
	std::vector<double>		 rhs, rmatval;
	std::vector<char>		 sense; 
	std::vector<std::string> rname;
	std::vector<CPXDIM>		 rmatind;
	std::vector<CPXNNZ>		 rmatbeg(1,0);

	for(int k = 0; k < K; k++){
		rcnt++;
		rhs.push_back(0);
		sense.push_back('E');
		nzcnt += 2;
		rmatind.push_back(getVariableIndex("x",arcRouting.getAfromAd(a),k));
		rmatval.push_back(1);
		rmatind.push_back(getVariableIndex("z",arcRouting.getAfromAd(a),k));
		rmatval.push_back(-1);
		rname.push_back("TraversedDemandArcConstraint(tour:" +num2string(k) + ",vertex" + num2string(a) + ")");
		rmatbeg.push_back(rmatind.size());
	}

	/* Check consistency of arguments */
	const int numrows = K*Ad, numnzs = K*Ad*2;
	assert(rcnt==numrows);// assert(nzcnt==numnzs);
	assert((int)rhs.size()==rcnt); assert(sense.size()==rhs.size()); assert(rname.size()==rhs.size());
	assert((int)rmatind.size()==nzcnt); assert(rmatval.size()==rmatind.size());
	rmatbeg.pop_back(); assert(rmatbeg.size()==rhs.size());

	/* Add constraints to problem */
	std::vector< const char*> rowname; for(size_t i=0; i<rname.size(); i++) rowname.push_back(rname[i].c_str());
	int status = CPXXaddrows(env, lp, 0, rcnt, nzcnt, &rhs[0], &sense[0], &rmatbeg[0], &rmatind[0], &rmatval[0], nullptr, &rowname[0]);
	return status;
}


static int Build_model(CPXCENVptr env, CPXLPptr lp, ArcRouting &aR) {
	arcRouting = aR;
	V = arcRouting.getVertices();
	K = arcRouting.getTours();
	A = arcRouting.getArcs();
	Q = arcRouting.getMaxCapacity();
	Ad = arcRouting.getSizeOfAd();

	cout << "V " << V << endl;
	cout << "K " << K << endl;
	cout << "A " << A << endl;
	cout << "Q " << Q << endl;
	cout << "Ad " << Ad << endl;

	int status = 0;
	cout << " PopulateByColumn" << endl;
	system("PAUSE");
	// == DEFINE VARIABLES
	status = PopulateByColumn				(env, lp);
	if(status) { std::cout<<"Could not create PopulateByColumn.\n"; return status; }
	cout << " Capacity_Limiting_Constraint" << endl;
	system("PAUSE");
	status = Capacity_Limiting_Constraint	(env, lp);
	if(status) { std::cout<<"Could not create Capacity_Limiting_Constraint.\n"; return status; }
	cout << " Ensure_Demand_Arc_Served" << endl;
	system("PAUSE");
	status = Ensure_Demand_Arc_Served		(env, lp);
	if(status) { std::cout<<"Could not create Ensure_Demand_Arc_Served.\n"; return status; }
	cout << " Flow_Constraint" << endl;
	system("PAUSE");
	status = Flow_Constraint				(env, lp);
	if(status) { std::cout<<"Could not create Flow_Constraint.\n"; return status; }
	cout << " Traversed_Demand_Arc_Constraint" << endl;
	system("PAUSE");
	status = Traversed_Demand_Arc_Constraint(env, lp);
	if(status) { std::cout<<"Could not create Traversed_Demand_Arc_Constraint.\n"; return status; }
}

#endif