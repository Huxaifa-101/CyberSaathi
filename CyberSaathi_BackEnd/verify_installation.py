"""
Installation Verification Script
Checks if all dependencies and configuration are correct
"""
import sys
import os

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def check_python_version():
    """Check Python version"""
    print("\n🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} (requires 3.8+)")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    print("\n📦 Checking dependencies...")
    
    required_packages = [
        'langchain',
        'langchain_community',
        'langchain_google_genai',
        'langgraph',
        'langchain_huggingface',
        'pgvector',
        'psycopg2',
        'pypdf',
        'docx2txt',
        'fastapi',
        'uvicorn',
        'pydantic',
        'tavily',
        'dotenv',
        'sentence_transformers',
        'tabulate'
    ]
    
    missing = []
    for package in required_packages:
        try:
            if package == 'dotenv':
                __import__('dotenv')
            elif package == 'psycopg2':
                __import__('psycopg2')
            else:
                __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} (missing)")
            missing.append(package)
    
    return len(missing) == 0, missing

def check_env_file():
    """Check if .env file exists and has required variables"""
    print("\n⚙️  Checking configuration...")
    
    if not os.path.exists('.env'):
        print("   ❌ .env file not found")
        print("   💡 Copy .env.example to .env and fill in your API keys")
        return False
    
    print("   ✅ .env file exists")
    
    # Check for required variables
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = [
        'GOOGLE_API_KEY',
        'TAVILY_API_KEY',
        'POSTGRES_PASSWORD'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value or value.startswith('your_'):
            print(f"   ❌ {var} not set")
            missing_vars.append(var)
        else:
            print(f"   ✅ {var} configured")
    
    return len(missing_vars) == 0, missing_vars

def check_database_connection():
    """Check PostgreSQL connection"""
    print("\n🗄️  Checking database connection...")
    
    try:
        from config import Config
        import psycopg2
        
        conn = psycopg2.connect(
            host=Config.POSTGRES_HOST,
            port=Config.POSTGRES_PORT,
            database=Config.POSTGRES_DB,
            user=Config.POSTGRES_USER,
            password=Config.POSTGRES_PASSWORD
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"   ✅ Connected to PostgreSQL")
        print(f"   📊 {version[:50]}...")
        
        # Check for pgvector extension
        cursor.execute("SELECT * FROM pg_extension WHERE extname = 'vector';")
        if cursor.fetchone():
            print("   ✅ pgvector extension installed")
        else:
            print("   ❌ pgvector extension not found")
            print("   💡 Run: CREATE EXTENSION IF NOT EXISTS vector;")
            cursor.close()
            conn.close()
            return False
        
        # Check for tables
        cursor.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name IN ('law_documents', 'document_registry')
        """)
        tables = cursor.fetchall()
        
        if len(tables) == 2:
            print("   ✅ Database tables exist")
        else:
            print("   ❌ Database tables not found")
            print("   💡 Run: psql -U postgres -d pak_cyberlaw_db -f setup_postgres.sql")
            cursor.close()
            conn.close()
            return False
        
        cursor.close()
        conn.close()
        return True
    
    except Exception as e:
        print(f"   ❌ Database connection failed: {e}")
        print("   💡 Check your PostgreSQL credentials in .env")
        return False

def check_data_directory():
    """Check if data directories exist"""
    print("\n📁 Checking data directories...")
    
    from config import Config
    
    if os.path.exists(Config.RAW_DATA_DIR):
        print(f"   ✅ {Config.RAW_DATA_DIR} exists")
        
        # Count files
        files = list(os.listdir(Config.RAW_DATA_DIR))
        doc_files = [f for f in files if f.endswith(('.pdf', '.docx', '.doc', '.txt'))]
        
        if doc_files:
            print(f"   📄 Found {len(doc_files)} documents")
        else:
            print("   ⚠️  No documents found in data/raw/")
            print("   💡 Add PDF/DOCX files to data/raw/ and run: python index_documents.py")
    else:
        print(f"   ❌ {Config.RAW_DATA_DIR} not found")
        return False
    
    if os.path.exists(Config.PROCESSED_DATA_DIR):
        print(f"   ✅ {Config.PROCESSED_DATA_DIR} exists")
    else:
        print(f"   ❌ {Config.PROCESSED_DATA_DIR} not found")
        return False
    
    return True

def main():
    """Main verification function"""
    print_header("🇵🇰 CyberSaathi Installation Verification")
    
    all_checks = []
    
    # Run all checks
    all_checks.append(("Python Version", check_python_version()))
    
    deps_ok, missing = check_dependencies()
    all_checks.append(("Dependencies", deps_ok))
    
    env_ok, missing_vars = check_env_file()
    all_checks.append(("Configuration", env_ok))
    
    all_checks.append(("Database", check_database_connection()))
    all_checks.append(("Data Directories", check_data_directory()))
    
    # Summary
    print_header("📊 Verification Summary")
    
    for check_name, result in all_checks:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {check_name}: {status}")
    
    all_passed = all(result for _, result in all_checks)
    
    if all_passed:
        print("\n" + "="*60)
        print("  🎉 All checks passed! You're ready to go!")
        print("="*60)
        print("\n📝 Next steps:")
        print("   1. Add documents to data/raw/")
        print("   2. Run: python index_documents.py")
        print("   3. Run: uvicorn api:api --reload")
        print("   4. Visit: http://localhost:8000/docs")
    else:
        print("\n" + "="*60)
        print("  ⚠️  Some checks failed. Please fix the issues above.")
        print("="*60)
        print("\n💡 See QUICKSTART.md for detailed setup instructions")
    
    print()

if __name__ == "__main__":
    main()
