with customers as (
    select * from {{ ref('stg_customers') }}
),

orders as (
    select * from {{ ref('stg_orders') }}
),

order_items as (
    select * from {{ ref('stg_order_items') }}
),

order_with_items as (
    select
        o.order_id,
        o.customer_id,
        c.customer_name,
        c.customer_email,
        o.order_date,
        o.order_status,
        oi.order_item_id,
        oi.product_name,
        oi.quantity,
        oi.price,
        oi.line_total
    from orders o
    join customers c on o.customer_id = c.customer_id
    join order_items oi on o.order_id = oi.order_id
)

select * from order_with_items