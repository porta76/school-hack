import tools.SMS.sendRequest as request
import tools.SMS.randomData as randomData
__services = request.getServices()
def flood(target):
    service = randomData.random_service(__services)
    service = request.Service(service)
    service.sendMessage(target)