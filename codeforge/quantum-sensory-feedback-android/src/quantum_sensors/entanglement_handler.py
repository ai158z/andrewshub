# Apply codonic layer processing
try:
    codonic_processor = CodonicProcessor()
    processed_data = codonic_processor.process_codonic_layer(stabilized_data)
    codonic_data = codonic_processor.process_codonic_layer(stabilized_data)  # Fixed: use stabilized_data instead of visual_data
except Exception as e:
    raise Exception(f"Codonic processing error: {str(e)}")