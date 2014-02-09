requirejs.config({
    'baseUrl': 'lib',
    'paths': {
        'tawq': '../tawq',
        'slides': '../slides',
        'assets': '../../assets',
        'data': '../data'
    }
});

requirejs(['tawq/main']);
