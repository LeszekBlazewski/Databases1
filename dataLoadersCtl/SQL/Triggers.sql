-- Check data before creating a valid reservation
create or replace TRIGGER "VALID_RESERVATION" BEFORE INSERT OR UPDATE ON RESERVATIONS
FOR EACH ROW
DECLARE
    --declare variables section
    clientSkillLevel number;
    poolSkillLevel number;
    availableSpots number;
    skill_exce EXCEPTION;       --thrown when client does not meet required skill
    spot_exce EXCEPTION;        --thrown when there aren't any spots left
BEGIN
    -- get skill of the client which places reservation
    SELECT SWIMMINGSKILL INTO clientSkillLevel FROM CLIENTS
    WHERE id_c = :NEW.id_client;
    -- get required skill and number of places for pool on which reservation is made
    -- NVL is required because NUMBEROFPLACES can be null (anyone can swim in it)
    SELECT NVL(REQUIREDSKILL, 0), NUMBEROFPLACES INTO poolSkillLevel, availablespots FROM pools
    WHERE id_p = :NEW.id_pool;
    
    IF clientskilllevel < poolskilllevel THEN
        RAISE skill_exce;
    ELSIF availablespots = 0 THEN
        RAISE spot_exce;
    ELSE -- this means that the whole reservation is valid and we have to update the pool value
        UPDATE POOLS
        SET numberofplaces=numberofplaces - 1
        WHERE id_p = :NEW.id_pool;
    END IF;
    EXCEPTION
        WHEN skill_exce THEN
        DBMS_OUTPUT.PUT_LINE('Client does not meet skill requirements for this pool !');
        raise_application_error(-20000, 'Client does not meet skill requirements for this pool !');
        WHEN spot_exce THEN
        DBMS_OUTPUT.PUT_LINE('Pool does not have any available spots at this time !');
        raise_application_error(-20000, 'Pool does not have any available spots at this time !');
END;

-- update price of the reservation based on the age of the client
create or replace TRIGGER "DISCOUNT_RESERVATION" BEFORE INSERT ON RESERVATIONS
FOR EACH ROW
DECLARE
clientAge number(2);
BEGIN
  -- get client age
  SELECT age INTO clientAge
  FROM clients
  WHERE ID_C = :NEW.ID_CLIENT;
  -- check how old given client is and update aprioprate value when condition is met
  IF (clientAge < 18) THEN
    :new.price := :new.price * 0.5;
  ELSIF (clientAge > 75) THEN
    :new.price := :new.price * 0.75;
  END IF;
END;