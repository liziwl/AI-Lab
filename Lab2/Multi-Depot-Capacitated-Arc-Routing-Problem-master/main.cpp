
# include "Model.h"
int main(int argc, char*argv[]) {

	 CPXENVptr     env = NULL;
     CPXLPptr      lp = NULL;
     int           status = 0;
     int           i, j;
     int           cur_numrows, cur_numcols;

	 /* Setting the enviornment variable*/
	env = CPXopenCPLEX (&status);

	if ( env == nullptr ) {
		char errmsg[CPXMESSAGEBUFSIZE];
		std::cout<< "Could not open CPLEX Environment.\n";
		CPXXgeterrorstring (env,status,errmsg);
		std::cout<< errmsg;
		return 1;
	}
	/* Turning on the screen switch parameter*/
	status = CPXXsetintparam (env, CPXPARAM_ScreenOutput, CPX_ON); 
	if ( status ) {
		std::cout<<"Failed to turn on screen indicator,error.\n" <<std::endl;
		return 1;
	}

	/*Creating problem object*/
	lp = CPXXcreateprob(env, &status, "MDCARP");
	if ( lp == nullptr ) {
		std::cout<<"Failed to create CPLEX LP object" <<std::endl;
		return 1;
	}

	string file = "C:\\Users\\ktayal\\Documents\\ST_PROJECT\\ARPLIB\\ARPLIB\\lit\\egl-e1-A.txt";
	ArcRouting arcRouting(file);

	/*Building the model*/
	status = Build_model(env,lp, arcRouting);
	if (status) {
		std::cout<< " Failed to build MILP model. \n";
		return 1;
	}



}

int test(int argc, char*argv[]) {
	string file = "C:\\Users\\ktayal\\Documents\\ST_PROJECT\\ARPLIB\\ARPLIB\\lit\\egl-e1-A.txt";
	cout << file << endl;
	//system("PAUSE");
	ArcRouting arcRouting(file);
	system("PAUSE");
}