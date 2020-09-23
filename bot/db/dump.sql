--
-- PostgreSQL database dump
--

-- Dumped from database version 12.4 (Ubuntu 12.4-1.pgdg20.04+1)
-- Dumped by pg_dump version 12.4 (Ubuntu 12.4-1.pgdg20.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO postgres;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: matchbet; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.matchbet (
    slip_no text,
    status text,
    msg_id bigint
);


ALTER TABLE public.matchbet OWNER TO postgres;

--
-- Name: matchbet_data; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.matchbet_data (
    user_id bigint,
    slip_no text,
    amount bigint,
    choice text
);


ALTER TABLE public.matchbet_data OWNER TO postgres;

--
-- Name: profile_ext; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.profile_ext (
    user_id bigint,
    description text,
    waifus text,
    birthday text,
    reputation bigint,
    badges text[],
    bal bigint
);


ALTER TABLE public.profile_ext OWNER TO postgres;

--
-- Name: profiles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.profiles (
    user_id bigint,
    guild_id bigint,
    xp bigint
);


ALTER TABLE public.profiles OWNER TO postgres;

--
-- Name: shop; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.shop (
    name text,
    id text,
    money bigint
);


ALTER TABLE public.shop OWNER TO postgres;

--
-- Data for Name: matchbet; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: matchbet_data; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: profile_ext; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.profile_ext VALUES (523685858658746397, 'No description given', 'No waifus/husbandos', 'Birthday not set', 0, '{}', 9000);
INSERT INTO public.profile_ext VALUES (559601747333611536, 'No description given', 'No waifus/husbandos', 'Birthday not set', 0, '{}', 10000);
INSERT INTO public.profile_ext VALUES (729198037116649523, 'No description given', 'No waifus/husbandos', 'Birthday not set', 0, '{}', 14200);


--
-- Data for Name: profiles; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.profiles VALUES (729198037116649523, 752899871324897342, 1362);
INSERT INTO public.profiles VALUES (740929066009493505, 744132662196830229, 474);
INSERT INTO public.profiles VALUES (740929066009493505, 749526641361027092, 12);
INSERT INTO public.profiles VALUES (523685858658746397, 752899871324897342, 384);
INSERT INTO public.profiles VALUES (559601747333611536, 698357185448509610, 18);
INSERT INTO public.profiles VALUES (523685858658746397, 698357185448509610, 900);


--
-- Data for Name: shop; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.shop VALUES ('rand2', '🍪', 123);
INSERT INTO public.shop VALUES ('rad1', '🍰', 1233);
INSERT INTO public.shop VALUES ('rand', '🍪', 1232);
INSERT INTO public.shop VALUES ('random22', '🦀', 2400);
INSERT INTO public.shop VALUES ('RandOM232', '👐', 2323);
INSERT INTO public.shop VALUES ('high', '😭', 2000000);


--
-- PostgreSQL database dump complete
--

