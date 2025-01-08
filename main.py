import sha256
#import hashlib
import time
import custom_sha

message =  "00009876876536473627364"

start1 = time.time()
print("toSHA-256:", sha256.tosha256(message))
end1 = time.time()
time_diff1 = end1 - start1
print(time_diff1)


start2 = time.time()
print("Custom_SHA-256:", custom_sha.tocustom_sha256(message))
end2 = time.time()
time_diff2 = end2 - start2
print(time_diff2)



