with source as (
    select * from raw.orders
),

renamed as (
    select
        id as order_id,
        customer_id,
        order_date,
        total_amount,
        status as order_status
    from source
)

select * from renamed
