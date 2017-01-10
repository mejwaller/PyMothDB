DELIMITER //
CREATE PROCEDURE GetRecsBetweenDates(IN start DATE, IN end DATE, IN fileout VARCHAR(255))
BEGIN
 select t.vernacular_name, t.order_name, t.family_name, t.genus_name, t.species_name, t.subspecies_name, t.aberration_name, t.form_name, 
 e.record_date, e.record_type, e.grid_ref, 
 r.count, r.notes 
 FROM taxon_data AS t, 
 record_event AS e, 
 record_data AS r 
 WHERE t.id=r.taxon_id 
 AND r.recevent_id = e.event_id 
 AND e.record_date > 'start' 
 AND e.record_date < 'end' 
 INTO outfile 'fileout' fields terminated by ',' enclosed by '"' lines terminated by '\n';
END //
DELIMITER ; 
