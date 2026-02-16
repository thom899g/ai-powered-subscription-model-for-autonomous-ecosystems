from typing import Dict, Any
from fastapi import HTTPException

class TieredAccessGateway:
    def __init__(self, subscription_manager):
        self.subscription_manager = subscription_manager
        
    async def authorize(self, user_id: str, feature: str) -> bool:
        """Authorizes access to a specific feature based on the user's tier."""
        try:
            subscription = await self.subscription_manager.get_subscription_for_user(user_id)
            
            if not subscription:
                raise HTTPException(status_code=403, detail="User not subscribed.")
                
            # Check if feature is allowed in the current tier
            if feature not in self.tiers[subscription['tier']]['features']:
                raise HTTPException(status_code=403, detail="Feature not available for this tier.")
                
            return True
            
        except Exception as e:
            logging.error(f"Authorization failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error.")

    def get_usage_stats(self) -> Dict[str, Any]:
        """Retrieves usage statistics for all tiers."""
        # Mock implementation
        return {
            'total_subscribers': len(self.subscriptions),
            'tier_usage': {
                'basic': 100,
                'pro': 50,
                'enterprise': 20
            }
        }