BEGIN;
--
-- Create model SyncAttempt
--
DROP TABLE IF EXISTS scraper_syncattempt CASCADE;
DROP TABLE IF EXISTS scraper_vehiclelisting CASCADE;
CREATE TABLE "scraper_syncattempt" ("id" bigserial NOT NULL PRIMARY KEY, "start_time" timestamp with time zone NOT NULL, "end_time" timestamp with time zone NULL, "status" varchar(20) NOT NULL, "listings_added" integer NOT NULL, "listings_updated" integer NOT NULL, "error_message" text NULL, "task_id" varchar(255) NULL, "user_id" integer NOT NULL);
--
-- Create model VehicleListing
--
CREATE TABLE "scraper_vehiclelisting" ("id" serial NOT NULL PRIMARY KEY, "dealership" varchar(100) NOT NULL, "title" varchar(500) NOT NULL, "price" numeric(10, 2) NULL, "msrp" numeric(10, 2) NULL, "year" integer NOT NULL, "make" text NOT NULL, "model" text NOT NULL, "image_url" varchar(500) NOT NULL, "created_at" timestamp with time zone NOT NULL, "updated_at" timestamp with time zone NOT NULL, "views" integer NOT NULL, "needs_update" boolean NOT NULL, "dealer_specific_id" varchar(20) NOT NULL UNIQUE, "vin" varchar(17) NULL, "color" varchar(50) NULL, "user_id" integer NOT NULL);
ALTER TABLE "scraper_syncattempt" ADD CONSTRAINT "scraper_syncattempt_user_id_4882dcf6_fk_auth_user_id" FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "scraper_syncattempt_user_id_4882dcf6" ON "scraper_syncattempt" ("user_id");
ALTER TABLE "scraper_vehiclelisting" ADD CONSTRAINT "scraper_vehiclelisting_year_make_model_dealer_s_74651093_uniq" UNIQUE ("year", "make", "model", "dealer_specific_id");
ALTER TABLE "scraper_vehiclelisting" ADD CONSTRAINT "scraper_vehiclelisting_user_id_1b7d55d8_fk_auth_user_id" FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "scraper_vehiclelisting_dealer_specific_id_4f4886ec_like" ON "scraper_vehiclelisting" ("dealer_specific_id" varchar_pattern_ops);
CREATE INDEX "scraper_vehiclelisting_user_id_1b7d55d8" ON "scraper_vehiclelisting" ("user_id");
COMMIT;
