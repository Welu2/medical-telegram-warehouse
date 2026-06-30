from sqlalchemy import text


def get_top_products(db, limit):

    sql = text("""
        SELECT
            product_name,
            mentions
        FROM analytics.fct_product_mentions
        ORDER BY mentions DESC
        LIMIT :limit
    """)
    
    return db.execute(sql, {"limit": limit}).fetchall()


def get_channel_activity(db, channel):

    sql = text("""
        SELECT
            c.channel_name,
            d.full_date,
            COUNT(*) AS posts

        FROM analytics.fct_messages f

        JOIN analytics.dim_channels c
            ON f.channel_key = c.channel_key

        JOIN analytics.dim_dates d
            ON f.date_key = d.date_key

        WHERE LOWER(c.channel_name)=LOWER(:channel)

        GROUP BY
            c.channel_name,
            d.full_date

        ORDER BY d.full_date
    """)

    return db.execute(sql, {"channel": channel}).fetchall()


def search_messages(db, keyword, limit):

    sql = text("""
        SELECT
            f.message_id,
            c.channel_name,
            f.message_text,
            d.full_date

        FROM analytics.fct_messages f

        JOIN analytics.dim_channels c
            ON f.channel_key=c.channel_key

        JOIN analytics.dim_dates d
            ON f.date_key=d.date_key

        WHERE LOWER(f.message_text)
        LIKE LOWER(:keyword)

        ORDER BY d.full_date DESC

        LIMIT :limit
    """)

    return db.execute(
        sql,
        {
            "keyword": f"%{keyword}%",
            "limit": limit
        }
    ).fetchall()


def visual_stats(db):

    sql = text("""
        SELECT
            c.channel_name,
            COUNT(*) AS total_images,
            AVG(confidence_score) AS avg_confidence

        FROM analytics.fct_image_detections f

        JOIN analytics.dim_channels c
            ON f.channel_key=c.channel_key

        GROUP BY c.channel_name

        ORDER BY total_images DESC
    """)

    return db.execute(sql).fetchall()