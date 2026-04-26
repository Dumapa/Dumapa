CREATE OR REPLACE FUNCTION search_contacts(pattern TEXT)
RETURNS TABLE(contact_id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT p.contact_id, p.name, p.phone 
    FROM phonebook p
    WHERE p.name ILIKE '%' || pattern || '%'
       OR p.phone ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE phonebook.name = p_name) THEN
        UPDATE phonebook SET phone = p_phone WHERE phonebook.name = p_name;
    ELSE
        INSERT INTO phonebook(name, phone) VALUES(p_name, p_phone);
    END IF;
END;
$$;
CREATE OR REPLACE PROCEDURE bulk_insert_contacts(
    names VARCHAR[],
    phones VARCHAR[],
    INOUT invalid_records TEXT[] DEFAULT '{}'
)
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1 .. array_length(names, 1) LOOP
        -- Простая проверка: телефон должен быть длиннее 8 символов
        IF length(phones[i]) < 8 THEN
            invalid_records := array_append(invalid_records, names[i] || ' (Неверный номер: ' || phones[i] || ')');
        ELSE
            -- Если всё ок, вызываем нашу же процедуру добавления
            CALL upsert_contact(names[i], phones[i]);
        END IF;
    END LOOP;
END;
$$;
CREATE OR REPLACE FUNCTION get_contacts_paginated(l_limit INT, l_offset INT)
RETURNS TABLE(contact_id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT p.contact_id, p.name, p.phone 
    FROM phonebook p
    ORDER BY p.name
    LIMIT l_limit OFFSET l_offset;
END;
$$ LANGUAGE plpgsql;
CREATE OR REPLACE PROCEDURE delete_contact_by_identifier(identifier VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM phonebook
    WHERE name = identifier OR phone = identifier;
END;
$$;