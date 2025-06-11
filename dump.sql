--
-- PostgreSQL database dump
--

-- Dumped from database version 14.17 (Ubuntu 14.17-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.17 (Ubuntu 14.17-0ubuntu0.22.04.1)

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
-- Name: graduate; Type: TABLE; Schema: public; Owner: zebra
--

CREATE TABLE public.graduate (
    id integer NOT NULL,
    student_id integer,
    name character varying(50),
    "group" character varying(50),
    topic character varying(200),
    supervisor character varying(50),
    status character varying(50),
    message character varying(200)
);


ALTER TABLE public.graduate OWNER TO zebra;

--
-- Name: graduate_id_seq; Type: SEQUENCE; Schema: public; Owner: zebra
--

CREATE SEQUENCE public.graduate_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.graduate_id_seq OWNER TO zebra;

--
-- Name: graduate_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zebra
--

ALTER SEQUENCE public.graduate_id_seq OWNED BY public.graduate.id;


--
-- Name: group; Type: TABLE; Schema: public; Owner: zebra
--

CREATE TABLE public."group" (
    id integer NOT NULL,
    title character varying(50),
    year integer,
    head_teacher character varying(50)
);


ALTER TABLE public."group" OWNER TO zebra;

--
-- Name: group_id_seq; Type: SEQUENCE; Schema: public; Owner: zebra
--

CREATE SEQUENCE public.group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.group_id_seq OWNER TO zebra;

--
-- Name: group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zebra
--

ALTER SEQUENCE public.group_id_seq OWNED BY public."group".id;


--
-- Name: intern; Type: TABLE; Schema: public; Owner: zebra
--

CREATE TABLE public.intern (
    id integer NOT NULL,
    student_id integer,
    name character varying(50),
    place character varying(70),
    "group" character varying(50),
    year integer,
    head_teacher character varying(50),
    score numeric(8,6),
    letter character varying(200),
    status character varying(50),
    message character varying(200)
);


ALTER TABLE public.intern OWNER TO zebra;

--
-- Name: intern_id_seq; Type: SEQUENCE; Schema: public; Owner: zebra
--

CREATE SEQUENCE public.intern_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.intern_id_seq OWNER TO zebra;

--
-- Name: intern_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zebra
--

ALTER SEQUENCE public.intern_id_seq OWNED BY public.intern.id;


--
-- Name: place; Type: TABLE; Schema: public; Owner: zebra
--

CREATE TABLE public.place (
    id integer NOT NULL,
    title character varying(100) NOT NULL,
    occupation character varying(100),
    places integer NOT NULL,
    max_places integer NOT NULL,
    requirements character varying(500),
    outlook character varying(500),
    contacts character varying(100)
);


ALTER TABLE public.place OWNER TO zebra;

--
-- Name: place_id_seq; Type: SEQUENCE; Schema: public; Owner: zebra
--

CREATE SEQUENCE public.place_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.place_id_seq OWNER TO zebra;

--
-- Name: place_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zebra
--

ALTER SEQUENCE public.place_id_seq OWNED BY public.place.id;


--
-- Name: review; Type: TABLE; Schema: public; Owner: zebra
--

CREATE TABLE public.review (
    id integer NOT NULL,
    rating integer,
    text text,
    date timestamp without time zone,
    id_place integer
);


ALTER TABLE public.review OWNER TO zebra;

--
-- Name: review_id_seq; Type: SEQUENCE; Schema: public; Owner: zebra
--

CREATE SEQUENCE public.review_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.review_id_seq OWNER TO zebra;

--
-- Name: review_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zebra
--

ALTER SEQUENCE public.review_id_seq OWNED BY public.review.id;


--
-- Name: standart; Type: TABLE; Schema: public; Owner: zebra
--

CREATE TABLE public.standart (
    id integer NOT NULL,
    title character varying(100),
    taken integer
);


ALTER TABLE public.standart OWNER TO zebra;

--
-- Name: standart_id_seq; Type: SEQUENCE; Schema: public; Owner: zebra
--

CREATE SEQUENCE public.standart_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.standart_id_seq OWNER TO zebra;

--
-- Name: standart_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zebra
--

ALTER SEQUENCE public.standart_id_seq OWNED BY public.standart.id;


--
-- Name: student; Type: TABLE; Schema: public; Owner: zebra
--

CREATE TABLE public.student (
    id integer NOT NULL,
    name character varying(50),
    student_number character varying(20),
    score numeric(8,6),
    "group" character varying(50)
);


ALTER TABLE public.student OWNER TO zebra;

--
-- Name: student_id_seq; Type: SEQUENCE; Schema: public; Owner: zebra
--

CREATE SEQUENCE public.student_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.student_id_seq OWNER TO zebra;

--
-- Name: student_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zebra
--

ALTER SEQUENCE public.student_id_seq OWNED BY public.student.id;


--
-- Name: teacher; Type: TABLE; Schema: public; Owner: zebra
--

CREATE TABLE public.teacher (
    id integer NOT NULL,
    name character varying(50),
    url character varying(200)
);


ALTER TABLE public.teacher OWNER TO zebra;

--
-- Name: teacher_id_seq; Type: SEQUENCE; Schema: public; Owner: zebra
--

CREATE SEQUENCE public.teacher_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.teacher_id_seq OWNER TO zebra;

--
-- Name: teacher_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zebra
--

ALTER SEQUENCE public.teacher_id_seq OWNED BY public.teacher.id;


--
-- Name: topic; Type: TABLE; Schema: public; Owner: zebra
--

CREATE TABLE public.topic (
    id integer NOT NULL,
    title character varying(100)
);


ALTER TABLE public.topic OWNER TO zebra;

--
-- Name: topic_id_seq; Type: SEQUENCE; Schema: public; Owner: zebra
--

CREATE SEQUENCE public.topic_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.topic_id_seq OWNER TO zebra;

--
-- Name: topic_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zebra
--

ALTER SEQUENCE public.topic_id_seq OWNED BY public.topic.id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: zebra
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    name character varying(50),
    login character varying(50),
    password character varying(200),
    practice_deadline timestamp without time zone,
    vkr_deadline timestamp without time zone,
    supervisor_deadline timestamp without time zone,
    role character varying(50)
);


ALTER TABLE public."user" OWNER TO zebra;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: zebra
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_id_seq OWNER TO zebra;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zebra
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- Name: graduate id; Type: DEFAULT; Schema: public; Owner: zebra
--

ALTER TABLE ONLY public.graduate ALTER COLUMN id SET DEFAULT nextval('public.graduate_id_seq'::regclass);


--
-- Name: group id; Type: DEFAULT; Schema: public; Owner: zebra
--

ALTER TABLE ONLY public."group" ALTER COLUMN id SET DEFAULT nextval('public.group_id_seq'::regclass);


--
-- Name: intern id; Type: DEFAULT; Schema: public; Owner: zebra
--

ALTER TABLE ONLY public.intern ALTER COLUMN id SET DEFAULT nextval('public.intern_id_seq'::regclass);


--
-- Name: place id; Type: DEFAULT; Schema: public; Owner: zebra
--

ALTER TABLE ONLY public.place ALTER COLUMN id SET DEFAULT nextval('public.place_id_seq'::regclass);


--
-- Name: review id; Type: DEFAULT; Schema: public; Owner: zebra
--

ALTER TABLE ONLY public.review ALTER COLUMN id SET DEFAULT nextval('public.review_id_seq'::regclass);


--
-- Name: standart id; Type: DEFAULT; Schema: public; Owner: zebra
--

ALTER TABLE ONLY public.standart ALTER COLUMN id SET DEFAULT nextval('public.standart_id_seq'::regclass);


--
-- Name: student id; Type: DEFAULT; Schema: public; Owner: zebra
--

ALTER TABLE ONLY public.student ALTER COLUMN id SET DEFAULT nextval('public.student_id_seq'::regclass);


--
-- Name: teacher id; Type: DEFAULT; Schema: public; Owner: zebra
--

ALTER TABLE ONLY public.teacher ALTER COLUMN id SET DEFAULT nextval('public.teacher_id_seq'::regclass);


--
-- Name: topic id; Type: DEFAULT; Schema: public; Owner: zebra
--

ALTER TABLE ONLY public.topic ALTER COLUMN id SET DEFAULT nextval('public.topic_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: zebra
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- Data for Name: graduate; Type: TABLE DATA; Schema: public; Owner: zebra
--

COPY public.graduate (id, student_id, name, "group", topic, supervisor, status, message) FROM stdin;
\.


--
-- Data for Name: group; Type: TABLE DATA; Schema: public; Owner: zebra
--

COPY public."group" (id, title, year, head_teacher) FROM stdin;
\.


--
-- Data for Name: intern; Type: TABLE DATA; Schema: public; Owner: zebra
--

COPY public.intern (id, student_id, name, place, "group", year, head_teacher, score, letter, status, message) FROM stdin;
\.


--
-- Data for Name: place; Type: TABLE DATA; Schema: public; Owner: zebra
--

COPY public.place (id, title, occupation, places, max_places, requirements, outlook, contacts) FROM stdin;
\.


--
-- Data for Name: review; Type: TABLE DATA; Schema: public; Owner: zebra
--

COPY public.review (id, rating, text, date, id_place) FROM stdin;
\.


--
-- Data for Name: standart; Type: TABLE DATA; Schema: public; Owner: zebra
--

COPY public.standart (id, title, taken) FROM stdin;
\.


--
-- Data for Name: student; Type: TABLE DATA; Schema: public; Owner: zebra
--

COPY public.student (id, name, student_number, score, "group") FROM stdin;
\.


--
-- Data for Name: teacher; Type: TABLE DATA; Schema: public; Owner: zebra
--

COPY public.teacher (id, name, url) FROM stdin;
\.


--
-- Data for Name: topic; Type: TABLE DATA; Schema: public; Owner: zebra
--

COPY public.topic (id, title) FROM stdin;
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: zebra
--

COPY public."user" (id, name, login, password, practice_deadline, vkr_deadline, supervisor_deadline, role) FROM stdin;
\.


--
-- Name: graduate_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zebra
--

SELECT pg_catalog.setval('public.graduate_id_seq', 1, false);


--
-- Name: group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zebra
--

SELECT pg_catalog.setval('public.group_id_seq', 1, false);


--
-- Name: intern_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zebra
--

SELECT pg_catalog.setval('public.intern_id_seq', 1, false);


--
-- Name: place_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zebra
--

SELECT pg_catalog.setval('public.place_id_seq', 1, false);


--
-- Name: review_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zebra
--

SELECT pg_catalog.setval('public.review_id_seq', 1, false);


--
-- Name: standart_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zebra
--

SELECT pg_catalog.setval('public.standart_id_seq', 1, false);


--
-- Name: student_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zebra
--

SELECT pg_catalog.setval('public.student_id_seq', 1, false);


--
-- Name: teacher_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zebra
--

SELECT pg_catalog.setval('public.teacher_id_seq', 1, false);


--
-- Name: topic_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zebra
--

SELECT pg_catalog.setval('public.topic_id_seq', 1, false);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zebra
--

SELECT pg_catalog.setval('public.user_id_seq', 1, false);


--
-- Name: graduate graduate_pkey; Type: CONSTRAINT; Schema: public; Owner: zebra
--

ALTER TABLE ONLY public.graduate
    ADD CONSTRAINT graduate_pkey PRIMARY KEY (id);


--
-- Name: group group_pkey; Type: CONSTRAINT; Schema: public; Owner: zebra
--

ALTER TABLE ONLY public."group"
    ADD CONSTRAINT group_pkey PRIMARY KEY (id);


--
-- Name: intern intern_pkey; Type: CONSTRAINT; Schema: public; Owner: zebra
--

ALTER TABLE ONLY public.intern
    ADD CONSTRAINT intern_pkey PRIMARY KEY (id);


--
-- Name: place place_pkey; Type: CONSTRAINT; Schema: public; Owner: zebra
--

ALTER TABLE ONLY public.place
    ADD CONSTRAINT place_pkey PRIMARY KEY (id);


--
-- Name: review review_pkey; Type: CONSTRAINT; Schema: public; Owner: zebra
--

ALTER TABLE ONLY public.review
    ADD CONSTRAINT review_pkey PRIMARY KEY (id);


--
-- Name: standart standart_pkey; Type: CONSTRAINT; Schema: public; Owner: zebra
--

ALTER TABLE ONLY public.standart
    ADD CONSTRAINT standart_pkey PRIMARY KEY (id);


--
-- Name: student student_pkey; Type: CONSTRAINT; Schema: public; Owner: zebra
--

ALTER TABLE ONLY public.student
    ADD CONSTRAINT student_pkey PRIMARY KEY (id);


--
-- Name: teacher teacher_pkey; Type: CONSTRAINT; Schema: public; Owner: zebra
--

ALTER TABLE ONLY public.teacher
    ADD CONSTRAINT teacher_pkey PRIMARY KEY (id);


--
-- Name: topic topic_pkey; Type: CONSTRAINT; Schema: public; Owner: zebra
--

ALTER TABLE ONLY public.topic
    ADD CONSTRAINT topic_pkey PRIMARY KEY (id);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: zebra
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: review review_id_place_fkey; Type: FK CONSTRAINT; Schema: public; Owner: zebra
--

ALTER TABLE ONLY public.review
    ADD CONSTRAINT review_id_place_fkey FOREIGN KEY (id_place) REFERENCES public.place(id);


--
-- PostgreSQL database dump complete
--

