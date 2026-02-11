"""
Database module for Supabase integration
"""
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase client
supabase: Client = None

def get_supabase_client() -> Client:
    """
    Get or create Supabase client instance
    
    Returns:
        Client: Supabase client instance
    """
    global supabase
    
    if supabase is None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise ValueError(
                "SUPABASE_URL and SUPABASE_KEY must be set in environment variables"
            )
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    return supabase


def query_table(table_name: str, filters: dict = None):
    """
    Query a table with optional filters
    
    Args:
        table_name: Name of the table to query
        filters: Dictionary of column:value pairs to filter by (optional)
        
    Returns:
        Query result data
    """
    client = get_supabase_client()
    query = client.table(table_name).select("*")
    
    if filters:
        for column, value in filters.items():
            query = query.eq(column, value)
    
    response = query.execute()
    return response.data


def insert_record(table_name: str, data: dict):
    """
    Insert a new record into a table
    
    Args:
        table_name: Name of the table
        data: Dictionary of data to insert
        
    Returns:
        Inserted record data
    """
    client = get_supabase_client()
    try:
        response = client.table(table_name).insert(data).execute()
        return response.data
    except Exception as e:
        import traceback
        import sys
        error_msg = f"Error inserting into {table_name}: {str(e)}"
        print(f"[DATABASE ERROR] {error_msg}", file=sys.stderr)
        print(f"[DATABASE ERROR] Data: {data}", file=sys.stderr)
        print(f"[DATABASE ERROR] Traceback:\n{traceback.format_exc()}", file=sys.stderr)
        sys.stderr.flush()
        raise Exception(error_msg)


def update_record(table_name: str, record_id, data: dict):
    """
    Update a record in a table
    
    Args:
        table_name: Name of the table
        record_id: ID of the record to update (int or str for UUID)
        data: Dictionary of data to update
        
    Returns:
        Updated record data
    """
    client = get_supabase_client()
    response = client.table(table_name).update(data).eq("id", record_id).execute()
    return response.data


def delete_record(table_name: str, record_id):
    """
    Delete a record from a table
    
    Args:
        table_name: Name of the table
        record_id: ID of the record to delete (int or str for UUID)
        
    Returns:
        Deleted record data
    """
    client = get_supabase_client()
    response = client.table(table_name).delete().eq("id", record_id).execute()
    return response.data
