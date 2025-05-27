--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5 (Debian 17.5-1.pgdg120+1)
-- Dumped by pg_dump version 17.5 (Debian 17.5-1.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- Name: intern; Type: TABLE; Schema: public; Owner: zebra
--

CREATE TABLE public.intern (
    id integer NOT NULL,
    student_number character varying(20),
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


ALTER SEQUENCE public.intern_id_seq OWNER TO zebra;

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


ALTER SEQUENCE public.place_id_seq OWNER TO zebra;

--
-- Name: place_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zebra
--

ALTER SEQUENCE public.place_id_seq OWNED BY public.place.id;


--
-- Name: post; Type: TABLE; Schema: public; Owner: zebra
--

CREATE TABLE public.post (
    id integer NOT NULL,
    subject character varying(255),
    teacher character varying(255),
    student character varying(255),
    date timestamp without time zone
);


ALTER TABLE public.post OWNER TO zebra;

--
-- Name: post_id_seq; Type: SEQUENCE; Schema: public; Owner: zebra
--

CREATE SEQUENCE public.post_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.post_id_seq OWNER TO zebra;

--
-- Name: post_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zebra
--

ALTER SEQUENCE public.post_id_seq OWNED BY public.post.id;


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


ALTER SEQUENCE public.review_id_seq OWNER TO zebra;

--
-- Name: review_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zebra
--

ALTER SEQUENCE public.review_id_seq OWNED BY public.review.id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: zebra
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    name character varying(50),
    login character varying(50),
    password character varying(200),
    practice_deadline timestamp without time zone,
    vkr_deadline timestamp without time zone
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


ALTER SEQUENCE public.user_id_seq OWNER TO zebra;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zebra
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- Name: intern id; Type: DEFAULT; Schema: public; Owner: zebra
--

ALTER TABLE ONLY public.intern ALTER COLUMN id SET DEFAULT nextval('public.intern_id_seq'::regclass);


--
-- Name: place id; Type: DEFAULT; Schema: public; Owner: zebra
--

ALTER TABLE ONLY public.place ALTER COLUMN id SET DEFAULT nextval('public.place_id_seq'::regclass);


--
-- Name: post id; Type: DEFAULT; Schema: public; Owner: zebra
--

ALTER TABLE ONLY public.post ALTER COLUMN id SET DEFAULT nextval('public.post_id_seq'::regclass);


--
-- Name: review id; Type: DEFAULT; Schema: public; Owner: zebra
--

ALTER TABLE ONLY public.review ALTER COLUMN id SET DEFAULT nextval('public.review_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: zebra
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- Data for Name: intern; Type: TABLE DATA; Schema: public; Owner: zebra
--

COPY public.intern (id, student_number, name, place, "group", year, head_teacher, score, letter, status, message) FROM stdin;
2	21\\46395	Жазымбекова Айзирек Орозбаевна	\N	ИВТ(б)-1-22	3	Исраилова Н. А.	8.291667	\N	Без заявки	\N
3	21\\46031	Ырысова Саамал Алмазовна	\N	ИВТ(б)-1-22	3	Исраилова Н. А.	5.083333	\N	Без заявки	\N
4	22\\48772	Нурланова Жанара Нурлановна	\N	ИВТ(б)-1-22	3	Исраилова Н. А.	5.500000	\N	Без заявки	\N
5	22\\47839	Талантбеков Султанбек Талантбекович	\N	ИВТ(б)-1-22	3	Исраилова Н. А.	25.208333	\N	Без заявки	\N
6	21\\45416	Жыргалбекова Нурпери Жыргалбековна	\N	ИВТ(б)-1-22	3	Исраилова Н. А.	5.083333	\N	Без заявки	\N
7	22\\49416	Нургазиев Миранша Нургазиевич	\N	ИВТ(б)-1-22	3	Исраилова Н. А.	24.958333	\N	Без заявки	\N
8	21\\45865	Исакова Буузулайка Аллакуловна	\N	ИВТ(б)-1-22	3	Исраилова Н. А.	8.208333	\N	Без заявки	\N
9	22\\47686	Шеримбекова Аяна Садырбековна	\N	ИВТ(б)-1-22	3	Исраилова Н. А.	10.125000	\N	Без заявки	\N
10	21\\47014	Урусалиев Марсел Мирланович	\N	ИВТ(б)-1-22	3	Исраилова Н. А.	2.750000	\N	Без заявки	\N
11	22\\48056	Оринбаев Муроджон Хурсанбекович	\N	ИВТ(б)-1-22	3	Исраилова Н. А.	23.250000	\N	Без заявки	\N
12	22\\48178	Керимбеков Нурбек Байышович	\N	ИВТ(б)-1-22	3	Исраилова Н. А.	28.000000	\N	Без заявки	\N
14	22\\49738	Бекболиев Эрлан Алмазбекович	\N	ИВТ(б)-1-22	3	Исраилова Н. А.	23.541667	\N	Без заявки	\N
15	23-139653	Амираев Амирбек Нурланбекович	\N	ИВТ(б)-1-22	3	Исраилова Н. А.	24.958333	\N	Без заявки	\N
17	22\\48255	Сулайманова Жеринди Нурдиновна	\N	ИВТ(б)-1-22	3	Исраилова Н. А.	0.416667	\N	Без заявки	\N
18	22\\47862	Дембицкий Николай Денисович	\N	ИВТ(б)-1-22	3	Исраилова Н. А.	4.375000	\N	Без заявки	\N
19	21\\46070	Шевелев Станислав Владимирович	\N	ИВТ(б)-1-22	3	Исраилова Н. А.	32.000000	\N	Без заявки	\N
22	21\\46027	Смаилбеков Иса Жаныбекович	\N	ИВТ(б)-1-22	3	Исраилова Н. А.	23.000000	\N	Без заявки	\N
23	20\\42079	Мединин Никита Анатольевич	\N	ИВТ(б)-1-22	3	Исраилова Н. А.	9.791667	\N	Без заявки	\N
24	22\\49218	Мукталипов Адис Абазбекович	\N	ИВТ(б)-1-22	3	Исраилова Н. А.	4.708333	\N	Без заявки	\N
25	22\\49911	Токтанбеков Алмаз Абу-Насирович	\N	ИВТ(б)-1-22	3	Исраилова Н. А.	13.333333	\N	Без заявки	\N
26	21\\46515	Асангулов Илгиз Талантбекович	\N	ИВТ(б)-1-22	3	Исраилова Н. А.	0.000000	\N	Без заявки	\N
31	22\\50548	Титов Александр Дмитриевич	\N	ИБ(инж)-1-22	3	Шаршеева К. Т.	13.333333	\N	Без заявки	\N
32	22\\49044	Абилесов Каныбек Дженишбекович	\N	ИБ(инж)-1-22	3	Шаршеева К. Т.	25.133333	\N	Без заявки	\N
33	22\\48019	Бейшекеев Максат Бисланович	\N	ИБ(инж)-1-22	3	Шаршеева К. Т.	18.800000	\N	Без заявки	\N
34	22\\49138	Калиев Жоомарт Умутбекович	\N	ИБ(инж)-1-22	3	Шаршеева К. Т.	26.400000	\N	Без заявки	\N
35	22\\48038	Гетман Даниил Олегович	\N	ИБ(инж)-1-22	3	Шаршеева К. Т.	12.733333	\N	Без заявки	\N
36	22\\49881	Руслан уулу Бакай 	\N	ИБ(инж)-1-22	3	Шаршеева К. Т.	13.466667	\N	Без заявки	\N
37	22\\48111	Сухарев Константин Владимирович	\N	ИБ(инж)-1-22	3	Шаршеева К. Т.	6.600000	\N	Без заявки	\N
38	22\\47944	Тагайбекова Астра Тагайбековна	\N	ИБ(инж)-1-22	3	Шаршеева К. Т.	42.866667	\N	Без заявки	\N
39	22\\50331	Элдияров Дастан Тельманович	\N	ИБ(инж)-1-22	3	Шаршеева К. Т.	23.933333	\N	Без заявки	\N
40	22\\49835	Бейшебаев Арген Нурланович	\N	ИБ(инж)-1-22	3	Шаршеева К. Т.	41.866667	\N	Без заявки	\N
41	22\\49763	Таалаев Эмир Таалаевич	\N	ИБ(инж)-1-22	3	Шаршеева К. Т.	15.933333	\N	Без заявки	\N
42	22\\49679	Мелисов Айбек Мелисович	\N	ИВТ(б)-2-22	3	Момуналиева Н. Т.	20.925926	\N	Без заявки	\N
43	22\\48562	Нурланова Акмарал 	\N	ИВТ(б)-2-22	3	Момуналиева Н. Т.	24.074074	\N	Без заявки	\N
44	22\\48803	Асанбекова Акылай Азаматовна	\N	ИВТ(б)-2-22	3	Момуналиева Н. Т.	0.851852	\N	Без заявки	\N
30	22\\47911	Белекова Айпери Кубанычбековна	Свое место практики	ИВТ(б)-1-22	3	Исраилова Н. А.	6.375000	105452d2eca9be0b.jpg	Ожидает подтверждения	\N
13	22\\48715	Тилекбекова Альбина Тилекбековна	“Партнер софт” ЖЧК	ИВТ(б)-1-22	3	Исраилова Н. А.	5.000000	\N	Подтвержден	\N
20	22\\50069	Тенизбаев Илимбек Абдирасулович	Intermedia	ИВТ(б)-1-22	3	Исраилова Н. А.	10.500000	\N	Подтвержден	\N
27	21\\46029	Раева Нуриза Алтынбековна	Свое место практики	ИВТ(б)-1-22	3	Исраилова Н. А.	8.166667	77b1c0e72024ae07.jpg	Подтвержден	\N
16	21\\46478	Сатылганова Бурулай Алтынбековна	Свое место практики	ИВТ(б)-1-22	3	Исраилова Н. А.	8.000000		Без заявки	\N
29	22-79634	Ибрагимов Эмир Мухтарджанович	Intermedia	ИВТ(б)-1-22	3	Исраилова Н. А.	6.541667	\N	Подтвержден	\N
45	22\\48420	Кыпчаков Рысбек Мурадилович	\N	ИВТ(б)-2-22	3	Момуналиева Н. Т.	9.481481	\N	Без заявки	\N
46	23-138436	Атаканов Адил Нуржанович	\N	ИВТ(б)-2-22	3	Момуналиева Н. Т.	4.074074	\N	Без заявки	\N
47	21\\46652	Султанов Динислам Султанович	\N	ИВТ(б)-2-22	3	Момуналиева Н. Т.	0.000000	\N	Без заявки	\N
48	22\\48228	Мирлан уулу Нурсултан 	\N	ИВТ(б)-2-22	3	Момуналиева Н. Т.	24.703704	\N	Без заявки	\N
49	22\\49326	Абдыжалиев Улукбек Бактыгулович	\N	ИВТ(б)-2-22	3	Момуналиева Н. Т.	5.407407	\N	Без заявки	\N
50	22\\49464	Полотов Айбек Авазбекович	\N	ИВТ(б)-2-22	3	Момуналиева Н. Т.	5.259259	\N	Без заявки	\N
51	21\\46410	Казбеков Актенир Бакытович	\N	ИВТ(б)-2-22	3	Момуналиева Н. Т.	10.370370	\N	Без заявки	\N
52	21\\47414	Сабирова Бактыгул Дыйканбаевна	\N	ИВТ(б)-2-22	3	Момуналиева Н. Т.	10.629630	\N	Без заявки	\N
53	21\\46033	Жусупова Асел Талантбековна	\N	ИВТ(б)-2-22	3	Момуналиева Н. Т.	13.703704	\N	Без заявки	\N
54	22\\49069	Мамыралиев Азамат Марсбекович	\N	ИВТ(б)-2-22	3	Момуналиева Н. Т.	6.185185	\N	Без заявки	\N
55	22\\49837	Таирбеков Нурислам Нурдинович	\N	ИВТ(б)-2-22	3	Момуналиева Н. Т.	4.592593	\N	Без заявки	\N
1	22-79615	Рыскадырова Сезим Кумаровна	Айыл банк	ИВТ(б)-1-22	3	Исраилова Н. А.	17.000000	\N	Подтвержден	\N
28	21\\46521	Абдылдаев Атагельди Маратович	Свое место практики	ИВТ(б)-1-22	3	Исраилова Н. А.	6.166667	879f5aa34fe3c172.jpg	Ожидает подтверждения	Мест не осталось. Выберите другое предприятие...
21	22\\48039	Ечин Илья Васильевич	Свое место практики	ИВТ(б)-1-22	3	Исраилова Н. А.	27.125000		Без заявки	\N
\.


--
-- Data for Name: place; Type: TABLE DATA; Schema: public; Owner: zebra
--

COPY public.place (id, title, occupation, places, max_places, requirements, outlook, contacts) FROM stdin;
5	Национальная Академия наук КР, Институт сейсмологии		3	3			
8	Оптима Банк	Веб-разработка, Мобильная разработка	0	0			Тихонов Федор Геннадьевич: 0551 987456\r\n
9	Мегалайн 	Специалист по обслуживанию компьютеров и сетей	0	0			Репецкая Евгения: 0500 924293\r\n
10	РКФР	Информационная безопасность	0	0			Куручбеков Бакыт Замирбекович: 0559 559 548\r\n
2	JUMP	Специалист по обслуживанию компьютеров и сетей	1	1			
7	Айыл банк	Веб-разработка, Мобильная разработка	4	5			Шабданбекова Асель: 0555 421203
1	“Партнер софт” ЖЧК	Специалист по обслуживанию компьютеров и сетей	2	3			Коваль Егор Николаевич: 0772 000 537\r\nКраснянский Денис Сергеевич: 0552 994991\r\n
4	Intermedia		0	2			
6	“Като Экономикс” ЖЧК	1C-программирование	1	2			Пак Александр Глебович: 0555 922 185\r\n
3	“NT computers” ЖЧК	Специалист по обслуживанию компьютеров и сетей	1	2			Лилия Александровна: 0553 906 736
\.


--
-- Data for Name: post; Type: TABLE DATA; Schema: public; Owner: zebra
--

COPY public.post (id, subject, teacher, student, date) FROM stdin;
\.


--
-- Data for Name: review; Type: TABLE DATA; Schema: public; Owner: zebra
--

COPY public.review (id, rating, text, date, id_place) FROM stdin;
2	3	зашибись	2025-05-26 00:00:00	4
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: zebra
--

COPY public."user" (id, name, login, password, practice_deadline, vkr_deadline) FROM stdin;
1	Исраилова Н. А.	nella11	$2b$12$dTe45PQ2xHfWraiWj3DefOb4E8n8TQOLSHHD8KsWpyfaH7VqHi0IC	2025-05-31 00:00:00	\N
\.


--
-- Name: intern_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zebra
--

SELECT pg_catalog.setval('public.intern_id_seq', 55, true);


--
-- Name: place_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zebra
--

SELECT pg_catalog.setval('public.place_id_seq', 10, true);


--
-- Name: post_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zebra
--

SELECT pg_catalog.setval('public.post_id_seq', 1, false);


--
-- Name: review_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zebra
--

SELECT pg_catalog.setval('public.review_id_seq', 2, true);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zebra
--

SELECT pg_catalog.setval('public.user_id_seq', 1, true);


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
-- Name: post post_pkey; Type: CONSTRAINT; Schema: public; Owner: zebra
--

ALTER TABLE ONLY public.post
    ADD CONSTRAINT post_pkey PRIMARY KEY (id);


--
-- Name: review review_pkey; Type: CONSTRAINT; Schema: public; Owner: zebra
--

ALTER TABLE ONLY public.review
    ADD CONSTRAINT review_pkey PRIMARY KEY (id);


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

