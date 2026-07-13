from services.influencer_service import InfluencerService

class ChatbotService:
    def generate_response(self, topic: str, top_n: int = 5):
        service = InfluencerService()
        influencers = service.find_influencers(topic, top_n)
        
        if isinstance(influencers, dict) and "message" in influencers:
            return {"message": influencers["message"], "influencers": []}
        
        # Friendly text response
        lines = [f"Here are the top {len(influencers)} influencers for **{topic}**:\n"]
        
        for i, inf in enumerate(influencers, 1):
            lines.append(f"{i}. **@{inf['username']}** ({inf['platform']})")
            lines.append(f"   - Relevance: {inf['relevance_score']}")
            lines.append(f"   - Influence: {inf['influence_score']}")
            lines.append(f"   - Overall Score: {inf['overall_score']}")
            lines.append(f"   - Why: {inf.get('selection_reason', 'Strong match')}\n")
        
        friendly_text = "\n".join(lines)
        
        return {
            "friendly_message": friendly_text,
            "influencers": influencers,
            "topic": topic
        }
