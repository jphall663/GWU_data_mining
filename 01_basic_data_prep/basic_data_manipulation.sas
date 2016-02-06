******************************************************************************;
* Copyright (c) 2015 by SAS Institute Inc., Cary, NC 27513 USA               *;
*                                                                            *;
* Licensed under the Apache License, Version 2.0 (the "License");            *;
* you may not use this file except in compliance with the License.           *;
* You may obtain a copy of the License at                                    *;
*                                                                            *;
*   http://www.apache.org/licenses/LICENSE-2.0                               *;
*                                                                            *;
* Unless required by applicable law or agreed to in writing, software        *;
* distributed under the License is distributed on an "AS IS" BASIS,          *;
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.   *;
* See the License for the specific language governing permissions and        *;
* limitations under the License.                                             *;
******************************************************************************;

******************************************************************************;
* SECTION 1: Hello World! - Standard SAS Output                              *;
******************************************************************************;

* the _null_ data step allows you to execute commands;
* or read a data set without creating a new data set;
data _null_;
	put 'Hello world!';
run;

* print the value of a variable to the log;
* VERY useful for debugging;
data _null_;
	x = 'Hello world!';
	put x;
	put x=;
run;

* file print writes to the open standard output;
* usually html or listing;
data _null_;
	file print;
	put 'Hello world!';
run;

* logging information levels;
* use these prefixes to print important information to the log;
data _null_;
	put 'NOTE: Hello world!';
	put 'WARNING: Hello world!';
	put 'ERROR: Hello world!';
run;

* you can also use the put macro statement;
%put Hello world!;
%put NOTE: Hello world!;
%put WARNING: Hello world!;
%put ERROR: Hello world!;

%put 'Hello world!'; /* macro variables are ALWAYS strings */

* the macro preprocessor resolves macro variables as text literals;
* before data step code is executed;
%let x = Hello world!;
%put &x;
%put '&x'; /* single quotes PREVENT macro resolution */
%put "&x"; /* double quotes ALLOW macro resolution */

******************************************************************************;
* SECTION 2 - SAS data sets                                                  *;
******************************************************************************;

*** sas data sets ************************************************************;

* the sas data set is the primary data structure in the SAS language;
* now you will make one called scratch;

%let n_rows = 1000; /* define number of rows */
%let n_vars = 5;    /* define number of character and numeric variables */

* options mprint; /* to see the macro variables resolve uncomment this line */
data scratch;

	/* since you did not specify a permanent library on the data statement */
	/* the scratch set will be created in the temporary library work */
	/* it will be deleted when you leave SAS */

	/* SAS is strongly typed - it is safest to declare variables */
	/* using a length statement - especially for character variables */
	/* $ denotes a character variable */

	/* arrays are a data structure that can exist during the data step */
	/* they are a reference to a group of variables */
	/* horizontally across a data set */
	/* $ denotes a character array */
	/* do loops are often used in conjuction with arrays */
	/* SAS arrays are indexed from 1 */

	/* a key is a variable with a unique value for each row */

	/* mod() is the modulo function */
	/* the eval() macro function performs math operations */
	/* before text substitution */

	/* the drop statement removes variables from the output data set */

	/* since you are not reading from a pre-existing data set */
	/* you must output rows explicitly using the output statement */

	length key 8 char1-char&n_vars $ 8 numeric1-numeric&n_vars 8;
	text_draw = 'AAAAAAAA BBBBBBBB CCCCCCCC DDDDDDDD EEEEEEEE FFFFFFFF GGGGGGGG';
	array c $ char1-char&n_vars;
	array n numeric1-numeric&n_vars;
	do i=1 to &n_rows;
		key = i;
		do j=1 to %eval(&n_vars);
			/* assign a random value from text_draw */
			/* to each element of the array c */
			c[j] = scan(text_draw, floor(7*ranuni(12345)+1), ' ');
			/* assign a random numeric value to each element of the n array */
			/* ranuni() requires a seed value */
			n[j] = ranuni(%eval(&n_rows*&n_vars));
		end;
	  if mod(i, %eval(&n_rows/10)) = 0 then put 'Processing line ' i '...';
		drop i j text_draw;
		output;
	end;
	put 'Done.';
run;

*** basic data analysis ******************************************************;

* use proc contents to understand basic information about a data set;
proc contents data=scratch;
run;

* use proc freq to analyze categorical data;
proc freq
	/* nlevels counts the discreet levels in each variable */
	/* the colon operator expands to include variable names with prefix char */
	data=scratch nlevels;
	/* request frequency bar charts for each variable */
	tables char: / plots=freqplot(type=bar);
run;

* use proc univariate to analyze numeric data;
proc univariate
	data=scratch;
	/* request univariate statistics for variables names with prefix numeric */
	var numeric:;
	/* request histograms for the same variables */
	histogram numeric:;
	/* inset basic statistics on the histograms */
	inset min max mean / position=ne;
run;

*** basic data manipulation **************************************************;

* subsetting columns;
* create scratch2 set;
data scratch2;
	/* set statement reads from a pre-existing data set */
	/* no output statement is required */
	/* using data set options: keep, drop, etc. is often more efficient than */
	/* corresponding data step statements */
	/* : notation */
	set scratch(keep=numeric:);
run;

* overwrite scratch2 set;
data scratch2;
	/* ranges of vars */
	set scratch(keep=char1-char&n_vars);
run;

* overwrite scratch2 set;
data scratch2;
	/* by name */
	set scratch(keep=key numeric1 char1);
run;

* subsetting and modifying columns;
* select two columns and modify them with data step functions;
* overwrite scratch2 set;
data scratch2;
	/* use length statement to ensure correct length of trans_char1 */
	/* the lag function saves the value from the row above */
	/* lag will create a numeric missing value in the first row */
	/* tranwrd finds and replaces character values */
	set scratch(keep=key char1 numeric1
		rename=(char1=new_char1 numeric1=new_numeric1));
 	length trans_char1 $8;
	lag_numeric1 = lag(new_numeric1);
	trans_char1 = tranwrd(new_char1, 'GGGGGGGG', 'foo');
run;

* subsetting rows;
* select only the first row and impute the missing value;
* create scratch3 set;
data scratch3;
	/* the where data set option can subset rows of data sets */
	/* there are MANY other ways to do this ... */
	set scratch2 (where=(key=1));
	lag_numeric1 = 0;
run;

* subsetting rows;
* remove the problematic first row containing the missing value;
* from scratch2 set;
data scratch2;
	set scratch2;
	if key > 1;
run;

* combining data sets top-to-bottom;
* add scratch3 to the bottom of scratch2;
proc append
	base=scratch2  /* proc append does not read the base set */
	data=scratch3; /* for performance reasons base set should be largest */
run;

* sorting data sets;
* sort scratch2 in place;
proc sort
	data=scratch2;
	by key; /* you must specificy a variables to sort by */
run;

* sorting data sets;
* create the new scratch4 set;
proc sort
	data=scratch2
	out=scratch4; /* specifying an out set creates a new data set */
	by new_char1 new_numeric1; /* you can sort by many variables */
run;

* combining data sets side-by-side;
* to create scratch5 set;
* create messy scratch5 set;
data scratch5;
	/* merge simply attaches two or more data sets together side-by-side*/
	/* it overwrites common variables - be careful */
	merge scratch scratch4;
run;

* combining data sets side-by-side;
* join columns to scratch from scratch2 when key variable matches;
* to create scratch6 correctly;
data scratch6;
	/* merging with a by variable is safer */
	/* it requires that both sets be sorted */
	/* then rows are matched when key values are equal */
	/* very similar to SQL join */
	merge scratch scratch2;
	by key;
run;

* don't forget PROC SQL;
* nearly all common SQL statements and functions are supported by PROC SQL;
* join columns to scratch from scratch2 when key variable matches;
* to create scratch7 correctly;
proc sql noprint; /* noprint suppresses procedure output */
	create table scratch7 as
	select *
	from scratch
	join scratch2
	on scratch.key = scratch2.key;
quit;

* comparing data sets;
* results from data step merge with by variable and PROC SQL join;
* should be equal;
proc compare base=scratch6 compare=scratch7;
run;

* export data set;
* to create a csv file;
* in default working directory;
proc export
	data=scratch7
	/* create scratch7.csv in working directory */
	/* . ends a macro variable name */
	outfile='/folders/myfolders/scratch7.csv'
	/* create a csv */
	dbms=csv
	/* replace an existing file with that name */
	replace;
run;

* import data set;
* from the csv file;
* to overwrite scratch7 set;
proc import
	/* import from scratch7.csv */
	datafile='/folders/myfolders/scratch7.csv'
	/* create a sas table in the work library */
	out=scratch7
	/* from a csv file */
	dbms=csv
	/* replace an existing data set with that name */
	replace;
run;

* results from export/import should match previously created scratch6 set;
proc compare
	base=scratch6
	compare=scratch7
	criterion=0.000001; /* we can except tiny differences */
run;

* by group processing;
* by variables can be used in the data step;
* the data set must be sorted;
* create scratch8 summary set;
data scratch8;
	set scratch4;
	by new_char1 new_numeric1;
	retain count 0; /* retained variables are remembered from row-to-row */
	if last.new_char1 then do; /* first. and last. are used with by vars */
		count + 1; /* shorthand to increment a retained variable */
		output; /* output the last row of a sorted by group */
	end;
run;

* by group processing;
* by variables can be used efficiently in most procedures;
* the data set must be sorted;
proc univariate
	data=scratch4;
	var lag_numeric1;
	histogram lag_numeric1;
	inset min max mean / position=ne;
	by new_char1;
run;

******************************************************************************;
* SECTION 3 - generating analytical graphics                                 *;
******************************************************************************;

*** histograms using PROC SGPLOT *********************************************;

proc sgplot
	/* binwidth - bin width in terms of histogram variable */
	/* datalabel - display counts or percents for each bin */
	/* showbins - use bins to determine x-axis tickmarks */
	data=sashelp.iris;
	histogram petalwidth /
		binwidth=2
		datalabel=count
		showbins;
run;

*** bubble plots using PROC SGPLOT *******************************************;

proc sgplot
	/* group - color by a categorical variable */
	/* lineattrs - sets the bubble outline color and other outline attributes */
	data=sashelp.iris;
	bubble x=petalwidth y=petallength size=sepallength /
		group=species
		lineattrs=(color=grey);
run;

*** scatter plot with regression information using PROC SGPLOT ***************;

proc sgplot
	/* clm - confidence limits for mean predicted values */
	/* cli - prediction limits for individual predicted values */
	/* alpha - set threshold for clm and cli limits */
	data=sashelp.iris;
	reg x=petalwidth y=petallength /
	clm cli alpha=0.1;
run;

*** stacked bar chart using PROC SGPLOT **************************************;

proc sgplot
	/* vbar variable on x-axis */
	/* group - splits vertical bars */
	/* add title */
	data=sashelp.cars;
	vbar type / group=origin;
	title 'Car Types by Country of Origin';
run;

*** correlation heatmap using GTL ********************************************;

* use PROC CORR to create correlation matrix;
* create corr set;
proc corr
	data=sashelp.cars
	outp=corr
	noprint;
run;

* change correlation matrix into x y z contours;
* x and y will be variable names;
* z will be correlation values;
* create xyz set;
data xyz;

	/* define an array out of the numeric variables in corr */
	/* move backwards across array */
	/* to preserve traditional correlation matrix appearance */

	keep x y z;
	set corr(where=(_type_='CORR'));
	array zs[*] _numeric_;
	x = _NAME_;
	do i = dim(zs) to 1 by -1;
		y = vname(zs[i]);
		z = zs[i];
		/* creates a lower triangular matrix */
		if (i < _n_) then z = .;
		output;
	end;
run;

* define a GTL template;
* create the corrheatmap template;
* define a template once, then it can be rendered many times;
proc template;

	/* name the statgraph template */
	/* define a dynamic title for the template */
	/* overlay a continous legend on top of a heatmap */
	/* define overlay axes options */
	/* define heatmap options */
	/* define legend options */

	define statgraph corrheatmap;
		dynamic _title;
		begingraph;
			entrytitle _title;
			layout overlay /
				xaxisopts=(display=(line ticks tickvalues))
				yaxisopts=(display=(line ticks tickvalues));
				heatmapparm x=x y=y colorresponse=z /
					xbinaxis=false ybinaxis=false
					name="heatmap" display=all;
				continuouslegend "heatmap" /
					orient=vertical location=outside title="Correlation";
			endlayout;
		endgraph;
	end;
run;

* render the defined template using xyz set;
proc sgrender
	data=xyz
	/* refers to defined template by name */
	template=corrheatmap;
	/* passes in title to template */
	dynamic _title='Correlation Heat Map for Car Information';
run;