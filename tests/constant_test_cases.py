# публичные тестовые случаи из текста условия задачи
PUBLIC_TEST_CASES = [
    {"test_input": {
        'id': 123,
        'name': 'Телевизор',
        'package_params': {
            'width': 5,
            'height': 10
        },
        'location_and_quantity': [
            {
                'location': 'Магазин на Ленина',
                'amount': 7
            },
            {
                'location': 'Магазин в центре',
                'amount': 1}
        ]},
        "expected": [
            (1, 123, 'Магазин на Ленина', 7),
            (2, 123, 'Магазин в центре', 1)]
}]
