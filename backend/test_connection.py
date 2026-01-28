from sqlmodel import create_engine, text

DATABASE_URL = "postgresql://postgres:postgres123@localhost:5432/kairoflow"

try:
    engine = create_engine(DATABASE_URL, echo=True)
    
    with engine.connect() as conn:
        print(" Tentando conectar ao banco...")
        
        result = conn.execute(text("SELECT version()"))
        version = result.scalar()
        print(f" PostgreSQL version: {version}")
        
        result = conn.execute(text("SELECT current_database()"))
        db_name = result.scalar()
        print(f" Banco atual: {db_name}")
        
        result = conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """))
        tables = result.fetchall()
        print(f" Tabelas encontradas: {len(tables)}")
        for table in tables:
            print(f"   - {table[0]}")
            
except Exception as e:
    print(f" Erro: {e}")