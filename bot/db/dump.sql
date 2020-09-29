--
-- PostgreSQL database dump
--

-- Dumped from database version 12.4 (Ubuntu 12.4-0ubuntu0.20.04.1)
-- Dumped by pg_dump version 12.4 (Ubuntu 12.4-0ubuntu0.20.04.1)

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
    bal bigint,
    gender text
);


ALTER TABLE public.profile_ext OWNER TO postgres;

--
-- Name: profiles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.profiles (
    user_id bigint,
    guild_id bigint
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

INSERT INTO public.profile_ext VALUES (523685858658746397, 'No description given', 'No waifus/husbandos', 'Birthday not set', 0, '{}', 50000, 'Gender not set');


--
-- Data for Name: profiles; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.profiles VALUES (523685858658746397, 758458965784133632);


--
-- Data for Name: shop; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.shop VALUES ('Baby Bettor', '👶', 60000);
INSERT INTO public.shop VALUES ('Kid Bettor', '🧒', 120000);
INSERT INTO public.shop VALUES ('Teen Bettor', '👦', 180000);
INSERT INTO public.shop VALUES ('Adult Bettor', '👨', 250000);
INSERT INTO public.shop VALUES ('Old Bettor', '👴', 350000);
INSERT INTO public.shop VALUES ('Wheelchair Bettor', '♿', 500000);
INSERT INTO public.shop VALUES ('Clown Bettor', '🤡', 700000);
INSERT INTO public.shop VALUES ('Demon Bettor', '👹', 1000000);
INSERT INTO public.shop VALUES ('God Bettor', '👼', 1500000);


--
-- PostgreSQL database dump complete
--

