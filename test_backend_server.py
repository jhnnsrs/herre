from herre.herre import Herre
from herre.grants.backend import BackendGrant

x = Herre(
    base_url="http://localhost:8000/o",
    grant=BackendGrant(),
    client_id="7JbA1yi2iQuqc6b4BUjtcYLBOB92V6fQfaE87EFF",
    client_secret="699FBMqg32oRcwQ4m06R8m5j1AWIoXiDnJ2UqEpAEtNoegtpmk69Wg3zD8Hk3C8pKws6QHzEhuuIU14LmUHq2qM12Pze37atxTslAnrOPBGv3PEKjKGMvcSguRW1JGZ6",
)

with x:
    print(x.get_token())
    print(x.user)
