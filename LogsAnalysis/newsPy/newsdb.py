# "Database code" for the logs Analysis, taken from the code in Forum.db to start

import datetime
import psycopg2
import bleach

DBNAME ="news"

## What are the most popular three articles of all time? Which articles have been accessed the most? Present this information as a sorted list with the most popular article at the top.
def get_topArticles():
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  get_posts_SQL = "select art.title, views from (select split_part(log.path,'/',3) as top_three_articles, count (*) as views from log group by log.path order by views desc Limit 3 offset 1) as a inner join articles as art on art.slug = top_three_articles;"
  c.execute(get_posts_SQL)
  db.close
  return c.fetchall()

## Who are the most popular article authors of all time? That is, when you sum up all of the articles each author has written, which authors get the most page views? Present this as a sorted list with the most popular author at the top.
def get_topAuthors():
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  get_posts_SQL = " select aut.name, author_count from \
                        (select art.author as authorid, sum(views) as author_count from\
                        (select split_part(log.path,'/',3) as top_three_articles, count (*) as views from log group by log.path order by views desc offset 1) \
                        as a inner join articles as art on art.slug = top_three_articles group by art.author order by author_count desc) as a inner join authors as aut on authorid =  aut.id;"
  c.execute(get_posts_SQL)
  db.close
  return c.fetchall()

##On which days did more than 1% of requests lead to errors? The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser. (Refer to this lesson for more information about the idea of HTTP status codes.)
def get_topBugs():
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  get_posts_SQL = "select datelog, percent_daily_errors from (select datelog, (sum(numerrors)/sum(numhttpreq)*100)::real as percent_daily_errors from (select tot_req.datelog as datelog, err_req.numerrors as numerrors, tot_req.numhttprequests as numhttpreq from http_requests_per_day as tot_req, http_errors_per_day as err_req whe\
re tot_req.datelog = err_req.datelog) as subq group by datelog order by percent_daily_errors desc) as subq2 where percent_daily_errors >1;"
  c.execute(get_posts_SQL)
  db.close
  return c.fetchall()

print(get_topArticles())
print(get_topAuthors())
print(get_topBugs())