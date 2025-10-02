import os
import asyncio
import ssl
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models.user import User
from app.models.admin import Admin
import logging

logger = logging.getLogger(__name__)

# Global client instance
client = None
database = None


async def init_database():
    """Initialize database with basic Atlas configuration"""
    global client, database
    
    connection_string = os.getenv("MONGODB_URL")
    if not connection_string:
        logger.warning("⚠️ No MongoDB URL found - running without database")
        return
    
    # Clean the connection string
    connection_string = connection_string.strip()
    database_name = os.getenv("DATABASE_NAME", "fdm_diabetes_db")
    
    logger.info(f"🚀 Connecting to MongoDB Atlas...")
    logger.info(f"📋 Database: {database_name}")
    
    try:
        # Create client with minimal configuration
        client = AsyncIOMotorClient(connection_string)
        
        # Test connection with single attempt
        try:
            logger.info("📡 Testing MongoDB Atlas connection...")
            
            # Simple ping test with shorter timeout
            await asyncio.wait_for(
                client.admin.command('ping'), 
                timeout=5.0
            )
            
            logger.info("✅ MongoDB Atlas connection successful!")
            
        except Exception as e:
            logger.warning(f"⚠️ Connection test failed: {e}")
            logger.info("🔄 Continuing without database - prediction features will work")
            client = None
            return
        
        # Set database
        database = client[database_name]
        
        # Test database access
        logger.info("🔍 Testing database access...")
        try:
            collections = await database.list_collection_names()
            logger.info(f"📁 Found collections: {collections}")
        except Exception as e:
            logger.warning(f"⚠️ Could not list collections: {e}")
        
        # Initialize Beanie
        logger.info("🔧 Initializing Beanie ODM...")
        await init_beanie(database=database, document_models=[User, Admin])
        
        logger.info("✅ Database connected and initialized successfully!")
        
    except Exception as e:
        logger.warning(f"⚠️ Database setup failed: {e}")
        logger.info("🔄 Continuing without database - prediction features will work")
        client = None
        database = None


async def close_database():
    """Close database connection"""
    global client
    if client:
        try:
            client.close()
        except:
            pass


async def get_database():
    """Get database instance"""
    return database


async def health_check():
    """Check if database is available"""
    global client
    if not client:
        return False
    try:
        await client.admin.command('ping')
        return True
    except:
        return False