"""
CRM Models for Malaysia Corridor Ops
=====================================
SQLite-based CRM with lead scoring, pipeline tracking, and conversion analytics.
"""

import sqlite3
import json
import uuid
from dataclasses import dataclass, asdict, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Optional, List, Dict, Any
from contextlib import contextmanager

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "crm.db"


# =============================================================================
# ENUMS
# =============================================================================

class LeadSource(str, Enum):
    WEBSITE = "website"
    LINKEDIN = "linkedin"
    REFERRAL = "referral"
    DIRECTORY = "directory"  # FMM, CIDB, MATRADE, MPOB
    COLD_OUTREACH = "cold_outreach"
    EVENT = "event"
    PARTNER = "partner"
    ORGANIC = "organic"


class LeadStatus(str, Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    WON = "won"
    LOST = "lost"
    NURTURING = "nurturing"


class ActivityType(str, Enum):
    EMAIL_SENT = "email_sent"
    EMAIL_OPENED = "email_opened"
    EMAIL_CLICKED = "email_clicked"
    EMAIL_REPLIED = "email_replied"
    CALL_MADE = "call_made"
    CALL_CONNECTED = "call_connected"
    MEETING_SCHEDULED = "meeting_scheduled"
    MEETING_HELD = "meeting_held"
    PROPOSAL_SENT = "proposal_sent"
    NOTE = "note"
    TASK = "task"


class CompanySize(str, Enum):
    STARTUP = "1-10"
    SMALL = "11-50"
    MEDIUM = "51-200"
    LARGE = "201-500"
    ENTERPRISE = "501-1000"
    CORPORATE = "1000+"


class Industry(str, Enum):
    MANUFACTURING = "manufacturing"
    ELECTRONICS = "electronics"
    CONSTRUCTION = "construction"
    PLANTATION = "plantation"
    HOSPITALITY = "hospitality"
    RETAIL = "retail"
    SERVICES = "services"
    LOGISTICS = "logistics"
    SECURITY = "security"
    CLEANING = "cleaning"
    OTHER = "other"


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class Company:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    website: str = ""
    phone: str = ""
    email: str = ""
    hr_email: str = ""
    linkedin: str = ""
    address: str = ""
    city: str = ""
    state: str = ""
    industry: Industry = Industry.OTHER
    sub_industry: str = ""
    size: CompanySize = CompanySize.MEDIUM
    employee_count: int = 0
    foreign_worker_count: int = 0
    levy_tier: str = "RM1850"  # RM1850 or RM640
    priority_score: float = 50.0
    source: LeadSource = LeadSource.DIRECTORY
    source_url: str = ""
    notes: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_contacted_at: Optional[str] = None
    last_activity_at: Optional[str] = None

    def to_dict(self) -> dict:
        d = asdict(self)
        d['industry'] = self.industry.value
        d['size'] = self.size.value
        d['source'] = self.source.value
        return d

    @classmethod
    def from_dict(cls, d: dict) -> 'Company':
        d = d.copy()
        d['industry'] = Industry(d.get('industry', 'other'))
        d['size'] = CompanySize(d.get('size', 'medium'))
        d['source'] = LeadSource(d.get('source', 'directory'))
        return cls(**d)


@dataclass
class Contact:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    company_id: str = ""
    name: str = ""
    title: str = ""
    email: str = ""
    phone: str = ""
    linkedin: str = ""
    is_decision_maker: bool = False
    is_hr: bool = False
    is_primary: bool = False
    notes: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Lead:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    company_id: str = ""
    contact_id: str = ""
    status: LeadStatus = LeadStatus.NEW
    source: LeadSource = LeadSource.DIRECTORY
    score: float = 0.0
    estimated_value: float = 0.0  # RM per year
    expected_workers: int = 0
    assigned_to: str = ""
    tags: List[str] = field(default_factory=list)
    notes: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    qualified_at: Optional[str] = None
    closed_at: Optional[str] = None
    lost_reason: str = ""

    def to_dict(self) -> dict:
        d = asdict(self)
        d['status'] = self.status.value
        d['source'] = self.source.value
        return d

    @classmethod
    def from_dict(cls, d: dict) -> 'Lead':
        d = d.copy()
        d['status'] = LeadStatus(d.get('status', 'new'))
        d['source'] = LeadSource(d.get('source', 'directory'))
        d['tags'] = d.get('tags', [])
        if isinstance(d['tags'], str):
            d['tags'] = json.loads(d['tags'])
        return cls(**d)


@dataclass
class Activity:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    lead_id: str = ""
    company_id: str = ""
    contact_id: str = ""
    type: ActivityType = ActivityType.NOTE
    subject: str = ""
    description: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_by: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        d = asdict(self)
        d['type'] = self.type.value
        d['metadata'] = json.dumps(self.metadata)
        return d

    @classmethod
    def from_dict(cls, d: dict) -> 'Activity':
        d = d.copy()
        d['type'] = ActivityType(d.get('type', 'note'))
        d['metadata'] = json.loads(d.get('metadata', '{}'))
        return cls(**d)


@dataclass
class Deal:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    lead_id: str = ""
    company_id: str = ""
    name: str = ""
    value: float = 0.0  # RM
    workers_count: int = 0
    stage: LeadStatus = LeadStatus.PROPOSAL
    probability: float = 0.0
    expected_close_date: Optional[str] = None
    actual_close_date: Optional[str] = None
    terms: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        d = asdict(self)
        d['stage'] = self.stage.value
        return d


@dataclass
class EmailTemplate:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    subject: str = ""
    body_html: str = ""
    body_text: str = ""
    variables: List[str] = field(default_factory=list)
    category: str = ""  # cold, followup, proposal, nurture
    language: str = "en"  # en, bn, ms
    is_active: bool = True
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class OutreachSequence:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    steps: List[Dict[str, Any]] = field(default_factory=list)
    # steps: [{"delay_days": 0, "template_id": "...", "channel": "email"}, ...]
    is_active: bool = True
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


# =============================================================================
# DATABASE
# =============================================================================

SCHEMA = """
-- Companies
CREATE TABLE IF NOT EXISTS companies (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    website TEXT,
    phone TEXT,
    email TEXT,
    hr_email TEXT,
    linkedin TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    industry TEXT DEFAULT 'other',
    sub_industry TEXT,
    size TEXT DEFAULT 'medium',
    employee_count INTEGER DEFAULT 0,
    foreign_worker_count INTEGER DEFAULT 0,
    levy_tier TEXT DEFAULT 'RM1850',
    priority_score REAL DEFAULT 50.0,
    source TEXT DEFAULT 'directory',
    source_url TEXT,
    notes TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    last_contacted_at TEXT,
    last_activity_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_companies_name ON companies(name);
CREATE INDEX IF NOT EXISTS idx_companies_industry ON companies(industry);
CREATE INDEX IF NOT EXISTS idx_companies_state ON companies(state);
CREATE INDEX IF NOT EXISTS idx_companies_priority ON companies(priority_score DESC);
CREATE INDEX IF NOT EXISTS idx_companies_source ON companies(source);

-- Contacts
CREATE TABLE IF NOT EXISTS contacts (
    id TEXT PRIMARY KEY,
    company_id TEXT NOT NULL,
    name TEXT,
    title TEXT,
    email TEXT,
    phone TEXT,
    linkedin TEXT,
    is_decision_maker INTEGER DEFAULT 0,
    is_hr INTEGER DEFAULT 0,
    is_primary INTEGER DEFAULT 0,
    notes TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (company_id) REFERENCES companies(id)
);

CREATE INDEX IF NOT EXISTS idx_contacts_company ON contacts(company_id);
CREATE INDEX IF NOT EXISTS idx_contacts_email ON contacts(email);

-- Leads
CREATE TABLE IF NOT EXISTS leads (
    id TEXT PRIMARY KEY,
    company_id TEXT NOT NULL,
    contact_id TEXT,
    status TEXT DEFAULT 'new',
    source TEXT DEFAULT 'directory',
    score REAL DEFAULT 0.0,
    estimated_value REAL DEFAULT 0.0,
    expected_workers INTEGER DEFAULT 0,
    assigned_to TEXT,
    tags TEXT DEFAULT '[]',
    notes TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    qualified_at TEXT,
    closed_at TEXT,
    lost_reason TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (contact_id) REFERENCES contacts(id)
);

CREATE INDEX IF NOT EXISTS idx_leads_company ON leads(company_id);
CREATE INDEX IF NOT EXISTS idx_leads_status ON leads(status);
CREATE INDEX IF NOT EXISTS idx_leads_score ON leads(score DESC);
CREATE INDEX IF NOT EXISTS idx_leads_assigned ON leads(assigned_to);

-- Activities
CREATE TABLE IF NOT EXISTS activities (
    id TEXT PRIMARY KEY,
    lead_id TEXT,
    company_id TEXT,
    contact_id TEXT,
    type TEXT NOT NULL,
    subject TEXT,
    description TEXT,
    metadata TEXT DEFAULT '{}',
    created_by TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (lead_id) REFERENCES leads(id),
    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (contact_id) REFERENCES contacts(id)
);

CREATE INDEX IF NOT EXISTS idx_activities_lead ON activities(lead_id);
CREATE INDEX IF NOT EXISTS idx_activities_company ON activities(company_id);
CREATE INDEX IF NOT EXISTS idx_activities_created ON activities(created_at DESC);

-- Deals
CREATE TABLE IF NOT EXISTS deals (
    id TEXT PRIMARY KEY,
    lead_id TEXT NOT NULL,
    company_id TEXT NOT NULL,
    name TEXT,
    value REAL DEFAULT 0.0,
    workers_count INTEGER DEFAULT 0,
    stage TEXT DEFAULT 'proposal',
    probability REAL DEFAULT 0.0,
    expected_close_date TEXT,
    actual_close_date TEXT,
    terms TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (lead_id) REFERENCES leads(id),
    FOREIGN KEY (company_id) REFERENCES companies(id)
);

CREATE INDEX IF NOT EXISTS idx_deals_lead ON deals(lead_id);
CREATE INDEX IF NOT EXISTS idx_deals_stage ON deals(stage);

-- Email Templates
CREATE TABLE IF NOT EXISTS email_templates (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    subject TEXT NOT NULL,
    body_html TEXT,
    body_text TEXT,
    variables TEXT DEFAULT '[]',
    category TEXT,
    language TEXT DEFAULT 'en',
    is_active INTEGER DEFAULT 1,
    created_at TEXT NOT NULL
);

-- Outreach Sequences
CREATE TABLE IF NOT EXISTS outreach_sequences (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    steps TEXT DEFAULT '[]',
    is_active INTEGER DEFAULT 1,
    created_at TEXT NOT NULL
);

-- Sequence Enrollments (which lead is in which sequence at which step)
CREATE TABLE IF NOT EXISTS sequence_enrollments (
    id TEXT PRIMARY KEY,
    sequence_id TEXT NOT NULL,
    lead_id TEXT NOT NULL,
    current_step INTEGER DEFAULT 0,
    status TEXT DEFAULT 'active',  -- active, paused, completed, stopped
    next_action_at TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (sequence_id) REFERENCES outreach_sequences(id),
    FOREIGN KEY (lead_id) REFERENCES leads(id)
);

CREATE INDEX IF NOT EXISTS idx_enrollments_lead ON sequence_enrollments(lead_id);
CREATE INDEX IF NOT EXISTS idx_enrollments_next_action ON sequence_enrollments(next_action_at);
"""


@contextmanager
def get_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    with get_db() as conn:
        conn.executescript(SCHEMA)
        conn.commit()
    print(f"CRM database initialized at {DB_PATH}")


# =============================================================================
# REPOSITORY CLASSES
# =============================================================================

class CompanyRepo:
    @staticmethod
    def create(company: Company) -> Company:
        with get_db() as conn:
            conn.execute("""
                INSERT INTO companies (id, name, website, phone, email, hr_email, linkedin,
                    address, city, state, industry, sub_industry, size, employee_count,
                    foreign_worker_count, levy_tier, priority_score, source, source_url,
                    notes, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                company.id, company.name, company.website, company.phone, company.email,
                company.hr_email, company.linkedin, company.address, company.city,
                company.state, company.industry.value, company.sub_industry,
                company.size.value, company.employee_count, company.foreign_worker_count,
                company.levy_tier, company.priority_score, company.source.value,
                company.source_url, company.notes, company.created_at, company.updated_at
            ))
            conn.commit()
        return company

    @staticmethod
    def get(company_id: str) -> Optional[Company]:
        with get_db() as conn:
            row = conn.execute("SELECT * FROM companies WHERE id = ?", (company_id,)).fetchone()
            return Company.from_dict(dict(row)) if row else None

    @staticmethod
    def get_by_name(name: str) -> Optional[Company]:
        with get_db() as conn:
            row = conn.execute("SELECT * FROM companies WHERE name = ?", (name,)).fetchone()
            return Company.from_dict(dict(row)) if row else None

    @staticmethod
    def update(company: Company) -> Company:
        company.updated_at = datetime.now().isoformat()
        with get_db() as conn:
            conn.execute("""
                UPDATE companies SET name=?, website=?, phone=?, email=?, hr_email=?,
                    linkedin=?, address=?, city=?, state=?, industry=?, sub_industry=?,
                    size=?, employee_count=?, foreign_worker_count=?, levy_tier=?,
                    priority_score=?, source=?, source_url=?, notes=?, updated_at=?,
                    last_contacted_at=?, last_activity_at=?
                WHERE id=?
            """, (
                company.name, company.website, company.phone, company.email, company.hr_email,
                company.linkedin, company.address, company.city, company.state,
                company.industry.value, company.sub_industry, company.size.value,
                company.employee_count, company.foreign_worker_count, company.levy_tier,
                company.priority_score, company.source.value, company.source_url,
                company.notes, company.updated_at, company.last_contacted_at,
                company.last_activity_at, company.id
            ))
            conn.commit()
        return company

    @staticmethod
    def list(limit: int = 100, offset: int = 0, industry: Optional[str] = None,
             state: Optional[str] = None, min_score: float = 0) -> List[Company]:
        with get_db() as conn:
            query = "SELECT * FROM companies WHERE priority_score >= ?"
            params = [min_score]
            if industry:
                query += " AND industry = ?"
                params.append(industry)
            if state:
                query += " AND state = ?"
                params.append(state)
            query += " ORDER BY priority_score DESC LIMIT ? OFFSET ?"
            params.extend([limit, offset])
            rows = conn.execute(query, params).fetchall()
            return [Company.from_dict(dict(r)) for r in rows]

    @staticmethod
    def search(q: str, limit: int = 50) -> List[Company]:
        with get_db() as conn:
            rows = conn.execute("""
                SELECT * FROM companies 
                WHERE name LIKE ? OR website LIKE ? OR industry LIKE ? OR city LIKE ?
                ORDER BY priority_score DESC LIMIT ?
            """, (f"%{q}%", f"%{q}%", f"%{q}%", f"%{q}%", limit)).fetchall()
            return [Company.from_dict(dict(r)) for r in rows]

    @staticmethod
    def count() -> int:
        with get_db() as conn:
            return conn.execute("SELECT COUNT(*) FROM companies").fetchone()[0]


class ContactRepo:
    @staticmethod
    def create(contact: Contact) -> Contact:
        with get_db() as conn:
            conn.execute("""
                INSERT INTO contacts (id, company_id, name, title, email, phone, linkedin,
                    is_decision_maker, is_hr, is_primary, notes, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                contact.id, contact.company_id, contact.name, contact.title,
                contact.email, contact.phone, contact.linkedin,
                int(contact.is_decision_maker), int(contact.is_hr), int(contact.is_primary),
                contact.notes, contact.created_at, contact.updated_at
            ))
            conn.commit()
        return contact

    @staticmethod
    def get_by_company(company_id: str) -> List[Contact]:
        with get_db() as conn:
            rows = conn.execute("SELECT * FROM contacts WHERE company_id = ? ORDER BY is_primary DESC", (company_id,)).fetchall()
            return [Contact(**dict(r)) for r in rows]

    @staticmethod
    def get_by_email(email: str) -> Optional[Contact]:
        with get_db() as conn:
            row = conn.execute("SELECT * FROM contacts WHERE email = ?", (email,)).fetchone()
            return Contact(**dict(row)) if row else None

    @staticmethod
    def update(contact: Contact) -> Contact:
        contact.updated_at = datetime.now().isoformat()
        with get_db() as conn:
            conn.execute("""
                UPDATE contacts SET name=?, title=?, email=?, phone=?, linkedin=?,
                    is_decision_maker=?, is_hr=?, is_primary=?, notes=?, updated_at=?
                WHERE id=?
            """, (contact.name, contact.title, contact.email, contact.phone, contact.linkedin,
                  int(contact.is_decision_maker), int(contact.is_hr), int(contact.is_primary),
                  contact.notes, contact.updated_at, contact.id))
            conn.commit()
        return contact


class LeadRepo:
    @staticmethod
    def create(lead: Lead) -> Lead:
        with get_db() as conn:
            conn.execute("""
                INSERT INTO leads (id, company_id, contact_id, status, source, score,
                    estimated_value, expected_workers, assigned_to, tags, notes,
                    created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                lead.id, lead.company_id, lead.contact_id, lead.status.value,
                lead.source.value, lead.score, lead.estimated_value, lead.expected_workers,
                lead.assigned_to, json.dumps(lead.tags), lead.notes,
                lead.created_at, lead.updated_at
            ))
            conn.commit()
        return lead

    @staticmethod
    def get(lead_id: str) -> Optional[Lead]:
        with get_db() as conn:
            row = conn.execute("SELECT * FROM leads WHERE id = ?", (lead_id,)).fetchone()
            return Lead.from_dict(dict(row)) if row else None

    @staticmethod
    def get_by_company(company_id: str) -> Optional[Lead]:
        with get_db() as conn:
            row = conn.execute("SELECT * FROM leads WHERE company_id = ? ORDER BY created_at DESC LIMIT 1", (company_id,)).fetchone()
            return Lead.from_dict(dict(row)) if row else None

    @staticmethod
    def update(lead: Lead) -> Lead:
        lead.updated_at = datetime.now().isoformat()
        if lead.status == LeadStatus.QUALIFIED and not lead.qualified_at:
            lead.qualified_at = datetime.now().isoformat()
        if lead.status in (LeadStatus.WON, LeadStatus.LOST) and not lead.closed_at:
            lead.closed_at = datetime.now().isoformat()
        with get_db() as conn:
            conn.execute("""
                UPDATE leads SET status=?, score=?, estimated_value=?, expected_workers=?,
                    assigned_to=?, tags=?, notes=?, updated_at=?, qualified_at=?, closed_at=?, lost_reason=?
                WHERE id=?
            """, (lead.status.value, lead.score, lead.estimated_value, lead.expected_workers,
                  lead.assigned_to, json.dumps(lead.tags), lead.notes, lead.updated_at,
                  lead.qualified_at, lead.closed_at, lead.lost_reason, lead.id))
            conn.commit()
        return lead

    @staticmethod
    def list(status: Optional[LeadStatus] = None, assigned_to: Optional[str] = None,
             min_score: float = 0, limit: int = 100, offset: int = 0) -> List[Lead]:
        with get_db() as conn:
            query = "SELECT * FROM leads WHERE score >= ?"
            params = [min_score]
            if status:
                query += " AND status = ?"
                params.append(status.value)
            if assigned_to:
                query += " AND assigned_to = ?"
                params.append(assigned_to)
            query += " ORDER BY score DESC, created_at DESC LIMIT ? OFFSET ?"
            params.extend([limit, offset])
            rows = conn.execute(query, params).fetchall()
            return [Lead.from_dict(dict(r)) for r in rows]

    @staticmethod
    def pipeline_counts() -> Dict[str, int]:
        with get_db() as conn:
            rows = conn.execute("SELECT status, COUNT(*) as cnt FROM leads GROUP BY status").fetchall()
            return {r['status']: r['cnt'] for r in rows}


class ActivityRepo:
    @staticmethod
    def create(activity: Activity) -> Activity:
        with get_db() as conn:
            conn.execute("""
                INSERT INTO activities (id, lead_id, company_id, contact_id, type, subject,
                    description, metadata, created_by, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                activity.id, activity.lead_id, activity.company_id, activity.contact_id,
                activity.type.value, activity.subject, activity.description,
                json.dumps(activity.metadata), activity.created_by, activity.created_at
            ))
            # Update last_activity_at on company and lead
            if activity.company_id:
                conn.execute("UPDATE companies SET last_activity_at = ? WHERE id = ?",
                             (activity.created_at, activity.company_id))
            if activity.lead_id:
                conn.execute("UPDATE leads SET updated_at = ? WHERE id = ?",
                             (activity.created_at, activity.lead_id))
            conn.commit()
        return activity

    @staticmethod
    def get_for_lead(lead_id: str, limit: int = 50) -> List[Activity]:
        with get_db() as conn:
            rows = conn.execute("""
                SELECT * FROM activities WHERE lead_id = ? ORDER BY created_at DESC LIMIT ?
            """, (lead_id, limit)).fetchall()
            return [Activity.from_dict(dict(r)) for r in rows]

    @staticmethod
    def get_for_company(company_id: str, limit: int = 50) -> List[Activity]:
        with get_db() as conn:
            rows = conn.execute("""
                SELECT * FROM activities WHERE company_id = ? ORDER BY created_at DESC LIMIT ?
            """, (company_id, limit)).fetchall()
            return [Activity.from_dict(dict(r)) for r in rows]


class DealRepo:
    @staticmethod
    def create(deal: Deal) -> Deal:
        with get_db() as conn:
            conn.execute("""
                INSERT INTO deals (id, lead_id, company_id, name, value, workers_count,
                    stage, probability, expected_close_date, terms, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                deal.id, deal.lead_id, deal.company_id, deal.name, deal.value,
                deal.workers_count, deal.stage.value, deal.probability,
                deal.expected_close_date, deal.terms, deal.created_at, deal.updated_at
            ))
            conn.commit()
        return deal

    @staticmethod
    def get(deal_id: str) -> Optional[Deal]:
        with get_db() as conn:
            row = conn.execute("SELECT * FROM deals WHERE id = ?", (deal_id,)).fetchone()
            if row:
                d = dict(row)
                d['stage'] = LeadStatus(d['stage'])
                return Deal(**d)
            return None

    @staticmethod
    def get_by_lead(lead_id: str) -> Optional[Deal]:
        with get_db() as conn:
            row = conn.execute("SELECT * FROM deals WHERE lead_id = ?", (lead_id,)).fetchone()
            if row:
                d = dict(row)
                d['stage'] = LeadStatus(d['stage'])
                return Deal(**d)
            return None

    @staticmethod
    def update(deal: Deal) -> Deal:
        deal.updated_at = datetime.now().isoformat()
        if deal.stage in (LeadStatus.WON, LeadStatus.LOST) and not deal.actual_close_date:
            deal.actual_close_date = datetime.now().date().isoformat()
        with get_db() as conn:
            conn.execute("""
                UPDATE deals SET name=?, value=?, workers_count=?, stage=?, probability=?,
                    expected_close_date=?, actual_close_date=?, terms=?, updated_at=?
                WHERE id=?
            """, (deal.name, deal.value, deal.workers_count, deal.stage.value,
                  deal.probability, deal.expected_close_date, deal.actual_close_date,
                  deal.terms, deal.updated_at, deal.id))
            conn.commit()
        return deal

    @staticmethod
    def pipeline_value() -> Dict[str, float]:
        with get_db() as conn:
            rows = conn.execute("""
                SELECT stage, SUM(value * probability / 100) as weighted_value
                FROM deals WHERE stage NOT IN ('won', 'lost')
                GROUP BY stage
            """).fetchall()
            return {r['stage']: r['weighted_value'] or 0 for r in rows}


class TemplateRepo:
    @staticmethod
    def create(template: EmailTemplate) -> EmailTemplate:
        with get_db() as conn:
            conn.execute("""
                INSERT INTO email_templates (id, name, subject, body_html, body_text,
                    variables, category, language, is_active, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                template.id, template.name, template.subject, template.body_html,
                template.body_text, json.dumps(template.variables), template.category,
                template.language, int(template.is_active), template.created_at
            ))
            conn.commit()
        return template

    @staticmethod
    def get(template_id: str) -> Optional[EmailTemplate]:
        with get_db() as conn:
            row = conn.execute("SELECT * FROM email_templates WHERE id = ?", (template_id,)).fetchone()
            if row:
                d = dict(row)
                d['variables'] = json.loads(d['variables'])
                d['is_active'] = bool(d['is_active'])
                return EmailTemplate(**d)
            return None

    @staticmethod
    def list(category: Optional[str] = None, language: Optional[str] = None) -> List[EmailTemplate]:
        with get_db() as conn:
            query = "SELECT * FROM email_templates WHERE is_active = 1"
            params = []
            if category:
                query += " AND category = ?"
                params.append(category)
            if language:
                query += " AND language = ?"
                params.append(language)
            rows = conn.execute(query + " ORDER BY category, name", params).fetchall()
            result = []
            for r in rows:
                d = dict(r)
                d['variables'] = json.loads(d['variables'])
                d['is_active'] = bool(d['is_active'])
                result.append(EmailTemplate(**d))
            return result


class SequenceRepo:
    @staticmethod
    def create(seq: OutreachSequence) -> OutreachSequence:
        with get_db() as conn:
            conn.execute("""
                INSERT INTO outreach_sequences (id, name, steps, is_active, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (seq.id, seq.name, json.dumps(seq.steps), int(seq.is_active), seq.created_at))
            conn.commit()
        return seq

    @staticmethod
    def get(seq_id: str) -> Optional[OutreachSequence]:
        with get_db() as conn:
            row = conn.execute("SELECT * FROM outreach_sequences WHERE id = ?", (seq_id,)).fetchone()
            if row:
                d = dict(row)
                d['steps'] = json.loads(d['steps'])
                d['is_active'] = bool(d['is_active'])
                return OutreachSequence(**d)
            return None

    @staticmethod
    def list() -> List[OutreachSequence]:
        with get_db() as conn:
            rows = conn.execute("SELECT * FROM outreach_sequences WHERE is_active = 1 ORDER BY name").fetchall()
            result = []
            for r in rows:
                d = dict(r)
                d['steps'] = json.loads(d['steps'])
                d['is_active'] = bool(d['is_active'])
                result.append(OutreachSequence(**d))
            return result


class EnrollmentRepo:
    @staticmethod
    def enroll(lead_id: str, sequence_id: str, start_delay_days: int = 0) -> str:
        enrollment_id = str(uuid.uuid4())[:8]
        next_action = (datetime.now() + timedelta(days=start_delay_days)).isoformat()
        with get_db() as conn:
            conn.execute("""
                INSERT INTO sequence_enrollments (id, sequence_id, lead_id, current_step,
                    status, next_action_at, created_at, updated_at)
                VALUES (?, ?, ?, 0, 'active', ?, ?, ?)
            """, (enrollment_id, sequence_id, lead_id, next_action,
                  datetime.now().isoformat(), datetime.now().isoformat()))
            conn.commit()
        return enrollment_id

    @staticmethod
    def get_due_enrollments(limit: int = 100) -> List[Dict]:
        now = datetime.now().isoformat()
        with get_db() as conn:
            rows = conn.execute("""
                SELECT se.*, s.steps, s.name as seq_name, l.company_id, l.status as lead_status
                FROM sequence_enrollments se
                JOIN outreach_sequences s ON se.sequence_id = s.id
                JOIN leads l ON se.lead_id = l.id
                WHERE se.status = 'active' AND se.next_action_at <= ? AND s.is_active = 1
                ORDER BY se.next_action_at LIMIT ?
            """, (now, limit)).fetchall()
            result = []
            for r in rows:
                d = dict(r)
                d['steps'] = json.loads(d['steps'])
                result.append(d)
            return result

    @staticmethod
    def advance(enrollment_id: str, next_step: int, next_delay_days: int) -> bool:
        next_action = (datetime.now() + timedelta(days=next_delay_days)).isoformat()
        status = 'active'
        if next_step < 0:  # completed
            status = 'completed'
            next_action = None
        with get_db() as conn:
            conn.execute("""
                UPDATE sequence_enrollments SET current_step=?, status=?, next_action_at=?, updated_at=?
                WHERE id=?
            """, (next_step, status, next_action, datetime.now().isoformat(), enrollment_id))
            conn.commit()
        return True

    @staticmethod
    def pause(enrollment_id: str) -> bool:
        with get_db() as conn:
            conn.execute("UPDATE sequence_enrollments SET status='paused', updated_at=? WHERE id=?",
                         (datetime.now().isoformat(), enrollment_id))
            conn.commit()
        return True


# =============================================================================
# LEAD SCORING
# =============================================================================

def calculate_lead_score(company: Company, contact: Optional[Contact] = None) -> float:
    """Calculate lead score 0-100 based on company attributes and engagement."""
    score = 0.0

    # Industry weight (high foreign worker demand)
    industry_weights = {
        Industry.PLANTATION: 25,
        Industry.MANUFACTURING: 20,
        Industry.ELECTRONICS: 20,
        Industry.CONSTRUCTION: 18,
        Industry.HOSPITALITY: 12,
        Industry.LOGISTICS: 10,
        Industry.SERVICES: 8,
        Industry.CLEANING: 10,
        Industry.SECURITY: 10,
        Industry.RETAIL: 6,
        Industry.OTHER: 5,
    }
    score += industry_weights.get(company.industry, 5)

    # Company size
    size_weights = {
        CompanySize.CORPORATE: 20,
        CompanySize.ENTERPRISE: 18,
        CompanySize.LARGE: 15,
        CompanySize.MEDIUM: 10,
        CompanySize.SMALL: 5,
        CompanySize.STARTUP: 2,
    }
    score += size_weights.get(company.size, 5)

    # Foreign worker count (if known)
    if company.foreign_worker_count >= 500:
        score += 15
    elif company.foreign_worker_count >= 100:
        score += 10
    elif company.foreign_worker_count >= 20:
        score += 5

    # Contact quality
    if contact:
        if contact.is_decision_maker:
            score += 10
        if contact.is_hr:
            score += 8
        if contact.email:
            score += 5
        if contact.phone:
            score += 3
        if contact.linkedin:
            score += 2

    # Company contact info completeness
    if company.hr_email:
        score += 8
    elif company.email:
        score += 5
    if company.phone:
        score += 3
    if company.linkedin:
        score += 2
    if company.website:
        score += 2

    # Priority score from scraper
    score += min(company.priority_score / 10, 10)

    # Levy tier (lower levy = higher volume potential)
    if company.levy_tier == "RM640":
        score += 5

    return min(score, 100.0)


def create_lead_from_company(company: Company, contact: Optional[Contact] = None) -> Lead:
    """Create or update a lead from company data with calculated score."""
    score = calculate_lead_score(company, contact)
    
    # Estimate value: RM 15,000-25,000 per worker per year (agency margin)
    estimated_workers = max(company.foreign_worker_count, 
                           int(company.employee_count * 0.15) if company.employee_count > 0 else 5)
    estimated_value = estimated_workers * 20000  # Conservative RM 20k/worker/year

    lead = Lead(
        company_id=company.id,
        contact_id=contact.id if contact else "",
        status=LeadStatus.NEW,
        source=company.source,
        score=score,
        estimated_value=estimated_value,
        expected_workers=estimated_workers,
        tags=[company.industry.value, company.size.value, company.state],
        notes=f"Auto-created from {company.source.value}. Industry: {company.industry.value}, Size: {company.size.value}"
    )
    return lead


# =============================================================================
# SECTOR MAPPING HELPER
# =============================================================================

def _map_sector_to_industry(sector: str) -> 'Industry':
    """Map scraper sector strings to Industry enum."""
    sector_lower = sector.lower().strip()
    
    mapping = {
        'manufacturing': Industry.MANUFACTURING,
        'electrical & electronics': Industry.ELECTRONICS,
        'electronics': Industry.ELECTRONICS,
        'e&e': Industry.ELECTRONICS,
        'construction': Industry.CONSTRUCTION,
        'plantation': Industry.PLANTATION,
        'hospitality': Industry.HOSPITALITY,
        'retail': Industry.RETAIL,
        'services': Industry.SERVICES,
        'logistics': Industry.LOGISTICS,
        'security': Industry.SECURITY,
        'cleaning': Industry.CLEANING,
        'agriculture': Industry.PLANTATION,
        'furniture': Industry.MANUFACTURING,
        'rubber': Industry.MANUFACTURING,
        'food processing': Industry.MANUFACTURING,
        'chemical': Industry.MANUFACTURING,
        'metal': Industry.MANUFACTURING,
        'machinery': Industry.MANUFACTURING,
        'automotive': Industry.MANUFACTURING,
        'plastic': Industry.MANUFACTURING,
    }
    
    return mapping.get(sector_lower, Industry.OTHER)
    """Import companies from the existing companies.csv into CRM."""
    import csv
    
    with get_db() as conn:
        cursor = conn.cursor()
        imported = 0
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Skip if already exists
                existing = cursor.execute("SELECT id FROM companies WHERE name = ?", 
                                          (row.get('company_name', ''),)).fetchone()
                if existing:
                    continue
                
                company = Company(
                    name=row.get('company_name', ''),
                    website=row.get('website', ''),
                    phone=row.get('phone', ''),
                    email=row.get('email', ''),
                    hr_email=row.get('hr_contact', ''),
                    industry=_map_sector_to_industry(row.get('sector', 'other')),
                    state=row.get('state', ''),
                    city=row.get('city', ''),
                    employee_count=int(row.get('employees_est', 0)) if row.get('employees_est', '').isdigit() else 0,
                    foreign_worker_count=0,
                    levy_tier=row.get('levy_tier', 'RM1850').replace('"', '').strip(),
                    priority_score=float(row.get('priority_score', 50)) if row.get('priority_score', '').replace('.', '').isdigit() else 50,
                    source=LeadSource.DIRECTORY,
                    source_url=row.get('source_url', ''),
                    notes=row.get('notes', ''),
                )
                
                cursor.execute("""
                    INSERT INTO companies (id, name, website, phone, email, hr_email, linkedin,
                        address, city, state, industry, sub_industry, size, employee_count,
                        foreign_worker_count, levy_tier, priority_score, source, source_url,
                        notes, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    company.id, company.name, company.website, company.phone, company.email,
                    company.hr_email, company.linkedin, company.address, company.city,
                    company.state, company.industry.value, company.sub_industry,
                    company.size.value, company.employee_count, company.foreign_worker_count,
                    company.levy_tier, company.priority_score, company.source.value,
                    company.source_url, company.notes, company.created_at, company.updated_at
                ))
                imported += 1
        
        conn.commit()
    
    print(f"Imported {imported} companies from {csv_path}")
    return imported


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="CRM Database Management")
    parser.add_argument("--init", action="store_true", help="Initialize database")
    parser.add_argument("--import-csv", type=str, help="Import from companies.csv")
    parser.add_argument("--score-all", action="store_true", help="Score all companies and create leads")
    parser.add_argument("--stats", action="store_true", help="Show CRM statistics")
    
    args = parser.parse_args()
    
    if args.init:
        init_db()
    
    if args.import_csv:
        import_from_companies_csv(Path(args.import_csv))
    
    if args.score_all:
        with get_db() as conn:
            companies = conn.execute("SELECT * FROM companies WHERE priority_score > 0").fetchall()
            lead_repo = LeadRepo()
            contact_repo = ContactRepo()
            
            created = 0
            for row in companies:
                company = Company.from_dict(dict(row))
                contacts = contact_repo.get_by_company(company.id)
                primary_contact = next((c for c in contacts if c.is_primary), contacts[0] if contacts else None)
                
                # Check if lead exists
                existing = lead_repo.get_by_company(company.id)
                if not existing:
                    lead = create_lead_from_company(company, primary_contact)
                    lead_repo.create(lead)
                    created += 1
            
            print(f"Created {created} new leads")
    
    if args.stats:
        with get_db() as conn:
            print("\n=== CRM STATISTICS ===")
            print(f"Companies: {conn.execute('SELECT COUNT(*) FROM companies').fetchone()[0]}")
            print(f"Contacts: {conn.execute('SELECT COUNT(*) FROM contacts').fetchone()[0]}")
            print(f"Leads: {conn.execute('SELECT COUNT(*) FROM leads').fetchone()[0]}")
            print(f"Activities: {conn.execute('SELECT COUNT(*) FROM activities').fetchone()[0]}")
            print(f"Deals: {conn.execute('SELECT COUNT(*) FROM deals').fetchone()[0]}")
            
            print("\nLead Pipeline:")
            for status, count in LeadRepo.pipeline_counts().items():
                print(f"  {status}: {count}")
            
            print("\nWeighted Pipeline Value:")
            for stage, value in DealRepo.pipeline_value().items():
                print(f"  {stage}: RM {value:,.0f}")