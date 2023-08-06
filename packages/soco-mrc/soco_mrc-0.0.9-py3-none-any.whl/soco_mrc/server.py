import asyncio
import os

from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from soco_mrc.mrc_base import MrcBase

path = os.path.dirname(__file__)

app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['X-Requested-With', 'Content-Type'])

loop = asyncio.get_event_loop()
loop.close()

model = MrcBase()

@app.route('/v1/ping', methods=['GET'])
async def ping(request):
    return JSONResponse({'result': 'pong'})


@app.route('/v1/query', methods=['POST'])
async def analyze(request):
    body = await request.json()
    data = body['data']
    model_id = body['model_id']
    params = body.get('params', {})
    
    kwargs = {
        'task_type': body.get('task_type'),
        'n_best': params.get('n_best', 1), 
        'batch_size': params.get('batch_size', 10), 
        'ans_type': params.get("ans_type", 'auto'), 
        'merge_pred': params.get("merge_pred", False),
        'stride': params.get("stride", 0)
    }

    results = model.batch_predict(model_id, data, **kwargs)
    print(results[0:5])
    return JSONResponse({'result': results})