from sqlalchemy.orm import Session
from core.database import SessionLocal

# ✅ IMPORT ALL MODELS (CRITICAL)
from models.departments import DepartmentMaster
from models.role import RoleMaster
from models.user import UserMaster
from models.module import Module
from models.actions import Action
from models.role_permissions import RolePermission

from core.security import hash_password
from utils.logger import logger

# Default configuration
DEFAULT_ROLES = ["ADMIN", "STAFF"]
DEFAULT_DEPARTMENTS = ["ADMIN"]

DEFAULT_ADMIN = {
    "username": "aslam",
    "password": "aslam"
}


def seed_roles(db: Session):
    """
    Create default roles (ADMIN, STAFF) if they do not exist.
    Uses role_name (as per your model).
    """
    try:
        for role_name in DEFAULT_ROLES:
            exists = db.query(RoleMaster).filter(
                RoleMaster.role_name == role_name
            ).first()

            if not exists:
                db.add(RoleMaster(role_name=role_name))
                logger.info(f"Created role: {role_name}")

        # Flush instead of commit (keeps transaction open)
        db.flush()

    except Exception as e:
        logger.error(f"Error in seed_roles: {str(e)}")
        raise

def seed_departments(db: Session):
    """
    Create default departments (ADMIN) if they do not exist.
    Uses department_name (as per your model).
    """
    try:
        for department_name in DEFAULT_DEPARTMENTS:
            exists = db.query(DepartmentMaster).filter(
                DepartmentMaster.department_name == department_name
            ).first()

            if not exists:
                db.add(DepartmentMaster(department_name=department_name))
                logger.info(f"Created department: {department_name}")

        # Flush instead of commit (keeps transaction open)
        db.flush()

    except Exception as e:
        logger.error(f"Error in seed_departments: {str(e)}")
        raise


def seed_admin_user(db: Session):
    try:
        existing_user = db.query(UserMaster).filter(
            UserMaster.username == DEFAULT_ADMIN["username"]
        ).first()

        if existing_user:
            logger.info("Admin user already exists. Skipping.")
            return

        admin_role = db.query(RoleMaster).filter(
            RoleMaster.role_name == "ADMIN"
        ).first()

        if not admin_role:
            raise Exception("ADMIN role not found.")
        
        admin_department = db.query(DepartmentMaster).filter(
            DepartmentMaster.department_name == "ADMIN"
        ).first()

        if not admin_department:
            raise Exception("ADMIN department not found.")

        new_admin = UserMaster(
            username=DEFAULT_ADMIN["username"],
            email="admin@example.com",  # ⚠️ REQUIRED (nullable=False)
            password=hash_password(DEFAULT_ADMIN["password"]),
            roleid=admin_role.id,   # ✅ FIXED HERE
            department_id=admin_department.id,  # ✅ FIXED HERE
            status=True
        )

        db.add(new_admin)
        db.flush()

        logger.info("Default admin user created.")

    except Exception as e:
        logger.error(f"Error in seed_admin_user: {str(e)}")
        raise


def run_seed():
    """
    Main bootstrap runner (like Spring Boot CommandLineRunner).
    Ensures:
    - roles exist
    - admin user exists
    """
    db: Session = SessionLocal()

    try:
        logger.info("Starting DB seed...")

        # Run in single transaction
        seed_roles(db)
        seed_departments(db)
        seed_admin_user(db)
        
        db.commit()

        logger.info("DB seed completed successfully.")

    except Exception as e:
        db.rollback()
        logger.error(f"Seeding failed: {str(e)}")

    finally:
        db.close()