def test_process_codonic_layer_with_valid_data():
    # Test that the layer processes valid data correctly
    processor = CodonicProcessor()
    result = processor.process_codonic_layer({
        'visual': {'intensity': 0.5, 'contrast': 0.3, 'sharpness': 0.8},  # Fixed: added 'ness': 0.8
        'tactile': {'pressure': 0.7, 'temperature': 0.4, 'vibration': 0.2}
    })
    assert result is not None