<<<<<<< HEAD
create database ecommerce;

use ecommerce;

#building out the tables
create table
    role (
        role_id int auto_increment primary key,
        role_name varchar(10) not null unique
    );

create table
    user (
        user_id int auto_increment primary key,
        role_id int not null,
        email varchar(100) not null unique,
        username varchar(50) not null unique,
        name varchar(80) not null,
        password varchar(60) not null
    );

create table
    vendor_product (
        vendor_item_id int auto_increment primary key,
        user_id int not null,
        product_id int not null
    );

create table
    product (
        product_id int auto_increment not null primary key,
        product_name varchar(255) not null,
        product_description text(10000),
        product_images text,
        in_stock boolean not null,
        stock_amount int default 1,
        warranty_period int,
        product_price dec(10, 2) not null,
        discount_percentage dec(2, 2),
        discount_start_date date,
        discount_end_date date
    );

create table
    cart (
        cart_id int auto_increment primary key,
        user_id int not null,
        total_price dec(10, 2) not null default 0.00
    );

create table
    cart_item (
        cart_item_id int auto_increment primary key,
        cart_id int not null,
        product_variant_id int not null,
        quantity int not null default 1,
        price dec(10, 2) not null
    );

create table
    product_variant (
        product_variant_id int auto_increment primary key,
        product_id int not null,
        color_id int not null,
        size_id int not null
    );

create table
    color (
        color_id int auto_increment primary key,
        color_name varchar(30) not null unique
    );

create table
    size (
        size_id int auto_increment primary key,
        size_name varchar(30) not null unique
    );

create table
    orders (
        order_id int auto_increment primary key,
        user_id int not null,
        order_date date not null default (current_date()),
        total_price dec(10, 2) not null default 0.00,
        order_status varchar(30) not null
    );

create table
    purchased_item (
        purchased_item_id int auto_increment primary key,
        order_id int not null,
        product_variant_id int not null,
        quantity int not null,
        price dec(10, 2) not null,
        warranty_period int
    );

create table
    review (
        review_id int auto_increment primary key,
        user_id int not null,
        product_id int not null,
        review_date date not null default (current_date()),
        customer_review text(3000) not null,
        images text,
        rating int not null
    );

create table
    chat (
        chat_id int auto_increment primary key,
        customer_id int not null,
        representative_id int not null
    );

create table
    message (
        message_id int auto_increment primary key,
        chat_id int not null,
        sender_id int not null,
        message_text text(3000) not null,
        image text,
        timestamp timestamp not null default current_timestamp
    );

create table
    dispute (
        dispute_id int auto_increment primary key,
        dispute_customer int not null,
        dispute_admin int not null,
        order_id int not null,
        purchased_item_id int not null,
        dispute_type varchar(12) not null,
        subject varchar(100) not null,
        description varchar(3000) not null,
        images text,
        dispute_date date not null,
        dispute_status varchar(30) not null
    );

# adding extra constraints
alter table user
add
    constraint user_role_fk foreign key (role_id) references role(role_id);

alter table vendor_product
add
    constraint vend_prod_user_fk foreign key (user_id) references user(user_id),
add
    constraint vend_prod_prod_fk foreign key (product_id) references product(product_id);

alter table cart
add
    constraint cart_user_fk foreign key (user_id) references user(user_id);

alter table cart_item
add
    constraint cart_item_cart_fk foreign key (cart_id) references cart(cart_id),
add
    constraint cart_item_prod_var_fk foreign key (product_variant_id) references product_variant(product_variant_id);

alter table product_variant
add
    constraint prod_var_prod_fk foreign key (product_id) references product(product_id),
add
    constraint prod_var_color_fk foreign key (color_id) references color(color_id),
add
    constraint prod_var_size_fk foreign key (size_id) references size(size_id);

alter table orders
add
    constraint orders_user_fk foreign key (user_id) references user(user_id);

alter table purchased_item
add
    constraint purch_item_order_fk foreign key (order_id) references orders(order_id),
add
    constraint purch_item_prod_var_fk foreign key (product_variant_id) references product_variant(product_variant_id);

alter table review
add
    constraint review_user_fk foreign key (user_id) references user(user_id),
add
    constraint review_prod_fk foreign key (product_id) references product(product_id);

alter table chat
add
    constraint chat_cust_fk foreign key (customer_id) references user(user_id),
add
    constraint chat_rep_fk foreign key (representative_id) references user(user_id);

alter table message
add
    constraint message_chat_fk foreign key (chat_id) references chat(chat_id),
add
    constraint message_sender_fk foreign key (sender_id) references user(user_id);

alter table dispute
add
    constraint dispute_cust_fk foreign key (dispute_customer) references user(user_id),
add
    constraint dispute_admin_fk foreign key (dispute_admin) references user(user_id),
add
    constraint dispute_order_fk foreign key (order_id) references orders(order_id),
add
    constraint dispute_purch_item_fk foreign key (purchased_item_id) references purchased_item(purchased_item_id);

alter table orders
add
    constraint order_status_check check (
        order_status in (
            'pending',
            'confirmed',
            'handed to delivery partner',
            'shipped'
        )
    );

alter table review
add
    constraint check_rating check (
        rating between 1 and 5
    );

alter table dispute
add
    constraint dispute_type_check check (
        dispute_type in (
            'return',
            'refund',
            'exchange',
            'warranty'
        )
    );

alter table dispute
add
    constraint dispute_status_check check (
        dispute_status in (
            'pending',
            'rejected',
            'confirmed',
            'processing',
            'complete'
        )
    );

=======

create database ecommerce;
use ecommerce;
#building out the tables
create table role (
    role_id int auto_increment primary key,
    role_name varchar(10) not null unique
);
create table user (
	user_id int auto_increment primary key,
	role_id int not null,
	email varchar(100) not null unique,
	username varchar(50) not null unique,
	name varchar(80) not null,
	password varchar(60) not null
);
create table vendor_product (
    vendor_item_id int auto_increment primary key,
	user_id int not null,
	product_id int not null
);
create table product (
	product_id int auto_increment not null primary key,
	product_name varchar(255) not null,
	product_description text(10000),
	product_images text,
	in_stock boolean not null,
	stock_amount int default 1,
	warranty_period int,
	product_price dec(10, 2) not null,
	discount_percentage dec(2, 2),
	discount_start_date date,
	discount_end_date date
);
create table cart (
	cart_id int auto_increment primary key,
	user_id int not null,
	total_price dec(10, 2) not null default 0.00
);
create table cart_item (
	cart_item_id int auto_increment primary key,
	cart_id int not null,
	product_variant_id int not null,
	quantity int not null default 1,
	price dec(10, 2) not null
);
create table product_variant (
	product_variant_id int auto_increment primary key,
	product_id int not null,
	color_id int not null,
	size_id int not null
);
create table color (
    color_id int auto_increment primary key,
    color_name varchar(30) not null unique
);
create table size (
    size_id int auto_increment primary key,
    size_name varchar(30) not null unique
);
create table orders (
	order_id int auto_increment primary key,
	user_id int not null,
	order_date date not null default (current_date()),
	total_price dec(10, 2) not null default 0.00,
	order_status varchar(30) not null
);
create table purchased_item (
    purchased_item_id int auto_increment primary key,
    order_id int not null,
    product_variant_id int not null,
    quantity int not null,
    price dec(10, 2) not null,
    warranty_period int
);
create table review (
	review_id int auto_increment primary key,
	user_id int not null,
	product_id int not null,
	review_date date not null default (current_date()),
	customer_review text(3000) not null,
	images text,
	rating int not null
);
create table chat (
	chat_id int auto_increment primary key,
	customer_id int not null,
	representative_id int not null
);
create table message (
	message_id int auto_increment primary key,
	chat_id int not null,
	sender_id int not null,
	message_text text(3000) not null,
	image text,
	timestamp timestamp not null default current_timestamp
);
create table dispute (
	dispute_id int auto_increment primary key,
	dispute_customer int not null,
	dispute_admin int not null,
	order_id int not null,
	purchased_item_id int not null,
	dispute_type varchar(12) not null,
	subject varchar(100) not null,
	description varchar(3000) not null,
	images text,
	dispute_date date not null,
	dispute_status varchar(30) not null
);

# adding extra constraints
alter table user add constraint user_role_fk foreign key (role_id) references role(role_id);
alter table vendor_product add constraint vend_prod_user_fk foreign key (user_id) references user(user_id),
add constraint vend_prod_prod_fk foreign key (product_id) references product(product_id);
alter table cart add constraint cart_user_fk foreign key (user_id) references user(user_id);
alter table cart_item add constraint cart_item_cart_fk foreign key (cart_id) references cart(cart_id),
add constraint cart_item_prod_var_fk foreign key (product_variant_id) references product_variant(product_variant_id);
alter table product_variant add constraint prod_var_prod_fk foreign key (product_id) references product(product_id),
add constraint prod_var_color_fk foreign key (color_id) references color(color_id),
add constraint prod_var_size_fk foreign key (size_id) references size(size_id);
alter table orders add constraint orders_user_fk foreign key (user_id) references user(user_id);
alter table purchased_item add constraint purch_item_order_fk foreign key (order_id) references orders(order_id),
add constraint purch_item_prod_var_fk foreign key (product_variant_id) references product_variant(product_variant_id);
alter table review add constraint review_user_fk foreign key (user_id) references user(user_id),
add constraint review_prod_fk foreign key (product_id) references product(product_id);
alter table chat add constraint chat_cust_fk foreign key (customer_id) references user(user_id),
add constraint chat_rep_fk foreign key (representative_id) references user(user_id);
alter table message add constraint message_chat_fk foreign key (chat_id) references chat(chat_id),
add constraint message_sender_fk foreign key (sender_id) references user(user_id);
alter table dispute add constraint dispute_cust_fk foreign key (dispute_customer) references user(user_id),
add constraint dispute_admin_fk foreign key (dispute_admin) references user(user_id),
add constraint dispute_order_fk foreign key (order_id) references orders(order_id),
add constraint dispute_purch_item_fk foreign key (purchased_item_id) references purchased_item(purchased_item_id);
alter table orders add constraint order_status_check check (order_status in ('pending', 'confirmed', 'handed to delivery partner', 'shipped'));
alter table review add constraint check_rating check (rating between 1 and 5);
alter table dispute add constraint dispute_type_check check (dispute_type in ('return', 'refund', 'exchange', 'warranty'));
alter table dispute add constraint dispute_status_check check (dispute_status in ('pending', 'rejected', 'confirmed', 'processing', 'complete'));
>>>>>>> c51ff083378648056e3ff61b5b9e794ac01eea22
alter table product_variant modify size_id int null;