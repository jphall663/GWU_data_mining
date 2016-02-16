*** libname to data;
libname l 'C:\workspace\GWU_data_mining\02_analytical_data_prep\assignment\raw';

* import: File -> Import Data;

*** #1; 

/* train_set – 35 column, 13184290 rows */
/* test_set – 34 columns, 4314865 rows */

*** #2;

proc sql noprint; 

	create table non_zero_households as 
	select household_id,
           count(household_id) as cnt_past_household_claims,
           sum(claim_amount) as sum_past_claim_amounts
	from l.train_set
	where claim_amount > 0
	group by household_id; 

quit;

data l.train_set; 
	merge l.train_set(in=x) non_zero_households;
	by household_id;
	if cnt_past_household_claims = . then cnt_past_household_claims = 0;
	if sum_past_claim_amounts = . then sum_past_claim_amounts = 0;
	if x;
run;

data l.test_set; 
	merge l.test_set(in=x) non_zero_households;
	by household_id;
	if cnt_past_household_claims = . then cnt_past_household_claims = 0;
	if sum_past_claim_amounts = . then sum_past_claim_amounts = 0;
	if x;
run;

proc sql; 

	select cnt_past_household_claims, sum_past_claim_amounts
	from l.train_set
	where household_id = 4719940;

	select cnt_past_household_claims, sum_past_claim_amounts
	from l.test_set
	where household_id = 3372413;

quit;

/* 4719940, 1, 562.4142 */
/* 3372413, 1, 1390.159 */ 

*** #3;

proc freq noprint
	data=l.train_set(keep=blind_model);
	table blind_model / out=blind_model_train_levels(keep=blind_model);
run;

proc freq noprint
	data=l.test_set(keep=blind_model);
	table blind_model / out=blind_model_test_levels(keep=blind_model);
run;

proc sort data=blind_model_train_levels; by blind_model; run;
proc sort data=blind_model_test_levels; by blind_model; run;

data blind_model_bad; 
	merge blind_model_test_levels (in=a) blind_model_train_levels (in=b);
	by blind_model;
	if a and ^b;
run;

/* 126 */

*** #4;

* assign a binary marker for nonzero claims;
data train_bin;
	set l.train_set; 
	if claim_amount = 0 then bin_claim = 0;
	else bin_claim = 1;
	keep claim_amount blind_model blind_submodel bin_claim; 
run;

* count event and nonevent totals;
proc sql; 

	select count(bin_claim) into :total_num_event
	from train_bin 
	where bin_claim = 1; 

	select count(bin_claim) into :total_num_nonevent
	from train_bin 
	where bin_claim = 0;

quit; 
%put total_num_event=&total_num_event; /* 95605 */
%put total_num_nonevent=&total_num_nonevent; /* 13088685 */

* calculate frequencies;
proc freq noprint
	data=train_bin; 
	table blind_model*bin_claim / out=model(where=(blind_model='X.45'));
	table blind_submodel*bin_claim / out=submodel(where=(blind_submodel='X.45.2'));
run;

proc print data=model; run; 
/* X.45 0 289628 */
/* X.45 1 2331 */

proc print data=submodel; run;
/* X.45.2 0 82706 */
/* X.45.2 1 678 */

data _null_; 
	x45woe = 100*log((2331/&total_num_event)/(289628/&total_num_nonevent));
	put x45woe=; /* 9.697829468 */
run;

data _null_; 
	x452woe = 100*log((678/&total_num_event)/(82706/&total_num_nonevent));
	put x452woe=; /* 11.537813372 */
run;

*** #5;
%put %eval(&total_num_event*2); /* 191210 */
