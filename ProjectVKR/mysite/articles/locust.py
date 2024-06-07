from locust import HttpUser, TaskSet, task, between

class ArticleExportTasks(TaskSet):
    @task
    def export_rdf(self):
        self.client.get("/export/rdf/25/")

    @task
    def export_jats_1_0(self):
        self.client.get("/normalize/jats/1.0/25/")

    @task
    def export_jats_1_1(self):
        self.client.get("/normalize/jats/1.1/25/")

    @task
    def export_eudml(self):
        self.client.get("/normalize/eudml/2/")

    @task
    def export_dublincore(self):
        self.client.get("/normalize/dublincore/25/")

class WebsiteUser(HttpUser):
    tasks = [ArticleExportTasks]
    min_wait = 5000
    max_wait = 9000
