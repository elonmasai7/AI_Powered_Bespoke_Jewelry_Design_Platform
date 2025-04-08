def validate_design(model_data, constraints):
    """Validate generated design against manufacturing constraints"""
    errors = []
    
    # Example validation logic
    if 'ring' in model_data['prompt'].lower():
        if model_data.get('thickness', 0) < constraints['min_thickness']:
            errors.append(f"Thickness below minimum {constraints['min_thickness']}mm")
            
        if model_data.get('weight', 0) > constraints['max_weight']:
            errors.append(f"Weight exceeds maximum {constraints['max_weight']}g")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': []
    }