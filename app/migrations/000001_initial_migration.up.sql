CREATE TABLE IF NOT EXISTS "sales" (
  "id" uuid PRIMARY KEY,
  "user_id" uuid NOT NULL,
  "order_id" uuid NOT NULL,
  "product_id" uuid NOT NULL,
  "product_quantity" integer NOT NULL,
  "margin_per_product" float NOT NULL,
  "created_at" timestamp NOT NULL,
);

CREATE INDEX idx_user_id ON "sales" ("user_id");
CREATE INDEX idx_order_id ON "sales" ("order_id");
CREATE INDEX idx_product_id ON "sales" ("product_id");
