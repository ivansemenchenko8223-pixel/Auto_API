from sqlalchemy import create_engine, text


engine = create_engine('sqlite:///detal.db')

with engine.connect() as conn:
    conn.execute(text("ALTER TABLE users ADD COLUMN is_admin BOOLEAN DEFAULT 0"))
    conn.commit()