** libname to data;
libname l '';

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

