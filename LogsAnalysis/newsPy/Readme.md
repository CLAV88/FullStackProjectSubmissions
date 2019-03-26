#Notes on the news database

###The db schema \dt

          List of relations
 Schema |   Name   | Type  |  Owner
--------+----------+-------+---------
 public | articles | table | vagrant
 public | authors  | table | vagrant
 public | log      | table | vagrant
(3 rows)

###Notes on the Articles Table of the news db

news=> \d articles;
                                  Table "public.articles"
 Column |           Type           |                       Modifiers
--------+--------------------------+-------------------------------------------------------
 author | integer                  | not null
 title  | text                     | not null
 slug   | text                     | not null
 lead   | text                     |
 body   | text                     |
 time   | timestamp with time zone | default now()
 id     | integer                  | not null default nextval('articles_id_seq'::regclass)

 ###Notes on the Authors Table of the news db

                          Table "public.authors"
 Column |  Type   |                      Modifiers
--------+---------+------------------------------------------------------
 name   | text    | not null
 bio    | text    |
 id     | integer | not null default nextval('authors_id_seq'::regclass)
Indexes:
    "authors_pkey" PRIMARY KEY, btree (id)
Referenced by:
    TABLE "articles" CONSTRAINT "articles_author_fkey" FOREIGN KEY (author) REFERENCES authors(id)

###Notes on the Logs Table of the news db
                                  Table "public.log"
 Column |           Type           |                    Modifiers
--------+--------------------------+--------------------------------------------------
 path   | text                     |
 ip     | inet                     |
 method | text                     |
 status | text                     |
 time   | timestamp with time zone | default now()
 id     | integer                  | not null default nextval('log_id_seq'::regclass)
Indexes:
    "log_pkey" PRIMARY KEY, btree (id)

##Status Line Codes

1. 1xx — Informational. The request is in progress or there's another step to take.
2. 2xx — Success! The request succeeded. The server is sending the data the client asked for.
3. 3xx — Redirection. The server is telling the client a different URI it should redirect to. The headers will usually contain a Location header with the updated URI. Different codes tell the client whether a redirect is permanent or temporary.
4. 4xx — Client error. The server didn't understand the client's request, or can't or won't fill it. Different codes tell the client whether it was a bad URI, a permissions problem, or another sort of error.
5. 5xx — Server error. Something went wrong on the server side.

*..Used to select the numerrors per day (logs Table) => http_errors_per_day view
*  select time::date as datelog, count(*) as numerrors from log where left(log.status,3)::integer > 400 group by datelog order by numerrors desc;

*.. Used to select the numhttprequests per day (logs Table) => http_requests_per_day view
* select time::date as datelog, count(*) as numhttprequests from log group by datelog order by numhttprequests desc;
