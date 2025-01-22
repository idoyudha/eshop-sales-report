CREATE TABLE sales (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL,
  order_id UUID NOT NULL,
  product_id UUID NOT NULL,
  product_quantity INTEGER NOT NULL,
  margin_per_product DOUBLE PRECISION NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX sales_user_id_idx ON sales(user_id);
CREATE INDEX sales_order_id_idx ON sales(order_id);
CREATE INDEX sales_product_id_idx ON sales(product_id);