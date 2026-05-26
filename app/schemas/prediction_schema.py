from pydantic import BaseModel, Field, field_validator


class PurchaseData(BaseModel):
    """Schema for purchase prediction input."""
    
    user_total_spent: float = Field(
        ..., 
        ge=0.0, 
        description="Total amount spent by user"
    )
    user_transaction_count: int = Field(
        ..., 
        ge=0, 
        description="Number of transactions by user"
    )
    user_unique_items: int = Field(
        ..., 
        ge=0, 
        description="Number of unique items purchased"
    )
    item_popularity: int = Field(
        ..., 
        ge=0, 
        description="Popularity score of the item"
    )
    item_avg_quantity: float = Field(
        ..., 
        ge=0.0, 
        description="Average quantity per transaction"
    )
    item_unit_price: float = Field(
        ..., 
        ge=0.0, 
        description="Unit price of the item"
    )
    
    @field_validator('user_total_spent', 'item_avg_quantity', 'item_unit_price')
    @classmethod
    def validate_positive_values(cls, v):
        """Ensure float values are reasonable."""
        if v < 0:
            raise ValueError('Value must be non-negative')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_total_spent": 500.0,
                "user_transaction_count": 5,
                "user_unique_items": 10,
                "item_popularity": 150,
                "item_avg_quantity": 2.5,
                "item_unit_price": 15.0
            }
        }