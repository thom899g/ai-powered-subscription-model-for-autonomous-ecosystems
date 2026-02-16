from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import logging
from jose import JWTError, jwt
from fastapi import HTTPException

class SubscriptionManager:
    def __init__(self, config):
        self.config = config
        self.subscriptions = {}
        self.tiers = config['tiers']
        self.max_retries = 3
        
    class TierNotFoundException(Exception):
        pass
    
    class InvalidSubscriptionRequest(Exception):
        pass
    
    def create_subscription(self, user_id: str, tier: str) -> str:
        """Creates a new subscription for the specified user and tier."""
        if tier not in self.tiers:
            raise SubscriptionManager.TierNotFoundException(f"Tier {tier} does not exist.")
            
        # Generate subscription ID
        subscription_id = f"{user_id}_{datetime.now().isoformat()}"
        
        try:
            # Mock payment processing
            billing_integration.process_payment(user_id, tier)
            
            self.subscriptions[subscription_id] = {
                'user_id': user_id,
                'tier': tier,
                'start_date': datetime.now(),
                'status': 'active'
            }
            
            return subscription_id
            
        except Exception as e:
            logging.error(f"Subscription creation failed: {str(e)}")
            raise SubscriptionManager.InvalidSubscriptionRequest("Subscription creation failed.")
    
    def get_subscription(self, subscription_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves a subscription by ID."""
        return self.subscriptions.get(subscription_id)
    
    def cancel_subscription(self, subscription_id: str) -> None:
        """Cancels an existing subscription."""
        if subscription_id not in self.subscriptions:
            raise SubscriptionManager.TierNotFoundException(f"Subscription {subscription_id} not found.")
            
        # Trigger cleanup process
        billing_integration.cancel_subscription(subscription_id)
    
    def upgrade_tier(self, subscription_id: str, new_tier: str) -> None:
        """Upgrades a subscription to a higher tier."""
        if subscription_id not in self.subscriptions:
            raise SubscriptionManager.TierNotFoundException(f"Subscription {subscription_id} not found.")
            
        if new_tier not in self.tiers or self.tiers[new_tier] <= self.tiers[self.subscriptions[subscription_id]['tier']]:
            raise SubscriptionManager.InvalidSubscriptionRequest("Invalid tier upgrade request.")
            
        try:
            billing_integration.upgrade_plan(subscription_id, new_tier)
        except Exception as e:
            logging.error(f"Tier upgrade failed: {str(e)}")
            raise SubscriptionManager.InvalidSubscriptionRequest("Tier upgrade failed.")