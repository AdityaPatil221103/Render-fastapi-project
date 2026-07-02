from fastapi import FastAPI, Depends, Header, HTTPException

app = FastAPI()

def common_logic():
    return{
        "message":"Common logic executed"
    }

@app.get("/home")
def home(data = Depends(common_logic)):
    return data


#For Reusable logic
def  get_current_user():
    return {
        "user":"Mohit"
    }

@app.get("/profile")
def profile(user = Depends(get_current_user)):
    return user

@app.get("/dashboard")
def dashboard(user = Depends(get_current_user)):
    return user

#Auth
def verify_token(token : str= Header(None)):
    if token != "mysecerettoken":
        raise HTTPException(
            status_code=401,
            detail="Unauthorized User"
        )
    return{
        "user":"Authorized user"
    }

@app.get("/secure-data")
def secure_data(user = Depends(verify_token)):
    return{
        "message":"secure data accessed",
        "user":user
    }