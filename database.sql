-- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler  version: 0.9.3-beta1
-- PostgreSQL version: 12.0
-- Project Site: pgmodeler.io
-- Model Author: ---

-- Database creation must be performed outside a multi lined SQL file. 
-- These commands were put in this file only as a convenience.

CREATE SEQUENCE public.friends_id_seq
	INCREMENT BY 1
	MINVALUE 0
	MAXVALUE 2147483647
	START WITH 1
	CACHE 1
	NO CYCLE
	OWNED BY NONE;

CREATE SEQUENCE public.task_id_seq
	INCREMENT BY 1
	MINVALUE 0
	MAXVALUE 2147483647
	START WITH 1
	CACHE 1
	NO CYCLE
	OWNED BY NONE;

CREATE SEQUENCE public.birthdate_id_seq
	INCREMENT BY 1
	MINVALUE 0
	MAXVALUE 2147483647
	START WITH 1
	CACHE 1
	NO CYCLE
	OWNED BY NONE;

CREATE SEQUENCE public.share_id_seq
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
ALTER SEQUENCE public.task_id_seq OWNER TO postgres;
-- ddl-end --
ALTER SEQUENCE public.share_id_seq OWNER TO postgres;

-- ddl-end --
ALTER SEQUENCE public.friends_id_seq OWNER TO postgres;
-- ddl-end --

-- object: public.main_task | type: TABLE --
-- DROP TABLE IF EXISTS public.main_task CASCADE;
CREATE TABLE public.main_task (
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
ALTER TABLE public.main_task OWNER TO postgres;
-- ddl-end --

-- object: public.main_holidays | type: TABLE --
-- DROP TABLE IF EXISTS public.main_holidays CASCADE;
CREATE TABLE public.main_birthdate (
	id integer NOT NULL DEFAULT nextval('birthdate_id_seq'),
	birthdate date NOT NULL,
    user_id integer,
	CONSTRAINT birthdate_pk PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE public.main_birthdate OWNER TO postgres;
-- ddl-end --

-- object: public.task_id_seq | type: SEQUENCE --
-- DROP SEQUENCE IF EXISTS public.task_id_seq CASCADE;

-- object: public.main_friends | type: TABLE --
-- DROP TABLE IF EXISTS public.main_friends CASCADE;
CREATE TABLE public.main_friends (
	id integer NOT NULL DEFAULT nextval('friends_id_seq'),
	user1_id integer,
	user2_id integer,
	is_accepted boolean DEFAULT False,
	CONSTRAINT friends_pk PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE public.main_friends OWNER TO postgres;
-- ddl-end --

-- object: public.main_friends | type: TABLE --
-- DROP TABLE IF EXISTS public.main_friends CASCADE;
CREATE TABLE public.main_share (
	id integer NOT NULL DEFAULT nextval('share_id_seq'),
	friendship_id integer,
	task_id integer,
	CONSTRAINT share_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.main_share OWNER TO postgres;
-- ddl-end --

-- object: user_id_fkey | type: CONSTRAINT --
-- ALTER TABLE public.main_task DROP CONSTRAINT IF EXISTS user_id_fkey CASCADE;
ALTER TABLE public.main_task ADD CONSTRAINT user_id_fkey FOREIGN KEY (user_id)
REFERENCES public.auth_user (id) MATCH FULL
ON DELETE CASCADE ON UPDATE CASCADE;
-- ddl-end --



-- object: friends_user1_fkey | type: CONSTRAINT --
-- ALTER TABLE public.main_friends DROP CONSTRAINT IF EXISTS friends_user1_fkey CASCADE;
ALTER TABLE public.main_friends ADD CONSTRAINT friends_user1_fkey FOREIGN KEY (user1_id)
REFERENCES public.auth_user (id) MATCH FULL
ON DELETE CASCADE ON UPDATE CASCADE;
-- ddl-end --

-- object: friends_user2_fkey | type: CONSTRAINT --
-- ALTER TABLE public.main_friends DROP CONSTRAINT IF EXISTS friends_user2_fkey CASCADE;
ALTER TABLE public.main_friends ADD CONSTRAINT friends_user2_fkey FOREIGN KEY (user2_id)
REFERENCES public.auth_user (id) MATCH FULL
ON DELETE CASCADE ON UPDATE CASCADE;
-- ddl-end --

ALTER TABLE public.main_share ADD CONSTRAINT share_user_fkey FOREIGN KEY (friendship_id)
REFERENCES public.main_friends (id) MATCH FULL
ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE public.main_share ADD CONSTRAINT share_task_fkey FOREIGN KEY (task_id)
REFERENCES public.main_task (id) MATCH FULL
ON DELETE CASCADE ON UPDATE CASCADE;
