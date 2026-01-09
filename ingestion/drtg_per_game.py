"""Planning
- To get the list of curry seasons we need
- <div id = "inner_nav_new" class = "open">
    <ul>
        <li class = "full current open hasmore">
            <div>
                <ul>
                    <li> <a href = LINK>yyyy-yyyy</a>
- After accessing that link we go to the table on the page
    <table id = "player_game_log_reg">
        <tbody>
            THE FIRST INSTANCE OF <tr id = "player_game_log_reg.***">
                <td class = "left" data-stat = "date">
                    <a href = "LINK-WE-NEED.html">date</a>
-Then just follow steps below
-OR WE COULD JUST GET THE LINKS FOR THESE MANUALLY PROBABLY DO THIS CUZ ITS ONLY LIKE 10 LINKS



HTML on each game page has table with advanced box score stats
- id = "box-TEAMABBRV-game-advanced"
- class = "sortable stats_table now_sortable"

- Use scraper to grab advanced box score stats for both Opposing team and GSW, and then parse to use
- the opp team stats table

- in that table go to <tfoot> look for data-stat = "def_rtg" and get the contend inside that <td>

- To get to next game we can access a <a> element with class = "button2 next" and then parse results
- for a link that include GSW.html

- To get the date of the game we can go to <div id = "content" class = "box" role = "main> and grab the
- VERY FIRST <h1> it will contain a csv row of 3 values. 
        Golden State Warriors at Los Angeles Lakers Box Score, November 4, 2016
- Parse it to get the date and use pd.todatetime or whatever the funciton is

- player team city and player team name and opp team city and opp team name can be found using the same 
- csv for the date, just split at the 'at'

- We keep using the "button2 next" until it is no longer found, and therefore we have reached the end of 
that regular season

- This will get us every single GSW regular season game's opp defensive rating. However we need to use
- pandas to only grab the games we need (ones where curry plays)
"""
