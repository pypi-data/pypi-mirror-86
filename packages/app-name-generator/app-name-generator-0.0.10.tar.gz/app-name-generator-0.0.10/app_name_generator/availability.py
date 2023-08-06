import dns.resolver
import concurrent.futures


def domain_available(fqdn, exclusive=False):
    try:
        dns.resolver.resolve(fqdn)
        return False
    except (
        dns.resolver.NoAnswer,
        dns.resolver.NXDOMAIN,
        dns.resolver.NoNameservers,
    ):
        return True
    except (
        dns.name.EmptyLabel,
        dns.exception.Timeout,
    ):
        return False


def domain_available_for_tlds(domain_name, exclusive=False, tlds=["com", "fr", "io"]):
    domains = [domain_name + "." + tld for tld in tlds]
    tasks = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for fqdn in domains:
            tasks.append(executor.submit(domain_available, fqdn))

    domains_availables = [task.result() for task in tasks]

    if exclusive and sum(x is False for x in domains_availables) > 0:
        return []
    else:
        return [domains[k] for k in range(len(domains)) if domains_availables[k]]
