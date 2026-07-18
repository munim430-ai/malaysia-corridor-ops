"""
CRM Pipeline — Lead Scoring, Stage Management, Conversion Tracking
===================================================================
Full pipeline automation: scoring, stage transitions, conversion analytics,
outreach sequence enrollment, and forecasting.
"""

import json
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

from crm.models import (
    Company, Contact, Lead, Activity, Deal, EmailTemplate, OutreachSequence,
    LeadStatus, LeadSource, ActivityType, Industry, CompanySize,
    CompanyRepo, ContactRepo, LeadRepo, ActivityRepo, init_db, get_db
)


# =============================================================================
# LEAD SCORING ENGINE
# =============================================================================

SCORING_WEIGHTS = {
    # Company attributes
    "priority_score": 0.25,        # 0-100 from scraper
    "employee_count": 0.15,        # More employees = more workers needed
    "foreign_worker_count": 0.20,  # Proven track record
    "industry_fit": 0.15,          # High-demand sectors
    "levy_tier": 0.10,             # RM1850 > RM640 (more budget)
    "has_contact": 0.15,           # Phone/email available
    
    # Engagement signals
    "email_opens": 0.05,           # Per open
    "email_clicks": 0.10,          # Per click
    "email_replies": 0.30,         # Per reply (strong signal)
    "meetings_held": 0.25,         # Per meeting
    "proposal_sent": 0.20,         # Binary
}

INDUSTRY_MULTIPLIERS = {
    "manufacturing": 1.2,
    "electronics": 1.3,
    "construction": 1.15,
    "plantation": 1.1,
    "hospitality": 1.0,
    "retail": 0.9,
    "services": 0.85,
    "logistics": 0.95,
    "security": 0.9,
    "cleaning": 0.85,
    "other": 0.8,
}

LEVY_MULTIPLIERS = {
    "RM1850": 1.0,
    "RM640": 0.7,
}

SIZE_MULTIPLIERS = {
    "1-10": 0.5,
    "11-50": 0.7,
    "51-200": 1.0,
    "201-500": 1.2,
    "501-1000": 1.3,
    "1000+": 1.5,
}


def calculate_lead_score(lead: 'Lead', company: 'Company', 
                         activities: List['Activity'] = None) -> float:
    """
    Calculate lead score 0-100 based on company attributes + engagement.
    """
    score = 0.0
    
    # Company attributes (static)
    score += min(company.priority_score, 100) * SCORING_WEIGHTS["priority_score"]
    
    # Employee count score (logarithmic)
    emp_score = min(company.employee_count / 1000 * 100, 100) if company.employee_count > 0 else 20
    score += emp_score * SCORING_WEIGHTS["employee_count"]
    
    # Foreign worker track record
    fw_score = min(company.foreign_worker_count / 500 * 100, 100) if company.foreign_worker_count > 0 else 10
    score += fw_score * SCORING_WEIGHTS["foreign_worker_count"]
    
    # Industry fit
    industry_mult = INDUSTRY_MULTIPLIERS.get(company.industry.value, 0.8)
    score += 50 * industry_mult * SCORING_WEIGHTS["industry_fit"] / 1.3  # Normalize
    
    # Levy tier
    levy_mult = LEVY_MULTIPLIERS.get(company.levy_tier, 0.8)
    score += 50 * levy_mult * SCORING_WEIGHTS["levy_tier"]
    
    # Contact availability
    contact_score = 0
    if company.phone: contact_score += 30
    if company.email: contact_score += 30
    if company.hr_email: contact_score += 20
    if company.linkedin: contact_score += 20
    score += min(contact_score, 100) * SCORING_WEIGHTS["has_contact"]
    
    # Engagement signals (dynamic)
    if activities:
        opens = sum(1 for a in activities if a.type.value == "email_opened")
        clicks = sum(1 for a in activities if a.type.value == "email_clicked")
        replies = sum(1 for a in activities if a.type.value == "email_replied")
        meetings = sum(1 for a in activities if a.type.value in ("meeting_scheduled", "meeting_held"))
        proposals = sum(1 for a in activities if a.type.value == "proposal_sent")
        
        score += min(opens * 2, 20) * SCORING_WEIGHTS["email_opens"]
        score += min(clicks * 5, 30) * SCORING_WEIGHTS["email_clicks"]
        score += min(replies * 15, 50) * SCORING_WEIGHTS["email_replies"]
        score += min(meetings * 10, 40) * SCORING_WEIGHTS["meetings_held"]
        score += (25 if proposals > 0 else 0) * SCORING_WEIGHTS["proposal_sent"]
    
    # Apply multipliers
    score *= SIZE_MULTIPLIERS.get(company.size.value, 1.0)
    
    return min(max(score, 0), 100)


def score_all_leads():
    """Recalculate scores for all leads in database."""
    leads = LeadRepo.list(limit=10000)
    updated = 0
    
    for lead in leads:
        company = CompanyRepo.get(lead.company_id)
        if not company:
            continue
            
        activities = []
        with get_db() as conn:
            rows = conn.execute(
                "SELECT * FROM activities WHERE lead_id = ? ORDER BY created_at DESC",
                (lead.id,)
            ).fetchall()
            activities = [Activity(**dict(r)) for r in rows]
        
        new_score = calculate_lead_score(lead, company, activities)
        
        if abs(lead.score - new_score) > 1:
            lead.score = round(new_score, 1)
            LeadRepo.update(lead)
            updated += 1
    
    return updated


# =============================================================================
# PIPELINE STAGE MANAGEMENT
# =============================================================================

STAGE_ORDER = [
    LeadStatus.NEW,
    LeadStatus.CONTACTED,
    LeadStatus.QUALIFIED,
    LeadStatus.PROPOSAL,
    LeadStatus.NEGOTIATION,
    LeadStatus.WON,
    LeadStatus.LOST,
    LeadStatus.NURTURING,
]

STAGE_PROBABILITIES = {
    LeadStatus.NEW: 0.05,
    LeadStatus.CONTACTED: 0.10,
    LeadStatus.QUALIFIED: 0.25,
    LeadStatus.PROPOSAL: 0.50,
    LeadStatus.NEGOTIATION: 0.75,
    LeadStatus.WON: 1.0,
    LeadStatus.LOST: 0.0,
    LeadStatus.NURTURING: 0.05,
}

STAGE_REQUIREMENTS = {
    LeadStatus.NEW: [],
    LeadStatus.CONTACTED: ["at_least_one_activity"],
    LeadStatus.QUALIFIED: ["contact_person_identified", "need_confirmed", "budget_qualified"],
    LeadStatus.PROPOSAL: ["proposal_sent", "decision_maker_engaged"],
    LeadStatus.NEGOTIATION: ["terms_discussed", "decision_maker_committed"],
    LeadStatus.WON: ["contract_signed", "deposit_received"],
    LeadStatus.LOST: ["lost_reason_recorded"],
    LeadStatus.NURTURING: ["nurture_sequence_active"],
}


def can_advance_stage(lead: Lead, target_stage: LeadStatus, 
                      company: Company, contact: Contact = None,
                      activities: List[Activity] = None) -> Tuple[bool, List[str]]:
    """Check if lead meets requirements to advance to target stage."""
    missing = []
    
    if target_stage not in STAGE_REQUIREMENTS:
        return False, ["Invalid target stage"]
    
    current_idx = STAGE_ORDER.index(lead.status)
    target_idx = STAGE_ORDER.index(target_stage)
    
    if target_idx <= current_idx:
        return False, ["Target stage must be ahead of current stage"]
    
    # Check all intermediate stages' requirements
    for idx in range(current_idx + 1, target_idx + 1):
        stage = STAGE_ORDER[idx]
        reqs = STAGE_REQUIREMENTS.get(stage, [])
        
        for req in reqs:
            if req == "at_least_one_activity":
                if not activities or len(activities) == 0:
                    missing.append(f"{stage.value}: at least one activity required")
            elif req == "contact_person_identified":
                if not contact or not contact.name:
                    missing.append(f"{stage.value}: contact person required")
            elif req == "need_confirmed":
                if not lead.expected_workers or lead.expected_workers == 0:
                    missing.append(f"{stage.value}: expected worker count required")
            elif req == "budget_qualified":
                if lead.estimated_value < 10000:  # Min RM10k/year
                    missing.append(f"{stage.value}: minimum RM10k annual value")
            elif req == "proposal_sent":
                prop_sent = any(a.type.value == "proposal_sent" for a in (activities or []))
                if not prop_sent:
                    missing.append(f"{stage.value}: proposal must be sent")
            elif req == "decision_maker_engaged":
                dm_engaged = any(
                    a.type.value in ("meeting_held", "call_connected") and 
                    contact and contact.is_decision_maker
                    for a in (activities or [])
                )
                if not dm_engaged:
                    missing.append(f"{stage.value}: decision maker meeting required")
            elif req == "terms_discussed":
                terms_discussed = any(
                    "terms" in a.description.lower() or "pricing" in a.description.lower()
                    for a in (activities or [])
                )
                if not terms_discussed:
                    missing.append(f"{stage.value}: terms discussion required")
            elif req == "decision_maker_committed":
                committed = any(
                    "commit" in a.description.lower() or "approve" in a.description.lower()
                    for a in (activities or [])
                )
                if not committed:
                    missing.append(f"{stage.value}: decision maker commitment required")
            elif req == "contract_signed":
                signed = any(
                    "signed" in a.description.lower() or "contract" in a.description.lower()
                    for a in (activities or [])
                )
                if not signed:
                    missing.append(f"{stage.value}: contract signing required")
            elif req == "deposit_received":
                deposit = any(
                    "deposit" in a.description.lower() or "payment" in a.description.lower()
                    for a in (activities or [])
                )
                if not deposit:
                    missing.append(f"{stage.value}: deposit confirmation required")
            elif req == "lost_reason_recorded":
                if not lead.lost_reason:
                    missing.append(f"{stage.value}: lost reason required")
            elif req == "nurture_sequence_active":
                with get_db() as conn:
                    enrolled = conn.execute(
                        "SELECT 1 FROM sequence_enrollments WHERE lead_id = ? AND status = 'active'",
                        (lead.id,)
                    ).fetchone()
                    if not enrolled:
                        missing.append(f"{stage.value}: must be enrolled in nurture sequence")
    
    return len(missing) == 0, missing


def advance_stage(lead: Lead, target_stage: LeadStatus, 
                  company: Company, contact: Contact = None,
                  note: str = "") -> Tuple[bool, str]:
    """Advance lead to target stage if requirements met."""
    activities = []
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM activities WHERE lead_id = ?", (lead.id,)
        ).fetchall()
        activities = [Activity(**dict(r)) for r in rows]
    
    can_advance, missing = can_advance_stage(lead, target_stage, company, contact, activities)
    
    if not can_advance:
        return False, f"Requirements not met: {', '.join(missing)}"
    
    old_stage = lead.status
    lead.status = target_stage
    lead.score = STAGE_PROBABILITIES[target_stage] * 100
    LeadRepo.update(lead)
    
    # Log activity
    ActivityRepo.create(Activity(
        lead_id=lead.id,
        company_id=lead.company_id,
        contact_id=lead.contact_id,
        type=ActivityType.NOTE,
        subject=f"Stage changed: {old_stage.value} → {target_stage.value}",
        description=note or f"Advanced from {old_stage.value} to {target_stage.value}",
        created_by="system"
    ))
    
    # Create deal if reaching PROPOSAL
    if target_stage == LeadStatus.PROPOSAL:
        existing = DealRepo.get_by_lead(lead.id)
        if not existing:
            DealRepo.create(Deal(
                lead_id=lead.id,
                company_id=lead.company_id,
                name=f"Deal - {company.name}",
                value=lead.estimated_value,
                workers_count=lead.expected_workers,
                stage=LeadStatus.PROPOSAL,
                probability=0.5,
                expected_close_date=(datetime.now() + timedelta(days=30)).date().isoformat(),
            ))
    
    return True, f"Advanced to {target_stage.value}"


# =============================================================================
# CONVERSION TRACKING & ANALYTICS
# =============================================================================

@dataclass
class PipelineMetrics:
    total_leads: int = 0
    by_stage: Dict[str, int] = None
    conversion_rates: Dict[str, float] = None
    avg_score_by_stage: Dict[str, float] = None
    total_pipeline_value: float = 0.0
    weighted_pipeline_value: float = 0.0
    avg_deal_size: float = 0.0
    avg_sales_cycle_days: float = 0.0
    win_rate: float = 0.0
    
    def __post_init__(self):
        if self.by_stage is None:
            self.by_stage = {}
        if self.conversion_rates is None:
            self.conversion_rates = {}
        if self.avg_score_by_stage is None:
            self.avg_score_by_stage = {}


def get_pipeline_metrics() -> PipelineMetrics:
    """Calculate comprehensive pipeline metrics."""
    metrics = PipelineMetrics()
    
    with get_db() as conn:
        # Total leads
        metrics.total_leads = conn.execute("SELECT COUNT(*) FROM leads").fetchone()[0]
        
        # By stage
        rows = conn.execute("SELECT status, COUNT(*) as cnt FROM leads GROUP BY status").fetchall()
        metrics.by_stage = {r['status']: r['cnt'] for r in rows}
        
        # Conversion rates (stage-to-stage)
        stages = [s.value for s in STAGE_ORDER if s not in (LeadStatus.WON, LeadStatus.LOST)]
        for i in range(len(stages) - 1):
            current = stages[i]
            next_stage = stages[i + 1]
            current_count = metrics.by_stage.get(current, 0)
            next_count = metrics.by_stage.get(next_stage, 0)
            if current_count > 0:
                metrics.conversion_rates[f"{current}_to_{next_stage}"] = round(next_count / current_count * 100, 1)
            else:
                metrics.conversion_rates[f"{current}_to_{next_stage}"] = 0.0
        
        # Avg score by stage
        rows = conn.execute("SELECT status, AVG(score) as avg_score FROM leads GROUP BY status").fetchall()
        metrics.avg_score_by_stage = {r['status']: round(r['avg_score'], 1) for r in rows}
        
        # Pipeline value
        rows = conn.execute("""
            SELECT 
                SUM(d.value) as total_value,
                SUM(d.value * d.probability) as weighted_value,
                AVG(d.value) as avg_deal_size
            FROM deals d
            JOIN leads l ON d.lead_id = l.id
            WHERE l.status NOT IN ('won', 'lost')
        """).fetchone()
        if rows:
            metrics.total_pipeline_value = rows['total_value'] or 0
            metrics.weighted_pipeline_value = rows['weighted_value'] or 0
            metrics.avg_deal_size = rows['avg_deal_size'] or 0
        
        # Win rate
        won = metrics.by_stage.get('won', 0)
        lost = metrics.by_stage.get('lost', 0)
        closed = won + lost
        if closed > 0:
            metrics.win_rate = round(won / closed * 100, 1)
        
        # Avg sales cycle (days from NEW to WON)
        row = conn.execute("""
            SELECT AVG(julianday(closed_at) - julianday(created_at)) as avg_days
            FROM leads WHERE status = 'won' AND closed_at IS NOT NULL
        """).fetchone()
        if row and row['avg_days']:
            metrics.avg_sales_cycle_days = round(row['avg_days'], 1)
    
    return metrics


def get_lead_velocity() -> Dict[str, Any]:
    """Track lead velocity: new leads, stage changes, closures per week."""
    with get_db() as conn:
        # Last 12 weeks
        weeks_data = []
        for i in range(11, -1, -1):
            week_start = datetime.now() - timedelta(weeks=i+1)
            week_end = datetime.now() - timedelta(weeks=i)
            
            ws = week_start.date().isoformat()
            we = week_end.date().isoformat()
            
            new_leads = conn.execute("""
                SELECT COUNT(*) FROM leads 
                WHERE date(created_at) BETWEEN ? AND ?
            """, (ws, we)).fetchone()[0]
            
            won = conn.execute("""
                SELECT COUNT(*) FROM leads 
                WHERE status = 'won' AND date(closed_at) BETWEEN ? AND ?
            """, (ws, we)).fetchone()[0]
            
            lost = conn.execute("""
                SELECT COUNT(*) FROM leads 
                WHERE status = 'lost' AND date(closed_at) BETWEEN ? AND ?
            """, (ws, we)).fetchone()[0]
            
            stage_changes = conn.execute("""
                SELECT COUNT(*) FROM activities a
                WHERE a.type = 'note' AND a.subject LIKE '%Stage changed%'
                AND date(a.created_at) BETWEEN ? AND ?
            """, (ws, we)).fetchone()[0]
            
            weeks_data.append({
                "week": week_start.strftime("%Y-W%U"),
                "start_date": ws,
                "end_date": we,
                "new_leads": new_leads,
                "won": won,
                "lost": lost,
                "stage_changes": stage_changes,
            })
        
        return {"weekly_velocity": weeks_data}


# =============================================================================
# OUTREACH SEQUENCE AUTOMATION
# =============================================================================

DEFAULT_SEQUENCES = {
    "cold_outreach_manufacturing": {
        "name": "Cold Outreach - Manufacturing/E&E",
        "steps": [
            {"delay_days": 0, "template": "cold_manufacturing_1", "channel": "email"},
            {"delay_days": 3, "template": "cold_manufacturing_2", "channel": "email"},
            {"delay_days": 7, "template": "cold_manufacturing_3", "channel": "email"},
            {"delay_days": 14, "template": "cold_manufacturing_4", "channel": "email"},
            {"delay_days": 21, "template": "cold_manufacturing_5", "channel": "email"},
            {"delay_days": 30, "template": "cold_manufacturing_breakup", "channel": "email"},
        ]
    },
    "cold_outreach_construction": {
        "name": "Cold Outreach - Construction",
        "steps": [
            {"delay_days": 0, "template": "cold_construction_1", "channel": "email"},
            {"delay_days": 3, "template": "cold_construction_2", "channel": "email"},
            {"delay_days": 7, "template": "cold_construction_3", "channel": "email"},
            {"delay_days": 14, "template": "cold_construction_4", "channel": "email"},
            {"delay_days": 21, "template": "cold_construction_5", "channel": "email"},
        ]
    },
    "cold_outreach_plantation": {
        "name": "Cold Outreach - Plantation",
        "steps": [
            {"delay_days": 0, "template": "cold_plantation_1", "channel": "email"},
            {"delay_days": 4, "template": "cold_plantation_2", "channel": "email"},
            {"delay_days": 10, "template": "cold_plantation_3", "channel": "email"},
            {"delay_days": 20, "template": "cold_plantation_breakup", "channel": "email"},
        ]
    },
    "warm_nurture": {
        "name": "Warm Lead Nurture",
        "steps": [
            {"delay_days": 0, "template": "nurture_value_1", "channel": "email"},
            {"delay_days": 7, "template": "nurture_case_study", "channel": "email"},
            {"delay_days": 14, "template": "nurture_insight", "channel": "email"},
            {"delay_days": 30, "template": "nurture_checkin", "channel": "email"},
        ]
    },
    "proposal_followup": {
        "name": "Proposal Follow-up",
        "steps": [
            {"delay_days": 1, "template": "proposal_followup_1", "channel": "email"},
            {"delay_days": 3, "template": "proposal_followup_2", "channel": "email"},
            {"delay_days": 7, "template": "proposal_followup_3", "channel": "email"},
            {"delay_days": 14, "template": "proposal_final", "channel": "email"},
        ]
    },
}


def create_default_sequences():
    """Create default outreach sequences in database."""
    for key, seq_data in DEFAULT_SEQUENCES.items():
        with get_db() as conn:
            existing = conn.execute(
                "SELECT id FROM outreach_sequences WHERE name = ?", (seq_data["name"],)
            ).fetchone()
            if existing:
                continue
            
            seq_id = str(uuid.uuid4())[:8]
            conn.execute("""
                INSERT INTO outreach_sequences (id, name, steps, is_active, created_at)
                VALUES (?, ?, ?, 1, ?)
            """, (seq_id, seq_data["name"], json.dumps(seq_data["steps"]), datetime.now().isoformat()))
            conn.commit()
    
    print("Default outreach sequences created")


def enroll_lead_in_sequence(lead_id: str, sequence_name: str) -> bool:
    """Enroll a lead in an outreach sequence."""
    with get_db() as conn:
        seq = conn.execute(
            "SELECT id, steps FROM outreach_sequences WHERE name = ? AND is_active = 1",
            (sequence_name,)
        ).fetchone()
        
        if not seq:
            return False
        
        steps = json.loads(seq['steps'])
        first_step = steps[0] if steps else None
        next_action = (datetime.now() + timedelta(days=first_step.get('delay_days', 0))).isoformat() if first_step else None
        
        existing = conn.execute(
            "SELECT id FROM sequence_enrollments WHERE lead_id = ? AND sequence_id = ? AND status = 'active'",
            (lead_id, seq['id'])
        ).fetchone()
        
        if existing:
            return False  # Already enrolled
        
        enrollment_id = str(uuid.uuid4())[:8]
        conn.execute("""
            INSERT INTO sequence_enrollments (id, sequence_id, lead_id, current_step, status, next_action_at, created_at, updated_at)
            VALUES (?, ?, ?, 0, 'active', ?, ?, ?)
        """, (enrollment_id, seq['id'], lead_id, next_action, datetime.now().isoformat(), datetime.now().isoformat()))
        conn.commit()
        
        # If first step delay is 0, send immediately (handled by worker)
        return True


def process_sequence_enrollments():
    """Process due sequence steps - call from cron/worker."""
    sent_count = 0
    
    with get_db() as conn:
        # Get enrollments due for action
        now = datetime.now().isoformat()
        rows = conn.execute("""
            SELECT e.*, s.steps, s.name as seq_name, l.company_id, l.contact_id
            FROM sequence_enrollments e
            JOIN outreach_sequences s ON e.sequence_id = s.id
            JOIN leads l ON e.lead_id = l.id
            WHERE e.status = 'active' AND e.next_action_at <= ?
        """, (now,)).fetchall()
        
        for row in rows:
            enrollment = dict(row)
            steps = json.loads(enrollment['steps'])
            current_step = enrollment['current_step']
            
            if current_step >= len(steps):
                # Sequence complete
                conn.execute(
                    "UPDATE sequence_enrollments SET status = 'completed', updated_at = ? WHERE id = ?",
                    (datetime.now().isoformat(), enrollment['id'])
                )
                continue
            
            step = steps[current_step]
            template_name = step.get('template')
            channel = step.get('channel', 'email')
            
            # Get template
            tmpl = conn.execute(
                "SELECT * FROM email_templates WHERE name = ? AND is_active = 1",
                (template_name,)
            ).fetchone()
            
            if tmpl:
                # Send email (placeholder - integrate with actual sender)
                send_email_via_template(
                    lead_id=enrollment['lead_id'],
                    company_id=enrollment['company_id'],
                    contact_id=enrollment['contact_id'],
                    template=dict(tmpl),
                    step_data=step
                )
                sent_count += 1
                
                # Log activity
                conn.execute("""
                    INSERT INTO activities (id, lead_id, company_id, contact_id, type, subject, description, metadata, created_by, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'sequence', ?)
                """, (
                    str(uuid.uuid4())[:8], enrollment['lead_id'], enrollment['company_id'],
                    enrollment['contact_id'], ActivityType.EMAIL_SENT.value,
                    f"Sequence: {enrollment['seq_name']} - Step {current_step + 1}",
                    f"Sent template: {template_name}",
                    json.dumps({"sequence": enrollment['seq_name'], "step": current_step, "template": template_name}),
                    datetime.now().isoformat()
                ))
            
            # Advance to next step
            next_step_idx = current_step + 1
            if next_step_idx < len(steps):
                next_delay = steps[next_step_idx].get('delay_days', 0)
                next_action = (datetime.now() + timedelta(days=next_delay)).isoformat()
                conn.execute("""
                    UPDATE sequence_enrollments 
                    SET current_step = ?, next_action_at = ?, updated_at = ?
                    WHERE id = ?
                """, (next_step_idx, next_action, datetime.now().isoformat(), enrollment['id']))
            else:
                conn.execute("""
                    UPDATE sequence_enrollments 
                    SET status = 'completed', current_step = ?, updated_at = ?
                    WHERE id = ?
                """, (next_step_idx, datetime.now().isoformat(), enrollment['id']))
            
            conn.commit()
    
    return sent_count


def send_email_via_template(lead_id: str, company_id: str, contact_id: str,
                            template: dict, step_data: dict):
    """Placeholder - integrate with actual email sender (SMTP, SendGrid, etc.)"""
    # This would render template with lead/company/contact variables
    # and send via SMTP/API
    pass


# =============================================================================
# FORECASTING
# =============================================================================

def forecast_revenue(months: int = 3) -> Dict[str, Any]:
    """Forecast revenue based on pipeline and historical conversion."""
    metrics = get_pipeline_metrics()
    
    # Weighted pipeline value by stage
    stage_weights = {
        'new': 0.05, 'contacted': 0.10, 'qualified': 0.25,
        'proposal': 0.50, 'negotiation': 0.75, 'nurturing': 0.05
    }
    
    forecast = {}
    for month in range(1, months + 1):
        # Simple model: assume 1/3 of weighted pipeline closes per month
        monthly_close = metrics.weighted_pipeline_value / 3
        forecast[f"month_{month}"] = {
            "expected_revenue": round(monthly_close, 0),
            "expected_workers": round(monthly_close / 50000, 0),  # RM50k/worker/year
            "confidence": "low" if month == 1 else "medium" if month == 2 else "high"
        }
    
    return {
        "current_weighted_pipeline": metrics.weighted_pipeline_value,
        "total_pipeline": metrics.total_pipeline_value,
        "win_rate": metrics.win_rate,
        "avg_deal_size": metrics.avg_deal_size,
        "forecast": forecast,
        "generated_at": datetime.now().isoformat()
    }


# =============================================================================
# DEAL REPOSITORY
# =============================================================================

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
    def get_by_lead(lead_id: str) -> Optional[Deal]:
        with get_db() as conn:
            row = conn.execute("SELECT * FROM deals WHERE lead_id = ?", (lead_id,)).fetchone()
            if row:
                d = dict(row)
                d['stage'] = LeadStatus(d['stage'])
                return Deal(**d)
            return None


# =============================================================================
# MAIN / CLI
# =============================================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(description="CRM Pipeline Operations")
    parser.add_argument("--init", action="store_true", help="Initialize CRM database")
    parser.add_argument("--score-all", action="store_true", help="Recalculate all lead scores")
    parser.add_argument("--create-sequences", action="store_true", help="Create default outreach sequences")
    parser.add_argument("--metrics", action="store_true", help="Show pipeline metrics")
    parser.add_argument("--forecast", type=int, default=3, help="Forecast revenue (months)")
    parser.add_argument("--velocity", action="store_true", help="Show lead velocity")
    parser.add_argument("--process-sequences", action="store_true", help="Process due sequence steps")
    parser.add_argument("--enroll", nargs=2, metavar=("LEAD_ID", "SEQUENCE"), help="Enroll lead in sequence")
    args = parser.parse_args()

    if args.init:
        init_db()
        print("CRM database initialized")
        return

    # Ensure DB exists
    if not Path(DB_PATH).exists():
        init_db()

    if args.score_all:
        updated = score_all_leads()
        print(f"Updated {updated} lead scores")

    if args.create_sequences:
        create_default_sequences()

    if args.metrics:
        metrics = get_pipeline_metrics()
        print(json.dumps({
            "total_leads": metrics.total_leads,
            "by_stage": metrics.by_stage,
            "conversion_rates": metrics.conversion_rates,
            "avg_score_by_stage": metrics.avg_score_by_stage,
            "total_pipeline_value": metrics.total_pipeline_value,
            "weighted_pipeline_value": metrics.weighted_pipeline_value,
            "avg_deal_size": metrics.avg_deal_size,
            "win_rate": metrics.win_rate,
            "avg_sales_cycle_days": metrics.avg_sales_cycle_days,
        }, indent=2))

    if args.forecast:
        forecast = forecast_revenue(args.forecast)
        print(json.dumps(forecast, indent=2))

    if args.velocity:
        velocity = get_lead_velocity()
        print(json.dumps(velocity, indent=2))

    if args.process_sequences:
        sent = process_sequence_enrollments()
        print(f"Sent {sent} sequence emails")

    if args.enroll:
        lead_id, sequence = args.enroll
        success = enroll_lead_in_sequence(lead_id, sequence)
        print(f"Enrollment {'successful' if success else 'failed'}")


if __name__ == "__main__":
    main()