DELIMITER //
#CREATE PROCEDURE GetRecsForDateToFile(IN thedate DATE)
CREATE PROCEDURE GetRecsForDateToFile(IN thedate DATE, IN fileout VARCHAR(255))
#CREATE PROCEDURE GetRecsForDateToFile(IN fileout VARCHAR(255))
BEGIN
# from: https://forums.mysql.com/read.php?20,90709,93744#msg-93744
set @myvar = concat("select r.*, e.record_date, e.event_id 
from record_data as r, record_event as e 
where e.record_date = ","'",thedate,"'",
and r.recevent_id = e.event_id
INTO outfile ","'",fileout,"'",
" fields terminated by ',' enclosed by '\"' lines terminated by '\n'");
PREPARE stmt1 FROM @myvar;
EXECUTE stmt1;
Deallocate prepare stmt1; 
END // 
DELIMITER ;