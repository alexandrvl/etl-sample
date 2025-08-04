with source as (
    select * from raw.customers
),

renamed as (
    select
        id as customer_id,
        name as customer_name,
        email as customer_email,
        created_at,
        updated_at
    from source
)

select * from renamed
