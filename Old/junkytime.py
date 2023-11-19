from datetime import *

start = datetime.strptime('08:00:00', '%H:%M:%S')
end = start + timedelta(minutes=82.4)

print(start.time())
print(end.time())

str = "Hello t there buddy t"

print(str.replace(" t ", "bruh"))

