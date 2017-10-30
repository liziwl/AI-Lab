# include < ilcplex / ilocplex .h >
ILOSTLBEGIN
	int main () {
		IloEnv env ;
		IloModel model( env );
		IloNumVarArray x( env );
		IloRangeArray c( env );
		x.add( IloNumVar( env , 0, 40));
		x.add( IloNumVar( env )); // default : between 0 and +∞
		x.add( IloNumVar( env ));
		c.add( - x [0] + x [1] + x [2] <= 20);
		c.add( x [0] - 3 * x [1] + x [2] <= 30);
		model.add( c );
		model.add( IloMaximize ( env , x [0]+2* x [1]+3* x [2]));
		IloCplex cplex( model );
		cplex.solve();
		cout << " Max =" << cplex . getObjValue() << endl ;
		env.end();
}