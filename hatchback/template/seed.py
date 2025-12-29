import os
import sys
import bcrypt
from sqlalchemy.orm import Session

# Add current directory to path
sys.path.insert(0, os.getcwd())

from app.config.database import SessionLocal
from app.models.user import User
from app.models.tenant import Tenant

def seed():
    db = SessionLocal()
    try:
        print("Seeding database...")
        
        # 1. Create Default Tenant
        default_tenant_name = "Default Tenant"
        default_subdomain = "default"
        
        tenant = db.query(Tenant).filter(Tenant.subdomain == default_subdomain).first()
        if not tenant:
            print(f"Creating default tenant: {default_tenant_name}")
            tenant = Tenant(
                name=default_tenant_name,
                subdomain=default_subdomain,
                domain="localhost",
                is_active=True
            )
            db.add(tenant)
            db.commit()
            db.refresh(tenant)
        else:
            print(f"Tenant {default_tenant_name} already exists.")

        # 2. Create Admin User
        admin_username = "admin"
        admin_email = "admin@example.com"
        
        admin = db.query(User).filter(User.username == admin_username, User.tenant_id == tenant.id).first()
        if not admin:
            print(f"Creating admin user: {admin_username}")
            
            password = os.environ.get("ADMIN_PASSWORD", "admin")
            # Hash password using bcrypt
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            admin = User(
                tenant_id=tenant.id,
                username=admin_username,
                email=admin_email,
                hashed_password=hashed_password,
                role="admin",
                status="active",
                name="Admin",
                surname="User"
            )
            db.add(admin)
            db.commit()
            print(f"Admin user created successfully! Username: {admin_username}, Password: {password}")
        else:
            print(f"User {admin_username} already exists.")
            
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
