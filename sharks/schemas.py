from __future__ import annotations

from dataclasses import dataclass

from pydantic import BaseModel, Field


@dataclass
class StudentProfile:
    whatsapp_id: str
    name: str | None = None
    email: str | None = None
    marks: float | None = None
    budget: float | None = None
    target_country: str | None = None
    target_course: str | None = None
    work_experience: float | None = None
    family_income: float | None = None


class ProfileIn(BaseModel):
    whatsapp_id: str = Field(..., min_length=5)
    name: str | None = None
    email: str | None = None
    marks: float | None = Field(default=None, ge=0, le=100)
    budget: float | None = Field(default=None, ge=0)
    target_country: str | None = None
    target_course: str | None = None
    work_experience: float | None = Field(default=None, ge=0)
    family_income: float | None = Field(default=None, ge=0)


class MentorIn(BaseModel):
    whatsapp_id: str
    message: str


class ScoringIn(BaseModel):
    marks: float = Field(..., ge=0, le=100)
    budget: float = Field(..., ge=0)
    target_country: str | None = None
    target_course: str | None = None
    work_experience: float = Field(default=0, ge=0)


class RoiIn(BaseModel):
    course: str
    country: str
    tuition_cost: float = Field(..., ge=0)
    living_cost_per_year: float = Field(..., ge=0)
    duration_years: float = Field(..., ge=0.25)


class LoanIn(BaseModel):
    whatsapp_id: str
    marks: float = Field(..., ge=0, le=100)
    family_income: float = Field(..., ge=0)
    budget: float = Field(..., ge=0)
    target_country: str | None = None
    target_course: str | None = None


class DocumentIn(BaseModel):
    whatsapp_id: str
    document_type: str = Field(..., min_length=2)
    raw_text: str | None = None


class WhatsAppMessageIn(BaseModel):
    to: str
    text: str
