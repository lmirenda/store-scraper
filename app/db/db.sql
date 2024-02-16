create extension pgcrypto;

create schema "orders" authorization postgres;

CREATE TABLE "orders"."order_logs" (
	log_id uuid NOT NULL,
	user_id uuid NOT NULL,
	"order" json not null,
	"order_date" timestamp DEFAULT CURRENT_TIMESTAMP NOT null,
    CONSTRAINT log_pk PRIMARY KEY (log_id),
	CONSTRAINT user_fk FOREIGN KEY (user_id) REFERENCES "user"."user"(user_id)
);

CREATE SCHEMA "user" AUTHORIZATION postgres;

CREATE TABLE "user"."user" (
	user_id uuid NOT NULL,
	username varchar NOT NULL,
	password varchar not NULL,
	email varchar not null,
	"creation_date" timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
	CONSTRAINT user_pk PRIMARY KEY (user_id),
	CONSTRAINT user_unique UNIQUE (username),
	CONSTRAINT email_unique UNIQUE (email)
);

CREATE SCHEMA scraping AUTHORIZATION postgres;

CREATE TABLE scraping.product (
	product_id uuid NOT NULL,
	category_id uuid NOT NULL,
	provider_id uuid NOT NULL,
	price float4 NOT NULL,
	price_date timestamp NOT NULL,
	description varchar NOT NULL,
	CONSTRAINT product_pk PRIMARY KEY (product_id),
	CONSTRAINT product_product_category_fk FOREIGN KEY (category_id) REFERENCES scraping.product_category(category_id),
	CONSTRAINT product_provider_fk FOREIGN KEY (provider_id) REFERENCES scraping.provider(provider_id)
);

CREATE TABLE scraping.product_category (
	category_id uuid NOT NULL,
	description varchar NOT NULL,
	"creation_date" timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
	CONSTRAINT product_category_pk PRIMARY KEY (category_id)
);

CREATE TABLE scraping.provider (
	provider_id uuid NOT NULL,
	"name" varchar NOT NULL,
	url varchar NOT NULL,
	"creation_date" timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
	CONSTRAINT provider_pk PRIMARY KEY (provider_id)
);