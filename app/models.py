from pydantic import BaseModel, Field

class HomeBudgetInput(BaseModel):
    total_budget: float = Field(gt=0)
    num_lights: int = Field(default=1, ge=0, le=100)
    num_fans: int = Field(default=1, ge=0, le=100)
    num_furniture: int = Field(default=1, ge=0, le=100)
    num_dining_tables: int = Field(default=0, ge=0, le=50)
    rooms: list[str] = Field(default_factory=list)
    special_requirements: str = Field(default="", max_length=1000)

class PartyBudgetInput(BaseModel):
    total_budget: float = Field(gt=0)
    party_type: str = Field(min_length=2, max_length=80)
    num_guests: int = Field(gt=0, le=5000)
    needs: list[str] = Field(default_factory=list)
    special_requirements: str = Field(default="", max_length=1000)
