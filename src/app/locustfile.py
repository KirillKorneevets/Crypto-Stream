from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(0.1, 0.5)  
    
    @task
    def get_courses(self):
        self.client.get("/courses")

    @task
    def get_ethusdt(self):
        self.client.get("/ethusdt")

    @task
    def get_xrpusdt(self):
        self.client.get("/xrpusdt")

    @task
    def get_btcusdt(self):
        self.client.get("/btcusdt")