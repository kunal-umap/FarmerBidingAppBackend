from flask import Blueprint, request, jsonify
from app.models import ProductBid, Bid, db
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('businessman', __name__)

@bp.route('/product_bids', methods=['GET'])
@jwt_required()
def get_product_bids():
    bids = ProductBid.query.all()
    result = [{
        "id": bid.id,
        "farmer_id": bid.farmer_id,
        "product_name": bid.product_name,
        "quantity": bid.quantity,
        "price": bid.price,
        "description": bid.description,
        "harvested_date": bid.harvested_date.isoformat(),
        "status": bid.status,
        "bid_count": bid.bid_count
    } for bid in bids]
    return jsonify(result), 200

@bp.route('/bid', methods=['POST'])
@jwt_required()
def place_bid():
    businessman_id = get_jwt_identity()
    data = request.json
    product_bid = ProductBid.query.get(data['product_bid_id'])
    if not product_bid:
        return jsonify({"message": "Product bid not found"}), 404
    
    new_bid = Bid(
        product_bid_id=product_bid.id,
        businessman_id=businessman_id,
        price=data['price']
    )
    db.session.add(new_bid)
    
    product_bid.bid_count += 1
    product_bid.status = 'processing'
    
    db.session.commit()
    return jsonify({"message": "Bid placed successfully"}), 201