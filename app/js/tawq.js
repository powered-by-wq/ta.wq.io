requirejs.config({
    'baseUrl': '/js/lib',
    'paths': {
        'tawq': '../tawq',
        'data': '../data/'
    }
});

requirejs(['tawq/main']);
