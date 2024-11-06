from flask import Blueprint, request, jsonify
from app.models import ProductBid, Bid, db
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('farmer', __name__)

@bp.route('/product_bid', methods=['POST'])
@jwt_required()
def create_product_bid():
    farmer_id = get_jwt_identity()
    data = request.json
    new_bid = ProductBid(
        farmer_id=farmer_id,
        product_name=data['product_name'],
        quantity=data['quantity'],
        price=data['price'],
        description=data['description'],
        harvested_date=data['harvested_date']
    )
    db.session.add(new_bid)
    db.session.commit()
    return jsonify({"message": "Product bid created successfully"}), 201

@bp.route('/my_bids', methods=['GET'])
@jwt_required()
def get_my_bids():
    farmer_id = get_jwt_identity()
    bids = ProductBid.query.filter_by(farmer_id=farmer_id).all()
    result = []
    for bid in bids:
        bid_data = {
            "id": bid.id,
            "product_name": bid.product_name,
            "quantity": bid.quantity,
            "price": bid.price,
            "description": bid.description,
            "harvested_date": bid.harvested_date.isoformat(),
            "status": bid.status,
            "bid_count": bid.bid_count,
            "bids": []
        }
        businessman_bids = Bid.query.filter_by(product_bid_id=bid.id).all()
        for b_bid in businessman_bids:
            bid_data["bids"].append({
                "businessman_id": b_bid.businessman_id,
                "price": b_bid.price
            })
        result.append(bid_data)
    return jsonify(result), 200