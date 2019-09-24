default = 'redis'

drivers = {
    'redis': {
        'use': 'laravel.Queue.RedisQueue',
    },
    'database': {
        'use': 'laravel.Queue.DatabaseQueue'
    }
}
