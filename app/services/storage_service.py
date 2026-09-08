import uuid
from datetime import datetime
from fastapi import UploadFile
from supabase import create_client, Client
from app.config import settings

def get_supabase_client() -> Client:
    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        raise ValueError("Supabase URL and Key must be set.")
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

async def upload_document_service(file: UploadFile) -> dict:
    supabase = get_supabase_client()
    file_id = str(uuid.uuid4())
    file_bytes = await file.read()
    storage_path = f"raw/{file_id}_{file.filename}"

    supabase.storage.from_(settings.SUPABASE_BUCKET).upload(
        path=storage_path,
        file=file_bytes,
        file_options={"content-type": file.content_type or "application/octet-stream"}
    )

    doc_record = {
        "id": file_id,
        "filename": file.filename,
        "content_type": file.content_type,
        "size_bytes": len(file_bytes),
        "storage_path": storage_path,
        "status": "pending",  
        "created_at": datetime.utcnow().isoformat()
    }

    res = supabase.table("documents").insert(doc_record).execute()
    return res.data[0] if res.data else doc_record

def list_documents_service() -> list[dict]:
    supabase = get_supabase_client()
    res = supabase.table("documents").select("*").order("created_at", desc=True).execute()
    return res.data or []

def get_document_status_service(document_id: str) -> dict:
    supabase = get_supabase_client()
    res = supabase.table("documents").select("id", "filename", "status", "created_at").eq("id", document_id).execute()
    if not res.data:
        raise ValueError("Document not found")
    return res.data[0]