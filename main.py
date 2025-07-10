from fastapi.responses import JSONResponse

@app.get("/")
async def 根路径():
    from fastapi.responses import JSONResponse
    return JSONResponse(
        content={"消息": "游历诗地图API服务运行中", "版本": "2.0"},
        status_code=200
    ) 