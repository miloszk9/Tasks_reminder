-- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler  version: 0.9.3-beta1
-- PostgreSQL version: 12.0
-- Project Site: pgmodeler.io
-- Model Author: Miłosz Kaszuba

-- object: public.task_id_seq | type: SEQUENCE --
-- DROP SEQUENCE IF EXISTS public.task_id_seq CASCADE;
CREATE SEQUENCE public.task_id_seq
	INCREMENT BY 1
	MINVALUE 0
	MAXVALUE 2147483647
	START WITH 1
	CACHE 1
	NO CYCLE
	OWNED BY NONE;

-- ddl-end --
ALTER SEQUENCE public.task_id_seq OWNER TO postgres;
-- ddl-end --

-- object: public.birthdate_id_seq | type: SEQUENCE --
-- DROP SEQUENCE IF EXISTS public.birthdate_id_seq CASCADE;
CREATE SEQUENCE public.birthdate_id_seq
	INCREMENT BY 1
	MINVALUE 0
	MAXVALUE 2147483647
	START WITH 1
	CACHE 1
	NO CYCLE
	OWNED BY NONE;

-- ddl-end --
ALTER SEQUENCE public.birthdate_id_seq OWNER TO postgres;
-- ddl-end --

-- object: public.friends_id_seq | type: SEQUENCE --
-- DROP SEQUENCE IF EXISTS public.friends_id_seq CASCADE;
CREATE SEQUENCE public.friends_id_seq
	INCREMENT BY 1
	MINVALUE 0
	MAXVALUE 2147483647
	START WITH 1
	CACHE 1
	NO CYCLE
	OWNED BY NONE;

-- ddl-end --
ALTER SEQUENCE public.friends_id_seq OWNER TO postgres;
-- ddl-end --

-- object: public.share_id_seq | type: SEQUENCE --
-- DROP SEQUENCE IF EXISTS public.share_id_seq CASCADE;
CREATE SEQUENCE public.share_id_seq
	INCREMENT BY 1
	MINVALUE 0
	MAXVALUE 2147483647
	START WITH 1
	CACHE 1
	NO CYCLE
	OWNED BY NONE;

-- ddl-end --
ALTER SEQUENCE public.share_id_seq OWNER TO postgres;
-- ddl-end --

-- object: public.task | type: TABLE --
-- DROP TABLE IF EXISTS public.task CASCADE;
CREATE TABLE public.task (
	id integer NOT NULL DEFAULT nextval('task_id_seq'),
	user_id integer,
	name char(100) NOT NULL,
	date_create timestamp,
	todo_timestamp timestamp,
	is_done boolean DEFAULT False,
	todo_date date,
	CONSTRAINT task_pk PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE public.task OWNER TO postgres;
-- ddl-end --

-- object: public.birthdate | type: TABLE --
-- DROP TABLE IF EXISTS public.birthdate CASCADE;
CREATE TABLE public.birthdate (
	id integer NOT NULL DEFAULT nextval('public.birthdate_id_seq'::regclass),
	birthdate date NOT NULL,
	user_id integer,
	CONSTRAINT birthdate_pk PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE public.birthdate OWNER TO postgres;
-- ddl-end --

-- object: public.friends | type: TABLE --
-- DROP TABLE IF EXISTS public.friends CASCADE;
CREATE TABLE public.friends (
	id integer NOT NULL DEFAULT nextval('friends_id_seq'),
	user1_id integer,
	user2_id integer,
	is_accepted boolean DEFAULT False,
	CONSTRAINT friends_pk PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE public.friends OWNER TO postgres;
-- ddl-end --

-- object: public.task_share | type: TABLE --
-- DROP TABLE IF EXISTS public.task_share CASCADE;
CREATE TABLE public.task_share (
	id integer NOT NULL DEFAULT nextval('public.share_id_seq'::regclass),
	friendship_id integer,
	task_id integer,
	CONSTRAINT task_share_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.task_share OWNER TO postgres;
-- ddl-end --

-- object: task_fk | type: CONSTRAINT --
-- ALTER TABLE public.task DROP CONSTRAINT IF EXISTS task_fk CASCADE;
ALTER TABLE public.task ADD CONSTRAINT task_fk FOREIGN KEY (user_id)
REFERENCES public.auth_user (id) MATCH FULL
ON DELETE CASCADE ON UPDATE CASCADE;
-- ddl-end --

-- object: birthdate_fk | type: CONSTRAINT --
-- ALTER TABLE public.birthdate DROP CONSTRAINT IF EXISTS birthdate_fk CASCADE;
ALTER TABLE public.birthdate ADD CONSTRAINT birthdate_fk FOREIGN KEY (user_id)
REFERENCES public.auth_user (id) MATCH FULL
ON DELETE CASCADE ON UPDATE CASCADE;
-- ddl-end --

-- object: friend_user1_fk | type: CONSTRAINT --
-- ALTER TABLE public.friends DROP CONSTRAINT IF EXISTS friend_user1_fk CASCADE;
ALTER TABLE public.friends ADD CONSTRAINT friend_user1_fk FOREIGN KEY (user1_id)
REFERENCES public.auth_user (id) MATCH FULL
ON DELETE CASCADE ON UPDATE CASCADE;
-- ddl-end --

-- object: friend_user2_fk | type: CONSTRAINT --
-- ALTER TABLE public.friends DROP CONSTRAINT IF EXISTS friend_user2_fk CASCADE;
ALTER TABLE public.friends ADD CONSTRAINT friend_user2_fk FOREIGN KEY (user2_id)
REFERENCES public.auth_user (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: share_task_fk | type: CONSTRAINT --
-- ALTER TABLE public.task_share DROP CONSTRAINT IF EXISTS share_task_fk CASCADE;
ALTER TABLE public.task_share ADD CONSTRAINT share_task_fk FOREIGN KEY (task_id)
REFERENCES public.task (id) MATCH FULL
ON DELETE CASCADE ON UPDATE CASCADE;
-- ddl-end --

-- object: share_friendship_fk | type: CONSTRAINT --
-- ALTER TABLE public.task_share DROP CONSTRAINT IF EXISTS share_friendship_fk CASCADE;
ALTER TABLE public.task_share ADD CONSTRAINT share_friendship_fk FOREIGN KEY (friendship_id)
REFERENCES public.friends (id) MATCH FULL
ON DELETE CASCADE ON UPDATE CASCADE;
-- ddl-end --

-- Trigger - checks if task is shared already
create function share_check() returns trigger as '
declare
    row task_share%rowtype;
begin
    for row in SELECT id,friendship_id,task_id from task_share loop
        if NEW.friendship_id = row.friendship_id and NEW.task_id = row.task_id THEN
			return NULL;
        end if;
    END LOOP;
	return NEW;
end;
' language 'plpgsql';

create trigger share_trigger before insert on task_share for each row execute procedure share_check();

-- Function - checks if user with passed username exists - if exists: returns id; else: null
create function username_id(varchar(150)) returns integer as '
declare
    row auth_user%rowtype;
begin
    for row in SELECT * from auth_user loop
        if $1 = row.username THEN
			return row.id;
        end if;
    END LOOP;
	return NULL;
end;
' language 'plpgsql';
