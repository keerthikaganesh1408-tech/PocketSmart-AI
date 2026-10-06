from .gemini_service import text,image_text
from .models import HomeBudgetInput,PartyBudgetInput
def home(d:HomeBudgetInput):
    return text(f"""You are PocketSmart AI. Create a practical Indian-rupee home interior budget recommendation.
Budget: ₹{d.total_budget:,.0f}
Lights: {d.num_lights}; Fans: {d.num_fans}; Furniture: {d.num_furniture}; Dining tables: {d.num_dining_tables}
Rooms: {", ".join(d.rooms) or "Not specified"}
Preferences: {d.special_requirements or "None"}
Return a concise summary, category-wise suggested allocation, reasons, contingency, and 3 saving tips.
Stay within the budget. Prices are estimates, not live quotes.""")
def party(d:PartyBudgetInput):
    return text(f"""You are PocketSmart AI. Create a practical Indian-rupee party budget.
Budget: ₹{d.total_budget:,.0f}; Party: {d.party_type}; Guests: {d.num_guests}
Needs: {", ".join(d.needs) or "Not specified"}; Preferences: {d.special_requirements or "None"}
Return summary, suggested venue/food/decor/entertainment/misc allocation, per-person guidance,
contingency and 3 saving tips. Stay within budget. Treat prices as estimates.""")
def jewelry(budget,occasion,jewelry_type,preferences,path=None):
    prompt=f"""You are PocketSmart AI, a jewelry budget recommendation assistant.
Budget: ₹{budget:,.0f}; Occasion: {occasion}; Jewelry type: {jewelry_type}; Preferences: {preferences or "None"}.
If an outfit image is supplied, use only broad visual features such as clothing color and style.
Return style recommendation, pieces, budget allocation, matching guidance and 3 buying tips.
Do not claim live prices, gemstone authenticity or purity from an image."""
    return image_text(prompt,path) if path else text(prompt)
