with customers as (
    select * from {{ ref('stg_customers') }}
),

orders as (
    select * from {{ ref('stg_orders') }}
),

order_items as (
    select * from {{ ref('stg_order_items') }}
),

order_details as (
    select
        o.order_id,
        o.customer_id,
        o.order_date,
        o.total_amount,
        o.order_status,
        count(oi.order_item_id) as item_count,
        sum(oi.line_total) as calculated_total
    from orders o
    left join order_items oi on o.order_id = oi.order_id
    group by 1, 2, 3, 4, 5
),

customer_orders as (
    select
        c.customer_id,
        c.customer_name,
        c.customer_email,
        count(od.order_id) as order_count,
        sum(od.total_amount) as total_spent,
        min(od.order_date) as first_order_date,
        max(od.order_date) as most_recent_order_date
    from customers c
    left join order_details od on c.customer_id = od.customer_id
    group by 1, 2, 3
)

select * from customer_orders