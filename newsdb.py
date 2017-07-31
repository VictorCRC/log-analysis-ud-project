import psycopg2


DBASE = 'news'

question_1 = "What are the most popular three articles of all time?"
query_q1 = """SELECT article, CONCAT(pageviews, ' views')
				FROM articles_ranking
				LIMIT 3;"""

question_2 = "Who are the most popular article authors of all time?"
query_q2 = """SELECT author, CONCAT(SUM(pageviews), ' views')
				AS pageviews
				FROM articles_ranking
				GROUP BY author
				ORDER BY pageviews DESC;"""

question_3 = "On which days did more than 1% of requests lead to errors?"
query_q3 = """SELECT day_error_index.date, CONCAT(day_error_index.error_percentage, '%') FROM
					(SELECT daily_visits.date, ROUND((error_report.errors + 0.0) * 100 / (daily_visits.visits + 0.0), 2) AS error_percentage
					FROM daily_visits JOIN error_report ON daily_visits.date = error_report.date
					ORDER BY error_percentage DESC)
				AS day_error_index
				WHERE day_error_index.error_percentage > 1;"""


def query_db(query, content=DBASE):
	db = psycopg2.connect(database=content)
	cursor = db.cursor()
	cursor.execute(query)
	query_result = cursor.fetchall()
	db.close()
	return query_result


def print_answer(question, result):
	print(question)
	for i in result:
		print("-> {} --> {}".format(i[0], i[1]))
	print("")


if __name__ == '__main__':
	print_answer(question_1, query_db(query_q1))
	print_answer(question_2, query_db(query_q2))
	print_answer(question_3, query_db(query_q3))
