from unittest import result
from dns import resolver

def dns_query(host,query):
    res = resolver.Resolver()
    res.nameservers = [host]
    answers = res.resolve(query, "A")
    results = []
    for rdata in answers:
        results.append(rdata.address)
    return results

def resolve(query):
    try:
        results = dns_query("8.8.8.8",query)
        if results[0] == "10.10.34.35":
            results = dns_query("1.1.1.1",query)
        return results
    except:
        print("Error to Resolve DNS.")
        return []

def isFiltred(query):
    try:
        results = dns_query("8.8.8.8",query)
        if results[0] == "10.10.34.35":
            return True
        return False
    except:
        return False

  


