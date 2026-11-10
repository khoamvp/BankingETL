--Cau 1
select c.customer_code, c.full_name, c.city, c.customer_segment from public.customers c 
where c.city ='Ha Noi'
order by c.created_at desc 


--Cau 2 
select t.status, count(status) as soluong from public.transactions t 
group by t.status 
order by soluong desc



--Cau 3 
select t.transaction_id , t.amount, b.branch_name  from public.transactions t 
left join branches b on t.branch_id = b.branch_id 
order by t.amount desc
limit 20

--Cau 4
select c.customer_code,
       c.full_name,
       sum(t.amount) as tong_amount
from public.transactions t
join public.accounts a on t.source_account_id = a.account_id
join public.customers c on a.customer_id = c.customer_id
where t.status = 'SUCCESS'
group by c.customer_id, c.customer_code, c.full_name
order by tong_amount desc
limit 10;


-- Cau 5
with nhieu_lan as (
    select transaction_id
    from public.transaction_status_history
    group by transaction_id
    having count(*) > 2
)
select tsh.transaction_id, tsh.old_status, tsh.new_status, tsh.event_time
from public.transaction_status_history tsh
join nhieu_lan n on tsh.transaction_id = n.transaction_id
order by tsh.transaction_id, tsh.event_time;

--Cau 6
select c.customer_segment , count(c.customer_id ) as soluong from public.customers c 
group by c.customer_segment 
order by soluong desc

--Cau 7
select b.branch_name,b.city, count(a.account_id) as so_tai_khoan
from public.branches b
join public.accounts a on b.branch_id = a.branch_id
where a.account_status = 'ACTIVE'
group by b.branch_id, b.branch_name, b.city
order by so_tai_khoan desc, b.branch_name
limit 10;


--Cau 8
select c.channel_id,
       c.channel_name,
       count(*) as tong_gd,
       count(*) filter (where t.status = 'FAILED') as so_that_bai,
       round(count(*) filter (where t.status = 'FAILED') * 100.0 / count(*), 2) as ty_le_that_bai
from public.transactions t
join public.channels c on c.channel_id = t.channel_id
group by c.channel_id, c.channel_name
order by ty_le_that_bai desc;


--Cau 9
select (t.transaction_time at time zone 'Asia/Ho_Chi_Minh')::date as ngay,
       count(*)      as so_giao_dich,
       sum(t.amount) as tong_gia_tri
from public.transactions t
where t.transaction_time >= (select max(transaction_time) from public.transactions) - interval '30 days'
group by ngay
order by ngay desc

--Cau 10
select m.merchant_category, sum(t.amount) as tong_gia_tri
from public.transactions t
join public.merchants m on m.merchant_id = t.merchant_id
where t.status = 'SUCCESS'
group by m.merchant_category
order by tong_gia_tri desc
limit 5;