from risk.position_manager import PositionManager


def test_position_calculation():

    manager = PositionManager(
        capital=50000
    )

    result = manager.calculate_position(
        entry_price=20,
        stop_price=18,
        confidence=1.0
    )

    assert result["shares"] >= 0

    assert result["position_money"] <= 10000

    assert result["risk_money"] <= 500
