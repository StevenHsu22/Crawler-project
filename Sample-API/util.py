from datetime import datetime


def success(data=None):
    if data is None:
        return {'message': 'success'}, 200

    return {
        'message': 'success',
        'data': data,
        'datatime': datetime.utcnow().isoformat()
    }, 200




def failure(data=None):
    if data is not None:
        return {'message': 'failure'}, 500
    
    return {
        'message': 'failure',
        'datatime': datetime.utcnow().isoformat()
    }, 500