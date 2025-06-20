from rest_framework.response import Response



class MyResponse:
    @staticmethod
    def success(data=None,message="",status_code=200,**extra):
        response_data = {
            "success":True,
            "data":data,
            "message":message
        }

        if extra:
            response_data.update(extra)

        return Response(data=response_data,status=status_code)
    
    @staticmethod
    def failure(message="",data=None,status_code=400):
        response_data = {
                "success":False,
                "errors":data,
                "message":message
            }
        return Response(
            data=response_data,
            status=status_code
        )