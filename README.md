# Log Analysis Project
## About
Third project in Udacity’s Full Stack Nanodegree. The assignment consists in building an internal reporting tool for a fictitious newspaper site. Students should use information from a previously configured database to discover what kind of articles the site's readers like.


### Goals
Using SQL queries, students must answer the following three questions:
1. **What are the most popular three articles of all time?**
2. **Who are the most popular article authors of all time?**
3. **On which days did more than 1% of requests lead to errors?**


### More details
* This is a Python program using the `psycopg2` module to connect to the database.
* It runs from the command line. No user input is taken.
* The database contains 3 tables: 
	>The `authors` table includes information about the articles’ authors.
	>The `articles` table includes the articles themselves.
	>The `log` table includes one entry for each time a user has accessed the site.
* Students are encouraged to get the database to do the heavy lifting, leaving minimal "post-processing" in the Python code itself.
* The project makes use of a Linux-based virtual machine (VM).



## Getting Started
### Pre-requisites
* Python3
* VirtualBox
* Vagrant



### Setup
1. Install VirtualBox. Download it [here](https://www.virtualbox.org/wiki/Downloads).
2. Install Vagrant. Download it [here](https://www.vagrantup.com/downloads.html).
3. Fork then clone [fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm) repository.
4. Next, [download the data here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) and unzip it.
5. Fork then clone this current repository and move it into the previously cloned _fullstack-nanodegree-vm/vagrant_ subdirectory, together with the _newsdata.sql_ file.


### Firing up the Virtual Machine
1. Using your terminal, start the Linux virtual machine from within the Vagrant subdirectory. For that, run the command:
```
vagrant up
```

2. When `vagrant up` finishes downloading and installing the Linux operating system, run `vagrant ssh` to log into it.

3. Inside the VM, `cd` into `/vagrant` .


### Configure the database
1. Load the site's data into your local database:
```
psql -d news -f newsdata.sql
```

2. Next, connect to your database using `psql -d news` .

1. Create the views `articles_ranking` , `daily_visits`  and  `error_report` (all specified below).


### Running the program
Finally, from the vagrant subdirectory — within the Linux virtual machine — run the following command to test the reporting tool:
```
python newsdb.py
```
 
**And that’s it!**


## Created VIEWS
Three views were created:

1. `articles_ranking` -> lists articles by most pageviews; includes its authors’ names.
```
CREATE VIEW articles_ranking AS
	SELECT articles.slug AS article, art_rank.pageviews, authors.name AS author
	FROM articles, authors, 
		(SELECT path, count(*) AS pageviews
			FROM log
			WHERE path LIKE '%article/%'
			GROUP BY path
			ORDER BY pageviews DESC
			LIMIT 8)
	AS art_rank
	WHERE articles.author = authors.id
	AND art_rank.path LIKE concat('%', articles.slug)
	ORDER BY pageviews DESC;
```


2. `daily_visits` -> lists the total number of pageviews per date.
```
CREATE VIEW daily_visits AS
	SELECT date(time), count(*) as visits
		FROM log
		GROUP BY date
		ORDER BY date;
```


3. `error_report` -> lists the total number of 404s per date.
```
CREATE VIEW error_report AS
	SELECT date(time), count(*) AS errors
		FROM log
		WHERE status LIKE '%404%'
		GROUP BY date
		ORDER BY date;
```
