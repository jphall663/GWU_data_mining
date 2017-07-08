******************************************************************************;
* Copyright (C) 2017 by J. Patrick Hall, jphall@gwu.edu                      *;
*                                                                            *;
* Permission is hereby granted, free of charge, to any person obtaining a    *;
* copy of this software and associated documentation files (the "Software"), *;
* to deal in the Software without restriction, including without limitation  *;
* the rights to use, copy, modify, merge, publish, distribute, sublicense,   *;
* and/or sell copies of the Software, and to permit persons to whom the      *;
* Software is furnished to do so, subject to the following conditions:       *;
*                                                                            *;
* The above copyright notice and this permission notice shall be included    *;
* in all copies or substantial portions of the Software.                     *;
*                                                                            *;
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS    *;
* OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,*;
* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL    *;
* THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER *;
* LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING    *;
* FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER        *;
* DEALINGS IN THE SOFTWARE.                                                  *;
******************************************************************************;

******************************************************************************;
* simple SQL operations demonstrated using SAS PROC SQL                      *;
* a *VERY BASIC* introduction to SQL                                         *;
******************************************************************************;

******************************************************************************;
* NOTE: examples are meant for the free SAS University Edition               *;
* to install see: http://www.sas.com/en_us/software/university-edition.html  *;
* Refer to part 0                                                            *;
******************************************************************************;

*** simulate some small example tables using SAS data step *******************; 
* table1 has a primary key called key and two numeric variables: x1 and x2;
* table1 is located in the SAS work library, it could be called work.table1;
data table1; 
	do key=1 to 20;
		x1 = key * 10; 
		x2 = key + 10;
		output;
	end; 
run; 
proc print; run;

* table2 has a primary key called key and two character variables: x3 and x4;
* table2 is located in the SAS work library, it could be called work.table2;
data table2; 
	do key=2 to 20 by 2; 
		x3 = scan('a b c d e f g h i j', key/2);
		x4 = scan('k l m n o p q r s t', key/2);
		output;
	end; 
run;
proc print; run;

******************************************************************************;
* SAS PROC SQL allows users to execute valid SQL statements;
* often called queries, from SAS;
* in a more typical SQL environment the proc sql and quit statements;
* would be unnecessary and unrecognized in a query;	

proc sql;
 
 	* display basic information about table1 in the SAS log;
 	* in SQL parlance work is the database and table1 is the table;
	describe table work.table1;
	
quit;	
	
proc sql;
	
	* display the variable x1 from table1;
	select x1 from work.table1; 
		
quit; 	

* the NOPRINT option can be used to supress output;
* very important for large tables;
proc sql /* noprint */; 

	* create table3 in the work library/database;
	* x1 from table1 will be named x5 in the new table;
	* the SQL statement as creates a temporary name or alias;
	create table table3 as 
	select key, x1 as x5
	from table1;
	
quit;

proc sql;
	
	* a where clause is used to subset rows of a table;
	* the order by statement sorts displayed results or created tables;
	* desc refers to descending sort order;
	create table table4 as 
	select key, x2 as x6 
	from table1 
	where key <= 10
	order by x6 desc;
	
quit;	
	
proc sql;
	
	* insert can be used to add data to a table;
	insert into table1
	values (21, 210, 31);

quit;
	
proc sql;

	* update can be used to change the value of previously existing data;
	update table1
	set key = 6, x1 = 60, x2 = 16
	where key = 7;

quit;
	
proc sql; 	
	
	* an inner join only retains rows from both tables;
	* where key values match;
	create table table5 as
	select * 
	from table1
	join table2
	on table1.key = table2.key; 
	
quit;
	
proc sql;

	* left joins retain all the rows from one table;
	* and only retain rows where key values match from the other table;
	* aliases can also be used for tables;
	create table table6 as 
	select * 
	from table1 as t1 /* left table */
	left join table2 as t2 /* right table */
	on t1.key = t2.key;

quit;

proc sql;

	* the where statement cannot be used with aggregate functions;
	* instead use the having statement;
	* where sum_x1 > 100 would cause errors in this query;
	create table table7 as
	select key, sum(x1) as sum_x1
	from table1 
	group by key
	having sum_x1 > 100;

quit;

proc sql;

	* a subquery is a query embedded in another query;
	select *
	from 
	(select key, x1, x2
	from table1
	where key <= 10);

quit;
