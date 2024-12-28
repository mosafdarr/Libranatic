from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

class HeaderMiddleware:
    @staticmethod
    def add_middleware(app: FastAPI):
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        @app.middleware("http")
        async def add_process_time_header(request: Request, call_next):
            response = await call_next(request)
            response.headers["X-Process-Time"] = "Processed in {time} seconds".format(
                time=0.0
            )
            return response

        @app.exception_handler(Exception)
        async def exception_handler(request: Request, exc: Exception):
            return JSONResponse(status_code=500, content={"message": "Internal Server Error"})
