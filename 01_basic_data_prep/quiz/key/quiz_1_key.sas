*** #3;

data _1; 
	input ID $ X1 X2 $;
	datalines;
123A 1 A
1234 2 B
1235 3 C
1235B 4 D
; 
run;
proc print; where X1 >= 3; run;

*** #4;

data _2;
	input ID $ X3;
	datalines;
123A 5
1234 6
1235 7
1235B 8
1234 9
1235 10
1235B 11
;
run;

proc sql; 
	select ID, mean(X3) as ave_x3
	from _2
	group by ID;
quit; 

*** #5;

proc sql; 
	select * 
    from _2 
	left join _1
	on _2.ID = _1.ID;
quit; 
