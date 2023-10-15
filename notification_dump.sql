CREATE SCHEMA notification;

ALTER SCHEMA notification OWNER TO app;


CREATE TABLE notification.mailing (
    id uuid NOT NULL,
    receiver_ids uuid[] NOT NULL,
    status character varying(50) NOT NULL,
    subject character varying(255) NOT NULL,
    template_params jsonb NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    template_id uuid NOT NULL
);


ALTER TABLE notification.mailing OWNER TO app;

--
-- Name: template; Type: TABLE; Schema: notification; Owner: app
--

CREATE TABLE notification.template (
    id uuid NOT NULL,
    name character varying(64) NOT NULL,
    html_template text NOT NULL,
    attributes jsonb NOT NULL
);


ALTER TABLE notification.template OWNER TO app;