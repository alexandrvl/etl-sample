with source as (
    select * from raw.order_items
),

renamed as (
    select
        id as order_item_id,
        order_id,
        product_name,
        quantity,
        price,
        quantity * price as line_total
    from source
)

select * from renamed
