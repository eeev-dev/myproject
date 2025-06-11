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
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: zebra
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO zebra;

--
-- Name: graduate; Type: TABLE; Schema: public; Owner: zebra
--

CREATE TABLE public.graduate (
    id integer NOT NULL,
    topic character varying(200),
    status character varying(50),
    message character varying(200),
    name character varying(50),
    "group" character varying(50),
    supervisor character varying(50)
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
    status character varying(50),
    place character varying(70),
    letter character varying(200),
    message character varying(200),
    head_teacher character varying(50),
    name character varying(50),
    "group" character varying(50),
    year integer,
    score numeric(8,6)
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
    places integer NOT NULL,
    requirements character varying(500),
    outlook character varying(500),
    contacts character varying(100),
    occupation character varying(100),
    max_places integer DEFAULT 0 NOT NULL
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
    id_place integer,
    date timestamp without time zone
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
    role character varying(50),
    supervisor_deadline timestamp without time zone
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
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: zebra
--

COPY public.alembic_version (version_num) FROM stdin;
ffed8e679a2e
\.


--
-- Data for Name: graduate; Type: TABLE DATA; Schema: public; Owner: zebra
--

COPY public.graduate (id, topic, status, message, name, "group", supervisor) FROM stdin;
3	\N	Без заявки	\N	Ырысова Саамал Алмазовна	ИВТ(б)-1-22	\N
4	\N	Без заявки	\N	Нурланова Жанара Нурлановна	ИВТ(б)-1-22	\N
5	\N	Без заявки	\N	Талантбеков Султанбек Талантбекович	ИВТ(б)-1-22	\N
6	\N	Без заявки	\N	Жыргалбекова Нурпери Жыргалбековна	ИВТ(б)-1-22	\N
7	\N	Без заявки	\N	Нургазиев Миранша Нургазиевич	ИВТ(б)-1-22	\N
8	\N	Без заявки	\N	Исакова Буузулайка Аллакуловна	ИВТ(б)-1-22	\N
9	\N	Без заявки	\N	Шеримбекова Аяна Садырбековна	ИВТ(б)-1-22	\N
10	\N	Без заявки	\N	Урусалиев Марсел Мирланович	ИВТ(б)-1-22	\N
11	\N	Без заявки	\N	Оринбаев Муроджон Хурсанбекович	ИВТ(б)-1-22	\N
12	\N	Без заявки	\N	Керимбеков Нурбек Байышович	ИВТ(б)-1-22	\N
13	\N	Без заявки	\N	Тилекбекова Альбина Тилекбековна	ИВТ(б)-1-22	\N
1	Разработка клиент-серверного мобильного приложения "Студент"	Проверка пройдена	\N	Рыскадырова Сезим Кумаровна	ИВТ(б)-1-22	Исраилова Н.А.
2	\N	Без заявки	\N	Жазымбекова Айзирек Орозбаевна	ИВТ(б)-1-22	Исраилова Н.А.
14	\N	Без заявки	\N	Бекболиев Эрлан Алмазбекович	ИВТ(б)-1-22	\N
15	\N	Без заявки	\N	Амираев Амирбек Нурланбекович	ИВТ(б)-1-22	\N
16	\N	Без заявки	\N	Сатылганова Бурулай Алтынбековна	ИВТ(б)-1-22	\N
17	\N	Без заявки	\N	Сулайманова Жеринди Нурдиновна	ИВТ(б)-1-22	\N
18	\N	Без заявки	\N	Дембицкий Николай Денисович	ИВТ(б)-1-22	\N
19	\N	Без заявки	\N	Шевелев Станислав Владимирович	ИВТ(б)-1-22	\N
20	\N	Без заявки	\N	Тенизбаев Илимбек Абдирасулович	ИВТ(б)-1-22	\N
21	\N	Без заявки	\N	Ечин Илья Васильевич	ИВТ(б)-1-22	\N
22	\N	Без заявки	\N	Смаилбеков Иса Жаныбекович	ИВТ(б)-1-22	\N
23	\N	Без заявки	\N	Мединин Никита Анатольевич	ИВТ(б)-1-22	\N
24	\N	Без заявки	\N	Мукталипов Адис Абазбекович	ИВТ(б)-1-22	\N
25	\N	Без заявки	\N	Токтанбеков Алмаз Абу-Насирович	ИВТ(б)-1-22	\N
26	\N	Без заявки	\N	Асангулов Илгиз Талантбекович	ИВТ(б)-1-22	\N
27	\N	Без заявки	\N	Раева Нуриза Алтынбековна	ИВТ(б)-1-22	\N
28	\N	Без заявки	\N	Абдылдаев Атагельди Маратович	ИВТ(б)-1-22	\N
29	\N	Без заявки	\N	Ибрагимов Эмир Мухтарджанович	ИВТ(б)-1-22	\N
30	\N	Без заявки	\N	Белекова Айпери Кубанычбековна	ИВТ(б)-1-22	\N
31	\N	Без заявки	\N	Титов Александр Дмитриевич	ИБ(инж)-1-22	\N
32	\N	Без заявки	\N	Абилесов Каныбек Дженишбекович	ИБ(инж)-1-22	\N
33	\N	Без заявки	\N	Бейшекеев Максат Бисланович	ИБ(инж)-1-22	\N
34	\N	Без заявки	\N	Калиев Жоомарт Умутбекович	ИБ(инж)-1-22	\N
35	\N	Без заявки	\N	Гетман Даниил Олегович	ИБ(инж)-1-22	\N
36	\N	Без заявки	\N	Руслан уулу Бакай 	ИБ(инж)-1-22	\N
37	\N	Без заявки	\N	Сухарев Константин Владимирович	ИБ(инж)-1-22	\N
38	\N	Без заявки	\N	Тагайбекова Астра Тагайбековна	ИБ(инж)-1-22	\N
39	\N	Без заявки	\N	Элдияров Дастан Тельманович	ИБ(инж)-1-22	\N
40	\N	Без заявки	\N	Бейшебаев Арген Нурланович	ИБ(инж)-1-22	\N
41	\N	Без заявки	\N	Таалаев Эмир Таалаевич	ИБ(инж)-1-22	\N
42	\N	Без заявки	\N	Мелисов Айбек Мелисович	ИВТ(б)-2-22	\N
43	\N	Без заявки	\N	Нурланова Акмарал 	ИВТ(б)-2-22	\N
44	\N	Без заявки	\N	Асанбекова Акылай Азаматовна	ИВТ(б)-2-22	\N
45	\N	Без заявки	\N	Кыпчаков Рысбек Мурадилович	ИВТ(б)-2-22	\N
46	\N	Без заявки	\N	Атаканов Адил Нуржанович	ИВТ(б)-2-22	\N
47	\N	Без заявки	\N	Султанов Динислам Султанович	ИВТ(б)-2-22	\N
48	\N	Без заявки	\N	Мирлан уулу Нурсултан 	ИВТ(б)-2-22	\N
49	\N	Без заявки	\N	Абдыжалиев Улукбек Бактыгулович	ИВТ(б)-2-22	\N
50	\N	Без заявки	\N	Полотов Айбек Авазбекович	ИВТ(б)-2-22	\N
51	\N	Без заявки	\N	Казбеков Актенир Бакытович	ИВТ(б)-2-22	\N
52	\N	Без заявки	\N	Сабирова Бактыгул Дыйканбаевна	ИВТ(б)-2-22	\N
53	\N	Без заявки	\N	Жусупова Асел Талантбековна	ИВТ(б)-2-22	\N
54	\N	Без заявки	\N	Мамыралиев Азамат Марсбекович	ИВТ(б)-2-22	\N
55	\N	Без заявки	\N	Таирбеков Нурислам Нурдинович	ИВТ(б)-2-22	\N
\.


--
-- Data for Name: group; Type: TABLE DATA; Schema: public; Owner: zebra
--

COPY public."group" (id, title, year, head_teacher) FROM stdin;
1	ИВТ(б)-1-22	4	Исраилова Н.А.
3	ИБ(инж)-1-22	4	Шаршеева К.Т.
2	ИВТ(б)-2-22	4	Момуналиева Н.Т.
\.


--
-- Data for Name: intern; Type: TABLE DATA; Schema: public; Owner: zebra
--

COPY public.intern (id, status, place, letter, message, head_teacher, name, "group", year, score) FROM stdin;
1	Выбор кафедры	\N	\N	\N	Исраилова Н.А.	Рыскадырова Сезим Кумаровна	ИВТ(б)-1-22	4	17.000000
2	Выбор кафедры	\N	\N	\N	Исраилова Н.А.	Жазымбекова Айзирек Орозбаевна	ИВТ(б)-1-22	4	8.291667
3	Выбор кафедры	\N	\N	\N	Исраилова Н.А.	Ырысова Саамал Алмазовна	ИВТ(б)-1-22	4	5.083333
4	Выбор кафедры	\N	\N	\N	Исраилова Н.А.	Нурланова Жанара Нурлановна	ИВТ(б)-1-22	4	5.500000
5	Выбор кафедры	\N	\N	\N	Исраилова Н.А.	Талантбеков Султанбек Талантбекович	ИВТ(б)-1-22	4	25.208333
6	Выбор кафедры	\N	\N	\N	Исраилова Н.А.	Жыргалбекова Нурпери Жыргалбековна	ИВТ(б)-1-22	4	5.083333
7	Выбор кафедры	\N	\N	\N	Исраилова Н.А.	Нургазиев Миранша Нургазиевич	ИВТ(б)-1-22	4	24.958333
8	Выбор кафедры	\N	\N	\N	Исраилова Н.А.	Исакова Буузулайка Аллакуловна	ИВТ(б)-1-22	4	8.208333
9	Выбор кафедры	\N	\N	\N	Исраилова Н.А.	Шеримбекова Аяна Садырбековна	ИВТ(б)-1-22	4	10.125000
10	Выбор кафедры	\N	\N	\N	Исраилова Н.А.	Урусалиев Марсел Мирланович	ИВТ(б)-1-22	4	2.750000
11	Выбор кафедры	\N	\N	\N	Исраилова Н.А.	Оринбаев Муроджон Хурсанбекович	ИВТ(б)-1-22	4	23.250000
12	Выбор кафедры	\N	\N	\N	Исраилова Н.А.	Керимбеков Нурбек Байышович	ИВТ(б)-1-22	4	28.000000
13	Выбор кафедры	\N	\N	\N	Исраилова Н.А.	Тилекбекова Альбина Тилекбековна	ИВТ(б)-1-22	4	5.000000
14	Выбор кафедры	\N	\N	\N	Исраилова Н.А.	Бекболиев Эрлан Алмазбекович	ИВТ(б)-1-22	4	23.541667
15	Выбор кафедры	\N	\N	\N	Исраилова Н.А.	Амираев Амирбек Нурланбекович	ИВТ(б)-1-22	4	24.958333
16	Выбор кафедры	\N	\N	\N	Исраилова Н.А.	Сатылганова Бурулай Алтынбековна	ИВТ(б)-1-22	4	8.000000
17	Выбор кафедры	\N	\N	\N	Исраилова Н.А.	Сулайманова Жеринди Нурдиновна	ИВТ(б)-1-22	4	0.416667
18	Выбор кафедры	\N	\N	\N	Исраилова Н.А.	Дембицкий Николай Денисович	ИВТ(б)-1-22	4	4.375000
19	Выбор кафедры	\N	\N	\N	Исраилова Н.А.	Шевелев Станислав Владимирович	ИВТ(б)-1-22	4	32.000000
20	Выбор кафедры	\N	\N	\N	Исраилова Н.А.	Тенизбаев Илимбек Абдирасулович	ИВТ(б)-1-22	4	10.500000
21	Выбор кафедры	\N	\N	\N	Исраилова Н.А.	Ечин Илья Васильевич	ИВТ(б)-1-22	4	27.125000
22	Выбор кафедры	\N	\N	\N	Исраилова Н.А.	Смаилбеков Иса Жаныбекович	ИВТ(б)-1-22	4	23.000000
23	Выбор кафедры	\N	\N	\N	Исраилова Н.А.	Мединин Никита Анатольевич	ИВТ(б)-1-22	4	9.791667
24	Выбор кафедры	\N	\N	\N	Исраилова Н.А.	Мукталипов Адис Абазбекович	ИВТ(б)-1-22	4	4.708333
25	Выбор кафедры	\N	\N	\N	Исраилова Н.А.	Токтанбеков Алмаз Абу-Насирович	ИВТ(б)-1-22	4	13.333333
26	Выбор кафедры	\N	\N	\N	Исраилова Н.А.	Асангулов Илгиз Талантбекович	ИВТ(б)-1-22	4	0.000000
27	Выбор кафедры	\N	\N	\N	Исраилова Н.А.	Раева Нуриза Алтынбековна	ИВТ(б)-1-22	4	8.166667
28	Выбор кафедры	\N	\N	\N	Исраилова Н.А.	Абдылдаев Атагельди Маратович	ИВТ(б)-1-22	4	6.166667
29	Выбор кафедры	\N	\N	\N	Исраилова Н.А.	Ибрагимов Эмир Мухтарджанович	ИВТ(б)-1-22	4	6.541667
30	Выбор кафедры	\N	\N	\N	Исраилова Н.А.	Белекова Айпери Кубанычбековна	ИВТ(б)-1-22	4	6.375000
\.


--
-- Data for Name: place; Type: TABLE DATA; Schema: public; Owner: zebra
--

COPY public.place (id, title, places, requirements, outlook, contacts, occupation, max_places) FROM stdin;
\.


--
-- Data for Name: review; Type: TABLE DATA; Schema: public; Owner: zebra
--

COPY public.review (id, rating, text, id_place, date) FROM stdin;
\.


--
-- Data for Name: standart; Type: TABLE DATA; Schema: public; Owner: zebra
--

COPY public.standart (id, title, taken) FROM stdin;
1	Разработка клиент-серверного мобильного приложения "Студент"	1
\.


--
-- Data for Name: student; Type: TABLE DATA; Schema: public; Owner: zebra
--

COPY public.student (id, name, student_number, score, "group") FROM stdin;
1	Рыскадырова Сезим Кумаровна	22-79615	17.000000	ИВТ(б)-1-22
2	Жазымбекова Айзирек Орозбаевна	21\\46395	8.291667	ИВТ(б)-1-22
3	Ырысова Саамал Алмазовна	21\\46031	5.083333	ИВТ(б)-1-22
4	Нурланова Жанара Нурлановна	22\\48772	5.500000	ИВТ(б)-1-22
5	Талантбеков Султанбек Талантбекович	22\\47839	25.208333	ИВТ(б)-1-22
6	Жыргалбекова Нурпери Жыргалбековна	21\\45416	5.083333	ИВТ(б)-1-22
7	Нургазиев Миранша Нургазиевич	22\\49416	24.958333	ИВТ(б)-1-22
8	Исакова Буузулайка Аллакуловна	21\\45865	8.208333	ИВТ(б)-1-22
9	Шеримбекова Аяна Садырбековна	22\\47686	10.125000	ИВТ(б)-1-22
10	Урусалиев Марсел Мирланович	21\\47014	2.750000	ИВТ(б)-1-22
11	Оринбаев Муроджон Хурсанбекович	22\\48056	23.250000	ИВТ(б)-1-22
12	Керимбеков Нурбек Байышович	22\\48178	28.000000	ИВТ(б)-1-22
13	Тилекбекова Альбина Тилекбековна	22\\48715	5.000000	ИВТ(б)-1-22
14	Бекболиев Эрлан Алмазбекович	22\\49738	23.541667	ИВТ(б)-1-22
15	Амираев Амирбек Нурланбекович	23-139653	24.958333	ИВТ(б)-1-22
16	Сатылганова Бурулай Алтынбековна	21\\46478	8.000000	ИВТ(б)-1-22
17	Сулайманова Жеринди Нурдиновна	22\\48255	0.416667	ИВТ(б)-1-22
18	Дембицкий Николай Денисович	22\\47862	4.375000	ИВТ(б)-1-22
19	Шевелев Станислав Владимирович	21\\46070	32.000000	ИВТ(б)-1-22
20	Тенизбаев Илимбек Абдирасулович	22\\50069	10.500000	ИВТ(б)-1-22
21	Ечин Илья Васильевич	22\\48039	27.125000	ИВТ(б)-1-22
22	Смаилбеков Иса Жаныбекович	21\\46027	23.000000	ИВТ(б)-1-22
23	Мединин Никита Анатольевич	20\\42079	9.791667	ИВТ(б)-1-22
24	Мукталипов Адис Абазбекович	22\\49218	4.708333	ИВТ(б)-1-22
25	Токтанбеков Алмаз Абу-Насирович	22\\49911	13.333333	ИВТ(б)-1-22
26	Асангулов Илгиз Талантбекович	21\\46515	0.000000	ИВТ(б)-1-22
27	Раева Нуриза Алтынбековна	21\\46029	8.166667	ИВТ(б)-1-22
28	Абдылдаев Атагельди Маратович	21\\46521	6.166667	ИВТ(б)-1-22
29	Ибрагимов Эмир Мухтарджанович	22-79634	6.541667	ИВТ(б)-1-22
30	Белекова Айпери Кубанычбековна	22\\47911	6.375000	ИВТ(б)-1-22
31	Титов Александр Дмитриевич	22\\50548	13.333333	ИБ(инж)-1-22
32	Абилесов Каныбек Дженишбекович	22\\49044	25.133333	ИБ(инж)-1-22
33	Бейшекеев Максат Бисланович	22\\48019	18.800000	ИБ(инж)-1-22
34	Калиев Жоомарт Умутбекович	22\\49138	26.400000	ИБ(инж)-1-22
35	Гетман Даниил Олегович	22\\48038	12.733333	ИБ(инж)-1-22
36	Руслан уулу Бакай 	22\\49881	13.466667	ИБ(инж)-1-22
37	Сухарев Константин Владимирович	22\\48111	6.600000	ИБ(инж)-1-22
38	Тагайбекова Астра Тагайбековна	22\\47944	42.866667	ИБ(инж)-1-22
39	Элдияров Дастан Тельманович	22\\50331	23.933333	ИБ(инж)-1-22
40	Бейшебаев Арген Нурланович	22\\49835	41.866667	ИБ(инж)-1-22
41	Таалаев Эмир Таалаевич	22\\49763	15.933333	ИБ(инж)-1-22
42	Мелисов Айбек Мелисович	22\\49679	20.925926	ИВТ(б)-2-22
43	Нурланова Акмарал 	22\\48562	24.074074	ИВТ(б)-2-22
44	Асанбекова Акылай Азаматовна	22\\48803	0.851852	ИВТ(б)-2-22
45	Кыпчаков Рысбек Мурадилович	22\\48420	9.481481	ИВТ(б)-2-22
46	Атаканов Адил Нуржанович	23-138436	4.074074	ИВТ(б)-2-22
47	Султанов Динислам Султанович	21\\46652	0.000000	ИВТ(б)-2-22
48	Мирлан уулу Нурсултан 	22\\48228	24.703704	ИВТ(б)-2-22
49	Абдыжалиев Улукбек Бактыгулович	22\\49326	5.407407	ИВТ(б)-2-22
50	Полотов Айбек Авазбекович	22\\49464	5.259259	ИВТ(б)-2-22
51	Казбеков Актенир Бакытович	21\\46410	10.370370	ИВТ(б)-2-22
52	Сабирова Бактыгул Дыйканбаевна	21\\47414	10.629630	ИВТ(б)-2-22
53	Жусупова Асел Талантбековна	21\\46033	13.703704	ИВТ(б)-2-22
54	Мамыралиев Азамат Марсбекович	22\\49069	6.185185	ИВТ(б)-2-22
55	Таирбеков Нурислам Нурдинович	22\\49837	4.592593	ИВТ(б)-2-22
\.


--
-- Data for Name: teacher; Type: TABLE DATA; Schema: public; Owner: zebra
--

COPY public.teacher (id, name, url) FROM stdin;
1	Исраилова Нелла Амантаевна	https://us04web.zoom.us/j/3260530013?pwd=SzdGNDI4TDQwRnBVM3pjREgvdFdWdz09
2	Бакасова Пери Султановна	https://meet.google.com/tbw-itkf-xka
3	Эркинбек кызы Алтынай	https://meet.google.com/oed-ssio-ndm
4	Момуналиева Нуризат Тыныбековна	https://us04web.zoom.us/j/72602412886?pwd=pHjNgqaVrnWERdizLbyQZRDM1Nl6o6.1
5	Шаршеева Кундуз Токтобековна	https://us04web.zoom.us/j/78136553614?pwd=dU1jK2Z0NjFQZXBSZ1pBZ0pNQTRYZz09
\.


--
-- Data for Name: topic; Type: TABLE DATA; Schema: public; Owner: zebra
--

COPY public.topic (id, title) FROM stdin;
1	Разработка веб-приложения для управления задачами
2	Создание мобильного приложения для учета личных расходов
3	Система онлайн-тестирования с автоматической проверкой
4	Веб-платформа для организации дистанционного обучения
5	Разработка чат-бота для Telegram на Python
6	Информационная система учета студентов учебного заведения
7	Программа для распознавания лиц с использованием OpenCV
8	Приложение для отслеживания физической активности пользователей
9	Разработка игры с использованием Unity и C#
10	Сервис рекомендаций фильмов на основе машинного обучения
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: zebra
--

COPY public."user" (id, name, login, password, practice_deadline, vkr_deadline, role, supervisor_deadline) FROM stdin;
5	Ъеъев Ъ. Ъ.	admin	$2b$12$x9/9OjkmLpm3Ux7o3SnGUOiBGEKXP5bBubniMqE9NGvsH5u9K081q	\N	\N	admin	\N
1	alkhflajlf	akljflajf	$2b$12$EHcuSkt7HHFM2g/TjmWHruvWfxYtletZgVCRkN3rIbAdXqrBpDZFS	\N	\N	user	\N
2	Я убила	ikilled45	$2b$12$66Qp.rN5mvZ/mb/42gnIpe3Skiy9wORwGT8QrLEjuxwQk75mju/0i	\N	\N	user	\N
3	Исраилова Н.А.	nella11	$2b$12$MGHuuRKPxcGw3RZAoR9CI.dXkZwuNMsGSxltQY/4qMhq18voP9XaC	2025-05-23 12:00:00	2025-06-15 00:00:00	user	2025-06-13 00:00:00
4	Шаршеева К.Т.	shkunduz	$2b$12$D4M6Iqr4QIt9YjKWhz6PgOqVSUE80FUIq7WfGt0fSiFgXj7ouqaLa	\N	2025-06-14 00:00:00	user	2025-06-12 00:00:00
\.


--
-- Name: graduate_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zebra
--

SELECT pg_catalog.setval('public.graduate_id_seq', 55, true);


--
-- Name: group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zebra
--

SELECT pg_catalog.setval('public.group_id_seq', 3, true);


--
-- Name: intern_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zebra
--

SELECT pg_catalog.setval('public.intern_id_seq', 30, true);


--
-- Name: place_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zebra
--

SELECT pg_catalog.setval('public.place_id_seq', 2, true);


--
-- Name: review_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zebra
--

SELECT pg_catalog.setval('public.review_id_seq', 4, true);


--
-- Name: standart_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zebra
--

SELECT pg_catalog.setval('public.standart_id_seq', 1, true);


--
-- Name: student_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zebra
--

SELECT pg_catalog.setval('public.student_id_seq', 55, true);


--
-- Name: teacher_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zebra
--

SELECT pg_catalog.setval('public.teacher_id_seq', 5, true);


--
-- Name: topic_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zebra
--

SELECT pg_catalog.setval('public.topic_id_seq', 10, true);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zebra
--

SELECT pg_catalog.setval('public.user_id_seq', 5, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: zebra
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


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
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

GRANT ALL ON SCHEMA public TO zebra;


--
-- PostgreSQL database dump complete
--

