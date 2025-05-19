# ActiBot/app/schemas/project_schemas.py
from pydantic import BaseModel
from typing import Optional

class ProjectBase(BaseModel):
    numero_proyecto: str
    nombre_cliente: Optional[str] = None
    etapa_actual: str
    pdf_path: str

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    class Config:
        orm_mode = True # Para compatibilidad con ORMs si se usan después