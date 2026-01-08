import os
import sys
import bcrypt
from sqlalchemy.orm import Session

# Add current directory to path
sys.path.insert(0, os.getcwd())

from app.config.database import SessionLocal
from app.models.user import User
from app.models.tenant import Tenant

import json

def seed():
    db = SessionLocal()
    try:
        print("Seeding database...")

        seeds_path = os.path.join(os.getcwd(), "seeds.json")
        if not os.path.exists(seeds_path):
             print(f"Seeds file not found at {seeds_path}. Skipping seeding.")
             return

        with open(seeds_path, "r") as f:
            seeds_data = json.load(f)

        # 1. Seed Tenants
        for tenant_data in seeds_data.get("tenants", []):
            tenant = db.query(Tenant).filter(Tenant.subdomain == tenant_data["subdomain"]).first()
            if not tenant:
                print(f"Creating tenant: {tenant_data['name']}")
                tenant = Tenant(**tenant_data)
                db.add(tenant)
                db.commit()
                db.refresh(tenant)
            else:
                 # existing tenant logic
                 pass

        # 2. Seed Users
        for user_data in seeds_data.get("users", []):
            tenant_name = user_data.pop("tenant", None)
            if not tenant_name:
                print(f"Skipping user {user_data.get('username')} - No tenant specified.")
                continue

            # Find tenant
            tenant = db.query(Tenant).filter(Tenant.name == tenant_name).first()
            if not tenant:
                print(f"Tenant '{tenant_name}' not found for user {user_data.get('username')}.")
                continue

            user = db.query(User).filter(User.username == user_data["username"], User.tenant_id == tenant.id).first()
            if not user:
                print(f"Creating user: {user_data['username']}")
                
                password = user_data.pop("password")
                # Hash password using bcrypt
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                
                user = User(
                    tenant_id=tenant.id,
                    hashed_password=hashed_password,
                    **user_data
                )
                db.add(user)
                db.commit()
                print(f"User {user_data['username']} created successfully!")
            else:
                print(f"User {user_data['username']} already exists.")
            
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
